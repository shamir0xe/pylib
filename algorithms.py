import math
import random
from queue import (Queue, PriorityQueue)
from .node import Node
from .utils import (debug_text, Logger)
from ortools.graph import pywrapgraph

def LIS(arr, order=+1):
    array = arr[:]
    n = len(array)
    for i in range(n):
        array[i] *= order
    dp = [1 for _ in range(n)]
    par = [None for _ in range(n)]
    reverse = [n - 1 - i for i in range(n)]
    # Utils.debug_text(array)
    for i in reverse:
        for j in [k for k in range(i + 1, n)]:
            # Utils.debug_text('(i, j) = (%, %)', i, j)
            if array[i] <= array[j]:
                if dp[i] < dp[j] + 1:
                    dp[i] = dp[j] + 1
                    par[i] = j
    u = -1
    for i in range(n):
        # Utils.debug_text('u = %', u)
        # Utils.debug_text('(i = (%)', i)
        if u == -1 or dp[i] > dp[u]:
            u = i
    seq = []
    uu = u
    while u != None:
        seq.append(u)
        u = par[u]
    return dp[uu], seq

class MinCostFlow:
    def __init__(self, n):
        self.n = n
        self.__maxflow = pywrapgraph.SimpleMinCostFlow()
    
    def add_edge(self, u, v, capacity, weight):
        self.__maxflow.AddArcWithCapacityAndUnitCost(u, v, capacity, weight)

    def add_supply(self, u, supply):
        self.__maxflow.SetNodeSupply(u, supply)

    def get_matched(self, u):
        return self.__edges[u]

    def solve(self):
        self.__edges = [[] for _ in range(self.n)]
        if self.__maxflow.Solve() == self.__maxflow.OPTIMAL:
            self.total_cost = self.__maxflow.OptimalCost()
            # print('Minimum cost:', self.total_cost)
            for i in range(self.__maxflow.NumArcs()):
                u = self.__maxflow.Tail(i)
                v = self.__maxflow.Head(i)
                f = self.__maxflow.Flow(i)
                if f > 0:
                    self.__edges[u].append((v, f))
            return True
        else:
            print('There was an issue with the min cost flow input.')
            return False


class MaxFlowEfficient:
    def __init__(self, n, random_order=False, order=None, logger=None):
        self.n = n
        self.__order = [i for i in range(n)]
        self.__reverse_map = [i for i in range(n)]
        self.cap = [[0 for j in range(n)] for i in range(n)]
        self.__edges = []
        self.__logger = logger if not logger is None else Logger("MaxFlow")
        if random_order:
            random.shuffle(self.__order)
        if not order is None:
            last = len(order)
            rest = [i for i in range(last, n)]
            if random_order:
                random.shuffle(rest)
            self.__order = [*order, *rest]
        iteration = 0
        for i in self.__order:
            self.__reverse_map[i] = iteration
            iteration += 1
        self.__maxflow = pywrapgraph.SimpleMaxFlow()

    def add_edge(self, u, v, c):
        # Utils.debug_text('% -> % -- %', u, v, c)
        self.cap[u][v] += c
        u = self.__order[u]
        v = self.__order[v]
        self.__maxflow.AddArcWithCapacity(u, v, c)


    def solve(self, source, sink):
        if self.__maxflow.Solve(self.__order[source], self.__order[sink]) != self.__maxflow.OPTIMAL:
            raise Exception('bad flow input'.format(flow))
        flow = self.__maxflow.OptimalFlow()
        self.__logger.add_log('initialization state', flow, timestamp = True)
        edges_cnt = self.__maxflow.NumArcs()
        for i in range(edges_cnt):
            u = self.__reverse_map[self.__maxflow.Tail(i)]
            v = self.__reverse_map[self.__maxflow.Head(i)]
            f = self.__maxflow.Flow(i)
            self.__edges.append((u, v, f))
            self.cap[u][v] -= f
        return flow

class MaxFlow:
    def __init__(self, n, random_order=False, order=None, algorithm="BFS", logger=None):
        self.n = n
        self.cap = [[0 for j in range(n)] for i in range(n)]
        self.order = [i for i in range(n)]
        self.algorithm = algorithm
        self.__logger = logger if not logger is None else Logger("MaxFlow")
        if random_order:
            random.shuffle(self.order)
        if not order is None:
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
        par = [-1 for i in range(self.n)]
        cur_flow = [0 for i in range(self.n)]
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
        cur_flow[u] = 1e20
        return func(u)

    def find_path(self, u, v):
        queue = Queue()
        visited = [False] * self.n
        uu = u
        vv = v

        par = [-1 for i in range(self.n)]
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
            if self.algorithm == "BFS":
                f, path = self.find_path(source, sink)
            elif self.algorithm == "DFS":
                f, path = self.find_path_dfs(source, sink)
            else:
                raise Exception('you must specify a correct algorithm for max-flow')

            if f == 0:
                break
            self.__logger.add_log('initialization state', flow + f, timestamp = True, stream=True)
            flow += f
            for pair in path:
                u, v = pair
                self.cap[u][v] -= f
                self.cap[v][u] += f

        return flow


class MST:
    def __init__(self, adj):
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
                if cost_prim < costs[v] and not v in alive:
                    costs[v] = cost_prim
                    pars[v] = u
                    q.put((-cost_prim, v))
            if len(alive) == n:
                break

        cost = 0
        # debug_text('n: %', n)
        for u in range(n):
            if pars[u] == -1:
                continue
            self.tree.append((pars[u], u))
            # debug_text('% -> %', pars[u], u)
            cost += self.__adj[pars[u]][u]
        return cost


class TSP:
    def __init__(self, adj):
        self.adj = adj
        self.points = []
        self.par = []

    def add_point(self, point):
        self.points.append(point)

    def solve(self):
        n = len(self.points)
        self.par = [[-1 for j in range(1 << n)] for i in range(n)]
        dp = [[1e20 for j in range(1 << n)] for i in range(n)]
        dp[0][1] = 0
        for bitmask in range(1 << n):
            for u in range(n):
                if ((bitmask >> u) & 1) != 0:
                    for v in range(n):
                        bitmask_prim = bitmask | (1 << v)
                        temp = dp[u][bitmask] + self.adj[self.points[u]][
                            self.points[v]]
                        if dp[v][bitmask_prim] > temp:
                            dp[v][bitmask_prim] = temp
                            self.par[v][bitmask_prim] = u
                        # dp[v][bitmask_prim] = min(dp[v][bitmask_prim], dp[u][bitmask] + \
                        #   self.adj[self.points[u]][self.points[v]])
                        # print("node: {}, bitmask: {:b}, ans: {}".format(v, bitmask_prim, dp[v][bitmask_prim]))

        # for i in range(n):
        #   print("node: {}\n".format(i))
        #   print(dp[i][:])

        # debug_text("final answer: {}".format(dp[0][(1 << n) - 1]))
        # raise Exception("abaas")
        return dp[0][(1 << n) - 1]

    def get_order(self):
        n = len(self.points)
        ans = []
        self.__get_order(self.par[0][(1 << n) - 1], (1 << n) - 1, ans)
        # print("order: {}".format(ans))
        return ans

    def __get_order(self, v, bitmask, array):
        array.append(self.points[v])

        u = self.par[v][bitmask]
        if u == -1:
            return
        return self.__get_order(u, bitmask ^ (1 << v), array)


class AvlTree:
    """
    implementation of the avl-tree
    all of the orders are optimum as hell
    node's value should have been implemented with __lt__ operator
    """
    def __init__(self):
        self.__root = None

    def get_root(self):
        """
        returns the current root of the tree
        """
        return self.__root

    def empty(self):
        return self.__root is None

    def insert(self, value):
        """
        adding a new node with a value equals to {value}
        """
        if self.get_root() is None:
            self.__root = Node(value)
        else:
            self.__root = self.__add(self.__root, Node(value))

    def find(self, objective):
        """
        returns the node with a value equals to {objective}
        """
        return self.__find(objective, self.__root)

    def find_node(self, node):
        """
        check whether the node is exist or not
        """
        # debug_text("finding node with value = {}".format(node.get_value()))
        # debug_text("node = {}".format(node))
        return self.__find(node.get_value(), self.__root, node.get_hash())

    def remove(self, objective):
        """
        removes the node with a value equals to {objective}"""
        node = self.find(objective)
        if node is None:
            return False
        self.__root = self.__remove(objective, self.__root)
        return True

    def remove_node(self, node):
        """
        removes the node with it's actual node
        """
        # debug_text("going to remove the node with {} as value".format(node.get_value()))
        node = self.find_node(node)
        if node is None:
            return False
        # debug_text("\n\n==>{}".format(node.get_hash()))
        self.__root = self.__remove(node.get_value(), self.__root,
                                    node.get_hash())
        return True

    def get_size(self):
        if self.__root is None:
            return 0
        return self.__root.get_size()

    def get_lowest(self):
        """
        returns the node with the lowest value in the tree
        """
        if self.__root is None:
            return None
        node = self.__root
        while not node.get_left() is None:
            node = node.get_left()
        return node

    def get_highest(self):
        """
        returns the node with the highest value in the tree
        """
        if self.__root is None:
            return None
        node = self.__root
        while not node.get_right() is None:
            node = node.get_right()
        return node

    def get_list(self):
        def fill_inorder(node, current_list):
            if node is None:
                return
            fill_inorder(node.get_left(), current_list)
            current_list.append(node.get_value())
            fill_inorder(node.get_right(), current_list)
        current_list = []
        fill_inorder(self.__root, current_list)
        return current_list

    def inorder_list(self, node, res):
        """
        returns the inorder list of the tree as array of string
        """
        if node is None:
            return
        res.append("(")
        self.inorder_list(node.get_left(), res)
        res.append(",")
        if node.get_value():
            res.append(str(node.get_value()))
            # res.append(node.get_hash())
        res.append(",")
        self.inorder_list(node.get_right(), res)
        res.append(")")

    def __remove(self, objective, node, node_hash=None):
        if node is None:
            return None
        if objective < node.get_value():
            left = self.__remove(objective, node.get_left(), node_hash)
            node.set_left(left)
        elif node.get_value() < objective:
            right = self.__remove(objective, node.get_right(), node_hash)
            node.set_right(right)
        else:
            if node_hash is None or node.get_hash() == node_hash:
                right = node.get_right()
                if not right is None:
                    node = self.__rotate_left(node)
                    left = self.__remove(objective, node.get_left(),
                                         node.get_left().get_hash())
                    node.set_left(left)
                else:
                    left = node.get_left()
                    if not left is None:
                        node = self.__rotate_right(node)
                        right = self.__remove(objective, node.get_right(),
                                              node.get_right().get_hash())
                        node.set_right(right)
                    else:
                        del node
                        return None
            else:
                right = self.__remove(objective, node.get_right(), node_hash)
                node.set_right(right)
        res = self.__relax(node)
        res.set_par(None)
        return res

    def __find(self, objective, node, node_hash=None):
        if node is None:
            return None

        c = '=='
        if objective < node.get_value():
            c = '<'
        if node.get_value() < objective:
            c = '>'
        # debug_text("obj{}node - {}/{}".format(c, node.get_hash(), node_hash))
        if objective < node.get_value():
            return self.__find(objective, node.get_left(), node_hash)
        if node.get_value() < objective:
            return self.__find(objective, node.get_right(), node_hash)
        if node_hash is None or node.get_hash() == node_hash:
            # debug_text("c'mon")
            return node
        return self.__find(objective, node.get_right(), node_hash)

    def __add(self, cur, node):
        if node < cur:
            if cur.get_left() is None:
                cur.set_left(node)
                node.set_par(cur)
            else:
                left = self.__add(cur.get_left(), node)
                left.set_par(cur)
                cur.set_left(left)
        else:
            if cur.get_right() is None:
                cur.set_right(node)
                node.set_par(cur)
            else:
                right = self.__add(cur.get_right(), node)
                right.set_par(cur)
                cur.set_right(right)
        return self.__relax(cur)

    def __get_height(self, node):
        if node is None:
            return 0
        return node.get_height()

    def __relax(self, node):
        if node is None:
            return
        node.update()
        balance = node.get_balance()
        if balance > 1:
            left_left = node.get_left().get_left()
            left_right = node.get_left().get_right()
            if self.__get_height(left_left) <= self.__get_height(left_right):
                node.set_left(self.__rotate_left(node.get_left()))
            return self.__rotate_right(node)
        elif balance < -1:
            right_right = node.get_right().get_right()
            right_left = node.get_right().get_left()
            if self.__get_height(right_right) <= self.__get_height(right_left):
                node.set_right(self.__rotate_right(node.get_right()))
            return self.__rotate_left(node)
        return node

    def __rotate_right(self, y):
        x = y.get_left()
        t_2 = x.get_right()
        x.set_right(y)
        y.set_left(t_2)
        y.update()
        x.update()
        x.set_par(None)
        return x

    def __rotate_left(self, x):
        y = x.get_right()
        t_2 = y.get_left()
        y.set_left(x)
        x.set_right(t_2)
        x.update()
        y.update()
        y.set_par(None)
        return y

    def __str__(self):
        res = []
        self.inorder_list(self.__root, res)
        list_string = ''.join(res)
        return 'list: {}\nbalance: {}, size: {}'.format(
            list_string, self.__root.get_balance(), self.__root.get_size())
