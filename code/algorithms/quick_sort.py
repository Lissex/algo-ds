import random


def quick_sort_simple(arr):
    """Быстрая сортировка — простой вариант (а): с новыми списками.
    Выбираем опорный элемент (pivot), раскладываем элементы на три списка:
    меньше pivot, равные, больше — и рекурсивно сортируем крайние.
    Возвращает НОВЫЙ отсортированный список.
    Время: O(n log n) в среднем, O(n²) в худшем (pivot каждый раз минимум/максимум).
    Память O(n): на каждом уровне рекурсии создаются новые списки."""
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[len(arr) // 2]               # средний элемент — защита от худшего случая на отсортированных данных
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_simple(left) + mid + quick_sort_simple(right)


def partition(arr, lo, hi):
    """Разбиение Ломуто: опорный — последний элемент отрезка [lo, hi].
    Всё, что меньше pivot, переносим влево; в конце ставим pivot между частями.
    Возвращает итоговый индекс pivot. Время O(hi - lo), память O(1)."""
    pivot = arr[hi]
    i = lo                                   # граница «меньших» элементов
    for j in range(lo, hi):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]        # pivot встаёт на своё место
    return i


def quick_sort(arr, lo=0, hi=None):
    """Быстрая сортировка — вариант (б): на месте, с разбиением.
    Сортирует переданный список.
    Время: O(n log n) в среднем, O(n²) в худшем.
    Память O(log n) в среднем — только стек рекурсии (новых списков нет)."""
    if hi is None:
        hi = len(arr) - 1
    if lo >= hi:
        return
    r = random.randint(lo, hi)               # случайный pivot — худший случай почти невозможен
    arr[r], arr[hi] = arr[hi], arr[r]
    p = partition(arr, lo, hi)
    quick_sort(arr, lo, p - 1)
    quick_sort(arr, p + 1, hi)
