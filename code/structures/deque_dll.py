class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None


class LinkedDeque:
    """Дек на двусвязном списке. Все 4 операции — честные O(1),
    без амортизации и без перевыделения памяти."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, val):
        node = Node(val)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.size += 1

    def appendleft(self, val):
        node = Node(val)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self.size += 1

    def pop(self):
        """popright"""
        if self.tail is None:
            raise IndexError("pop from empty deque")
        node = self.tail
        self.tail = node.prev
        if self.tail is None:      # был один элемент
            self.head = None
        else:
            self.tail.next = None
        self.size -= 1
        return node.val

    popright = pop

    def popleft(self):
        if self.head is None:
            raise IndexError("popleft from empty deque")
        node = self.head
        self.head = node.next
        if self.head is None:      # был один элемент
            self.tail = None
        else:
            self.head.prev = None
        self.size -= 1
        return node.val

    def __len__(self):
        return self.size

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.val
            cur = cur.next
