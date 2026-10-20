def is_palindrome(s):
    """Палиндром методом двух указателей.
    left идёт с начала, right — с конца; сравниваем и сдвигаем навстречу.
    Время O(n): каждый символ сравниваем не больше одного раза.
    Память O(1): два индекса, строку не копируем."""
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


# ---------- Другой вариант: игнорируем регистр, пробелы и знаки ----------

def is_palindrome_phrase(s):
    """«А роза упала на лапу Азора» → True. Пропускаем всё, кроме букв и цифр."""
    left, right = 0, len(s) - 1
    while left < right:
        if not s[left].isalnum():
            left += 1
        elif not s[right].isalnum():
            right -= 1
        elif s[left].lower() != s[right].lower():
            return False
        else:
            left += 1
            right -= 1
    return True
