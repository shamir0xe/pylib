import math
from __future__ import print_function
from ortools.graph import pywrapgraph
from .utils import (debug_text)
from .graph import Graph
from .geometry import Geometry


class KMeansFlow:
    def __init__(self, m, k, timeout=10, precision=100.):
        self.m = m  # number of tasks
        self.k = k  # number of clusters
        self.__precision = precision
        self.__source = m + k
        self.__sink = m + k + 1
        self.__graph = Graph(m + k + 2)  # last two are souce+sink nodes
        self.__done = False
        self.__last_cost = 1e20
        self.__points = [Geometry.Point(0, 0) for _ in range(m + k)]
        self.__assigned_tasks = [[] for _ in range(k)]

    def done(self):
        return self.__done

    def get_cluster_tasks(self, cluster_index):
        return self.__assigned_tasks[cluster_index]

    def get_source(self):
        return self.__source

    def get_sink(self):
        return self.__sink

    def set_point(self, index, point):
        self.__points[index] = point

    def update_edges(self):
        """
        only update the cost of edges
        """
        for i in range(self.m):
            u = self.__graph.get_node(i)
            for v in u.adj:
                edge_index = u.adj[v]
                e = self.__graph.get_edge(edge_index)
                # debug_text("{}->{}".format(u.index, v))
                e.cost = Geometry.translate('[0] [1] -',
                                            self.__points[u.index],
                                            self.__points[v]).length()

    def update_means(self):
        for i in range(self.k):
            if len(self.__assigned_tasks[i]) > 0:
                mean = Geometry.Point(0, 0)
                for u in self.__assigned_tasks[i]:
                    mean = Geometry.translate('[0] [1] +', mean,
                                              self.__points[u])
                mean = Geometry.translate('[0] [1] *.', mean,
                                          1. / len(self.__assigned_tasks[i]))
                # debug_text("new mean[{}]: {}".format(i, mean))
                self.__points[i + self.m] = mean

    def get_graph(self):
        return self.__graph

    def max_flow(self):
        max_flow = pywrapgraph.SimpleMaxFlow()
        for edge in self.__graph.get_edges():
            max_flow.AddArcWithCapacity(edge.start_node, edge.end_node,
                                        edge.capacity)

        if not max_flow.Solve(self.__source, self.__sink) == max_flow.OPTIMAL:
            # print('Max flow:', max_flow.OptimalFlow())
            # print('')
            # print('  Arc    Flow / Capacity')
            # for i in range(max_flow.NumArcs()):
            #   print('%1s -> %1s   %3s  / %3s' % (
            #       max_flow.Tail(i),
            #       max_flow.Head(i),
            #       max_flow.Flow(i),
            #   max_flow.Capacity(i)))
            # print('Source side min-cut:', max_flow.GetSourceSideMinCut())
            # print('Sink side min-cut:', max_flow.GetSinkSideMinCut())
        # else:
            print('There was an issue with the max flow input.')
        return max_flow.OptimalFlow()

    def min_cost_max_flow(self, f):
        # f = self.max_flow()
        # debug_text("max flow part: {}".format(f))

        self.__graph.reset_supplies()
        self.__graph.set_supply(self.__source, f)
        self.__graph.set_supply(self.__sink, -f)
        min_cost_flow = pywrapgraph.SimpleMinCostFlow()
        for edge in self.__graph.get_edges():
            # debug_text(edge)
            min_cost_flow.AddArcWithCapacityAndUnitCost(
                edge.start_node, edge.end_node, edge.capacity,
                round(edge.cost * self.__precision))
        for node in self.__graph.get_nodes():
            min_cost_flow.SetNodeSupply(node.index, node.supply)
        self.__assigned_tasks = [[] for _ in range(self.k)]
        if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
            # print('Total cost = ', min_cost_flow.OptimalCost())
            # print()
            for arc in range(min_cost_flow.NumArcs()):
                # Can ignore arcs leading out of source or into sink.
                if min_cost_flow.Flow(arc) > 0:

                    def better_node(cur_node):
                        if cur_node == self.__source:
                            return "source"
                        if cur_node == self.__sink:
                            return "sink"
                        return cur_node

                    u = min_cost_flow.Tail(arc)
                    v = min_cost_flow.Head(arc)
                    flow = min_cost_flow.Flow(arc)
                    # debug_text("{}->{} f:{}".format(better_node(u), better_node(v), flow))
                    if min_cost_flow.Tail(
                            arc) != self.__source and min_cost_flow.Head(
                                arc) != self.__sink:
                        # Arcs in the solution have a flow value of 1. Their start and end nodes
                        # give an assignment of worker to task.
                        self.__graph.set_flow(u, v, flow)
                        if u < self.m:
                            u = min_cost_flow.Tail(arc)
                            v = min_cost_flow.Head(arc)
                            flow = min_cost_flow.Flow(arc)
                            # debug_text("{}->{} f:{}".format(better_node(u), better_node(v - self.m), flow))
                            self.__assigned_tasks[v - self.m].append(u)
                        # print('Worker %d assigned to task %d.  Cost = %d' % (
                        #   min_cost_flow.Tail(arc),
                        #   min_cost_flow.Head(arc),
                        # min_cost_flow.UnitCost(arc)))
        else:
            print('There was an issue with the min cost flow input.')
        res = min_cost_flow.OptimalCost() / self.__precision
        # debug_text('% O %', math.fabs(res - self.__last_cost), 1 / self.__precision)
        # debug_text('%', math.fabs(res - self.__last_cost) < 1 / self.__precision)
        if math.fabs(res - self.__last_cost) < 1. / self.__precision or res > self.__last_cost:
            self.__done = True
        self.__last_cost = res
        return res
