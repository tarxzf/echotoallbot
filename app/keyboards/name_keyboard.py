from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class NameKeyboard:
    button_text_1 = '✏️ Установить имя'
    button_callback_1 = 'change_name'

    button_text_2 = '📄 Изменить имя'

    button_text_3 = '🫥 Скрыть имя'
    button_callback_3 = 'cover_name'

    button_text_4 = '🚫 Отмена'
    button_callback_4 = 'cancel_name'

    @classmethod
    async def markup(self, edit_name: bool = False) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=(self.button_text_1, self.button_text_2)[edit_name],
                        callback_data=self.button_callback_1
                    )
                ]
            ]
        )
    
    @classmethod
    async def changing_name_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=self.button_text_3,
                        callback_data=self.button_callback_3
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=self.button_text_4,
                        callback_data=self.button_callback_4
                    )
                ]
            ]
        )
