class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


class Linked_list:
    """Односвязный список (по коду преподавателя)."""

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
        return '->'.join(str(v) for v in self)

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.head is None

    def _get_item(self, idx):
        """Вернуть УЗЕЛ по индексу. Время O(n): idx шагов от head. Память O(1)."""
        if idx < 0 or idx >= self.size:
            raise IndexError("Index out of range")
        cur = self.head
        cur_idx = 0
        while cur_idx != idx:
            cur = cur.next
            cur_idx += 1
        return cur

    def __getitem__(self, idx):
        return self._get_item(idx).val

    def __setitem__(self, idx, value):
        """lst[idx] = value. Находим узел и меняем значение.
        Время O(n) — поиск узла, память O(1) — только указатель."""
        target = self._get_item(idx)
        target.val = value

    def append(self, val):
        """Добавить в конец. Время O(n): без указателя на хвост идём до конца.
        Память O(1): создаём один узел."""
        new_node = Node(val)
        if self.head is None:          # список пустой
            self.head = new_node
        else:
            cur = self.head
            while cur.next:            # идём до последнего узла
                cur = cur.next
            cur.next = new_node
        self.size += 1

    def insert(self, idx, val):
        """Вставить val так, чтобы он оказался на позиции idx.
        Время O(n) на поиск prev (в начало — O(1)), память O(1) — один узел."""
        if idx < 0 or idx > self.size:
            raise IndexError("Index out of range")
        new_node = Node(val)
        if idx == 0:                   # вставка в начало — O(1)
            new_node.next = self.head
            self.head = new_node
        else:
            prev = self._get_item(idx - 1)
            new_node.next = prev.next  # сначала цепляем хвост
            prev.next = new_node       # потом переключаем prev
        self.size += 1

    def remove(self, val):
        """Удалить первое вхождение val.
        Время O(n): в худшем случае проходим весь список. Память O(1): указатель cur."""
        if self.head is None:
            raise ValueError("Value not found")
        if self.head.val == val:       # удаляем голову
            self.head = self.head.next
            self.size -= 1
            return
        cur = self.head
        while cur.next is not None and cur.next.val != val:
            cur = cur.next
        if cur.next is None:
            raise ValueError("Value not found")
        cur.next = cur.next.next       # «перепрыгиваем» удаляемый узел
        self.size -= 1

    def pop(self, idx):
        """Удалить элемент по индексу и вернуть его. Время O(n), память O(1)."""
        if idx < 0 or idx >= self.size:
            raise IndexError("Index out of range")
        if idx == 0:
            target = self.head
            self.head = self.head.next
            self.size -= 1
            return target.val
        prev = self._get_item(idx - 1)
        target = prev.next
        prev.next = target.next
        self.size -= 1
        return target.val

    def reverse(self):
        """Развернуть список на месте. O(n) по времени, O(1) по памяти."""
        prev = None
        cur = self.head
        while cur:
            nxt = cur.next     # 1. запомнили следующий
            cur.next = prev    # 2. развернули стрелку
            prev = cur         # 3. сдвинули prev
            cur = nxt          # 4. сдвинули cur
        self.head = prev

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.val
            cur = cur.next
