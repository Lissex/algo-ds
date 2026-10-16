class Deque:
    """Дек на кольцевом массиве (по коду преподавателя).
    head — индекс первого элемента, size — сколько элементов.
    Последний элемент лежит в (head + size - 1) % capacity."""

    def __init__(self, capacity=10):
        self.capacity = capacity
        self.head = 0
        self.size = 0
        self.deque = [None] * self.capacity

    def append(self, val):
        """В правый конец. Время O(1) амортизированно (иногда resize за O(n)),
        память O(1) амортизированно: обычно просто пишем в свободную ячейку."""
        if self.size == self.capacity:
            self._resize()
        idx = (self.head + self.size) % self.capacity   # первая свободная справа
        self.deque[idx] = val
        self.size += 1

    def appendleft(self, val):
        """В левый конец. Время и память — O(1) амортизированно (как у append)."""
        if self.size == self.capacity:
            self._resize()
        self.head = (self.head - 1) % self.capacity     # шаг влево с «заворотом»
        self.deque[self.head] = val
        self.size += 1

    def pop(self):
        """popright: забрать справа. Время O(1): индекс считается формулой. Память O(1)."""
        if self.size == 0:
            raise IndexError("pop from empty deque")
        idx = (self.head + self.size - 1) % self.capacity
        val = self.deque[idx]
        self.deque[idx] = None
        self.size -= 1
        return val

    popright = pop   # в билетах метод называется popright

    def popleft(self):
        """Забрать слева. Время O(1): первый всегда в ячейке head. Память O(1)."""
        if self.size == 0:
            raise IndexError("popleft from empty deque")
        val = self.deque[self.head]
        self.deque[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return val

    def _resize(self):
        """Массив заполнен — создаём вдвое больший и «распрямляем» кольцо.
        Время O(n): копируем все элементы. Память O(n): новый массив на 2·capacity."""
        new_capacity = self.capacity * 2
        new_deque = [None] * new_capacity
        for i in range(self.size):
            new_deque[i] = self.deque[(self.head + i) % self.capacity]
        self.deque = new_deque
        self.capacity = new_capacity
        self.head = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        for i in range(self.size):
            yield self.deque[(self.head + i) % self.capacity]

    def __str__(self):
        return "[" + ", ".join(str(v) for v in self) + "]"
