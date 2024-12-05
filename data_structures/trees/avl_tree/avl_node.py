from __future__ import annotations

from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class AvlNode(Generic[T]):
    def __init__(self, data: T) -> None:
        self.data = data
        self.left: Optional[AvlNode[T]] = None
        self.right: Optional[AvlNode[T]] = None
        self.height: int = 1

    def update_height(self) -> None:
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = max(left_height, right_height) + 1

    def get_balance_factor(self) -> int:
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        return left_height - right_height

    def rotate_right(self) -> Optional[AvlNode[T]]:
        x = self.left
        if not x:
            return None
        t_2 = x.right
        x.right = self
        self.left = t_2
        self.update_height()
        x.update_height()
        return x

    def rotate_left(self) -> Optional[AvlNode[T]]:
        y = self.right
        if not y:
            return None
        t_2 = y.left
        y.left = self
        self.right = t_2
        self.update_height()
        y.update_height()
        return y

    def __repr__(self):
        return str(self.data)
