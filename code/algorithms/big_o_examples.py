# Примеры алгоритмов для каждого класса сложности.

def constant(arr):            # O(1) — не зависит от размера
    return arr[0]


def logarithmic(n):           # O(log n) — делим задачу пополам
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps


def linear(arr):              # O(n) — один проход
    total = 0
    for x in arr:
        total += x
    return total


def n_log_n(arr):             # O(n log n) — сортировка слиянием, sorted()
    return sorted(arr)


def quadratic(arr):           # O(n²) — вложенные циклы по всем парам
    pairs = 0
    for i in range(len(arr)):
        for j in range(len(arr)):
            pairs += 1
    return pairs


def exponential(n):           # O(2ⁿ) — наивный Фибоначчи
    if n <= 1:
        return n
    return exponential(n - 1) + exponential(n - 2)


def factorial_time(items):    # O(n!) — перебор всех перестановок
    if len(items) <= 1:
        return [items[:]]
    result = []
    for i in range(len(items)):
        rest = items[:i] + items[i + 1:]
        for p in factorial_time(rest):
            result.append([items[i]] + p)
    return result
