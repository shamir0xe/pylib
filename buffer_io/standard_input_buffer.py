import sys
from .buffer import Buffer


class StandardInputBuffer(Buffer):
    def __init__(self):
        self.__buff = ""
        self.__pos = 0

    def __load_buffer(self, count: int) -> str:
        self.__buff = ""
        self.__pos = 0
        try:
            self.__buff = sys.stdin.read(count)
        except Exception:
            return ""
        return self.__buff

    def read(self, count=1) -> str:
        res = ""
        if self.__pos >= len(self.__buff):
            self.__load_buffer(count)
        while count > 0 and self.__pos < len(self.__buff):
            res += self.__buff[self.__pos]
            count -= 1
            self.__pos += 1
        return res
