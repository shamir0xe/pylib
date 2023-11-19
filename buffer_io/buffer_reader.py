from .helpers.character_detector import CharacterDetector
from .buffer import Buffer


class BufferReader:
    """
    string buffer parser class
    """

    CHARACTER_READ_COUNT = 4096

    def __init__(
        self,
        input_buffer: Buffer,
        delimiters: str | None = None,
        exclude_delimiters: str | None = None,
    ):
        self.f = input_buffer
        self.__buff = ""
        self.__buff_position = 0
        self.__buff_length = 0
        self.c = " "
        self.last_char: str | None = None
        self.eof = False
        self.__delimiters = [*CharacterDetector.delimiters]
        if delimiters:
            for char in delimiters:
                self.__delimiters.append(ord(char))
        if exclude_delimiters:
            self.__delimiters = list(
                set(self.__delimiters) - {ord(char) for char in exclude_delimiters}
            )

    def is_space_char(self, character):
        return isinstance(character, str) and (
            character == "" or ord(character) in self.__delimiters
        )

    @staticmethod
    def is_return_char(character) -> bool:
        return character in {"\n", "\r\n", "\n\r"}

    def __read_char(self, pick=False):
        return self.__read_char_from_buffer(pick)

    def __read_char_from_buffer(self, pick=False):
        if self.is_space_char(self.last_char):
            if pick:
                return self.last_char
            temp = self.last_char
            self.last_char = None
            return temp
        if self.__buff_position >= self.__buff_length:
            self.__buff = self.f.read(BufferReader.CHARACTER_READ_COUNT)
            self.__buff_position = 0
            self.__buff_length = len(self.__buff)
            if self.__buff_length == 0:
                self.eof = True
                return ""
        res = self.__buff[self.__buff_position]
        self.__buff_position += 1 if not pick else 0
        return res

    def skip_spaces(self) -> None:
        while not self.eof and self.is_space_char(self.c):
            self.c = self.__read_char()

    def read(self) -> str:
        self.skip_spaces()
        res = []
        while not self.is_space_char(self.c):
            if self.c is not None:
                res.append(self.c)
            self.c = self.__read_char()
            self.last_char = self.c
        return "".join(res)

    def end_of_buffer(self) -> bool:
        return self.eof

    def next_string(self) -> str:
        return self.read()

    def next_int(self) -> int:
        return int(self.read())

    def next_float(self) -> float:
        return float(self.read())

    def next_line(self) -> str:
        res = []
        while True:
            self.c = self.__read_char()
            if self.c is not None:
                res.append(self.c)
            if self.eof or self.is_return_char(self.c):
                break
        return "".join(res)

    def next_char(self, pick=False) -> str | None:
        return self.__read_char(pick)

    def close(self):
        return self.f.close()
