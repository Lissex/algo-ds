class Node:
    def __init__(self, key=None, val=None):
        self.key = key
        self.next = None


class Hashset:
    def __init__(self, capacity = 10, load_factor = 0.75):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity
        self.load_factor = load_factor
        
    def __iter__(self):
        for el in self.buckets:
            while el:
                yield el
                el = el.next
    
    def __str__(self):
        res = ''
        count = 0
        for el in self:
            count += 1
            if count == self.size:
                res += f'{el.key}'
                break
            res += f'{el.key}, '
        return '{' + res + '}'
    
        
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
                self.add(node.key)
                node = node.next
    
    def add(self, key):
        if self._load_factor() >= self.load_factor:
            self._resize()
        idx = self._hash(key)
        head = self.buckets[idx]
        if head is None:
            self.buckets[idx] = Node(key)
            self.size += 1
            return
        while head:
            if head.key == key:
                return
            prev = head
            head = head.next
        prev.next = Node(key)
    
    def remove(self, key):
        idx = self._hash(key)
        head = self.buckets[idx]
        if head is None:
            raise KeyError("no key")
        if head.key == key:
            self.buckets[idx] = head.next
            self.size -= 1
            return
        
        while head:
            if head.next.key == key:
                head.next = head.next.next
                self.size -= 1
                return 
            head = head.next
        raise KeyError("no key")
                
                
            
        
        


