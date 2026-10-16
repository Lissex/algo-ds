from collections import deque


class MyStack:
    def __init__(self):
        self.q = deque()               # используем только append и popleft — как очередь

    def push(self, x: int) -> None:
        self.q.append(x)
        # прокручиваем очередь, чтобы новый элемент оказался в начале
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self) -> int:
        return self.q.popleft()

    def top(self) -> int:
        return self.q[0]

    def empty(self) -> bool:
        return not self.q
