from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from typing import Tuple, Optional

from data.config import TAGS_COMMAND_ENABLED, TAG_BUTTON_TYPE
from data.messages import Messages
from data.types import TagButtonType
from filters.enable import IsEnabledFilter
from filters.equals import Equals
from keyboards.name_keyboard import NameKeyboard
from loader import connection
from utils.escape import escape

router = Router()


class NameState(StatesGroup):
    name = State()
    message_id = State()


@router.message(
    Command('name'),
    IsEnabledFilter(TAGS_COMMAND_ENABLED),
    Equals(TAG_BUTTON_TYPE, TagButtonType.NAME)
)
async def get_name_command_handler(message: Message):
    user_id = message.from_user.id

    async with await connection.execute(
        'SELECT name FROM users WHERE id = ?;',
        (user_id,)
    ) as cursor:
        row: Tuple[Optional[str]] = await cursor.fetchone()
    
    user_name = row[0]

    if user_name is None:
        text = Messages.name_message_without_name
        markup = await NameKeyboard.markup()
    else:
        markup = await NameKeyboard.markup(True)
        text = Messages.name_message.format(user_name=user_name)
    
    await message.answer(text, reply_markup=markup)


@router.message(
        NameState.name,
        F.text
)
async def get_name_text_message_handler(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    user_name = await escape(message.text)

    await change_name(message, bot, state, user_id, user_name)


@router.callback_query(F.data.split()[0] == NameKeyboard.button_callback_1)
async def get_change_name_callback_query_handler(callback: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = callback.from_user.id

    markup = await NameKeyboard.changing_name_markup()
    info_message = await callback.message.edit_text(Messages.name_message_change,
                                                    reply_markup=markup)

    state_data = await state.get_data()
    await state.clear()

    if state_data:
        message_id: int = state_data.get('message_id')

        try:
            await bot.delete_message(user_id, message_id)
        except TelegramBadRequest:
            ...
    
    await state.update_data(message_id=info_message.message_id)
    await state.set_state(NameState.name)


@router.callback_query(F.data.split()[0] == NameKeyboard.button_callback_4)
async def get_cancel_name_callback_query_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.edit_text(Messages.name_message_canceled)


@router.callback_query(F.data.split()[0] == NameKeyboard.button_callback_3)
async def get_cover_name_callback_query_handler(callback: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = callback.from_user.id

    await change_name(callback.message, bot, state, user_id)


async def change_name(message: Message, bot: Bot, state: FSMContext, user_id: int, user_name: Optional[str] = None):
    state_data = await state.get_data()
    await state.clear()

    message_id: int = state_data.get('message_id')

    await connection.execute(
        'UPDATE users SET name = ? WHERE id = ?;',
        (user_name, user_id)
    )

    if user_name is not None:
        try:
            await bot.delete_message(user_id, message_id)
        except TelegramBadRequest:
            ...
        
        await message.answer(Messages.name_message_changed.format(user_name=user_name))
    else:
        text = Messages.name_message_covered_up

        try:
            await message.edit_text(text)
        except TelegramBadRequest:
            await message.answer(text)
