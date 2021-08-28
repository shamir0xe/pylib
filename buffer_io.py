import os.path
import sys

FLUSH = "$#!$$"


class StringBuffer:
    """
    Turn a string into buffer
    """
    def __init__(self, buff):
        self.buff = buff
        self.pos = 0
        self.length = len(buff)

    def read(self, count=1):
        res = ""
        while count > 0 and self.pos < self.length:
            res += self.buff[self.pos]
            self.pos += 1
            count -= 1
        return res

    def close(self):
        pass


class StandardInputBuffer:
    def __init__(self):
        self.__buff = ""
        self.__pos = 0
        self.__end = False

    def __in(self):
        return sys.stdin.read(1)
        # return sys.stdin.readline()
        # return input() + "\n"

    def __load_buffer(self):
        self.__buff = ""
        self.__pos = 0
        try:
            self.__buff = self.__in()
        except:
            return ""
        return self.__buff

    def read(self, count=1):
        res = ""
        if self.__pos >= len(self.__buff):
            self.__load_buffer()
        while count > 0 and self.__pos < len(self.__buff):
            res += self.__buff[self.__pos]
            count -= 1
            self.__pos += 1
        # print('RESSS: {}'.format(res))
        return res

    def close(self):
        pass


class CharacterTypes:
    Alphabet = 'alphabet'
    Digit = 'digit'
    Parenthesis = 'parenthesis'
    Operator = 'operator'
    Separator = 'separator'
    Unknown = ''


class CharacterHandler:
    delimiters = [
        ord(' '),
        ord('\t'),
        ord('\n'),
        ord('\r'),
        ord('\b'),
        ord('\v'),
        ord('\f'),
    ]

    @staticmethod
    def get_char_type(char):
        if CharacterHandler.is_separator(char):
            return CharacterTypes.Separator
        if CharacterHandler.is_parenthesis(char):
            return CharacterTypes.Parenthesis
        if CharacterHandler.is_operator(char):
            return CharacterTypes.Operator
        if CharacterHandler.is_digit(char):
            return CharacterTypes.Digit
        if CharacterHandler.is_alphabet(char):
            return CharacterTypes.Alphabet
        return CharacterTypes.Unknown

    @staticmethod
    def is_escape_char(char):
        return len(char) == 0 and ord(char) in CharacterHandler.delimiters

    @staticmethod
    def is_dot(char):
        return char in ('.')

    @staticmethod
    def is_separator(char):
        return char in ('\'', '"', '`', '/', '\\', ':', ',', ';', '.', '_')

    @staticmethod
    def is_parenthesis(char):
        return char in ('(', ')', '[', ']', '{', '}')

    @staticmethod
    def is_operator(char):
        return char in ('+', '-', '*', '^', '%', '&', '|', '~', '!', '=', '@',
                        '#', '$', '>', '<')

    @staticmethod
    def is_digit(char):
        return ord('0') <= ord(char) <= ord('9')

    @staticmethod
    def is_alphabet(char):
        return ord('a') <= ord(char) <= ord('z') or ord('A') <= ord(
            char) <= ord('Z')


class BufferReader:
    """
    string buffer parser class
    """
    def __init__(self, input_buffer, delimiters=None, log_writer=None, exclude_delimiters=None):
        self.f = input_buffer
        self.__buff = ""
        self.__buff_position = 0
        self.__buff_length = 0
        self.c = " "
        self.last_char = None
        self.eof = False
        self.__delimiters = [*CharacterHandler.delimiters]
        if delimiters:
            for char in delimiters:
                self.__delimiters.append(ord(char))
        if exclude_delimiters:
            for char in exclude_delimiters:
                self.__delimiters = list(
                    filter(lambda a: a != ord(char), self.__delimiters)
                    )
        self.__log_writer = log_writer

    def is_space_char(self, character):
        return type(character) is str and (character == '' or
                                           ord(character) in self.__delimiters)

    @staticmethod
    def is_return_char(character):
        return character in ('\n')

    def __read_char(self, pick=False):
        res = self.__read_char_from_buffer(pick)
        if self.__log_writer is not None and len(res) > 0 and True:
            # not (
            #         CharacterHandler.is_digit(res) or CharacterHandler.is_alphabet(res) or
            #         CharacterHandler.is_separator(res) or CharacterHandler.is_escape_char(res) or
            #         CharacterHandler.is_parenthesis(res) or CharacterHandler.is_operator(res)):
            self.__log_writer.add_log('[{}] -- [{}]'.format(
                CharacterHandler.get_char_type(res), ord(res)))
        return res

    def __read_char_from_buffer(self, pick=False):
        if self.is_space_char(self.last_char):
            if pick:
                return self.last_char
            temp = self.last_char
            self.last_char = None
            return temp
        if self.__buff_position >= self.__buff_length:
            self.__buff = self.f.read(10)
            self.__buff_position = 0
            self.__buff_length = len(self.__buff)

            if self.__buff_length == 0:
                self.eof = True
                return ''
        res = self.__buff[self.__buff_position]
        self.__buff_position += 1 if not pick else 0
        return res

    def skip_spaces(self):
        while True:
            if self.eof or not self.is_space_char(self.c):
                break
            self.c = self.__read_char()

    def read(self):
        self.skip_spaces()
        res = ""
        while not self.is_space_char(self.c):
            res += self.c
            self.c = self.__read_char()
            self.last_char = self.c
            # print('[~~~~~]{}-{}'.format(self.c, ord(self.c)))
        return res

    def end_of_buffer(self):
        self.skip_spaces()
        return self.eof

    def next_string(self):
        return self.read()

    def next_int(self):
        return int(self.read())

    def next_float(self):
        return float(self.read())

    def next_line(self):
        res = ""
        while True:
            if self.eof or self.is_return_char(self.c):
                # self.__read_char()  # it should be {return} char
                break
            res += self.c
            self.c = self.__read_char()
        return res

    def next_char(self, pick=False):
        return self.__read_char(pick)

    def close(self):
        return self.f.close()


class StandardInputReader(BufferReader):
    def __init__(self, log_writer=None):
        super().__init__(StandardInputBuffer(), log_writer=log_writer)


class FileReader(BufferReader):
    """
    an utility class for reading files
    """
    def __init__(self, file_name, **kwargs):
        if os.path.isfile(file_name):
            super().__init__(open(file_name, "r"), **kwargs)
        else:
            super().__init__(StringBuffer(""))

    def end_of_file(self):
        return self.end_of_buffer()


class BufferWriter:
    """
    writer buffer class for writing efficient into string buffer
    """
    def __init__(self):
        self.__buff = ""

    def write(self, string):
        self.__buff += str(string)

    def write_line(self, string):
        self.write(string)
        self.write("\n")

    def flush_buffer(self):
        res = self.__buff
        self.__buff = ""
        return res


class FileWriter(BufferWriter):
    """
    utility class for writing into files
    """
    def __init__(self, file_name, mode="w+"):
        super().__init__()
        self.f = open(file_name, mode)

    def flush(self):
        self.f.write(self.flush_buffer())

    def close(self):
        self.flush()
        self.f.close()


def append_to_file(filename, string):
    f = FileWriter(filename, "a+")
    f.write(string)
    f.close()
