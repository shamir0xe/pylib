class TSP:
    def __init__(self, adj):
        """
        Solving the Traveling Salesman Problem
        adj is the adjacency matrix
        """
        self.adj = adj
        self.points = []
        self.par = []

    def add_point(self, point):
        self.points.append(point)

    def solve(self):
        n = len(self.points)
        self.par = [[-1 for _ in range(1 << n)] for _ in range(n)]
        dp = [[1e20 for _ in range(1 << n)] for _ in range(n)]
        dp[0][1] = 0
        for bitmask in range(1 << n):
            for u in range(n):
                if ((bitmask >> u) & 1) != 0:
                    for v in range(n):
                        bitmask_prim = bitmask | (1 << v)
                        temp = dp[u][bitmask] + self.adj[self.points[u]][self.points[v]]
                        if dp[v][bitmask_prim] > temp:
                            dp[v][bitmask_prim] = temp
                            self.par[v][bitmask_prim] = u

        return dp[0][(1 << n) - 1]

    def get_order(self):
        n = len(self.points)
        ans = []
        self.__get_order(self.par[0][(1 << n) - 1], (1 << n) - 1, ans)
        return ans

    def __get_order(self, v, bitmask, array):
        array.append(self.points[v])

        u = self.par[v][bitmask]
        if u == -1:
            return
        return self.__get_order(u, bitmask ^ (1 << v), array)
