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
            delimiters: str = None,
            exclude_delimiters: str = None,
    ):
        self.f = input_buffer
        self.__buff = ""
        self.__buff_position = 0
        self.__buff_length = 0
        self.c = " "
        self.last_char = None
        self.eof = False
        self.__delimiters = [*CharacterDetector.delimiters]
        if delimiters:
            for char in delimiters:
                self.__delimiters.append(ord(char))
        if exclude_delimiters:
            for char in exclude_delimiters:
                self.__delimiters = list(
                    filter(lambda a: a != ord(char), self.__delimiters)
                )
        # self.__log_writer = log_writer

    def is_space_char(self, character):
        return type(character) is str and (character == '' or
                                           ord(character) in self.__delimiters)

    @staticmethod
    def is_return_char(character):
        return character in ['\n', '\r\n', '\n\r']

    def __read_char(self, pick=False):
        res = self.__read_char_from_buffer(pick)
        # print(f'~~~ {res}')
        # if self.__log_writer is not None and len(res) > 0 and True:
        #     # not (
        #     #         CharacterHandler.is_digit(res) or CharacterHandler.is_alphabet(res) or
        #     #         CharacterHandler.is_separator(res) or CharacterHandler.is_escape_char(res) or
        #     #         CharacterHandler.is_parenthesis(res) or CharacterHandler.is_operator(res)):
        #     self.__log_writer.add_log('[{}] -- [{}]'.format(
        #         CharacterHandler.get_char_type(res), ord(res)))
        return res

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
                return ''
        res = self.__buff[self.__buff_position]
        self.__buff_position += 1 if not pick else 0
        return res

    def skip_spaces(self) -> None:
        while True:
            if self.eof or not self.is_space_char(self.c):
                break
            self.c = self.__read_char()

    def read(self) -> str:
        self.skip_spaces()
        res = ""
        while not self.is_space_char(self.c):
            res += self.c
            self.c = self.__read_char()
            self.last_char = self.c
            # print('[~~~~~]{}-{}'.format(self.c, ord(self.c)))
        return res

    def end_of_buffer(self) -> bool:
        return self.eof

    def next_string(self) -> str:
        return self.read()

    def next_int(self) -> int:
        return int(self.read())

    def next_float(self) -> float:
        return float(self.read())

    def next_line(self) -> str:
        res = ""
        while True:
            self.c = self.__read_char()
            res += self.c
            if self.eof or self.is_return_char(self.c):
                break
        return res

    def next_char(self, pick=False) -> str:
        c = self.__read_char(pick)
        # print(f'~~~<{c}>')
        return c

    def close(self):
        return self.f.close()
