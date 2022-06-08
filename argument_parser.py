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
        self.opts = [opt for opt in self.buff if self.is_option(opt)]
        
    def is_option(self, string):
        return len(string) > 0 and string.startswith(self.prefix)

    def get_options(self):
        return self.opts

    def get_value(self, option):
        if self.buff.count(option) == 0:
            return False
        index = self.buff.index(option)
        index += 1
        if index < len(self.buff) and not self.is_option(self.buff[index]):
            return self.buff[index]
        return True
   
    @staticmethod
    def get_pairs(remove_prefix=False, *args, **kwargs) -> dict:
        parser = ArgumentParser(*args, **kwargs)
        pairs = {}
        for option in parser.opts:
            key_name = option
            if remove_prefix:
                while parser.is_option(key_name):
                    key_name = key_name[1:]
            pairs[key_name] = parser.get_value(option)
        return pairs
