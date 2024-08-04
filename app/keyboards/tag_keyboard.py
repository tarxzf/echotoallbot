from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class TagKeyboard:
    button_text_1 = '✅ Включить'
    button_callback_1 = 'tag_switch'

    button_text_2 = '❌ Выключить'

    button_text_3 = '✅ Ссылка на аккаунт: Да'
    button_callback_3 = 'url_switch'

    button_text_4 = '❌ Ссылка на аккаунт: Нет'

    @classmethod
    async def markup(self, tag: bool, url: bool) -> InlineKeyboardMarkup:
        tag_text = self.button_text_1 if tag else self.button_text_2
        url_text = self.button_text_3 if url else self.button_text_4
        
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=tag_text,
                        callback_data=self.button_callback_1
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=url_text,
                        callback_data=self.button_callback_3
                    )
                ]
            ]
        )
