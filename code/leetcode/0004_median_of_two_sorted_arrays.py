# Решение 1 (через merge): время O(m + n), память O(m + n).
# Решение 2 (бинарный поиск по разрезу): время O(log(min(m, n))), память O(1) — требуется по условию.
from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # Бинарный поиск по меньшему массиву: ищем такой разрез, чтобы
        # всё слева от разреза (в обоих массивах) было <= всего справа.
        a, b = nums1, nums2
        if len(a) > len(b):
            a, b = b, a
        m, n = len(a), len(b)
        half = (m + n + 1) // 2              # сколько элементов должно быть слева
        lo, hi = 0, m
        while lo <= hi:
            i = (lo + hi) // 2               # берём i элементов из a
            j = half - i                     # и j элементов из b
            a_left = a[i - 1] if i > 0 else float("-inf")
            a_right = a[i] if i < m else float("inf")
            b_left = b[j - 1] if j > 0 else float("-inf")
            b_right = b[j] if j < n else float("inf")
            if a_left <= b_right and b_left <= a_right:     # разрез правильный
                if (m + n) % 2:
                    return float(max(a_left, b_left))
                return (max(a_left, b_left) + min(a_right, b_right)) / 2
            if a_left > b_right:
                hi = i - 1                   # из a взяли слишком много
            else:
                lo = i + 1                   # из a взяли слишком мало

    def findMedianMerge(self, nums1: List[int], nums2: List[int]) -> float:
        # Простое решение: слить массивы (как merge из вопроса 7) и взять середину.
        merged, i, j = [], 0, 0
        while i < len(nums1) and j < len(nums2):
            if nums1[i] <= nums2[j]:
                merged.append(nums1[i]); i += 1
            else:
                merged.append(nums2[j]); j += 1
        merged += nums1[i:] + nums2[j:]
        k = len(merged)
        if k % 2:
            return float(merged[k // 2])
        return (merged[k // 2 - 1] + merged[k // 2]) / 2
