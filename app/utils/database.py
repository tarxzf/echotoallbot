from aiosqlite import connect, Connection
from asyncio import Lock
from typing import Any


class Database:
    def __init__(self, path: str):
        self.path = path

        self.connection: (Connection | None) = None

        self.lock = Lock()
    
    def __getattr__(self, item: str) -> Any:
        attr = getattr(self.connection, item)
        if callable(attr):
            async def func(*args, **kwargs) -> Any:
                async with self.lock:
                    result = await attr(*args, **kwargs)
                    await self.connection.commit()
                return result
            return func
        return attr
    
    async def initialize(self):
        if self.connection is None:
            self.connection = await connect(self.path)
    
    async def close(self):
        if self.connection is not None:
            await self.connection.close()
            self.connection = None
