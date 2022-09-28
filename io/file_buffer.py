import os
from .buffer import Buffer
os.umask(0)

def opener(path, flags):
    return os.open(path, flags, 0o777)

class FileBuffer(Buffer):
    def __init__(self, file_path: str, mode: str = "r"):
        self.f = open(file_path, mode, opener=opener)

    def read(self, count: int = 1):
        return self.f.read(count)

    def write(self, string: str) -> None:
        self.f.write(string)
    
    def flush(self) -> None:
        self.f.flush()

    def close(self):
        return self.f.close()
