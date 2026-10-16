class Node:
    def __init__(self, key=None, val=None):
        self.key = key
        self.val = val
        self.next = None


class Hashtable:
    def __init__(self, capacity = 10, load_factor = 0.75):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity
        self.load_factor = load_factor

    def _hash(self, key):
        if isinstance(key, str):
            data = key.encode('utf-8')
        else:
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
        if self._load_factor() >= self.load_factor:
            self._resize()
        head = self.buckets[self._hash(key)]
        if head is None:
            self.buckets[self._hash(key)] = Node(key, val)
            self.size += 1
            return

        while head:
            if head.key == key:
                head.val = val
                return
            prev = head
            head = head.next
        prev.next = Node(key, val)
        self.size += 1

    def __getitem__(self, key):
        head = self.buckets[self._hash(key)]
        while head.next:
            if head.key == key:
                return head.val
            head = head.next
        raise KeyError(f'no key {key}')

    def remove(self, key):
        head = self.buckets[self._hash(key)]
        if head is None:
            raise KeyError("No key")
        if head.key == key:
            self.buckets[self._hash(key)] = head.next
            self.size -= 1
            return
        while head:
            if head.next.key == key:
                head.next = head.next.next
                self.size -= 1
                return
        raise KeyError('No such key')
            

    def __len__(self):
        return self.size
    
    def __str__(self):
        res = ""
        count = 0
        for el in self:
            count += 1
            if count == self.size:
                res += f'{el.key}:{el.val}'
                break
            res += f'{el.key}:{el.val}, '
        return '{' + f'{res}' +'}'
    def __iter__(self):
        for head in self.buckets:
            while head:
                yield head
                head = head.next

    def keys(self):
        res = []
        for j in self:
            res.append(j.keys)
        return res

    def values(self):
        res = []
        for j in self:
            res.append(j.val)
        return res

    def items(self):
        res = []
        for j in self:
            res.append((j.key, j.val))
        return res

