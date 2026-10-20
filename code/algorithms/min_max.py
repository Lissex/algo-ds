def find_min_max(arr):
    """Минимум и максимум неотсортированного списка за один проход.
    Возвращает кортеж (min, max). Пустой список — ValueError.
    Время O(n): смотрим каждый элемент один раз (сортировка была бы O(n log n)).
    Память O(1): две переменные."""
    if not arr:
        raise ValueError("пустой список")
    lo = hi = arr[0]
    for x in arr[1:]:
        if x < lo:
            lo = x
        elif x > hi:
            hi = x
    return lo, hi
