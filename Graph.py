from abc import ABC, abstractmethod


class Graph(ABC):
    @abstractmethod
    def get_nodes() -> list[int]:
        pass

    @abstractmethod
    def get_adj_nodes(node: int) -> list[int]:
        pass

    @abstractmethod
    def add_node(node: int):
        pass

    @abstractmethod
    def add_edge(start: int, end: int, w: float):
        pass

    @abstractmethod
    def get_num_of_nodes() -> int:
        pass

    @abstractmethod
    def w(node1: int, node2: int) -> float:
        pass
