from __future__ import annotations
from .buffer import Buffer


class BufferWriter:
    """
    writer buffer class for writing efficient into string buffer
    """
    def __init__(self, buffer: Buffer):
        self.__buffer = buffer
        self.__inner_writer = ""

    def write(self, string) -> BufferWriter:
        self.__buffer.write(string)
        self.__buffer.flush()
        # self.__inner_writer += string
        return self

    def write_line(self, string) -> BufferWriter:
        self.write(f'{string}\n')
        return self

    def flush(self):
        flushed = self.__inner_writer
        self.__buffer.flush()
        return flushed

    def close(self) -> BufferWriter:
        self.flush()
        self.__buffer.close()
        return self
