from ..buffer_io.buffer_reader import BufferReader
from ..buffer_io.string_buffer import StringBuffer


class StringHelper:
    @staticmethod
    def camel_to_snake(word: str) -> str:
        res: list[str] = []
        i = 0
        cur_token = ""
        consecutive = 0
        while i < len(word):
            if word[i].upper() == word[i]:
                # AbcdEfgHIJ -> Abcd, Efg, HIJ
                if consecutive == 0:
                    # ABcde -> A, Bcde
                    res += [cur_token]
                    cur_token = ""
                consecutive += 1
            else:
                if consecutive != 0:
                    if consecutive > 1:
                        # AbcDEFg -> Abc, DE, Fg
                        res += [cur_token[:-1]]
                        cur_token = cur_token[-1]
                    else:
                        # AbcdEfg -> Abcd, Efg
                        pass
                consecutive = 0
            cur_token += word[i]
            i += 1
        if cur_token != "":
            res += [cur_token]
        res = [token.lower() for token in res if token != ""]
        return "_".join(res)

    @staticmethod
    def snake_to_camel(snake: str, first_capital: bool = False):
        reader = BufferReader(StringBuffer(snake), delimiters="_")
        camel = ""
        while not reader.end_of_buffer():
            token = reader.next_string()
            token_list = list(token)
            token_list[0] = chr(ord(token_list[0]) + ord("A") - ord("a"))
            camel += "".join(token_list)
        if not first_capital:
            camel = camel[0].lower() + camel[1:]
        return camel
