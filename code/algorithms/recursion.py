def factorial(n):
    """n! = 1 · 2 · ... · n рекурсивно.
    Базовый случай: 0! = 1. Шаг: n! = n · (n-1)!
    Время O(n): n вызовов. Память O(n): глубина стека вызовов."""
    if n < 0:
        raise ValueError("факториал определён для n >= 0")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fib(n):
    """n-е число Фибоначчи — наивная рекурсия: F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2).
    Время O(2ⁿ): каждый вызов порождает два, одни и те же значения считаются много раз.
    Память O(n): глубина рекурсии."""
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


def fib_memo(n, memo=None):
    """Фибоначчи с мемоизацией: запоминаем уже посчитанные значения.
    Время O(n): каждое F(k) считается один раз. Память O(n): словарь + стек."""
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


# ---------- Другой вариант: без рекурсии ----------

def factorial_iter(n):
    """Факториал циклом. Время O(n), память O(1)."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fib_iter(n):
    """Фибоначчи циклом: храним только два последних числа. Время O(n), память O(1)."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
