import csv
from exp2 import a_star
from final_project_part1 import DirectedWeightedGraph, dijkstra
import matplotlib.pyplot as plot
import timeit

"""
type: station row

id, latitude, longitude, ...

type: connection row

station1, station2
"""

stations_file = "./csv_files/london_stations.csv"
station_connections_file = "./csv_files/london_connections.csv"


def distance(station1, station2):
    """
    Calculates the distance between two stations.
    """
    lat1, long1 = station1
    lat2, long2 = station2

    return ((lat1 - lat2) ** 2 + (long1 - long2) ** 2) ** 0.5


def read_stations():
    stations = {}
    with open(stations_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for id, long, lat, *_ in reader:
            stations[int(id)] = (float(lat), float(long))
    return stations


stations = read_stations()


def read_station_connections():
    graph = DirectedWeightedGraph()
    connections: dict[(int, int):int] = {}
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

            graph.add_edge(station1, station2, weight)
            connections[(station1, station2)] = int(line)
    return graph, connections


graph, connections = read_station_connections()


def calc_sp_a_star(source, dest):
    heuristic = {
        node: distance(stations[node], stations[dest])
        for node in list(graph.adj.keys())
    }
    _, path = a_star(graph, source, dest, heuristic)
    dist: float = 0
    for i in range(1, len(path)):
        dist += graph.w(path[i - 1], path[i])
    return dist, path


def same_lines(path: list[int]):
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


def adjacent_lines(path: list[int]):
    if not path or len(path) == 2 or same_lines(path):
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


def multiple_line_transfers(path: list[int]):
    return len(path) > 2 and not same_lines(path) and not adjacent_lines(path)


def main():
    nodes = graph.adj.keys()
    time_d = []
    time_a = []
    distance = []

    time_a_same_line = []
    time_d_same_line = []
    distance_same_line = []

    time_a_adjacent_line = []
    time_d_adjacent_line = []
    distance_adjacent_line = []

    time_a_multiple_line_transfer = []
    time_d_multiple_line_transfer = []
    distance_multiple_line_transfer = []

    for i in nodes:
        for j in nodes:
            if i != j:
                start_time = timeit.default_timer()
                d, path = calc_sp_a_star(i, j)
                time_duration = timeit.default_timer() - start_time
                time_a.append(time_duration)

                if same_lines(path):
                    time_a_same_line.append(time_duration)
                    distance_same_line.append(d)
                elif adjacent_lines(path):
                    time_a_adjacent_line.append(time_duration)
                    distance_adjacent_line.append(d)
                elif multiple_line_transfers(path):
                    time_a_multiple_line_transfer.append(time_duration)
                    distance_multiple_line_transfer.append(d)

                start_time = timeit.default_timer()
                dijkstra(graph, i)
                time_duration = timeit.default_timer() - start_time
                time_d.append(time_duration)

                if same_lines(path):
                    time_d_same_line.append(time_duration)
                elif adjacent_lines(path):
                    time_d_adjacent_line.append(time_duration)
                elif multiple_line_transfers(path):
                    time_d_multiple_line_transfer.append(time_duration)

                distance.append(d)

    plot.title(
        f"Shortest path distance vs. run time\n(unreachable nodes are consider as distance 0)"
    )
    plot.xlabel("Distance")
    plot.ylabel("Run Time")
    plot.scatter(distance, time_d, label="Dijkstra")
    plot.scatter(distance, time_a, label="A*")
    plot.legend()
    plot.show()

    plot.title(f"Shortest path distance vs. run time for same line connections")
    plot.xlabel("Distance")
    plot.ylabel("Run Time")
    plot.scatter(distance_same_line, time_d_same_line, label="Dijkstra")
    plot.scatter(distance_same_line, time_a_same_line, label="A*")
    plot.legend()
    plot.show()

    plot.title(f"Shortest path distance vs. run time for adjacent line connections")
    plot.xlabel("Distance")
    plot.ylabel("Run Time")
    plot.scatter(distance_adjacent_line, time_d_adjacent_line, label="Dijkstra")
    plot.scatter(distance_adjacent_line, time_a_adjacent_line, label="A*")
    plot.legend()
    plot.show()

    plot.title(f"Shortest path distance vs. run time for multiple line transfers")
    plot.xlabel("Distance")
    plot.ylabel("Run Time")
    plot.scatter(
        distance_multiple_line_transfer, time_d_multiple_line_transfer, label="Dijkstra"
    )
    plot.scatter(
        distance_multiple_line_transfer, time_a_multiple_line_transfer, label="A*"
    )
    plot.legend()
    plot.show()


if __name__ == "__main__":
    main()
