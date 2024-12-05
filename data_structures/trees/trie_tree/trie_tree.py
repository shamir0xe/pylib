from __future__ import annotations

from typing import Callable, Generic, Optional, TypeVar, List, Dict

from .trie_node import TrieNode
from ....types.exception_types import ExceptionTypes

T = TypeVar("T")


class TrieTree(Generic[T]):
    root_id: int
    value_extractor: Callable[[T], str]
    node_updater: Callable[[TrieNode[T], T], TrieNode[T]]
    default_constructor: Callable[[], T]
    nodes: List[TrieNode[T]]
    edges: List[Dict[str, int]]

    @staticmethod
    def _default_node_updater(node: TrieNode[T], data: T) -> TrieNode[T]:
        node.data = data
        return node

    def __init__(
        self,
        value_extractor: Callable[[T], str],
        default_constructor: Callable[[], T],
        node_updater: Optional[Callable[[TrieNode[T], T], TrieNode[T]]] = None,
    ) -> None:
        self.root_id = -1
        self.value_extractor = value_extractor
        self.default_constructor = default_constructor
        self.node_updater = self._default_node_updater
        if node_updater:
            self.node_updater = node_updater
        self.nodes = []
        self.edges = []

    @property
    def root(self) -> TrieNode[T]:
        if self.root_id < 0:
            self.root_id = self._new_node()
        return self.nodes[self.root_id]

    def get(self, id: int) -> TrieNode[T]:
        """Gets the node assigned to it's id"""
        return self.nodes[id]

    def update(self, data: T) -> int:
        value = self.value_extractor(data)
        id = self._find(id=self.root.id, key=value)
        if id < 0:
            return -1
        self.nodes[id] = self.node_updater(self.nodes[id], data)
        return id

    def create(self, data: T) -> int:
        value = self.value_extractor(data)
        return self._create(id=self.root.id, key=value, data=data)

    def read(self, data: T) -> int:
        value = self.value_extractor(data)
        return self._find(id=self.root.id, key=value)

    def _find(self, id: int, key: str) -> int:
        """Finds the {key}-path in the tree"""
        if id < 0:
            return -1
        if key == "":
            return id
        if key[0] in self.edges[id]:
            return self._find(self.edges[id][key[0]], key[1:])
        return -1

    def _create(self, id: int, key: str, data: T) -> int:
        """
        Create {key} in the tree
        should be called with id >= 0"""
        if id < 0:
            raise Exception(ExceptionTypes.TRIE_TREE_INVALID)
        if key == "":
            self.nodes[id].data = data
            return id
        if key[0] not in self.edges[id]:
            id1 = self._new_node()
            self.edges[id][key[0]] = id1
        else:
            id1 = self.edges[id][key[0]]
        return self._create(id1, key[1:], data)

    def _new_node(self) -> int:
        node = TrieNode[T](data=self.default_constructor())
        node.id = len(self.nodes)
        self.nodes += [node]
        self.edges += [{}]
        return node.id
