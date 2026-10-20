# Время O(len(t)): указатель по t проходит строку один раз. Память O(1).
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        i = 0                                # указатель по s — что ищем
        for ch in t:                         # указатель по t — где ищем
            if i < len(s) and s[i] == ch:
                i += 1
        return i == len(s)                   # нашли все символы s по порядку
