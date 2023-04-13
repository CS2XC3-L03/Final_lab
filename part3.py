import csv

from final_project_part1 import DirectedWeightedGraph

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
            stations[id] = (float(lat), float(long))
    return stations


def read_station_connections(stations, graph):
    with open(station_connections_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for station1, station2, *_ in reader:
            weight = distance(stations[station1], stations[station2])

            if station1 not in graph.adj:
                graph.add_node(station1)
            if station2 not in graph.adj:
                graph.add_node(station2)

            graph.add_edge(station1, station2, weight)


def main():
    stations = read_stations()
    graph = DirectedWeightedGraph()
    read_station_connections(stations, graph)
    print(graph.adj)


if __name__ == "__main__":
    main()
