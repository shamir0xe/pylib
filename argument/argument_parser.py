import sys
from typing import Optional


class ArgumentParser:
    def __init__(self, index=1, option_prefix="-"):
        """
        Args:
            index (int, optional): [index where to start reading
                sys.argv]. Defaults to 1.
            option_prefix (str, optional): [the character that specifies
                an option]. Defaults to '-'.
        """
        self.buff = sys.argv[index:]
        self.prefix = option_prefix
        self.options = {}
        self.__pre_process()

    def __pre_process(self) -> None:
        last_opt = ""
        values: list[str] = []
        for temp in self.buff:
            if self.__is_option(temp):
                if last_opt != "":
                    self.options[last_opt] = " ".join(values)
                last_opt, values = (self.__trim(temp), [])
            else:
                values.append(str(temp))
        if last_opt != "":
            self.options[last_opt] = " ".join(values)

    def __trim(self, opt: str) -> str:
        while opt.startswith(self.prefix):
            opt = opt[len(self.prefix):]
        return opt

    def __is_option(self, candidate: str) -> bool:
        return len(candidate) > 0 and candidate.startswith(self.prefix)

    @staticmethod
    def get_options(**kwargs) -> dict[str, str]:
        return ArgumentParser(**kwargs).options

    @staticmethod
    def is_option(option: str, **kwargs) -> bool:
        return option in ArgumentParser(**kwargs).options

    @staticmethod
    def get_value(option: str, **kwargs) -> Optional[str]:
        options = ArgumentParser(**kwargs).options
        if option not in options or len(options[option]) == 0:
            return None
        return options[option]
