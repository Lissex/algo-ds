# Решение циклом: время O(n), память O(1).
# Наивная рекурсия была бы O(2ⁿ), с мемоизацией — O(n) времени и O(n) памяти.
class Solution:
    def fib(self, n: int) -> int:
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    def fibMemo(self, n: int, memo=None) -> int:
        if memo is None:
            memo = {}
        if n <= 1:
            return n
        if n not in memo:
            memo[n] = self.fibMemo(n - 1, memo) + self.fibMemo(n - 2, memo)
        return memo[n]
