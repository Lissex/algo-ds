class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


class Linked_list:
    def __init__(self, *lst):
        self.size = len(lst)
        if not lst:
            self.head = None
            return
        self.head = Node(lst[0])
        cur = self.head
        for i in range(1, len(lst)):
            cur.next = Node(lst[i])
            cur = cur.next

    def __str__(self):
        if not self.head:
            return 'empty'
        a = ''
        cur = self.head
        while cur:
            if not cur.next:
                a += f'{cur.val}'
                return a
            a += f'{cur.val}->'
            cur = cur.next

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.head is None

    def _get_item(self, idx):
        if idx < 0 or idx >= self.size:
            raise IndexError("Index out of range")
        cur = self.head
        cur_idx = 0
        while cur_idx != idx:
            cur = cur.next
            cur_idx += 1
        return cur

    def __getitem__(self, idx):
        target = self._get_item(idx)
        return target.val

    def append(self, val):
        new_node = Node(val)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node
        self.size += 1

    def insert(self, idx, val):
        if idx < 0 or idx > self.size:
            raise IndexError("Index out of range")

        new_node = Node(val)

        if idx == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            prev = self._get_item(idx - 1)
            new_node.next = prev.next
            prev.next = new_node

        self.size += 1

    def remove(self, val):
        if self.head is None:
            raise ValueError("Value not found")

        if self.head.val == val:
            self.head = self.head.next
            self.size -= 1
            return

        cur = self.head
        while cur.next is not None and cur.next.val != val:
            cur = cur.next

        if cur.next is None:
            raise ValueError("Value not found")

        cur.next = cur.next.next
        self.size -= 1

    def pop(self, idx):
        if idx < 0:
            raise IndexError("Negative index is not allowed")
        if idx >= self.size:
            raise IndexError("Index out of range")

        if idx == 0:
            target = self.head
            self.head = self.head.next
            self.size -= 1
            return target.val

        cur = self.head
        cur_idx = 0
        while cur_idx != idx - 1:
            cur = cur.next
            cur_idx += 1

        target = cur.next
        cur.next = target.next
        self.size -= 1
        return target.val

    def swap(self, idx1, idx2):
        node1 = self._get_item(idx1)
        node2 = self._get_item(idx2)
        node1.val, node2.val = node2.val, node1.val

    def reverse(self):
        prev = None
        cur = self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    def __setitem__(self, idx, value):
        target = self._get_item(idx)
        target.val = value

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.val
            cur = cur.next

