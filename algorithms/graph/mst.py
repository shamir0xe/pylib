from queue import PriorityQueue


class MST:
    def __init__(self, adj):
        """
        solving Minimum Spanning Tree problem
        adj is the adjacency matrix
        """
        self.__adj = adj
        self.tree = None

    def solve(self):
        n = len(self.__adj)
        self.tree = []
        if n == 0:
            return 0
        costs = [1e20 for _ in range(n)]
        pars = [-1 for _ in range(n)]
        q = PriorityQueue()
        q.put((0, 0))
        costs[0] = 0
        alive = set()
        while not q.empty():
            cost, u = q.get()
            cost *= -1
            if cost > costs[u]:
                continue
            alive.add(u)

            for v in range(n):
                if u == v:
                    continue
                cost_prim = self.__adj[u][v]
                if cost_prim < costs[v] and v not in alive:
                    costs[v] = cost_prim
                    pars[v] = u
                    q.put((-cost_prim, v))
            if len(alive) == n:
                break

        cost = 0
        for u in range(n):
            if pars[u] == -1:
                continue
            self.tree.append((pars[u], u))
            cost += self.__adj[pars[u]][u]
        return cost
