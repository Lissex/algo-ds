# Время O(n): каждый символ входит в окно и выходит из него один раз.
# Память O(min(n, k)): словарь последних индексов, k — размер алфавита.

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last = {}                      # символ -> последний индекс, где он встречался
        left = 0                       # левая граница окна
        best = 0
        for right, ch in enumerate(s):
            if ch in last and last[ch] >= left:
                left = last[ch] + 1    # повтор внутри окна — сдвигаем левую границу за него
            last[ch] = right
            best = max(best, right - left + 1)
        return best
