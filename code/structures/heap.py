"""Двоичная куча с настройкой min/max; API согласован с билетами."""


class Heap:
    def __init__(self, items=None, is_min=False):
        self.heap = []
        self._is_min = is_min
        if items is not None:
            self.heap = list(items)
            self.heapify()

    def _compare(self, a, b):
        return a < b if self._is_min else a > b

    def heapify(self):
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._sift_down(i)

    def _sift_down(self, i):
        n = len(self.heap)
        while True:
            best = i
            left, right = 2 * i + 1, 2 * i + 2
            if left < n and self._compare(self.heap[left], self.heap[best]):
                best = left
            if right < n and self._compare(self.heap[right], self.heap[best]):
                best = right
            if best == i:
                return
            self.heap[i], self.heap[best] = self.heap[best], self.heap[i]
            i = best

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if not self._compare(self.heap[i], self.heap[parent]):
                return
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            i = parent

    def add(self, value):
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)

    def remove(self):
        if not self.heap:
            raise IndexError("remove from empty heap")
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        value = self.heap.pop()
        if self.heap:
            self._sift_down(0)
        return value

    def peek(self):
        if not self.heap:
            raise IndexError("peek from empty heap")
        return self.heap[0]

    def __len__(self):
        return len(self.heap)
