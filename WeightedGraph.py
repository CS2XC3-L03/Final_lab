from Graph import *


class WeightedGraph(Graph):
    def __init__(self):
        self.__adj = {}
        self.__weights = {}

    def get_adj_nodes(self, node: int) -> list[int]:
        return self.__adj[node]

    def add_node(self, node: int):
        self.__adj[node] = []

    def add_edge(self, start: int, end: int, w: float):
        if end not in self.__adj[start]:
            self.__adj[start].append(end)
        self.__weights[(start, end)] = w

    def get_num_of_nodes(self) -> int:
        return len(self.__adj)

    def w(self, node1: int, node2: int) -> float:
        if node2 in self.__adj[node1]:
            return self.__weights[(node1, node2)]
