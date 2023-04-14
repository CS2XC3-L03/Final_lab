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


def read_station_connections(stations, graph):
    with open(station_connections_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for station1, station2, *_ in reader:
            station1 = int(station1)
            station2 = int(station2)
            weight = distance(stations[station1], stations[station2])

            if station1 not in graph.adj:
                graph.add_node(station1)
            if station2 not in graph.adj:
                graph.add_node(station2)

            graph.add_edge(station1, station2, weight)

stations = read_stations()

def main():
    graph = DirectedWeightedGraph()
    read_station_connections(stations, graph)

    nodes = graph.adj.keys()
    time_d = []
    time_a = []
    distance = []
    for i in nodes:
        for j in nodes:
            if i != j:
                start_time = timeit.default_timer()
                dists = dijkstra(graph, i)
                d = dists[j] if j in dists else 0
                time_duration = timeit.default_timer() - start_time
                time_d.append(time_duration)
                start_time = timeit.default_timer()
                d = calc_sp_a_star(graph, i ,j)
                time_duration = timeit.default_timer() - start_time
                time_a.append(time_duration)
                distance.append(d)
    
    plot.title(f"shortest path distance vs. run time\n(unreachable nodes are consider as distance 0)")
    plot.xlabel("Distance")
    plot.ylabel("Run Time")
    plot.scatter(distance, time_d, label = "dijkstra")
    plot.scatter(distance, time_a, label = "A*")
    plot.legend()
    plot.show()

def calc_sp_a_star(graph, source, dest):
    heuristic = {node: distance(stations[node], stations[dest]) for node in list(graph.adj.keys())}
    _, path = a_star(graph, source, dest, heuristic)
    dist: float = 0
    for i in range(1, len(path)):
        dist += graph.w(path[i - 1], path[i])
    return dist

if __name__ == "__main__":
    main()
