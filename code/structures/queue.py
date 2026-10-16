class Queue:
    """Очередь (FIFO — First In, First Out) на списке Python — так делали на парах.
    Добавляем в конец списка, забираем из начала (индекс 0).
    Сама очередь занимает O(n)."""

    def __init__(self):
        self.data = []

    def add(self, val):
        """Поставить элемент в конец очереди (enqueue).
        Время O(1) амортизированно (list.append), память O(1)."""
        self.data.append(val)

    def remove(self):
        """Забрать элемент из начала очереди (dequeue).
        Время O(n): после pop(0) все остальные элементы сдвигаются на одну позицию влево.
        Память O(1)."""
        if not self.data:
            raise IndexError("remove from empty queue")
        return self.data.pop(0)

    def peek(self):
        """Посмотреть первый элемент, не удаляя его. Время O(1), память O(1)."""
        if not self.data:
            raise IndexError("peek from empty queue")
        return self.data[0]

    def is_empty(self):
        return len(self.data) == 0

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return "front -> " + str(self.data) + " <- back"


# ---------- Другой вариант 1: очередь на связанном списке ----------

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


class LinkedQueue:
    """Очередь на связанном списке с указателями head и tail.
    Добавляем в хвост, забираем из головы — обе операции O(1) по времени и памяти."""

    def __init__(self):
        self.head = None   # отсюда забираем
        self.tail = None   # сюда добавляем
        self.size = 0

    def add(self, val):
        """Время O(1): tail известен, не нужно идти по списку. Память O(1) — один узел."""
        new_node = Node(val)
        if self.tail is None:          # очередь пустая
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def remove(self):
        """Время O(1): просто сдвигаем head. Память O(1)."""
        if self.head is None:
            raise IndexError("remove from empty queue")
        val = self.head.val
        self.head = self.head.next
        if self.head is None:          # забрали последний элемент
            self.tail = None
        self.size -= 1
        return val

    def peek(self):
        if self.head is None:
            raise IndexError("peek from empty queue")
        return self.head.val

    def is_empty(self):
        return self.head is None

    def __len__(self):
        return self.size


# ---------- Другой вариант 2: очередь на collections.deque ----------

from collections import deque


class DequeQueue:
    """Очередь на встроенном deque — так обычно пишут в реальном коде.
    append и popleft — O(1), ничего не сдвигается."""

    def __init__(self):
        self.data = deque()

    def add(self, val):
        self.data.append(val)

    def remove(self):
        if not self.data:
            raise IndexError("remove from empty queue")
        return self.data.popleft()

    def peek(self):
        if not self.data:
            raise IndexError("peek from empty queue")
        return self.data[0]

    def is_empty(self):
        return not self.data

    def __len__(self):
        return len(self.data)
