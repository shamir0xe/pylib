from abc import ABC


class Buffer(ABC):
    def read(self, count: int = 1) -> str:
        return ""

    def write(self, string: str) -> None:
        pass

    def write_line(self, string: str) -> None:
        pass

    def flush(self):
        pass

    def close(self) -> None:
        pass
