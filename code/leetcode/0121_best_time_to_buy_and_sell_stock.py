# Время O(n): один проход. Память O(1): минимальная цена и лучший результат.
from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = float("inf")             # самая дешёвая цена ДО текущего дня
        best = 0
        for p in prices:
            if p < min_price:
                min_price = p
            elif p - min_price > best:
                best = p - min_price         # продаём сегодня, купив по минимуму
        return best
