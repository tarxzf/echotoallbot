from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsEnabledFilter(BaseFilter):
    def __init__(self, option: bool):
        self.option = option
    
    async def __call__(self, _: Message) -> bool:
        return self.option
