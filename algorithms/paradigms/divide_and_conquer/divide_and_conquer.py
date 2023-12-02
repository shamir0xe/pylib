from __future__ import annotations
from typing import Generic, List, Callable, Optional, Protocol, TypeVar
from .merge_types import MergeTypes
from .node_wrapper import NodeWrapper


class CustomProtocol(Protocol):
    def __add__(self, other: CustomProtocol):
        return self + other

    def __len__(self) -> int:
        return len(self)

    def __getitem__(self, index: int):
        return self[index]


T = TypeVar("T", bound="CustomProtocol")


class DivideAndConquer(Generic[T]):
    """
    General implementation of Divide and Conquer
    """

    MAX_SIZE = 33

    def __init__(
        self, nodes: List[NodeWrapper], splitter_fn: Callable[..., Optional[T]], *args
    ):
        """
        splitter_fn: The function that should be applied on the smallest sample size
        args: The list of arguments to be passed to splitter_fn
        """
        self.nodes = nodes
        self.fn = splitter_fn
        self.fn_args = args
        self.max_size = DivideAndConquer.MAX_SIZE
        self.merge_type = MergeTypes.SUM
        self.dimension = len(nodes[0].point)
        self.total_points = len(nodes)
        self.process = 0

    def solve(self, max_size=MAX_SIZE, merge_type=MergeTypes.SUM) -> Optional[T]:
        self.max_size = max_size
        self.merge_type = merge_type
        return self._solve(0, 0, self.total_points)

    def merge_results(self, res_0: Optional[T], res_1: Optional[T]) -> Optional[T]:
        """
        You need to implement this part for how the outputs should be merged
        """
        if res_0 is None:
            return res_1
        if res_1 is None:
            return res_0
        if self.merge_type == MergeTypes.UNIFY:
            pass
            # res = []
            # min_length = min(len(res_0), len(res_1))
            # for i in range(min_length):
            #     temp = res_0[i]
            #     temp.extend(res_1[i])
            #     res.append(temp)
            # res.extend(res_0[min_length:])
            # res.extend(res_1[min_length:])
            # return res
        """For addition or appending"""
        return res_0 + res_1

    def callback_process(self, fraction):
        pass

    def _increase_process(self, amount):
        self.process += amount
        self.callback_process(self.process / self.total_points)

    def _solve(self, step_direction, start_idx, end_idx, depth=0) -> Optional[T]:
        if end_idx <= start_idx:
            return None
        if end_idx - start_idx <= self.max_size:
            self._increase_process(end_idx - start_idx)
            selection = [node.obj for node in self.nodes[start_idx:end_idx]]
            return self.fn(selection, *self.fn_args)
        self.nodes[start_idx:end_idx] = sorted(
            self.nodes[start_idx:end_idx], key=lambda node: node.point[step_direction]
        )
        mid = (end_idx + start_idx) >> 1
        results: list[Optional[T]] = [None, None]
        next_dir = (step_direction + 1) % self.dimension
        results[0] = self._solve(next_dir, start_idx, mid + 1, depth + 1)
        results[1] = self._solve(next_dir, mid + 1, end_idx, depth + 1)
        return self.merge_results(*results)
