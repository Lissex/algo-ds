class Node:
    def __init__(self, key=None, val=None):
        self.key = key
        self.val = val
        self.next = None


class Hashtable:
    """Хэш-таблица (словарь) с цепочками. Как Hashset, но узел хранит пару key: val."""

    def __init__(self, capacity=10, load_factor=0.75):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity
        self.load_factor = load_factor

    def _hash(self, key):
        data = str(key).encode('utf-8')
        hash_val = 0x811c9dc5
        for byte in data:
            hash_val ^= byte
            hash_val *= 0x01000193
            hash_val &= 0xFFFFFFFF
        return hash_val % self.capacity

    def _load_factor(self):
        return self.size / self.capacity

    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        for node in old_buckets:
            while node:
                self[node.key] = node.val
                node = node.next

    def __setitem__(self, key, val):
        """table[key] = val: вставка или обновление.
        Время: O(1) в среднем, O(n) в худшем. Память: O(1) — максимум один узел."""
        if self._load_factor() >= self.load_factor:
            self._resize()
        idx = self._hash(key)
        head = self.buckets[idx]
        if head is None:
            self.buckets[idx] = Node(key, val)
            self.size += 1
            return
        while head:
            if head.key == key:           # ключ есть — обновляем значение
                head.val = val
                return
            prev = head
            head = head.next
        prev.next = Node(key, val)
        self.size += 1

    def __getitem__(self, key):
        """table[key]. Нет ключа — KeyError."""
        head = self.buckets[self._hash(key)]
        while head:                       # у преподавателя `while head.next` —
            if head.key == key:           # пропускает последний узел и падает на None
                return head.val
            head = head.next
        raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def remove(self, key):
        idx = self._hash(key)
        head = self.buckets[idx]
        if head is None:
            raise KeyError(key)
        if head.key == key:
            self.buckets[idx] = head.next
            self.size -= 1
            return
        while head.next:
            if head.next.key == key:
                head.next = head.next.next
                self.size -= 1
                return
            head = head.next              # у преподавателя этой строки нет — вечный цикл
        raise KeyError(key)

    def __contains__(self, key):
        node = self.buckets[self._hash(key)]
        while node:
            if node.key == key:
                return True
            node = node.next
        return False

    def __len__(self):
        return self.size

    def __iter__(self):
        for head in self.buckets:
            while head:
                yield head
                head = head.next

    def keys(self):
        return [node.key for node in self]    # у преподавателя опечатка: j.keys

    def values(self):
        return [node.val for node in self]

    def items(self):
        return [(node.key, node.val) for node in self]

    def __str__(self):
        return '{' + ', '.join(f'{n.key}: {n.val}' for n in self) + '}'
