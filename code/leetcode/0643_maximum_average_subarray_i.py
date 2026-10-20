# Время O(n): окно сдвигается на 1, сумма пересчитывается за O(1). Память O(1).
from typing import List


class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        window = sum(nums[:k])               # сумма первого окна
        best = window
        for i in range(k, len(nums)):
            window += nums[i] - nums[i - k]  # добавили новый справа, убрали старый слева
            best = max(best, window)
        return best / k
