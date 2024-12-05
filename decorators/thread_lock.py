import functools
import logging

from ..asynchrone.get_lock import GetLock

LOGGER = logging.getLogger(__name__)


def thread_lock(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        ## before
        LOGGER.info(f"locking lock")
        async with GetLock.get():
            result = await func(*args, **kwargs)
        ## after
        LOGGER.info(f"releasing lock")
        return result

    return wrapper
