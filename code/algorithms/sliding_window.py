def longest_unique_substring(s):
    """Самая длинная подстрока без повторяющихся символов (возвращает саму подстроку).
    Окно [left, right]: расширяем вправо, а при повторе сдвигаем left за прошлое вхождение.
    Время O(n): right проходит строку один раз, left только двигается вперёд.
    Память O(k): словарь последних позиций, k — число различных символов."""
    last = {}                                # символ -> последний индекс
    left = 0
    best_start, best_len = 0, 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:  # повтор внутри окна
            left = last[ch] + 1
        last[ch] = right
        if right - left + 1 > best_len:
            best_start, best_len = left, right - left + 1
    return s[best_start:best_start + best_len]


# ---------- Другой вариант: окно через множество ----------

def longest_unique_substring_set(s):
    """То же через set: при повторе выкидываем символы слева по одному."""
    window = set()
    left = 0
    best = ""
    for right, ch in enumerate(s):
        while ch in window:
            window.remove(s[left])
            left += 1
        window.add(ch)
        if right - left + 1 > len(best):
            best = s[left:right + 1]
    return best
