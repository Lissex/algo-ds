# Время O(log x): бинарный поиск по ответу. Память O(1).
class Solution:
    def mySqrt(self, x: int) -> int:
        lo, hi = 0, x
        ans = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            if mid * mid <= x:
                ans = mid                    # mid подходит — пробуем больше
                lo = mid + 1
            else:
                hi = mid - 1
        return ans
