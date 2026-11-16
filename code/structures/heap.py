# Min-heap родители меньше детей, max-heap наоборот
# Массив
# parent(i)  = (i - 1) // 2 left(i)    = 2*i + 1 right(i)   = 2*i + 2

class Heap:
    def __init__(self):
        self.heap = []
        self._is_min = False
    
    def _compare(self, a, b) -> bool:
        # Одна функция сравнения задаёт min-heap или max-heap.
        return a < b if self._is_min else a > b
    
    def _shift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._compare(self.heap[i], self.heap[parent]):
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                i = parent
            else:
                break
            
    def heapify(self, items) -> None:
        # Копируем входные элементы и восстанавливаем порядок снизу вверх.
        self.heap = list(items)
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._shift_down(i)
    
    def _shift_down(self, i):
        # Меняем узел с лучшим ребёнком, пока нарушено свойство кучи.
        n = len(self.heap)
        while True:
            best = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and self._compare(self.heap[left], self.heap[best]):
                best = left
            if right < n and self._compare(self.heap[right], self.heap[best]):
                best = right

            if best == i:
                break
            self.heap[i], self.heap[best] = self.heap[best], self.heap[i]
            i = best
    
    def pop(self):
        if not self.heap:
            raise ValueError("Pop from empty heap")
        # Корень — приоритетный элемент; после удаления просеиваем замену.
        value = self.heap[0]
        self.heap[0], self.heap[len(self.heap) - 1] = self.heap[len(self.heap) - 1], self.heap[0]
        self.heap.pop()
        if self.heap:
            self._shift_down(0)
        return value
    
    def append(self, val):
        # Добавляем в конец, затем поднимаем элемент к подходящей позиции.
        self.heap.append(val)
        self._shift_up(len(self.heap) - 1)
        
    def peek(self):
        # Корень содержит минимум или максимум и не удаляется.
        if not self.heap:
            raise ValueError("Peek from empty heap")
        return self.heap[0]
