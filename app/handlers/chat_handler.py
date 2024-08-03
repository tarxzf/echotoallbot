from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from asyncio import create_task, gather, sleep
from typing import List, Optional, Tuple

from data.config import AUTODELETE_MESSAGE_INFO, AUTODELETE_MESSAGE_INFO_DELAY, SHOW_MEDIA_FILE_ID, REPLIES_ENABLED
from data.messages import Messages
from loader import connection
from utils.echo import send_message, MessageResponse
from utils.message import HandleMessageResponse

router = Router()


@router.message()
async def get_message_command_handler(message: Message, bot: Bot):
    # Если отображение файл айди медиа включено:
    if SHOW_MEDIA_FILE_ID:
        media = message.photo or message.animation
        if media is not None:
            if isinstance(media, list):
                media = media[-1]
            print(f'Your file-id: {media.file_id}')
    
    # Если реплаи включены
    replies = {}
    if REPLIES_ENABLED:
        replied_message = message.reply_to_message
        if replied_message:
            reply_to_message_id = replied_message.message_id

            replies = await _fetch_replies(reply_to_message_id)
    
    cursor = await connection.execute('SELECT id FROM users WHERE blocked = false;')
    rows: list[list[int]] = await cursor.fetchall()

    users: list[int] = [i[0] for i in rows]

    tasks = []
    for receiver_id in users:
        tasks.append(create_task(send_message(message, bot, receiver_id, reply_to=replies.get(receiver_id))))
    
    result: MessageResponse = await gather(*tasks)

    blocked_users = []  # Список заблокированных пользователей
    for msg_response in result:
        if msg_response[1] == False:
            # Пополняем список, если message_id = False
            blocked_users.append(tuple(msg_response[0]))
    
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

async def _handle_messages(messages: MessageResponse):
    # Функция для сохранения сообщения в таблицу messages
    handle_message_response = HandleMessageResponse(messages)
    await handle_message_response.save()


async def _fetch_replies(message_id: int):
    async with await connection.execute(
        'SELECT id, message_id FROM messages WHERE unique_id = (SELECT unique_id FROM messages WHERE message_id = ?);',
        (message_id,)
    ) as cursor:
        rows: List[Optional[Tuple[int, int]]] = await cursor.fetchall()
    
    replies = dict(rows)
    return replies
