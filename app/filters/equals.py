from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Any


class Equals(BaseFilter):
    def __init__(self, option: Any, need: Any):
        self.option = option
        self.need = need
    
    async def __call__(self, _: Message) -> bool:
        return self.option == self.need
