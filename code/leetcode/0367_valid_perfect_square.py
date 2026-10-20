# Время O(log n): бинарный поиск. Память O(1). Встроенный sqrt по условию нельзя.
class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        lo, hi = 1, num
        while lo <= hi:
            mid = (lo + hi) // 2
            sq = mid * mid
            if sq == num:
                return True
            if sq < num:
                lo = mid + 1
            else:
                hi = mid - 1
        return False
