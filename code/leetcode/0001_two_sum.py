# Время O(n): один проход, проверка in в словаре — O(1) в среднем.
# Память O(n): словарь хранит до n чисел.

from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}                      # число -> его индекс
        for i, num in enumerate(nums):
            need = target - num        # какое число нужно в пару
            if need in seen:           # проверка в хэш-таблице — O(1)
                return [seen[need], i]
            seen[num] = i
        return []
