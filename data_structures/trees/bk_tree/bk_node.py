from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class BkNode(Generic[T]):
    obj: T
    value: str
    id: int = field(default=0)

    def __repr__(self) -> str:
        return self.value
