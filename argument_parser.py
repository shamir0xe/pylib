import sys
import shlex


class ArgumentParser:
    def __init__(self, index = 1, option_prefix = '-'):
        """
        Args:
            index (int, optional): [index where to start reading sys.argv]. Defaults to 1.
            option_prefix (str, optional): [the character that specifies an option]. Defaults to '-'.
        """
        self.buff = sys.argv[index:]
        self.prefix = option_prefix
        # self.terminal = " ".join(map(shlex.quote, sys.argv[index:]))
        self.opts = [opt for opt in self.buff[index:] if self.__is_option(opt)]
        
    def __is_option(self, str):
        return len(str) > 0 and str.startswith(self.prefix)

    def get_options(self):
        return self.opts

    def get_value(self, option):
        if self.buff.count(option) == 0:
            return False
        index = self.buff.index(option)
        index += 1
        if index < len(self.buff) and not self.__is_option(self.buff[index]):
            return self.buff[index]
        return True

    def get_pairs(self, remove_prefix=False):
        pairs = {}
        for option in self.opts:
            key_name = option
            if remove_prefix:
                while self.__is_option(key_name):
                    key_name = key_name[1:]
            pairs[key_name] = self.get_value(option)
        return pairs

