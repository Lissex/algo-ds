class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None


class Double_Linked_List:
    """Двусвязный список с head и tail (по коду преподавателя)."""

    def __init__(self, *lst):
        self.size = 0
        self.head = None
        self.tail = None
        for i in lst:
            self.append(i)

    def _get_node(self, idx):
        """Узел по индексу. Идём с той стороны, которая ближе: до n/2 шагов.
        Время O(n) (константа ½ отбрасывается), память O(1) — один указатель."""
        if idx < 0:
            idx += self.size               # поддержка lst[-1]
        if idx < 0 or idx >= self.size:
            raise IndexError("out of range")
        if idx < self.size // 2:           # ближе к началу — идём от head
            cur = self.head
            for _ in range(idx):
                cur = cur.next
        else:                              # ближе к концу — идём от tail
            cur = self.tail
            for _ in range(self.size - 1 - idx):
                cur = cur.prev
        return cur

    def __getitem__(self, idx):
        """lst[idx]"""
        return self._get_node(idx).val

    def __setitem__(self, idx, value):
        """lst[idx] = value"""
        self._get_node(idx).val = value

    def __len__(self):
        return self.size

    def append(self, val):
        """В конец. Время O(1) — благодаря tail. Память O(1) — один новый узел."""
        new_node = Node(val)
        self.size += 1
        if not self.head:
            self.head = self.tail = new_node
            return
        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node

    def appendleft(self, val):
        """В начало. Время O(1), память O(1) — один новый узел."""
        new_node = Node(val)
        self.size += 1
        if not self.head:
            self.head = self.tail = new_node
            return
        self.head.prev = new_node
        new_node.next = self.head
        self.head = new_node

    def pop(self, idx=-1):
        """Удалить по индексу (по умолчанию последний) и вернуть значение.
        Время: с конца/начала — O(1), из середины — O(n). Память O(1) — только указатели."""
        if self.size == 0:
            raise IndexError("pop from empty list")
        node = self._get_node(idx)
        prev_node, next_node = node.prev, node.next
        if prev_node:
            prev_node.next = next_node
        else:                      # удалили голову
            self.head = next_node
        if next_node:
            next_node.prev = prev_node
        else:                      # удалили хвост
            self.tail = prev_node
        self.size -= 1
        return node.val

    def insert(self, idx, val):
        if idx < 0:
            idx += self.size
        idx = max(0, min(idx, self.size))
        if idx == 0:
            return self.appendleft(val)
        if idx == self.size:
            return self.append(val)
        new_node = Node(val)
        prev_node = self._get_node(idx - 1)
        next_node = prev_node.next
        new_node.prev, new_node.next = prev_node, next_node
        prev_node.next = new_node
        next_node.prev = new_node
        self.size += 1

    def remove(self, val):
        cur = self.head
        while cur:
            if cur.val == val:
                if cur.prev:
                    cur.prev.next = cur.next
                else:
                    self.head = cur.next
                if cur.next:
                    cur.next.prev = cur.prev
                else:
                    self.tail = cur.prev
                self.size -= 1
                return
            cur = cur.next
        raise ValueError(f"{val} not in list")

    def reverse(self):
        """Меняем местами prev и next у каждого узла.
        Время O(n) — один проход, память O(1) — разворот на месте."""
        cur = self.head
        while cur:
            cur.prev, cur.next = cur.next, cur.prev
            cur = cur.prev                 # бывший next
        self.head, self.tail = self.tail, self.head

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.val
            cur = cur.next

    def __str__(self):
        return "⇔".join(str(v) for v in self) if self.head else "empty"
