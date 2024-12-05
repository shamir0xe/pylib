import functools
import logging
import traceback

from ..utils.time.timer import Timer
from ..types.time_formats import TimeFormats


def time_checker(
    logger: logging.Logger = logging.getLogger(__name__),
    time_limit: float = -1,
    name: str = "",
):
    """Given a time limit in seconds"""

    name = name if name else "function-time"

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timer = Timer()
            error = None
            result = None
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                error = e
            elapsed_time = timer.elapsed_time(TimeFormats.SEC)
            if time_limit > -0.1:
                logger.info(
                    f"[{name}]: {elapsed_time:2.02f}s  << limit was {time_limit}s"
                )
            else:
                logger.info(f"[{name}]: {elapsed_time:2.02f}s")

            if error:
                traceback.print_exc()
                raise Exception(error)
            return result

        return wrapper

    return decorator
