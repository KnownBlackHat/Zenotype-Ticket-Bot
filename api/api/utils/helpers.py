from functools import wraps
from typing import Awaitable, Callable

from aiohttp import web


def ensure_guild[T, **P](func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T | web.Response]]:
    @wraps(func)
    async def inner(*args: P.args, **kwargs: P.kwargs) -> T | web.Response:
        if not isinstance(args[1], web.Request):
            raise ValueError("Didn't recieved request object")
        request: web.Request = args[1]
        guild_id = request.query.get("guild")
        if guild_id is None:
            return web.json_response({"success": False, "error": "missing guild query parameter"})
        try:
            guild_id = int(guild_id)
        except:
            return web.json_response({"success": False, "error": "guild query should be integer type only"})
        ret_val = await func(*args, **kwargs)
        return ret_val
    return inner

