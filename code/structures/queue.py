class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


class Queue:
    """Очередь (FIFO — First In, First Out) на связанном списке.
    Добавляем в хвост (tail), забираем из головы (head) — обе операции O(1)."""

    def __init__(self):
        self.head = None   # отсюда забираем
        self.tail = None   # сюда добавляем
        self.size = 0

    def add(self, val):
        """Поставить элемент в конец очереди (enqueue). O(1)"""
        new_node = Node(val)
        if self.tail is None:          # очередь пустая
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def remove(self):
        """Забрать элемент из начала очереди (dequeue). O(1)"""
        if self.head is None:
            raise IndexError("remove from empty queue")
        val = self.head.val
        self.head = self.head.next
        if self.head is None:          # забрали последний элемент
            self.tail = None
        self.size -= 1
        return val

    def peek(self):
        """Посмотреть первый элемент, не удаляя его. O(1)"""
        if self.head is None:
            raise IndexError("peek from empty queue")
        return self.head.val

    def is_empty(self):
        return self.head is None

    def __len__(self):
        return self.size

    def __str__(self):
        items = []
        cur = self.head
        while cur:
            items.append(str(cur.val))
            cur = cur.next
        return "front -> [" + ", ".join(items) + "] <- back"
