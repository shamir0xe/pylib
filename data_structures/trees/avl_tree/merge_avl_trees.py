from typing import Generic, TypeVar

from .avl_node import AvlNode
from .avl_tree import AvlTree
from ....utils.protocols.comparable import Comparable

T = TypeVar("T")
K = TypeVar("K", bound=Comparable)


class MergeAvlTrees(Generic[T]):

    @staticmethod
    def merge(
        avl_tree1: AvlTree[T, K], avl_tree2: AvlTree[T, K], cutoff_length: int = -1
    ) -> AvlTree[T, K]:
        if cutoff_length == -1:
            cutoff_length = avl_tree1.size + avl_tree2.size
        # insert the second tree items into the first one
        for item in avl_tree2:
            avl_tree1.insert(AvlNode(item.data))
        # remove items from the base tree till reach the {cutoff_length}
        while avl_tree1.size > cutoff_length:
            maximum = avl_tree1.get_maximum()
            if not maximum:
                break
            avl_tree1.remove(maximum)
        return avl_tree1
