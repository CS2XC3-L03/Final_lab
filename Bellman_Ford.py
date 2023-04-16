from SPAlgorithm import *
from Graph import *
from min_heap import *


class Bellman_Ford(SPAlgorithm):
    @staticmethod
    def calc_sp(graph: Graph, source: int, dest: int) -> float:
        pred = {}  # Predecessor dictionary. Isn't returned, but here for your understanding
        dist = {}  # Distance dictionary
        nodes = graph.get_nodes()

        # Initialize distances
        for node in nodes:
            dist[node] = float("inf")
        dist[source] = 0

        # Meat of the algorithm
        for _ in range(graph.number_of_nodes()):
            for node in nodes:
                for neighbour in graph.get_adj_nodes(node):
                    if dist[neighbour] > dist[node] + graph.w(node, neighbour):
                        dist[neighbour] = dist[node] + graph.w(node, neighbour)
                        pred[neighbour] = node
        return dist[dest]
