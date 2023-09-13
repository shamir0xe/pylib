from .buffer import Buffer
import sys


class StandardOutputBuffer(Buffer):
    def __init__(self) -> None:
        super().__init__()

    def write(self, string: str):
        print(string, end="")

    def flush(self):
        sys.stdout.flush()
