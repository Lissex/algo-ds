# Время O(1) амортизированно: каждый элемент перекладывается ровно один раз.
# Память O(n): два стека, в сумме n элементов.

class MyQueue:
    def __init__(self):
        self.inbox = []                # сюда пушим
        self.outbox = []               # отсюда забираем

    def push(self, x: int) -> None:
        self.inbox.append(x)

    def _move(self):
        # перекладываем, только когда outbox пуст: порядок разворачивается -> FIFO
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())

    def pop(self) -> int:
        self._move()
        return self.outbox.pop()

    def peek(self) -> int:
        self._move()
        return self.outbox[-1]

    def empty(self) -> bool:
        return not self.inbox and not self.outbox
