from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Comparable(Protocol):
    def __lt__(self, __x: Any) -> bool: ...

    def __le__(self, __x: Any) -> bool: ...
