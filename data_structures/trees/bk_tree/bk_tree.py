from typing import Callable, Dict, Generic, List, Optional, Tuple, TypeVar

from .bk_node import BkNode
from ..avl_tree.avl_node import AvlNode
from ..avl_tree.avl_tree import AvlTree
from ..avl_tree.merge_avl_trees import MergeAvlTrees
from ....types.exception_types import ExceptionTypes

T = TypeVar("T")


class BkTree(Generic[T]):
    root_id: int
    distance_calculator: Callable[[str, str], int]
    value_extractor: Callable[[T], str]
    cutoff_length: int
    edges: List[Dict[int, int]]
    nodes: List[BkNode[T]]

    def __init__(
        self,
        distance_calculator: Callable[[str, str], int],
        value_extractor: Callable[[T], str],
        cutoff_length: int,
    ) -> None:
        self.distance_calculator = distance_calculator
        self.value_extractor = value_extractor
        self.nodes = []
        self.edges = []
        self.root_id = -1
        self.cutoff_length = cutoff_length

    @property
    def root(self) -> Optional[BkNode[T]]:
        if self.root_id < 0:
            return None
        return self.nodes[self.root_id]

    def insert(self, word: T) -> None:
        """Insert the {word} into the tree"""
        self.root_id = self._insert(
            node=self.root, word=word, value=self.value_extractor(word)
        )

    def query(self, word: str) -> AvlTree[Tuple[BkNode[T], int], int]:
        """Finds the closest match to the word"""
        if not self.root:
            raise Exception(ExceptionTypes.BK_TREE_INVALID)
        return self._find(self.root, word, int(1e9))

    def _new_node(self, obj: T, value: str) -> int:
        """Returns id of the generated node"""
        node = BkNode(obj=obj, value=value)
        node.id = len(self.nodes)
        self.nodes += [node]
        self.edges += [{}]
        return node.id

    def _insert(self, node: Optional[BkNode[T]], word: T, value: str) -> int:
        if node is None:
            return self._new_node(obj=word, value=value)
        distance = self.distance_calculator(node.value, value)
        if distance in self.edges[node.id]:
            self._insert(self.nodes[self.edges[node.id][distance]], word, value)
        else:
            self.edges[node.id][distance] = self._insert(None, word, value)
        return node.id

    def _find(
        self, node: Optional[BkNode[T]], word: str, best_distance: int
    ) -> AvlTree[Tuple[BkNode[T], int], int]:
        avl_tree = AvlTree[Tuple[BkNode[T], int], int](lambda node: node.data[1])
        if not node:
            return avl_tree
        # logging.info(f"{word} / {node.value} / {best_distance}")
        du = self.distance_calculator(word, node.value)
        avl_tree.insert(AvlNode(data=(node, du)))
        if best_distance > du:
            best_distance = du
        for duv in self.edges[node.id].keys():
            if abs(duv - du) <= best_distance * 2:
                # if abs(duv - du) <= max(10, best_distance * 2):
                # if True:
                cur_avl_tree = self._find(
                    self.nodes[self.edges[node.id][duv]], word, best_distance
                )
                if cur_avl_tree.size:
                    MergeAvlTrees.merge(
                        avl_tree1=avl_tree,
                        avl_tree2=cur_avl_tree,
                        cutoff_length=self.cutoff_length,
                    )
                # logging.info(f"after merge: {avl_tree}")
                del cur_avl_tree
                min_node = avl_tree.get_minimum()
                if min_node and best_distance > min_node.data[1]:
                    best_distance = min_node.data[1]
        return avl_tree
