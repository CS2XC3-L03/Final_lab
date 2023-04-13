import math
import final_project_part1
import approx
import timeit
import matplotlib.pyplot as plot

def expt1_data(func, func_approx, node_num):
    KS = [0.1, 0.2, 0.4, 0.6]
    TRIAL_NUM = 10
    LOWER = 1
    avg_times = [[] for _ in range(len(KS) + 1)]

    for edge_num in range(node_num, 2 * final_project_part1.calc_max_edges(node_num-1) + 1):
        times = [0 for _ in range(len(KS) + 1)]
        for _ in range(TRIAL_NUM):
            G = final_project_part1.create_graph_with_random_edges(node_num, edge_num, LOWER, 900)

            start_time = timeit.default_timer()
            func(G, 0)
            time_duration = timeit.default_timer() - start_time

            times[0] += time_duration

            for i in range(len(KS)):
                start_time = timeit.default_timer()
                func_approx(G, 0, KS[i] * node_num)
                time_duration = timeit.default_timer() - start_time

                times[i+1] += time_duration

        for i in range(len(KS) + 1):
            avg_times[i].append(times[i] / TRIAL_NUM)

    return avg_times

def expt1_graph(data, node_num, algo_name):
    KS = [0.1, 0.2, 0.4, 0.6]
    plot.title(f"Graph Density vs Run Time Approximations\ndifferent k values (Node_number = {node_num})")
    plot.xlabel("Graph Density")
    plot.ylabel("Run Time")
    plot.plot(list(range(node_num, 2 * final_project_part1.calc_max_edges(node_num - 1) + 1)), data[0], label=f"{algo_name} Approximation (k=0)")
    print(len(data))
    for i in range(len(KS)):
        plot.plot(list(range(node_num, 2 * final_project_part1.calc_max_edges(node_num - 1) + 1)), data[i+1], label=f"{algo_name} Approximation (k={math.ceil(KS[i]*node_num)})")
    plot.legend()
    plot.show()

data = expt1_data(final_project_part1.dijkstra, approx.dijkstra_approx, 12)
expt1_graph(data, 12, "Dijkstra")

data = expt1_data(final_project_part1.dijkstra, approx.dijkstra_approx, 15)
expt1_graph(data, 15, "Dijkstra")

data = expt1_data(final_project_part1.dijkstra, approx.dijkstra_approx, 20)
expt1_graph(data, 20, "Dijkstra")

data = expt1_data(final_project_part1.bellman_ford, approx.bellman_ford_approx, 12)
expt1_graph(data, 12, "Bellman-Ford")

data = expt1_data(final_project_part1.bellman_ford, approx.bellman_ford_approx, 15)
expt1_graph(data, 15, "Bellman-Ford")

data = expt1_data(final_project_part1.bellman_ford, approx.bellman_ford_approx, 20)
expt1_graph(data, 20, "Bellman-Ford")
