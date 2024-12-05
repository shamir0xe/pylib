from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    data: T
    id: int = field(default=-1)
