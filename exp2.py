from typing import Callable
from final_project_part1 import DirectedWeightedGraph
from min_heap import MinHeap, Element

def a_star(G: DirectedWeightedGraph, source: int, des: int, heuristic: Callable[[int], float]):
    pred = {}
    Q = MinHeap([])
    Q.insert(Element(source, 0))
    nodes = list(G.adj.keys())
    hmap = {node: heuristic(node) for node in nodes}
    dist = {source: 0}

    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value

        for neighbour in G.adj[current_node]:
            dis = G.w(current_node, neighbour) + dist[current_node]
            if neighbour in dist and dist[neighbour] <= dis:
                    continue
            
            dist[neighbour] = dis
            pred[neighbour] = current_node
            f_score = dis + hmap[neighbour]
            if neighbour in Q.map:
                Q.decrease_key(neighbour, f_score)
            else:
                Q.insert(Element(neighbour, f_score))

    if (not(des in pred)):
        return (pred, [])
    
    path = [des, pred[des]]
    while path[-1] != source:
        path.append(pred[path[-1]])
    return (pred, list(reversed(path)))

