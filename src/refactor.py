from abc import ABC, abstractmethod
from typing import Callable
from min_heap import Element, MinHeap


class Graph(ABC):
    adj: dict[int, list[int]]

    @abstractmethod
    def get_nodes(self) -> list[int]:
        pass

    @abstractmethod
    def get_adj_nodes(self, node: int) -> list[int]:
        pass

    @abstractmethod
    def add_node(self, node: int):
        pass

    @abstractmethod
    def add_edge(self, start: int, end: int, w: float):
        pass

    @abstractmethod
    def get_num_of_nodes(self) -> int:
        pass

    @abstractmethod
    def w(self, node1: int, node2: int) -> float:
        pass


class SPAlgorithm(ABC):
    @staticmethod
    @abstractmethod
    def calc_sp(graph: Graph, source: int, dest: int) -> float:
        pass


class ShortPathFinder:
    def __init__(self, graph: Graph, algorithm: SPAlgorithm):
        self.__graph = graph
        self.__algorithm = algorithm

    def calc_short_path(self, source: int, dest: int) -> float:
        return self.__algorithm.calc_sp(self.__graph, source, dest)

    def set_graph(self, graph: Graph):
        self.__graph = graph

    def set_algorithm(self, algorithm: SPAlgorithm):
        self.__algorithm = algorithm


class WeightedGraph(Graph):
    def __init__(self):
        self.__adj: dict[int, list[int]] = {}
        self.__weights: dict[tuple[int, int], float] = {}

    def get_nodes(self) -> list[int]:
        return list(self.__adj.keys())

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

    def w(self, node1: int, node2: int):
        if node2 in self.__adj[node1]:
            return self.__weights[(node1, node2)]
        return float("inf")


class HeuristicGraph(WeightedGraph):
    def __init__(self):
        super().__init__()
        self.__heuristic: dict[int, float] = {}

    def get_heuristic(self) -> dict[int, float]:
        return self.__heuristic


class BellmanFord(SPAlgorithm):
    @staticmethod
    def calc_sp(graph: WeightedGraph, source: int, dest: int) -> float:
        pred = (
            {}
        )  # Predecessor dictionary. Isn't returned, but here for your understanding
        dist = {}  # Distance dictionary
        nodes = graph.get_nodes()

        # Initialize distances
        for node in nodes:
            dist[node] = float("inf")
        dist[source] = 0

        # Meat of the algorithm
        for _ in range(graph.get_num_of_nodes()):
            for node in nodes:
                for neighbour in graph.get_adj_nodes(node):
                    if dist[neighbour] > dist[node] + graph.w(node, neighbour):
                        dist[neighbour] = dist[node] + graph.w(node, neighbour)
                        pred[neighbour] = node
        return dist[dest]


class Dijkstra(SPAlgorithm):
    @staticmethod
    def calc_sp(graph: WeightedGraph, source: int, dest: int) -> float:
        pred = (
            {}
        )  # Predecessor dictionary. Isn't returned, but here for your understanding
        dist = {}  # Distance dictionary
        min_heap = MinHeap([])
        nodes = graph.get_nodes()

        # Initialize priority queue/heap and distances
        for node in nodes:
            min_heap.insert(Element(node, float("inf")))
            dist[node] = float("inf")
        min_heap.decrease_key(source, 0)

        # Meat of the algorithm
        while not min_heap.is_empty():
            current_element = min_heap.extract_min()
            current_node = current_element.value
            dist[current_node] = current_element.key
            for neighbour in graph.get_adj_nodes(current_node):
                if (
                    dist[current_node] + graph.w(current_node, neighbour)
                    < dist[neighbour]
                ):
                    min_heap.decrease_key(
                        neighbour, dist[current_node] + graph.w(current_node, neighbour)
                    )
                    dist[neighbour] = dist[current_node] + graph.w(
                        current_node, neighbour
                    )
                    pred[neighbour] = current_node
        return dist[dest]


class AStarAdapter(SPAlgorithm):
    @staticmethod
    def calc_sp(
        graph: WeightedGraph, source: int, dest: int, _heuristic: Callable[[int], float]
    ) -> float:
        heuristic = {}
        for node1 in graph.adj:
            heuristic[node1] = _heuristic(node1)
        return AStar.calc_sp(graph, source, dest, heuristic)


class AStar(SPAlgorithm):
    @staticmethod
    def calc_sp(
        graph: WeightedGraph, source: int, dest: int, heuristic: dict[int, float]
    ) -> float:
        pred = {}
        dist: dict[int, float] = {source: 0}
        min_heap = MinHeap([])
        min_heap.insert(Element(source, 0))

        while not min_heap.is_empty():
            current_element = min_heap.extract_min()
            current_node = current_element.value

            for neighbour in graph.get_adj_nodes(current_node):
                dis = graph.w(current_node, neighbour) + dist[current_node]
                if neighbour in dist and dist[neighbour] <= dis:
                    continue

                dist[neighbour] = dis
                pred[neighbour] = current_node
                f_score = dis + heuristic[neighbour]
                if neighbour in min_heap.map:
                    min_heap.decrease_key(neighbour, f_score)
                else:
                    min_heap.insert(Element(neighbour, f_score))

        return dist[dest]


def main():
    graph = WeightedGraph()
    for i in range(6):
        graph.add_node(i)
    for i, j in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 4), (3, 5), (4, 5)]:
        graph.add_edge(i, j, 1)

    pathFinder = ShortPathFinder(graph, Dijkstra())

    print(pathFinder.calc_short_path(0, 5))

    pathFinder.set_algorithm(BellmanFord())
    print(pathFinder.calc_short_path(0, 5))


if __name__ == "__main__":
    main()
