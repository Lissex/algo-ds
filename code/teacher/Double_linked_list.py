class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

class Double_Linked_List:
    def __init__(self, *lst):
        self.size = 0
        self.head = None
        self.tail = None

        for i in lst:
            self.append(i)

    def __get_item(self, idx):
        if idx < 0:
            idx += self.size
        if idx > self.size - 1 or idx < 0:
            raise IndexError("out of range")
        if idx < self.size // 2:
            cur = self.head
            cur_idx = 0
            while cur_idx != idx:
                cur = cur.next
                cur_idx += 1
            return cur
        else:
            cur = self.tail
            cur_idx = self.size - 1
            while cur_idx != idx:
                cur = cur.prev
                cur_idx -= 1
            return cur

    def __len__(self):
        return self.size

    def append(self, val):
        new_node = Node(val)
        self.size += 1
        if not self.head:
            self.head = self.tail = new_node
            return
        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = self.tail.next

    def appendleft(self, val):
        new_node = Node(val)
        self.size += 1
        if not self.head:
            self.head = self.tail = new_node
            return
        self.head.prev = new_node
        new_node.next = self.head
        self.head = new_node

    def reverse(self):
        cur = self.head
        while cur:
            cur.prev, cur.next = cur.next, cur.prev
            cur = cur.prev
        self.head, self.tail = self.tail, self.head

    def insert(self, idx, val):
        if idx < 0:
            idx += self.size
        if idx < 0:
            idx = 0
        if idx > self.size:
            idx = self.size

        if idx == 0:
            self.appendleft(val)
        elif idx == self.size:
            self.append(val)
        else:
            new_node = Node(val)
            prev_node = self.__get_item(idx - 1)
            next_node = prev_node.next

            new_node.prev = prev_node
            new_node.next = next_node
            prev_node.next = new_node
            if next_node:
                next_node.prev = new_node

            self.size += 1

    def pop(self, idx=-1):
        if self.size == 0:
            raise IndexError("pop from empty list")

        if idx < 0:
            idx += self.size
        if idx < 0 or idx >= self.size:
            raise IndexError("out of range")

        node = self.__get_item(idx)
        val = node.val

        prev_node = node.prev
        next_node = node.next

        if prev_node:
            prev_node.next = next_node
        else:
            self.head = next_node

        if next_node:
            next_node.prev = prev_node
        else:
            self.tail = prev_node

        self.size -= 1
        return val

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

    def find(self, val):
        cur = self.head
        idx = 0
        while cur:
            if cur.val == val:
                return idx
            cur = cur.next
            idx += 1
        return -1

    def __getitem__(self, idx):
        return self.__get_item(idx).val

    def __setitem__(self, idx, value):
        self.__get_item(idx).val = value

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.val
            cur = cur.next

    def __str__(self):
        if not self.head:
            return "empty"
        cur = self.head
        res = ""
        while cur:
            if not cur.next:
                res += f"{cur.val}"
                cur = cur.next
                continue
            res += f"{cur.val}⇔"
            cur = cur.next
        return res