# Время O(log₁₀ x): количество цифр. Память O(1): разворачиваем половину числа, без строки.
class Solution:
    def isPalindrome(self, x: int) -> bool:
        # отрицательные и числа, оканчивающиеся на 0 (кроме самого 0), — не палиндромы
        if x < 0 or (x % 10 == 0 and x != 0):
            return False
        rev = 0
        while x > rev:                       # разворачиваем только правую половину цифр
            rev = rev * 10 + x % 10
            x //= 10
        return x == rev or x == rev // 10    # для нечётной длины средняя цифра в rev лишняя

    def isPalindromeStr(self, x: int) -> bool:
        # Вариант через строку и два указателя: время O(d), память O(d).
        s = str(x)
        left, right = 0, len(s) - 1
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True
