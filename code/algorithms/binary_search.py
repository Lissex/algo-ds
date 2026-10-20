def binary_search(arr, target):
    """Бинарный поиск в ОТСОРТИРОВАННОМ массиве. Возвращает индекс или -1.
    Каждый шаг смотрим на середину и отбрасываем половину, где target быть не может.
    Время O(log n): отрезок уменьшается вдвое. Память O(1)."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1                     # target правее середины
        else:
            hi = mid - 1                     # target левее середины
    return -1


# ---------- Другой вариант: рекурсивный ----------

def binary_search_rec(arr, target, lo=0, hi=None):
    """Рекурсивная версия. Время O(log n), память O(log n) — стек вызовов."""
    if hi is None:
        hi = len(arr) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if arr[mid] == target:
        return mid
    if arr[mid] < target:
        return binary_search_rec(arr, target, mid + 1, hi)
    return binary_search_rec(arr, target, lo, mid - 1)
