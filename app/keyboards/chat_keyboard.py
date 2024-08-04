from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional


class ChatKeyboard:
    button_callback_1 = 'user_name'
    button_callback_2 = 'user_name_no_url'

    @classmethod
    async def markup(self, user_name: str, *, url: Optional[str]) -> InlineKeyboardMarkup:
        if url:
            button = InlineKeyboardButton(
                text=user_name,
                url=url
            )
        else:
            button = InlineKeyboardButton(
                text=user_name,
                callback_data=self.button_callback_2
            )
        return InlineKeyboardMarkup(inline_keyboard=[[button]])
