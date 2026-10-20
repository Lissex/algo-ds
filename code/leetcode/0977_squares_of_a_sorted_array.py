# Время O(n): два указателя с концов. Память O(n): массив-ответ.
from typing import List


class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [0] * n
        left, right = 0, n - 1
        for k in range(n - 1, -1, -1):       # заполняем ответ с конца — самыми большими
            if abs(nums[left]) > abs(nums[right]):
                res[k] = nums[left] ** 2
                left += 1
            else:
                res[k] = nums[right] ** 2
                right -= 1
        return res
