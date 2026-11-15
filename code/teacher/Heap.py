# Min-heap родители меньше детей, max-heap наоборот
# Массив
# parent(i)  = (i - 1) // 2 left(i)    = 2*i + 1 right(i)   = 2*i + 2

class Heap:
    def __init__(self):
        self.heap = []
        
    def heapify(self):
        pass
    
    def _compare(self, a, b) -> bool:
        return a < b if self._is_min else a > b
    
    def _shift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._compare(self._data[i], self._data[parent]):
                self._data[i], self._data[parent] = self._data[parent], self._data[i]
                i = parent
            else:
                break
            
    def heapify(self, items) -> None:
        self._data = list(items)
        for i in range(len(self._data) // 2 - 1, -1, -1):
            self._sift_down(i)
    
    def _shift_down(self, i):
        n = len(self.heap)
        while True:
            best = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and self._compare(self.heap[left], self.heap[best]):
                best = left
            if right < n and self._compare(self.heap[right], self.heap[best]):
                best = right

            if best == i:
                break
            self.heap[i], self.heap[best] = self.heap[best], self.heap[i]
            i = best
    
    def pop(self):
        if not self.heap:
            raise ValueError("Pop from empty heap")
        if not self.heap:
            return
        self.heap[0], self.heap[len(self.heap) - 1] = self.heap[len(self.heap) - 1], self.heap[0]
        self.heap.pop()
        self._shift_down(0)
    
    def append(self, val):
        self._data.append(val)
        self._sift_up(len(self._data) - 1)
        
    def peek(self):
        if not self.heap:
            raise ValueError("Peek from empty heap")
        return self.heap[0]