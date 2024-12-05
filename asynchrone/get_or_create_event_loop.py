import asyncio
import logging

from ..decorators.singleton import singleton

LOGGER = logging.getLogger("[GetOrCreateEventLoop]")


@singleton
class GetOrCreateEventLoop:
    event_loop: asyncio.AbstractEventLoop

    def __init__(self) -> None:
        self.event_loop = self.get_or_create()

    def get_or_create(self) -> asyncio.AbstractEventLoop:
        try:
            return asyncio.get_running_loop()
        except Exception as e:
            LOGGER.info(f"{e}, creating a new event-loop")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
