def merge_sort(arr):
    """Сортировка слиянием (сортирует переданный список, устойчивая).
    Разделяй и властвуй: делим пополам, сортируем половины рекурсивно, сливаем.
    Время O(n log n) всегда: log n уровней деления, на каждом — слияние за O(n).
    Память O(n): копии половин + O(log n) на стек рекурсии."""
    if len(arr) <= 1:                        # базовый случай: 0 или 1 элемент уже отсортированы
        return
    mid = len(arr) // 2
    left = arr[:mid]                         # копии половин
    right = arr[mid:]
    merge_sort(left)
    merge_sort(right)
    # сливаем отсортированные половины обратно в arr
    i = j = k = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1


# ---------- Другой вариант: возвращает новый список ----------

def merge_sort_new(arr):
    """Та же сортировка слиянием, но возвращает НОВЫЙ список (исходный не меняется)."""
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort_new(arr[:mid])
    right = merge_sort_new(arr[mid:])
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]
