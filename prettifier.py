import random
from enum import Enum

from .buffer_io import (StandardInputReader, FileReader, append_to_file)
from .utils import (debug_text)

class StringTypes(Enum):
    Alphabet = 'alphabet'
    Digit = 'digit'
    Parenthesis = 'parenthesis'
    Operator = 'operator'
    Separator = 'separator'


class Colors(Enum):
    Black = '\033[30m'
    Red = '\033[31m'
    Green = '\033[32m'
    Yellow = '\033[33m'
    Blue = '\033[34m'
    Magenta = '\033[35m'
    Cyan = '\033[36m'
    White = '\033[37m'
    Reset = '\033[0m'


class Log:
    def __init__(self, filename="/Users/shamir0xe/.prettifier_log"):
        self.filename = filename

    def add_log(self, string):
        append_to_file(self.filename, string + '\n')


class PrettifierConfig:
    class ConfigTypes(Enum):
        SwitcherConfig = 'SC'
        SpecialName = 'SN'

    def __init__(self, file_name="/Users/shamir0xe/.prettifier_cfg"):
        self.f = FileReader(file_name)
        self.__switcher = {}
        self.__special_names = {}
        self.__retrieve_config()

    def __retrieve_config(self):
        color_values = set(color for color in Colors)
        while not self.f.end_of_buffer():
            f = self.f
            cf_type, key, value = f.read(), f.read(), f.read()
            if cf_type == PrettifierConfig.ConfigTypes.SwitcherConfig.value:
                self.__switcher[StringTypes[key]] = Colors[value]
            elif cf_type == PrettifierConfig.ConfigTypes.SpecialName.value:
                self.__special_names[key.lower(
                )] = Colors[value] if value in color_values else value
            else:
                debug_text('Bad Config File: [%, %, %]', cf_type, key, value)

    def get(self, config_type):
        sw = {
            PrettifierConfig.ConfigTypes.SwitcherConfig: self.__switcher,
            PrettifierConfig.ConfigTypes.SpecialName: self.__special_names
        }
        return sw.get(config_type, 'bad input')


class PrettifierStream:
    def __init__(self, input_reader, config=None):
        self.input_reader = input_reader
        self.switcher = config.get(PrettifierConfig.ConfigTypes.SwitcherConfig)
        self.special_names = config.get(
            PrettifierConfig.ConfigTypes.SpecialName)

    @staticmethod
    def __escape_char(char):
        return char in (' ', '\t', '\n', '\r', '\b', '\v', '\f', chr(10), chr(32))

    @staticmethod
    def __is_dot(char):
        return char in ('.')

    @staticmethod
    def __is_separator(char):
        return char in ('\'', '"', '`', '/', '\\', ':', ',', ';', '.')

    @staticmethod
    def __is_parenthesis(char):
        return char in ('(', ')', '[', ']', '{', '}')

    @staticmethod
    def __is_operator(char):
        return char in ('+', '-', '*', '^', '%', '&', '|', '~', '!', '=', '@',
                        '#', '$', '>', '<')

    @staticmethod
    def __is_digit(char):
        return ord('0') <= ord(char) <= ord('9')

    @staticmethod
    def __is_alphabet(char):
        return (ord('a') <= ord(char) <= ord('z')) or (ord('A') <= ord(char) <=
                                                       ord('Z'))

    def __get_string_type(self, string):
        flag = False
        for char in string:
            flag |= self.__is_alphabet(char)
        if flag:
            return StringTypes.Alphabet
        # TODO
        return StringTypes.Digit

    def __get_char_type(self, char):
        if self.__is_separator(char):
            return StringTypes.Separator
        if self.__is_parenthesis(char):
            return StringTypes.Parenthesis
        if self.__is_operator(char):
            return StringTypes.Operator
        if self.__is_digit(char):
            return StringTypes.Digit
        return StringTypes.Alphabet

    def colorify(self, string, color_string):
        # debug_text('str, type: (%, %)', string, color_string)
        return '{}{}{}'.format(color_string, string, Colors.Reset.value)

    def __check_logic(self, string, index, *args):
        if index >= len(string) or index < 0:
            return True
        char = string[index]
        res = True
        idx = 0
        while idx < len(args):
            st_type = args[idx]
            logic = args[idx + 1]
            idx += 2
            if st_type is StringTypes.Digit:
                res &= self.__is_digit(char) is logic
            if st_type is StringTypes.Alphabet:
                res &= self.__is_alphabet(char) is logic
        return res

    def stream(self):
        input_reader = self.input_reader
        while not input_reader.eof:
            while self.__escape_char(input_reader.next_char(True)):
                escape_char = input_reader.next_char()
                print(escape_char, end='', flush=True)
            string = input_reader.next_string()
            if string in ("\033[F", "\033[A"):
                print(string, end='', flush=True)
            sz = len(string)
            colors_arr = [Colors.Reset for _ in range(sz)]

            idx = 0
            for char in string:
                char_type = self.__get_char_type(char)
                if char_type is StringTypes.Digit:
                    good_digit = True
                    i = idx - 1
                    while i >= 0 and self.__is_digit(string[i]):
                        i -= 1
                    good_digit &= self.__check_logic(string, i,
                                                     StringTypes.Alphabet,
                                                     False)
                    i = idx + 1
                    while i < len(string) and self.__is_digit(string[i]):
                        i += 1
                    good_digit &= self.__check_logic(string, i,
                                                     StringTypes.Alphabet,
                                                     False)
                    if not good_digit:
                        char_type = StringTypes.Alphabet
                colors_arr[idx] = self.switcher[char_type].value
                idx += 1

            color_values = set(color for color in Colors)
            keys = list(self.special_names.keys())
            keys = sorted(keys)
            keys.reverse()
            idx = 0
            while idx < sz:
                flag = False
                for name in keys:
                    end_idx = idx + len(name)
                    if end_idx <= sz and string[idx:end_idx].lower() == name:
                        check = True
                        check &= self.__check_logic(string, idx - 1,
                                                    StringTypes.Digit, False,
                                                    StringTypes.Alphabet,
                                                    False)
                        check &= self.__check_logic(string, end_idx,
                                                    StringTypes.Digit, False,
                                                    StringTypes.Alphabet,
                                                    False)
                        if check:
                            color = self.special_names[name]
                            cycle = [color]
                            if not color in color_values:
                                cycle = []
                                for char in color:
                                    for real_color in color_values:
                                        if real_color.name in ('Black',
                                                               'Reset'):
                                            continue
                                        if real_color.name[0] == char:
                                            cycle.append(real_color.value)
                                            break
                            flag = True
                            cycle_size = len(cycle)
                            random.shuffle(cycle)
                            for j in range(len(name)):
                                colors_arr[idx] = cycle[j % cycle_size]
                                idx += 1
                            break
                if not flag:
                    idx += 1
            idx = 0
            while idx < sz:
                char = self.colorify(string[idx], colors_arr[idx])
                print(char, end='', flush=True)
                idx += 1


def main():
    # log_writer = Log()
    input_reader = StandardInputReader(log_writer=None)
    config = PrettifierConfig()
    stream = PrettifierStream(input_reader, config)
    stream.stream()


if __name__ == '__main__':
    main()
