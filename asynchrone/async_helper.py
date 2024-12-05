import asyncio
import logging
from typing import Any, Callable

from .get_lock import GetLock
from .get_or_create_event_loop import GetOrCreateEventLoop

LOGGER = logging.getLogger(__name__)


class AsyncHelper:
    @staticmethod
    async def async_retry(
        fn: Callable,
        *args,
        timeout_seconds: float = -1,
        try_count: int = 5,
        sleep_time: float = 0.2,
    ) -> Any:
        if try_count <= 0:
            raise Exception("Maximum retries occurred")
        try:
            # Run the function with timeout
            task = asyncio.create_task(fn(*args), name="fn")
            if timeout_seconds > 0:
                try:
                    return await asyncio.wait_for(task, timeout=timeout_seconds)
                except asyncio.TimeoutError:
                    LOGGER.info(
                        f"[AsyncRetry] Timeout occurred, retrying in {sleep_time} // {try_count}"
                    )
                    task.cancel()
                    await asyncio.sleep(sleep_time)
                    return await AsyncHelper.async_retry(
                        fn,
                        *args,
                        timeout_seconds=timeout_seconds,
                        try_count=try_count - 1,
                        sleep_time=sleep_time,
                    )
            else:
                # No timeout, await task directly
                return await task
        except asyncio.CancelledError as e:
            LOGGER.info("[AsyncRetry] Operation cancelled")
            raise
        except Exception as e:
            LOGGER.error(f"[AsyncRetry] An error occurred: {e}")
            raise

    @staticmethod
    def run_with_retries(fn: Callable, *args, **kwargs) -> Any:
        timeout_seconds = kwargs.get("timeout_seconds", -1)
        try_count = kwargs.get("retry_count", 5)

        with GetLock.threading_lock() as _:
            loop = GetOrCreateEventLoop().event_loop

        if loop.is_running():
            # Submit to the running loop
            future = asyncio.run_coroutine_threadsafe(
                AsyncHelper.async_retry(
                    fn, *args, timeout_seconds=timeout_seconds, try_count=try_count
                ),
                loop,
            )
            return future.result()
        else:
            # Create a new loop for blocking context
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(
                AsyncHelper.async_retry(
                    fn, *args, timeout_seconds=timeout_seconds, try_count=try_count
                )
            )
