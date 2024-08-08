from asyncio import get_event_loop
from time import time as _time


async def time() -> float:
    loop = get_event_loop()
    result = await loop.run_in_executor(None, _time)
    return result
