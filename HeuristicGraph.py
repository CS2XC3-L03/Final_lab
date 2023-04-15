from WeightedGraph import *


class HeuristicGraph(WeightedGraph):
    def __init__(self):
        super().__init__()
        self.__heuristic: dict[int, float] = {}

    def get_heuristic(self) -> dict[int, float]:
        return self.__heuristic
