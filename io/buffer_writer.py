from .buffer import Buffer


class BufferWriter:
    """
    writer buffer class for writing efficient into string buffer
    """
    def __init__(self, buffer: Buffer):
        self.__buffer = buffer
        self.__inner_writer = ""

    def write(self, string):
        self.__inner_writer += str(string)

    def write_line(self, string):
        self.write(string)
        self.write("\n")

    def flush(self):
        flushed = self.__inner_writer
        self.__buffer.write(self.__inner_writer)
        self.__inner_writer = ""
        return flushed

    def close(self):
        self.flush()
        self.__buffer.close()
