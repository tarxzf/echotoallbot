from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional


class ChatKeyboard:
    button_callback_1 = 'user_name'
    button_callback_2 = 'user_name_no_url'
    button_callback_3 = 'custom_tag'

    @classmethod
    async def markup(
            self,
            user_name: str,
            *,
            url: Optional[str] = None,
            is_tag: bool = True,
            custom_tag: Optional[str] = None
    ) -> InlineKeyboardMarkup:
        if is_tag:
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
        else:
            button = InlineKeyboardButton(
                text=user_name,
                callback_data=self.button_callback_1
            )
        
        keyboard = [[button]]
        if custom_tag is not None:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=custom_tag,
                        callback_data=self.button_callback_3
                    )
                ]
            )

        return InlineKeyboardMarkup(inline_keyboard=keyboard)
