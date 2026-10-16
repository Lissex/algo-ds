class Deque:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.head = 0
        self.size = 0
        self.deque = [None] * self.capacity

    def append(self, val):
        if self.size == self.capacity:
            self._resize()
        idx = (self.head + self.size) % self.capacity
        self.deque[idx] = val
        self.size += 1

    def appendleft(self, val):
        if self.size == self.capacity:
            self._resize()
        self.head = (self.head - 1) % self.capacity
        self.deque[self.head] = val
        self.size += 1

    def pop(self):
        if self.size == 0:
            raise IndexError("pop from empty deque")
        idx = (self.head + self.size - 1) % self.capacity
        val = self.deque[idx]
        self.deque[idx] = None
        self.size -= 1
        return val

    def popleft(self):
        if self.size == 0:
            raise IndexError("popleft from empty deque")
        val = self.deque[self.head]
        self.deque[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return val

    def _resize(self):
        new_capacity = self.capacity * 2
        new_deque = [None] * new_capacity
        for i in range(self.size):
            new_deque[i] = self.deque[(self.head + i) % self.capacity]
        self.deque = new_deque
        self.capacity = new_capacity
        self.head = 0

    def __str__(self):
        if self.size == 0:
            return "[]"
        items = [str(self.deque[(self.head + i) % self.capacity]) for i in range(self.size)]
        return "[" + ", ".join(items) + "]"