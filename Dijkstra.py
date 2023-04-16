from SPAlgorithm import *
from min_heap import *


class Dijkstra(SPAlgorithm):
    @staticmethod
    def calc_sp(graph: Graph, source: int, dest: int) -> float:
        pred = {} # Predecessor dictionary. Isn't returned, but here for your understanding
        dist = {} # Distance dictionary
        Q = MinHeap([])
        nodes = graph.get_nodes()

        # Initialize priority queue/heap and distances
        for node in nodes:
            Q.insert(Element(node, float("inf")))
            dist[node] = float("inf")
        Q.decrease_key(source, 0)

        # Meat of the algorithm
        while not Q.is_empty():
            current_element = Q.extract_min()
            current_node = current_element.value
            dist[current_node] = current_element.key
            for neighbour in graph.get_adj_nodes(current_node):
                if (
                    dist[current_node] + graph.w(current_node, neighbour)
                    < dist[neighbour]
                ):
                    Q.decrease_key(
                        neighbour, dist[current_node] + graph.w(current_node, neighbour)
                    )
                    dist[neighbour] = dist[current_node] + graph.w(
                        current_node, neighbour
                    )
                    pred[neighbour] = current_node
        return dist[dest]
