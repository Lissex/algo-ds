# Время O(n): сумма за один проход. Память O(1).
from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        expected = n * (n + 1) // 2          # сумма 0 + 1 + ... + n по формуле Гаусса
        return expected - sum(nums)          # разница — пропущенное число

    def missingNumberXor(self, nums: List[int]) -> int:
        # Вариант через XOR: x ^ x = 0, поэтому все пары сокращаются.
        res = len(nums)
        for i, v in enumerate(nums):
            res ^= i ^ v
        return res
