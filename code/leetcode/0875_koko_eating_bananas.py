# Время O(n · log(max(piles))): бинарный поиск по скорости, на каждом шаге — проход по кучкам.
# Память O(1).
from typing import List


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        def hours(k):
            # (p + k - 1) // k — деление с округлением вверх
            return sum((p + k - 1) // k for p in piles)

        lo, hi = 1, max(piles)               # скорость точно в этих пределах
        while lo < hi:
            mid = (lo + hi) // 2
            if hours(mid) <= h:
                hi = mid                     # успевает — пробуем медленнее
            else:
                lo = mid + 1                 # не успевает — нужно быстрее
        return lo
