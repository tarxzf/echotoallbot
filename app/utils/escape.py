from asyncio import get_event_loop
from html import escape as _esc
from html import unescape


async def escape(text: str, un: bool = False) -> str:
    loop = get_event_loop()

    if not un:
        func = _esc
    else:
        func = unescape
    
    result = await loop.run_in_executor(None, func, text)
    return result
