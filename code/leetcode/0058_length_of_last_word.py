# Время O(n) в худшем (идём с конца строки). Память O(1).
class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        i = len(s) - 1
        while i >= 0 and s[i] == " ":        # пропускаем пробелы в конце
            i -= 1
        length = 0
        while i >= 0 and s[i] != " ":        # считаем буквы последнего слова
            length += 1
            i -= 1
        return length
