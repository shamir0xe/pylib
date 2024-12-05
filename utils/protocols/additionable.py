from typing import Any, Protocol, runtime_checkable

@runtime_checkable
class Additionable(Protocol):
    def __add__(self, __x: Any) -> Any: ...

    def __radd__(self, __x: Any) -> Any: ...
