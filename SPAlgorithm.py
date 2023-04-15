from abc import ABC, abstractmethod
from Graph import *


class SPAlgorithm(ABC):
    @abstractmethod
    def calc_sp(graph: Graph, source: int, dest: int) -> float:
        pass
