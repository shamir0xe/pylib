from typing import Callable, Generic, Iterator, List, Optional, TypeVar

from .avl_node import AvlNode
from ....utils.protocols.comparable import Comparable

T = TypeVar("T")
K = TypeVar("K", bound=Comparable)


class AvlTree(Generic[T, K]):
    """
    AvlTree implementation
    T is the stored node's object
    K is the output type of the comparator
    """

    comparator: Callable[[AvlNode[T]], K]
    root: Optional[AvlNode[T]] = None
    size: int = 0

    def __init__(self, comparator: Callable[[AvlNode[T]], K]) -> None:
        self.comparator = comparator

    def empty(self) -> bool:
        return self.root is None

    def insert(self, node: AvlNode[T]) -> Optional[AvlNode[T]]:
        """Inserts a new node"""
        self.root = self.__insert(self.root, node)
        self.size += 1
        return self.root

    def find(self, target: AvlNode[T]) -> Optional[AvlNode[T]]:
        """Finds a target node"""
        return self.__find(self.root, self.comparator(target))

    def remove(self, target: AvlNode[T]) -> None:
        """Removes the target node"""
        self.size -= 1
        self.root = self.__remove(self.root, self.comparator(target))

    def __insert(
        self, node: Optional[AvlNode[T]], target: AvlNode[T]
    ) -> Optional[AvlNode[T]]:
        if node is None:
            return target

        if self.comparator(target) <= self.comparator(node):
            node.left = self.__insert(node.left, target)
        else:
            node.right = self.__insert(node.right, target)

        return self.rebalance_subtree(node)

    def __find(
        self, node: Optional[AvlNode[T]], target_value: K
    ) -> Optional[AvlNode[T]]:
        if node is None or self.comparator(node) == target_value:
            return node

        if target_value < self.comparator(node):
            return self.__find(node.left, target_value)

        return self.__find(node.right, target_value)

    def __contains__(self, target_value: K) -> bool:
        return self.__find(self.root, target_value) != None

    def __remove(
        self, node: Optional[AvlNode[T]], target_value: K
    ) -> Optional[AvlNode[T]]:
        if node is None:
            return node

        node_value = self.comparator(node)
        if target_value < node_value:
            node.left = self.__remove(node.left, target_value)
        elif target_value > node_value:
            node.right = self.__remove(node.right, target_value)
        else:
            if node.left is None:
                result = node.right
                del node
                return result
            elif node.right is None:
                result = node.left
                del node
                return result

            min_node = self.__find_minimum(node.right)
            node.data = min_node.data
            node.right = self.__remove(node.right, self.comparator(min_node))

        return self.rebalance_subtree(node)

    def rebalance_subtree(self, node: Optional[AvlNode[T]]) -> Optional[AvlNode[T]]:
        """Rebalances subtree rooted from {node}"""
        if not node:
            return None

        node.update_height()
        balance_factor = node.get_balance_factor()

        if balance_factor > 1 and node.left:
            if node.left.get_balance_factor() >= 0:
                return node.rotate_right()
            else:
                node.left = node.left.rotate_left()
                return node.rotate_right()

        if balance_factor < -1 and node.right:
            if node.right.get_balance_factor() <= 0:
                return node.rotate_left()
            else:
                node.right = node.right.rotate_right()
                return node.rotate_left()

        return node

    def __find_minimum(self, node: AvlNode[T]) -> AvlNode[T]:
        return self.__find_minimum(node.left) if node.left else node

    def __find_maximum(self, node: AvlNode[T]) -> AvlNode[T]:
        return self.__find_maximum(node.right) if node.right else node

    def get_size(self) -> int:
        return self.size

    def get_minimum(self) -> Optional[AvlNode[T]]:
        return self.__find_minimum(self.root) if self.root else None

    def get_maximum(self) -> Optional[AvlNode[T]]:
        return self.__find_maximum(self.root) if self.root else None

    def inorder_list(self) -> List[AvlNode[T]]:
        """Returns inorder list of the nodes"""
        res = []
        for element in self:
            res += [element]
        return res

    def __inorder_traversal(self, node: Optional[AvlNode[T]]) -> Iterator[AvlNode[T]]:
        if node is not None:
            yield from self.__inorder_traversal(node.left)
            yield node
            yield from self.__inorder_traversal(node.right)

    def __iter__(self) -> Iterator[AvlNode[T]]:
        return self.__inorder_traversal(self.root)

    def __repr__(self) -> str:
        return str(self.inorder_list())
