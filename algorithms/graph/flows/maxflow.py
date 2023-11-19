import random
from enum import Enum
from queue import Queue


class MaxFlowAlgorithm(Enum):
    BFS = "BFS"
    DFS = "DFS"


class MaxFlow:
    def __init__(
        self,
        n: int,
        random_order: bool = False,
        order: list | None = None,
        algorithm=MaxFlowAlgorithm.BFS,
    ):
        self.n = n
        self.cap: list[list[int]] = [[0 for _ in range(n)] for _ in range(n)]
        self.order = [i for i in range(n)]
        self.algorithm = algorithm
        if random_order:
            random.shuffle(self.order)
        if order is not None:
            last = len(order)
            rest = [i for i in range(last, n)]
            if random_order:
                random.shuffle(rest)
            self.order = [*order, *rest]

    def add_edge(self, u, v, c):
        self.cap[u][v] += c

    def get_path(self, u, v, par):
        arr = []
        t = v
        while t != u:
            arr.append((par[t], t))
            t = par[t]
        return arr[::-1]

    def find_path_dfs(self, u, v):
        uu, vv = u, v
        par = [-1 for _ in range(self.n)]
        cur_flow = [0 for _ in range(self.n)]

        def func(u):
            nonlocal uu, vv, par
            # debug_text('current edge: %->%', par[u], u)
            if u == vv:
                return cur_flow[vv], self.get_path(uu, vv, par)
            for v in self.order:
                if par[v] == -1 and self.cap[u][v] > 0:
                    par[v] = u
                    cur_flow[v] = min(cur_flow[u], self.cap[u][v])
                    flow, path = func(v)
                    if flow > 0:
                        return (flow, path)
            return 0, []

        par[u] = -2
        cur_flow[u] = int(1e20)
        return func(u)

    def find_path(self, u, v):
        queue = Queue()
        visited = [False] * self.n
        uu = u
        vv = v

        par = [-1 for _ in range(self.n)]
        queue.put((u, 1e20))
        visited[u] = True
        while not queue.empty():
            u, cur_cap = queue.get()
            if u == vv:
                return cur_cap, self.get_path(uu, vv, par)

            for v in self.order:
                if self.cap[u][v] > 0 and not visited[v]:
                    queue.put((v, min(cur_cap, self.cap[u][v])))
                    par[v] = u
                    visited[v] = True

        return 0, []

    def ford_fulkerson(self, source, sink):
        flow = 0
        while True:
            if self.algorithm == MaxFlowAlgorithm.BFS:
                f, path = self.find_path(source, sink)
            elif self.algorithm == MaxFlowAlgorithm.DFS:
                f, path = self.find_path_dfs(source, sink)
            else:
                raise Exception("you must specify a correct algorithm for max-flow")
            if f == 0:
                break
            flow += f
            for pair in path:
                u, v = pair
                self.cap[u][v] -= f
                self.cap[v][u] += f

        return flow
