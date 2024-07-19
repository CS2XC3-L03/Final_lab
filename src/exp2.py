import matplotlib.pyplot as plot
import timeit
from part1 import dijkstra
from part3 import (
    read_stations,
    read_station_connections,
    calc_sp_a_star,
    same_lines,
    adjacent_lines,
    number_of_lines_in_path,
)


def main():
    stations = read_stations()
    graph, connections = read_station_connections(stations)

    nodes = graph.adj.keys()
    time_d = []
    time_a = []
    frequency_paths: dict[int, int] = {}
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
                start_time1 = timeit.default_timer()
                d, path = calc_sp_a_star(stations, graph, i, j)
                time_duration1 = timeit.default_timer() - start_time1
                time_a.append(time_duration1)

                start_time2 = timeit.default_timer()
                dijkstra(graph, i)
                time_duration2 = timeit.default_timer() - start_time2
                time_d.append(time_duration2)

                if same_lines(path, connections):
                    time_a_same_line.append(time_duration1)
                    time_d_same_line.append(time_duration2)
                    distance_same_line.append(d)
                elif adjacent_lines(path, connections):
                    time_a_adjacent_line.append(time_duration1)
                    time_d_adjacent_line.append(time_duration2)
                    distance_adjacent_line.append(d)
                elif len(path) > 2:
                    time_a_multiple_line_transfer.append(time_duration1)
                    time_d_multiple_line_transfer.append(time_duration2)
                    distance_multiple_line_transfer.append(d)

                distance.append(d)

                number_of_lines = number_of_lines_in_path(path, connections)
                if number_of_lines != 0:
                    frequency_paths[number_of_lines] = (
                        frequency_paths.get(number_of_lines, 0) + 1
                    )

    plot.title(
        "Shortest path distance vs. run time\n(unreachable nodes are consider as distance 0)"
    )
    plot.xlabel("Distance")
    plot.ylabel("Run Time")
    plot.scatter(distance, time_d, label="Dijkstra")
    plot.scatter(distance, time_a, label="A*")
    plot.legend()
    plot.show()

    plot.title("Shortest path distance vs. run time for same line connections")
    plot.xlabel("Distance")
    plot.ylabel("Run Time")
    plot.scatter(distance_same_line, time_d_same_line, label="Dijkstra")
    plot.scatter(distance_same_line, time_a_same_line, label="A*")
    plot.legend()
    plot.show()

    plot.title("Shortest path distance vs. run time for adjacent line connections")
    plot.xlabel("Distance")
    plot.ylabel("Run Time")
    plot.scatter(distance_adjacent_line, time_d_adjacent_line, label="Dijkstra")
    plot.scatter(distance_adjacent_line, time_a_adjacent_line, label="A*")
    plot.legend()
    plot.show()

    plot.title("Shortest path distance vs. run time for multiple line transfers")
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

    plot.title(
        "Number of lines in shortest path vs. frequency\n (Not including unreachable nodes)"
    )
    plot.xlabel("Number of lines")
    plot.ylabel("Frequency")
    plot.bar([*frequency_paths.keys()], [*frequency_paths.values()])
    plot.show()


if __name__ == "__main__":
    main()
