from aiogram import Bot, Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from asyncio import create_task, gather, sleep
from typing import List, Optional, Tuple, Union

from data.config import (AUTODELETE_MESSAGE_INFO, AUTODELETE_MESSAGE_INFO_DELAY, SHOW_MEDIA_FILE_ID,
                         REPLIES_ENABLED, TAG_BUTTON_TYPE, TAGS_COMMAND_ENABLED,
                         MESSAGE_COOLDOWN, MESSAGE_COOLDOWN_RESET, ADMINS)
from data.messages import Messages
from data.types import TagButtonType
from keyboards.chat_keyboard import ChatKeyboard
from loader import connection
from utils.echo import send_message, MessageResponse
from utils.format_time import format_time
from utils.message import HandleMessageResponse
from utils.time import time

cooldowns = {}

router = Router()


@router.message()
async def get_message_command_handler(message: Message, bot: Bot):
    user_id = message.from_user.id

    # Если отображение файл айди медиа включено:
    if SHOW_MEDIA_FILE_ID:
        media = message.photo or message.animation
        if media is not None:
            if isinstance(media, list):
                media = media[-1]
            print(f'Your file-id: {media.file_id}')
    
    # Проверка задержки
    user_cooldown: Union[float, int] = cooldowns.get(user_id, 0)
    current_time = await time()

    if user_id not in ADMINS.keys() and user_cooldown + MESSAGE_COOLDOWN > current_time:
        if MESSAGE_COOLDOWN_RESET:
            cooldowns[user_id] = int(current_time)
        
        time_left = user_cooldown + MESSAGE_COOLDOWN - int(current_time)
        time_left_formatted = await format_time(int(time_left))

        await message.answer(Messages.early_message.format(time_left=time_left_formatted))
        return
    else:
        cooldowns[user_id] = int(current_time)
    
    # Если реплаи включены
    replies = {}
    if REPLIES_ENABLED:
        replied_message = message.reply_to_message
        if replied_message:
            reply_to_message_id = replied_message.message_id

            replies = await _fetch_replies(reply_to_message_id)
    
    # Получаем всех юзеров из базы данных
    cursor = await connection.execute('SELECT id FROM users WHERE blocked = false;')
    rows: list[list[int]] = await cursor.fetchall()

    users: list[int] = [i[0] for i in rows]

    # Создаём клавиатуру под сообщением (с тегом)
    markup = await _get_markup(message, user_id, custom_tag=ADMINS.get(user_id))

    # Отправляем сообщения пользователям
    tasks = []
    for receiver_id in users:
        task = create_task(
            coro=send_message(
                message,
                bot,
                receiver_id,
                markup,
                reply_to=replies.get(receiver_id)
            )
        )
        tasks.append(task)
    
    result: MessageResponse = await gather(*tasks)

    # Список заблокированных пользователей
    blocked_users = [(i[0],) for i in result if i[1] == False]
    
    if blocked_users:
        await connection.executemany(
            'UPDATE users SET blocked = true WHERE id = ?;',
            blocked_users
        )
    
    users_received = len([0 for i in result if i[1]])
    info_message = await message.answer(Messages.message_received_info.format(users_received=users_received))
    
    # Выполняем функции параллельно 
    await gather(_delete_message(info_message), _handle_messages(result))


async def _delete_message(message: Message):
    # Функция для автоматического удаления сообщения
    if AUTODELETE_MESSAGE_INFO:
        await sleep(AUTODELETE_MESSAGE_INFO_DELAY)
        try:
            # Пытаемся удалить сообщение
            await message.delete()
        except TelegramBadRequest:
            # Если сообщеине не было найдено, или уже было удалено пользователем
            ...


@router.callback_query(F.data.split()[0] == ChatKeyboard.button_callback_2)
async def get_user_name_no_url_callback_query_handler(callback: CallbackQuery):
    await callback.answer(Messages.user_name_no_url_callback_message, True)


@router.callback_query(F.data.split()[0] == ChatKeyboard.button_callback_1)
async def get_user_name_callback_query_handler(callback: CallbackQuery):
    await callback.answer(Messages.user_name_callback_query, True)


@router.callback_query(F.data.split()[0] == ChatKeyboard.button_callback_3)
async def get_custom_tag_callback_query_handler(callback: CallbackQuery):
    await callback.answer(Messages.custom_tag_callback_message, True)


async def _handle_messages(messages: MessageResponse):
    # Функция для сохранения сообщения в таблицу messages
    handle_message_response = HandleMessageResponse(messages)
    await handle_message_response.save()


async def _get_markup(message: Message, user_id: int, *, custom_tag: Optional[str] = None) -> InlineKeyboardMarkup:
    markup = None
    if TAGS_COMMAND_ENABLED:
        if isinstance(TAG_BUTTON_TYPE, TagButtonType):
            if TAG_BUTTON_TYPE == TagButtonType.TAG:
                async with await connection.execute(
                    'SELECT tag_enabled, url_enabled FROM users WHERE id = ?;',
                    (user_id,)
                ) as cursor:
                    row: Tuple[bool, bool] = await cursor.fetchone()
                
                user_tag_enabled = row[0]
                user_url_enabled = row[1]

                if user_tag_enabled:
                    user_first_name = message.from_user.first_name

                    url = None
                    if user_url_enabled:
                        user_name = message.from_user.username
                        if user_name is not None:
                            url = f't.me/{user_name}'

                    markup = await ChatKeyboard.markup(user_first_name, url=url, custom_tag=custom_tag)
                    
            elif TAG_BUTTON_TYPE == TagButtonType.NAME:
                async with await connection.execute(
                    'SELECT name FROM users WHERE id = ?;',
                    (user_id,)
                ) as cursor:
                    row: Tuple[Optional[str]] = await cursor.fetchone()

                    user_name = row[0]
                    if user_name is not None:
                        markup = await ChatKeyboard.markup(user_name, is_tag=False, custom_tag=custom_tag)
    return markup


async def _fetch_replies(message_id: int):
    async with await connection.execute(
        'SELECT id, message_id FROM messages WHERE unique_id = (SELECT unique_id FROM messages WHERE message_id = ?);',
        (message_id,)
    ) as cursor:
        rows: List[Optional[Tuple[int, int]]] = await cursor.fetchall()
    
    replies = dict(rows)
    return replies
