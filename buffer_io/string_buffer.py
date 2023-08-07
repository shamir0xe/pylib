from .buffer import Buffer


class StringBuffer(Buffer):
    """
    Turn a string into buffer
    """

    def __init__(self, buff: str):
        self.buff = buff
        self.pos = 0
        self.length = len(buff)

    def read(self, count: int = 1) -> str:
        res = ""
        while count > 0 and self.pos < self.length:
            res += self.buff[self.pos]
            self.pos += 1
            count -= 1
        return res

    def update(self):
        self.length = len(self.buff)

    def write(self, string: str) -> None:
        self.buff += string
        self.update()

    def write_line(self, string: str) -> None:
        self.write(string)
        self.write("\n")
        self.update()
