# Время O(n): указатели сходятся, каждый шаг сдвигает один из них. Память O(1).
from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        best = 0
        while left < right:
            h = min(height[left], height[right])        # уровень воды задаёт меньшая стенка
            best = max(best, h * (right - left))
            # двигаем меньшую стенку: с ней площадь больше уже не станет
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return best
