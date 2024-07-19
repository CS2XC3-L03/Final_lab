from part1 import DirectedWeightedGraph
from min_heap import Element, MinHeap


def a_star(graph: DirectedWeightedGraph, source, dest, heuristic) -> tuple[dict, list]:
    """
    Computes the shortest path between a source and destination node in a weighted directed graph using the A* algorithm.

    Args:
        G (DirectedWeightedGraph): The graph to search for the shortest path.
        source (any): The node to start the search from.
        des (any): The destination node to search for.
        heuristic (dict[any, float]): A dictionary that takes a node, returns the estimated distance between a node and the destination node.

    Returns:
        A tuple of two elements:
        1. A dictionary that maps each node to its predecessor in the shortest path from the source node to that node.
        2. A list of the nodes in the shortest path from the source node to the destination node.
    """
    pred = {}
    min_heap = MinHeap([])
    min_heap.insert(Element(source, 0))
    dist: dict[int, float] = {source: 0}

    while not min_heap.is_empty():
        current_element = min_heap.extract_min()
        current_node = current_element.value

        for neighbour in graph.adj[current_node]:
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

    if dest not in pred:
        return (pred, [])

    path = [dest, pred[dest]]
    while path[-1] != source:
        path.append(pred[path[-1]])
    return (pred, list(reversed(path)))
