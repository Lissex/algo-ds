class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


class Stack:
    """Стек (LIFO — Last In, First Out) на связанном списке.
    Вершина стека — голова списка, поэтому все операции O(1) по времени и O(1) по памяти.
    Сам стек занимает O(n): n узлов."""

    def __init__(self):
        self.top = None
        self.size = 0

    def add(self, val):
        """Положить элемент на вершину (push). Время O(1), память O(1) — один узел."""
        new_node = Node(val)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

    def remove(self):
        """Снять элемент с вершины и вернуть его (pop). Время O(1), память O(1)."""
        if self.top is None:
            raise IndexError("remove from empty stack")
        val = self.top.val
        self.top = self.top.next
        self.size -= 1
        return val

    def peek(self):
        """Посмотреть верхний элемент, не удаляя его. Время O(1), память O(1)."""
        if self.top is None:
            raise IndexError("peek from empty stack")
        return self.top.val

    def is_empty(self):
        return self.top is None

    def __len__(self):
        return self.size

    def __str__(self):
        items = []
        cur = self.top
        while cur:
            items.append(str(cur.val))
            cur = cur.next
        return "top -> [" + ", ".join(items) + "]"


class ArrayStack:
    """Тот же стек на обычном списке Python: вершина — конец списка."""

    def __init__(self):
        self.data = []

    def add(self, val):
        self.data.append(val)       # O(1) амортизированно

    def remove(self):
        if not self.data:
            raise IndexError("remove from empty stack")
        return self.data.pop()      # O(1)

    def peek(self):
        if not self.data:
            raise IndexError("peek from empty stack")
        return self.data[-1]

    def is_empty(self):
        return not self.data

    def __len__(self):
        return len(self.data)
