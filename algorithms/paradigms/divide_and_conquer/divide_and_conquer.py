from typing import List
from .merge_types import MergeTypes
from .node_wrapper import NodeWrapper


MAX_SIZE = 33


class DivideAndConquer:
    """
    general implementation of D&C
    """

    def __init__(self, nodes: List[NodeWrapper], splitter_fn: function, *args):
        """
        splitter_fn: the function that should be applied on the smallest sample size
        args: the list of arguments to be passed to splitter_fn
        """
        self.nodes = nodes
        self.fn = splitter_fn
        self.fn_args = args
        self.max_size = None
        self.merge_type = MergeTypes.SUM
        self.__dimension = len(nodes[0].point)
        self.__total_points = len(nodes)
        self.__process = 0

    def solve(self, max_size=MAX_SIZE, merge_type=MergeTypes.SUM):
        self.max_size = max_size
        self.merge_type = merge_type
        return self.__solve(0, 0, self.__total_points)

    def merge_results(self, res_0, res_1):
        """
        you need to implement this part for merging the output of the function
        """
        if res_0 is None:
            return res_1
        if res_1 is None:
            return res_0
        if self.merge_type == MergeTypes.UNIFY:
            res = []
            min_length = min(len(res_0), len(res_1))
            for i in range(min_length):
                temp = res_0[i]
                temp.extend(res_1[i])
                res.append(temp)
            res.extend(res_0[min_length:])
            res.extend(res_1[min_length:])
            return res
        # APPEND and ADD
        return res_0 + res_1

    def callback_process(self, fraction):
        pass

    def __increase_process(self, amount):
        self.__process += amount
        self.callback_process(self.__process / self.__total_points)

    def __solve(self, step_direction, start_idx, end_idx, depth=0):
        if end_idx <= start_idx:
            return None
        if end_idx - start_idx <= self.max_size:
            self.__increase_process(end_idx - start_idx)
            selection = [node.obj for node in self.nodes[start_idx:end_idx]]
            return self.fn(selection, *self.fn_args)
        self.nodes[start_idx:end_idx] = sorted(
            self.nodes[start_idx:end_idx],
            key=lambda node: node.point[step_direction]
        )
        mid = (end_idx + start_idx) >> 1
        results = [None, None]
        next_dir = (step_direction + 1) % self.__dimension
        results[0] = self.__solve(next_dir, start_idx, mid + 1, depth + 1)
        results[1] = self.__solve(next_dir, mid + 1, end_idx, depth + 1)
        return self.merge_results(*results)
