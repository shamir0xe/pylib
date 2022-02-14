import sys
from io.buffer import Buffer


class StandardInputBuffer(Buffer):
    def __init__(self):
        self.__buff = ""
        self.__pos = 0
        self.__end = False

    @staticmethod
    def __in():
        return sys.stdin.read(1)

    def __load_buffer(self) -> str:
        self.__buff = ""
        self.__pos = 0
        try:
            self.__buff = StandardInputBuffer.__in()
        except:
            return ""
        return self.__buff

    def read(self, count=1) -> str:
        res = ""
        if self.__pos >= len(self.__buff):
            self.__load_buffer()
        while count > 0 and self.__pos < len(self.__buff):
            res += self.__buff[self.__pos]
            count -= 1
            self.__pos += 1
        # print('RESSS: {}'.format(res))
        return res

