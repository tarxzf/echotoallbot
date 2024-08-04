from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Awaitable, Callable, Optional, Tuple

from loader import connection
from utils.date import get_current_date


class RegisteringUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: dict[str, Any]
    ) -> Awaitable[Any]:
        if not message.from_user.is_bot:
            user_id = message.from_user.id

            async with await connection.execute(
                'SELECT blocked FROM users WHERE id = ?;',
                (user_id,)
            ) as cursor:
                row: Optional[Tuple[bool]] = await cursor.fetchone()
            
            if row is None:
                date = await get_current_date()
                await connection.execute(
                    'INSERT INTO users (id, registration_date, blocked) VALUES (?, ?, false);',
                    (user_id, date)
                )
            else:
                user_blocked = row[0]
                if user_blocked:
                    await connection.execute(
                        'UPDATE users SET blocked = false WHERE id = ?;',
                        (user_id,)
                    )
        
        result = await handler(message, data)
        return result
