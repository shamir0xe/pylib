from buffer_io import (BufferReader, StringBuffer)


class StringHelper:
    @staticmethod
    def camel_to_snake(word: str):
        # TODO
        pass

    @staticmethod
    def snake_to_camel(snake: str):
        reader = BufferReader(StringBuffer(snake), delimiters='_')
        camel = ''
        while not reader.end_of_buffer():
            token = reader.next_string()
            token_list = list(token)
            token_list[0] = chr(ord(token_list[0]) + ord('A') - ord('a'))
            camel += ''.join(token_list)
        return camel
