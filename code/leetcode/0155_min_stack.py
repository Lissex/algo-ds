class MinStack:
    def __init__(self):
        self.stack = []
        self.mins = []                 # mins[i] — минимум среди stack[0..i]

    def push(self, val: int) -> None:
        self.stack.append(val)
        self.mins.append(val if not self.mins else min(val, self.mins[-1]))

    def pop(self) -> None:
        self.stack.pop()
        self.mins.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.mins[-1]           # O(1)
