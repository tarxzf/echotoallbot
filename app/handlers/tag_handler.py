from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from typing import Tuple, Optional

from data.messages import Messages
from data.config import TAGS_COMMAND_ENABLED, TAG_BUTTON_TYPE
from data.types import TagButtonType
from filters.enable import IsEnabledFilter
from filters.equals import Equals
from keyboards.tag_keyboard import TagKeyboard
from loader import connection

router = Router()


@router.message(
    Command('tag'),
    IsEnabledFilter(TAGS_COMMAND_ENABLED),
    Equals(TAG_BUTTON_TYPE, TagButtonType.TAG)
)
async def get_tag_command_handler(message: Message, *, user_id: Optional[int] = None, edit: bool = False):
    if user_id is None:
        user_id = message.from_user.id
    
    if message.from_user.username is None:
        await connection.execute(
            'UPDATE users SET url_enabled = false WHERE id = ?;',
            (user_id,)
        )

    async with await connection.execute(
        'SELECT tag_enabled, url_enabled FROM users WHERE id = ?;',
        (user_id,)
    ) as cursor:
        row: Tuple[bool, bool] = await cursor.fetchone()
    
    tag_enabled = row[0]
    url_enabled = row[1]
    
    await _send_tag_message(message, tag_enabled, url_enabled, edit=edit)


@router.callback_query(F.data.split()[0] == TagKeyboard.button_callback_1)
async def get_switch_tag_callback_query_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    await connection.execute(
        'UPDATE users SET tag_enabled = NOT tag_enabled WHERE id = ?;',
        (user_id,)
    )

    await get_tag_command_handler(callback.message, user_id=user_id, edit=True)


@router.callback_query(F.data.split()[0] == TagKeyboard.button_callback_3)
async def get_switch_url_callback_query_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    if callback.from_user.username is None:
        await callback.answer(Messages.cannot_switch_url_callback_message, True)
        return
    
    await connection.execute(
        'UPDATE users SET url_enabled = NOT url_enabled WHERE id = ?;',
        (user_id,)
    )

    await get_tag_command_handler(callback.message, user_id=user_id, edit=True)


async def _send_tag_message(message: Message, tag_enabled: bool, url_enabled: bool, edit: bool):
    markup = await TagKeyboard.markup(not tag_enabled, url_enabled)
    if not tag_enabled:
        text = Messages.tag_message_no_name
    else:
        text = Messages.tag_message

    if not edit:
        await message.answer(text, reply_markup=markup)
    else:
        await message.edit_text(text, reply_markup=markup)
