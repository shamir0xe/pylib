import heapq
from dataclasses import dataclass, field
from typing import Callable, Dict, Generic, List, Tuple, TypeVar

from ..trees.fenwick_tree.fenwick_tree import FenwickTree

T = TypeVar("T", bound=int)


@dataclass
class Graph(Generic[T]):
    zero: T
    adj: Dict[int, Dict[int, T]] = field(default_factory=dict)
    MAX_DISTANCE: int = field(default=55)

    def add_edge(self, u: int, v: int, cost: T) -> None:
        if u not in self.adj:
            self.adj[u] = {}
        if v not in self.adj:
            self.adj[v] = {}
        if v in self.adj[u] and self.adj[u][v] < cost:
            # Already have the better edge
            return
        self.adj[u][v] = cost

    def get_edges(self, u: int) -> Dict[int, T]:
        if u in self.adj:
            return self.adj[u]
        return {}

    def prim_edges(
        self,
        u: int,
        par: int,
        cuttoff: int,
        evaluator: Callable[[int, int], bool] = lambda u_, v_: True,
    ) -> List[Tuple[int, int, int]]:
        """Returns the sorted edges of the subtree rooted from node {u}
        with max_depth equals to {depth} and at most have {cuttoff} members
        Edges are represented as (u, v, cost)
        """
        # cost, u, par, depth
        pq: List[Tuple[int, int, int, int]] = []
        heapq.heappush(pq, (self.zero, u, par, 0))
        best_distance: Dict[int, int] = {u: self.zero}
        edges: Dict[Tuple[int, int], int] = {(par, u): self.zero}  # par--0-->u
        distances_tree = FenwickTree(n=self.MAX_DISTANCE)
        distances_tree.add(0, 1)

        while len(pq) > 0:
            cost_u, u, par, d = heapq.heappop(pq)
            if cost_u >= self.MAX_DISTANCE or distances_tree.get(cost_u) >= cuttoff:
                break
            if cost_u > best_distance[u] or u not in self.adj:
                continue
            for v, cost_v in self.adj[u].items():
                cost = cost_u + cost_v
                if evaluator(u, v):
                    # v is a valid node
                    flag = (u, v) in edges
                    if not flag or edges[(u, v)] > cost:
                        if not flag:
                            distances_tree.add(cost, 1)
                        else:
                            distances_tree.add(edges[(u, v)], -1)
                            distances_tree.add(cost, 1)
                        edges[(u, v)] = cost
                if v not in best_distance or best_distance[v] > cost:
                    best_distance[v] = cost
                    heapq.heappush(pq, (cost, v, u, d + 1))
        result: List[Tuple[int, int, int]] = []
        for (u, v), cost in edges.items():
            result += [(u, v, cost)]
        return sorted(result, key=lambda tup: tup[2])[:cuttoff]
