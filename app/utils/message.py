from asyncio import Lock
from typing import Tuple, Optional

from loader import connection
from utils.echo import MessageResponse


class HandleMessageResponse:
    def __init__(self, messages: MessageResponse):
        self.messages = messages

        self._lock = Lock()
    
    async def save(self):
        async with self._lock:
            async with await connection.execute(
                'SELECT unique_id FROM messages ORDER BY -unique_id LIMIT 1 OFFSET 0;'
            ) as cursor:
                row: Optional[Tuple[int]] = await cursor.fetchone()
            
            if row is not None:
                unique_id = row[0] + 1
            else:
                unique_id = 0
            
            await connection.executemany(
                'INSERT INTO messages(id, message_id, unique_id) VALUES(?, ?, ?)',
                [(*i, unique_id) for i in self.messages]
            )
