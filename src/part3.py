import csv
from part1 import DirectedWeightedGraph
from part2 import a_star

stations_file = "./csv_files/london_stations.csv"
station_connections_file = "./csv_files/london_connections.csv"


def distance(station1, station2):
    """
    Calculates the distance between two stations.
    """
    lat1, long1 = station1
    lat2, long2 = station2

    return ((lat1 - lat2) ** 2 + (long1 - long2) ** 2) ** 0.5


def read_stations() -> dict[int, tuple[float, float]]:  # id: (lat, long)
    stations = {}
    with open(stations_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for id, long, lat, *_ in reader:
            stations[int(id)] = (float(lat), float(long))
    return stations


def read_station_connections(
    stations: dict[int, tuple[float, float]]
) -> tuple[DirectedWeightedGraph, dict[tuple[int, int], int]]:  # (graph, connections)
    graph = DirectedWeightedGraph()
    connections: dict[tuple[int, int], int] = {}
    with open(station_connections_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for station1, station2, line, *_ in reader:
            station1 = int(station1)
            station2 = int(station2)
            weight = distance(stations[station1], stations[station2])

            if station1 not in graph.adj:
                graph.add_node(station1)
            if station2 not in graph.adj:
                graph.add_node(station2)

            # assume stations are bidirectional
            graph.add_edge(station1, station2, weight)
            graph.add_edge(station2, station1, weight)
            connections[(station1, station2)] = connections[(station2, station1)] = int(
                line
            )
    return graph, connections


def calc_sp_a_star(
    stations: dict[int, tuple[float, float]],
    graph: DirectedWeightedGraph,
    source: int,
    dest: int,
) -> tuple[float, list[int]]:
    heuristic = {
        node: distance(stations[node], stations[dest])
        for node in list(graph.adj.keys())
    }
    _, path = a_star(graph, source, dest, heuristic)
    dist: float = 0
    for i in range(1, len(path)):
        dist += graph.w(path[i - 1], path[i])
    return dist, path


def same_lines(path: list[int], connections: dict[tuple[int, int], int]) -> bool:
    if not path:
        return False
    if len(path) == 2:
        return True
    for i in range(len(path) - 2):
        if (
            connections[(path[i], path[i + 1])]
            != connections[(path[i + 1], path[i + 2])]
        ):
            return False
    return True


def adjacent_lines(path: list[int], connections: dict[tuple[int, int], int]) -> bool:
    if not path or len(path) == 2 or same_lines(path, connections):
        return False
    for i in range(len(path) - 2):
        if (
            abs(
                connections[(path[i], path[i + 1])]
                - connections[(path[i + 1], path[i + 2])]
            )
            != 1
        ):
            return False

    return True


def number_of_lines_in_path(
    path: list[int], connections: dict[tuple[int, int], int]
) -> int:
    lines = set()
    for i in range(len(path) - 1):
        lines.add(connections[(path[i], path[i + 1])])
    return len(lines)
