import sys
from typing import Optional
from ..data.variable_type_modifier import VariableTypeModifier


class ArgumentParser:
    def __init__(self, index=1, option_prefix="-"):
        """
        Args:
        index (int, optional): [index where to start reading sys.argv]. Defaults to 1.
        option_prefix (str, optional): [the character that specifies an option]. Defaults to '-'.
        """
        self.buff = sys.argv[index:]
        self.prefix = option_prefix
        self.options = {}

        self.__pre_process()

    def __pre_process(self) -> None:
        last_opt = ""
        values = []
        for temp in self.buff:
            if self.__is_option(temp):
                if last_opt != "":
                    self.options[last_opt] = values
                last_opt, values = (self.__trim(temp), [])
            else:
                temp = VariableTypeModifier(temp).cast_int().cast_float().get()
                values.append(temp)
        if last_opt != "":
            self.options[last_opt] = values

    def __trim(self, opt: str) -> str:
        while opt.startswith(self.prefix):
            opt = opt[1:]
        return opt

    def __is_option(self, candidate: str) -> bool:
        return len(candidate) > 0 and candidate.startswith(self.prefix)

    @staticmethod
    def get_options() -> list:
        return ArgumentParser().options

    @staticmethod
    def is_option(option: str, **kwargs) -> bool:
        parser = ArgumentParser(**kwargs)
        return option in parser.options

    @staticmethod
    def get_value(option: str, **kwargs) -> Optional[tuple]:
        parser = ArgumentParser(**kwargs)
        options = parser.options
        if not option in options or len(options[option]) == 0:
            return None
        return tuple(options[option])
