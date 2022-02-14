import os.path

from io.buffer import Buffer


class FileBuffer(Buffer):
    def __init__(self, file_path: str, mode: str = "r"):
        self.f = None
        if os.path.isfile(file_path):
            self.f = open(file_path, mode)
        else:
            raise FileNotFoundError()

    def read(self, count: int = 1):
        return self.f.read(count)

    def write(self, string: str) -> None:
        self.f.write(string)

    def close(self):
        return self.f.close()
