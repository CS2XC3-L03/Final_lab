import random
from min_heap import Element, MinHeap


class DirectedWeightedGraph:
    def __init__(self):
        self.adj = {}
        self.weights: dict[tuple[int, int], float] = {}

    def are_connected(self, node1: int, node2: int):
        for neighbour in self.adj[node1]:
            if neighbour == node2:
                return True
        return False

    def adjacent_nodes(self, node: int):
        return self.adj[node]

    def add_node(self, node: int):
        self.adj[node] = []

    def add_edge(self, node1: int, node2: int, weight: float):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def w(self, node1: int, node2: int):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]
        return float("inf")

    def number_of_nodes(self):
        return len(self.adj)


def dijkstra(graph, source):
    pred = {}  # Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {}  # Distance dictionary
    min_heap = MinHeap([])
    nodes = list(graph.adj.keys())

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
        for neighbour in graph.adj[current_node]:
            if dist[current_node] + graph.w(current_node, neighbour) < dist[neighbour]:
                min_heap.decrease_key(
                    neighbour, dist[current_node] + graph.w(current_node, neighbour)
                )
                dist[neighbour] = dist[current_node] + graph.w(current_node, neighbour)
                pred[neighbour] = current_node
    return dist


def bellman_ford(graph, source):
    pred = {}  # Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {}  # Distance dictionary
    nodes = list(graph.adj.keys())

    # Initialize distances
    for node in nodes:
        dist[node] = float("inf")
    dist[source] = 0

    # Meat of the algorithm
    for _ in range(graph.number_of_nodes()):
        for node in nodes:
            for neighbour in graph.adj[node]:
                if dist[neighbour] > dist[node] + graph.w(node, neighbour):
                    dist[neighbour] = dist[node] + graph.w(node, neighbour)
                    pred[neighbour] = node
    return dist


def total_dist(dist):
    total = 0
    for key in dist.keys():
        total += dist[key]
    return total


def create_random_complete_graph(nodes, lower, upper):
    graph = DirectedWeightedGraph()
    for i in range(nodes):
        graph.add_node(i)
    for i in range(nodes):
        for j in range(nodes):
            if i != j:
                graph.add_edge(i, j, random.randint(lower, upper))
    return graph


def create_linear_graph(node_num, lower, upper):
    graph = DirectedWeightedGraph()
    for i in range(node_num):
        graph.add_node(i)
    for i in range(node_num - 1):
        graph.add_edge(i, i + 1, random.randint(lower, upper))
    graph.add_edge(node_num - 1, 0, random.randint(lower, upper))

    return graph


def create_graph_with_random_edges(node_num, edge_num, lower, upper):
    graph = create_linear_graph(node_num, lower, upper)  # Create a linear graph first

    # Add additional random edges to achieve desired number of edges e
    for _ in range(edge_num - node_num):
        node1, node2 = random.randint(0, node_num - 1), random.randint(0, node_num - 1)
        while node1 == node2 or node2 in graph.adjacent_nodes(node1):
            node1, node2 = random.randint(0, node_num - 1), random.randint(
                0, node_num - 1
            )
        graph.add_edge(node1, node2, random.randint(lower, upper))

    return graph


def calc_max_edges(n):
    return n * (n + 1) // 2


# Assumes G represents its nodes as integers 0,1,...,(n-1)
def mystery(graph):
    nodes = graph.number_of_nodes()
    d = init_d(graph)
    for k in range(nodes):
        for i in range(nodes):
            for j in range(nodes):
                if d[i][j] > d[i][k] + d[k][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def init_d(graph):
    nodes = graph.number_of_nodes()
    d = [[float("inf") for j in range(nodes)] for i in range(nodes)]
    for i in range(nodes):
        for j in range(nodes):
            if graph.are_connected(i, j):
                d[i][j] = graph.w(i, j)
        d[i][i] = 0
    return d
