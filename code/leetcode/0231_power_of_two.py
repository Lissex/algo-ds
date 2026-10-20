# Время O(1): одна битовая операция. Память O(1).
class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        # у степени двойки ровно один единичный бит: 8 = 1000, 7 = 0111, 8 & 7 = 0
        return n > 0 and n & (n - 1) == 0

    def isPowerOfTwoRec(self, n: int) -> bool:
        # Рекурсивный вариант: время O(log n), память O(log n) — стек.
        if n == 1:
            return True
        if n <= 0 or n % 2:
            return False
        return self.isPowerOfTwoRec(n // 2)
