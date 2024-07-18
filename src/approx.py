from min_heap import Element, MinHeap
from part1 import DirectedWeightedGraph as Graph


def dijkstra_approx(graph: Graph, source: int, k: int):
    relaxed = {}  # Used to count how many times a node takes relaxation
    pred = {}  # Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {}  # Distance dictionary
    min_heap = MinHeap([])
    nodes = list(graph.adj.keys())

    # Initialize priority queue/heap and distances
    for node in nodes:
        min_heap.insert(Element(node, float("inf")))
        dist[node] = float("inf")
        relaxed[node] = 0
    min_heap.decrease_key(source, 0)

    while not min_heap.is_empty():
        current_element = min_heap.extract_min()
        current_node = current_element.value
        dist[current_node] = current_element.key
        for neighbour in graph.adj[current_node]:
            if (
                dist[current_node] + graph.w(current_node, neighbour) < dist[neighbour]
                and relaxed[neighbour] < k
            ):
                min_heap.decrease_key(
                    neighbour, dist[current_node] + graph.w(current_node, neighbour)
                )
                dist[neighbour] = dist[current_node] + graph.w(current_node, neighbour)
                pred[neighbour] = current_node
                relaxed[neighbour] += 1
    return dist


def bellman_ford_approx(graph: Graph, source: int, k: int):
    relaxed = {}  # Used to count how many times a node takes relaxation
    pred = {}  # Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {}  # Distance dictionary
    nodes = list(graph.adj.keys())

    # Initialize distances
    for node in nodes:
        dist[node] = float("inf")
        relaxed[node] = 0
    dist[source] = 0

    for _ in range(graph.number_of_nodes()):
        for node in nodes:
            for neighbour in graph.adj[node]:
                if (
                    dist[neighbour] > dist[node] + graph.w(node, neighbour)
                    and relaxed[neighbour] < k
                ):
                    dist[neighbour] = dist[node] + graph.w(node, neighbour)
                    pred[neighbour] = node
                    relaxed[neighbour] += 1
    return dist
