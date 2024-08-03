from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from asyncio import create_task, gather, sleep

from data.config import AUTODELETE_MESSAGE_INFO, AUTODELETE_MESSAGE_INFO_DELAY, SHOW_MEDIA_FILE_ID
from data.messages import Messages
from loader import connection
from utils.echo import send_message, MessageResponse

router = Router()


@router.message()
async def get_message_command_handler(message: Message, bot: Bot):
    if SHOW_MEDIA_FILE_ID:
        media = message.photo or message.animation
        if media is not None:
            if isinstance(media, list):
                media = media[-1]
            print(f'Your file-id: {media.file_id}')
    
    cursor = await connection.execute('SELECT id FROM users WHERE blocked = false;')
    rows: list[list[int]] = await cursor.fetchall()

    users: list[int] = [i[0] for i in rows]

    tasks = []
    for receiver_id in users:
        tasks.append(create_task(send_message(message, bot, receiver_id)))
    
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

    if AUTODELETE_MESSAGE_INFO:
        await sleep(AUTODELETE_MESSAGE_INFO_DELAY)
        try:
            # Пытаемся удалить сообщение
            await info_message.delete()
        except TelegramBadRequest:
            # Если сообщеине не было найдено, или уже было удалено пользователем
            ...
