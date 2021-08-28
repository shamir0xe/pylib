class Graph:
    """
    general purpose graph class
    """
    class Node:
        def __init__(self, index, supply=0):
            self.index = index
            self.supply = supply
            self.adj = {}

        def set_edge(self, v, edge_index):
            self.adj[v] = edge_index

        def get_edge(self, v):
            if not v in self.adj:
                return None
            return self.adj[v]

        def __str__(self):
            return 'node[{}]'.format(self.index)

    class Edge:
        def __init__(self, start_node, end_node, capacity=0, cost=0):
            self.start_node = start_node
            self.end_node = end_node
            self.capacity = capacity
            self.cost = cost
            self.flow = 0

        def __str__(self):
            return '{}->{} {}/{} c:{:.02f}'.format(self.start_node,
                                                   self.end_node, self.flow,
                                                   self.capacity, self.cost)

    def __init__(self, nodes_count):
        self.__edges = []
        self.__nodes = [Graph.Node(i) for i in range(nodes_count)]

    def set_flow(self, u, v, flow):
        edge_index = self.__nodes[u].get_edge(v)
        if edge_index is None:
            return
        self.__edges[edge_index].flow = flow

    def set_edge(self, u, v, capacity=0, cost=0):
        edge_index = len(self.__edges)
        self.__nodes[u].set_edge(v, edge_index)
        self.__edges.append(Graph.Edge(u, v, capacity, cost))

    def set_supply(self, u, supply):
        self.__nodes[u].supply = supply

    def reset_supplies(self):
        for node in self.__nodes:
            node.supply = 0

    def get_edge(self, edge_index):
        return self.__edges[edge_index]

    def get_edges(self):
        return self.__edges

    def get_node(self, node_index):
        return self.__nodes[node_index]

    def get_nodes(self):
        return self.__nodes
