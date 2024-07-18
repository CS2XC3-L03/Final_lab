import math


class Element:

    def __init__(self, value: int, key: float):
        self.value = value
        self.key = key

    def __str__(self):
        return "(" + str(self.value) + "," + str(self.key) + ")"


class MinHeap:
    length = 0
    elements = []

    def __init__(self, elements: list[Element]):
        self.elements = elements
        self.length = len(elements)
        self.map = {}
        for i in range(len(elements)):
            self.map[elements[i].value] = i
        self.build_heap()

    def build_heap(self):
        for i in range(self.length // 2 - 1, -1, -1):
            self.sink(i)

    def sink(self, i: int):
        smallest_known = i
        if (
            self.left(i) < self.length
            and self.elements[self.left(i)].key < self.elements[i].key
        ):
            smallest_known = self.left(i)
        if (
            self.right(i) < self.length
            and self.elements[self.right(i)].key < self.elements[smallest_known].key
        ):
            smallest_known = self.right(i)
        if smallest_known != i:
            self.elements[i], self.elements[smallest_known] = (
                self.elements[smallest_known],
                self.elements[i],
            )
            self.map[self.elements[i].value] = i
            self.map[self.elements[smallest_known].value] = smallest_known
            self.sink(smallest_known)

    def insert(self, element: Element):
        if len(self.elements) == self.length:
            self.elements.append(element)
        else:
            self.elements[self.length] = element
        self.map[element.value] = self.length
        self.length += 1
        self.swim(self.length - 1)

    def insert_elements(self, elements: list[Element]):
        for element in elements:
            self.insert(element)

    def swim(self, i: int):
        while i > 0 and self.elements[i].key < self.elements[self.parent(i)].key:
            self.elements[i], self.elements[self.parent(i)] = (
                self.elements[self.parent(i)],
                self.elements[i],
            )
            self.map[self.elements[i].value] = i
            self.map[self.elements[self.parent(i)].value] = self.parent(i)
            i = self.parent(i)

    def get_min(self):
        if len(self.elements) > 0:
            return self.elements[0]

    def extract_min(self):
        self.elements[0], self.elements[self.length - 1] = (
            self.elements[self.length - 1],
            self.elements[0],
        )
        self.map[self.elements[self.length - 1].value] = self.length - 1
        self.map[self.elements[0].value] = 0
        min_element = self.elements[self.length - 1]
        self.length -= 1
        self.map.pop(min_element.value)
        self.sink(0)
        return min_element

    def decrease_key(self, value: int, new_key: float):
        if new_key >= self.elements[self.map[value]].key:
            return
        index = self.map[value]
        self.elements[index].key = new_key
        self.swim(index)

    def get_element_from_value(self, value):
        return self.elements[self.map[value]]

    def is_empty(self):
        return self.length == 0

    def left(self, i):
        return 2 * (i + 1) - 1

    def right(self, i):
        return 2 * (i + 1)

    def parent(self, i):
        return (i + 1) // 2 - 1

    def __str__(self):
        height = math.ceil(math.log(self.length + 1, 2))
        whitespace = 2**height + height
        s = ""
        for i in range(height):
            for j in range(2**i - 1, min(2 ** (i + 1) - 1, self.length)):
                s += " " * whitespace
                s += str(self.elements[j]) + " "
            s += "\n"
            whitespace = whitespace // 2
        return s
