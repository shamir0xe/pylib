from abc import ABC


class Buffer(ABC):
    def read(self, count: int = 1):
        pass

    def write(self):
        pass

    def close(self):
        pass
