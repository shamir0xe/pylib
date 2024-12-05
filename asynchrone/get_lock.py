import asyncio
import threading


lock = asyncio.Lock()
threading_lock = threading.Lock()


class GetLock:
    @staticmethod
    def get():
        return lock

    @staticmethod
    def threading_lock():
        return threading_lock
