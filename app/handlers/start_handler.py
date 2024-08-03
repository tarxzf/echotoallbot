from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from typing import Any, Optional

from data.config import USER_NAME, SEND_START_MEDIA, START_MEDIA_TYPE, START_MEDIA_FILE_ID
from data.messages import Messages
from data.types import StartMediaType
from loader import connection

router = Router()


@router.message(CommandStart())
async def get_start_command_handler(message: Message):
    user_id = message.from_user.id

    async with await connection.execute(
        'SELECT name FROM users WHERE id = ?;',
        (user_id,)
    ) as cursor:
        row: list[Any] = await cursor.fetchone()
    
    user_name: Optional[str] = row[0]
    if user_name is None:
        user_name = USER_NAME

    # Текст сообщения
    message_text = Messages.start_message.format(user_name=user_name)

    if not SEND_START_MEDIA:
        await message.answer(message_text)
    else:
        if not isinstance(START_MEDIA_TYPE, StartMediaType):
            raise ValueError(f'Incorrect media type: {START_MEDIA_TYPE}')
        else:
            if START_MEDIA_TYPE == StartMediaType.GIF:
                await message.answer_animation(START_MEDIA_FILE_ID, caption=message_text)
            elif START_MEDIA_TYPE == StartMediaType.PHOTO:
                await message.answer_photo(START_MEDIA_FILE_ID, message_text)
