class Stack:
    """Стек (LIFO — Last In, First Out) на списке Python — так делали на парах.
    Вершина стека — КОНЕЦ списка: append и pop в конце работают за O(1).
    Сам стек занимает O(n)."""

    def __init__(self):
        self.data = []

    def add(self, val):
        """Положить элемент на вершину (push).
        Время O(1) амортизированно: list.append пишет в конец, изредка список
        расширяется (копирование O(n)), но в среднем O(1). Память O(1)."""
        self.data.append(val)

    def remove(self):
        """Снять элемент с вершины и вернуть его (pop).
        Время O(1): удаление последнего элемента ничего не сдвигает. Память O(1)."""
        if not self.data:
            raise IndexError("remove from empty stack")
        return self.data.pop()

    def peek(self):
        """Посмотреть верхний элемент, не удаляя его. Время O(1), память O(1)."""
        if not self.data:
            raise IndexError("peek from empty stack")
        return self.data[-1]

    def is_empty(self):
        return len(self.data) == 0

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return "bottom -> " + str(self.data) + " <- top"


# ---------- Другой вариант: стек на связанном списке ----------

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


class LinkedStack:
    """Стек на связанном списке. Вершина — голова списка (head),
    потому что добавить/удалить в начале списка можно за O(1).
    Все операции — честные O(1) без амортизации; цена — ссылка next в каждом узле."""

    def __init__(self):
        self.top = None
        self.size = 0

    def add(self, val):
        """Время O(1), память O(1) — один новый узел."""
        new_node = Node(val)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

    def remove(self):
        """Время O(1), память O(1)."""
        if self.top is None:
            raise IndexError("remove from empty stack")
        val = self.top.val
        self.top = self.top.next
        self.size -= 1
        return val

    def peek(self):
        """Время O(1), память O(1)."""
        if self.top is None:
            raise IndexError("peek from empty stack")
        return self.top.val

    def is_empty(self):
        return self.top is None

    def __len__(self):
        return self.size
