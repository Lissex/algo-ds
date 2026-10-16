class Node:
    def __init__(self, key=None):
        self.key = key
        self.next = None


class Hashset:
    """Хэш-множество с цепочками (separate chaining).
    buckets — массив корзин, в каждой корзине — односвязный список узлов."""

    def __init__(self, capacity=10, load_factor=0.75):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity
        self.load_factor = load_factor

    def _hash(self, key):
        """FNV-1a (32 бита) -> номер корзины."""
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
        """Удваиваем capacity и заново раскладываем ВСЕ ключи:
        номер корзины зависит от capacity, поэтому старые индексы неверны."""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        for node in old_buckets:
            while node:
                self.add(node.key)
                node = node.next

    def add(self, key):
        """Добавить ключ (дубликаты игнорируются).
        Время: O(1) в среднем (короткая цепочка), O(n) в худшем.
        Память: O(1) — один узел (при resize — O(n), но редко)."""
        if self._load_factor() >= self.load_factor:
            self._resize()
        idx = self._hash(key)
        head = self.buckets[idx]
        if head is None:                  # корзина пустая
            self.buckets[idx] = Node(key)
            self.size += 1
            return
        while head:                       # проходим цепочку
            if head.key == key:           # уже есть — ничего не делаем
                return
            prev = head
            head = head.next
        prev.next = Node(key)             # коллизия: дописываем в конец цепочки
        self.size += 1                    # (у преподавателя этой строки нет)

    def remove(self, key):
        """Удалить ключ. Нет ключа — KeyError.
        Время: O(1) в среднем, O(n) в худшем. Память: O(1)."""
        idx = self._hash(key)
        head = self.buckets[idx]
        if head is None:
            raise KeyError(key)
        if head.key == key:               # удаляем первый узел цепочки
            self.buckets[idx] = head.next
            self.size -= 1
            return
        while head.next:                  # у преподавателя `while head` —
            if head.next.key == key:      # падает на head.next.key, если next = None
                head.next = head.next.next
                self.size -= 1
                return
            head = head.next
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
        for node in self.buckets:
            while node:
                yield node.key
                node = node.next

    def __str__(self):
        return '{' + ', '.join(str(k) for k in self) + '}'
