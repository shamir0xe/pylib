from enum import Enum
from .geometry import Geometry
from .utils import (debug_text)


class Steps(Enum):
    X = 0
    Y = 1


class MergeTypes(Enum):
    APPEND = 0
    UNIFY = 1
    SUM = 2


class PointWrapper:
    def __init__(self, obj, point):
        self.point = point
        self.obj = obj

    def __lt__(self, other):
        return self.point < other.point

    def __str__(self):
        return '({}, {})'.format(self.point, self.obj)


class DivideAndConquer:
    """
    implementation for 2D D&C
    """
    def __init__(self, points, splitter_fn, *args):
        self.points = points
        self.fn = splitter_fn
        self.fn_args = args
        self.max_size = None
        self.merge_type = MergeTypes.SUM
        self.__total_points = len(points)
        self.__process = 0

    def solve(self, max_size=33, merge_type=MergeTypes.SUM):
        self.max_size = max_size
        self.merge_type = merge_type
        n = len(self.points)
        return self.__solve(Steps.X, 0, n)

    def merge_results(self, res_0, res_1):
        """
        you need to implement this part for merging the output of the function
        """
        if res_0 is None:
            return res_1
        if res_1 is None:
            return res_0
        if self.merge_type == MergeTypes.UNIFY:
            debug_text("let's merge the results %-%", res_0, res_1)
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
        # print('{}-{}-[{}-{}]'.format(step_direction, depth, start_idx,
        #                              end_idx))
        if end_idx <= start_idx:
            return None
        if end_idx - start_idx <= self.max_size:
            self.__increase_process(end_idx - start_idx)
            selection = [point.obj for point in self.points[start_idx:end_idx]]
            return self.fn(selection, *self.fn_args)
        self.points[start_idx:end_idx] = \
            sorted(self.points[start_idx:end_idx], key=lambda point_wrap: point_wrap.point.x if
             step_direction is Steps.X else point_wrap.point.y)
        mid = (end_idx + start_idx) >> 1
        results = [None, None]
        next_dir = Steps.X if step_direction is Steps.Y else Steps.Y
        results[0] = self.__solve(next_dir, start_idx, mid + 1, depth + 1)
        results[1] = self.__solve(next_dir, mid + 1, end_idx, depth + 1)
        return self.merge_results(*results)
