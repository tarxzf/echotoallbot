from asyncio import get_event_loop
from datetime import datetime as _dt


async def get_current_date() -> str:
    def _func() -> str:
        return _dt.now().strftime('%x %X')
    
    loop = get_event_loop()
    result = await loop.run_in_executor(None, _func)
    return result
