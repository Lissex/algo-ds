"""Тренажёр раздела 1: заготовки, демо и тесты."""

COMMON1 = r'''
import re as _re, io as _io, tokenize as _tok

def _code_only(src):
    """Исходник без комментариев и строк — чтобы искать запрещённые вызовы."""
    out = []
    try:
        for t in _tok.generate_tokens(_io.StringIO(src).readline):
            if t.type not in (_tok.COMMENT, _tok.STRING):
                out.append(t.string)
    except Exception:
        return src
    return " ".join(out)

def forbid(*patterns):
    code = _code_only(SOURCE)
    for p, name in patterns:
        if _re.search(p, code):
            raise AssertionError(f"в решении используется {name} — здесь нужно написать алгоритм самому")

NO_SORT = [(r"\bsorted\s*\(", "sorted()"), (r"\.\s*sort\s*\(", ".sort()")]

class Item:
    """Элемент с ключом и меткой — для проверки устойчивости сортировки."""
    def __init__(self, k, tag): self.k, self.tag = k, tag
    def __lt__(self, o): return self.k < o.k
    def __gt__(self, o): return self.k > o.k
    def __le__(self, o): return self.k <= o.k
    def __ge__(self, o): return self.k >= o.k
    def __eq__(self, o): return self.k == o.k
    def __repr__(self): return f"{self.k}{self.tag}"

SORT_CASES = [[], [1], [2, 1], [1, 2], [3, 3, 3], [5, 4, 3, 2, 1], [0, -1, 5, -10, 3, 3]] + \
    [[_r.randint(-50, 50) for _ in range(_r.randint(0, 40))] for _ in range(150)]

def check_inplace_sort(fn):
    for c in SORT_CASES:
        a = c[:]
        fn(a)
        eq(a, sorted(c), f"список после сортировки {c}")

def check_stable(fn):
    for _ in range(60):
        items = [Item(_r.randint(0, 4), chr(97 + i % 26)) for i in range(_r.randint(2, 20))]
        a = items[:]
        fn(a)
        exp = sorted(items, key=lambda x: x.k)
        if [x.tag for x in a] != [x.tag for x in exp]:
            raise AssertionError(f"сортировка неустойчива: равные элементы поменяли порядок ({a} вместо {exp})")
'''

S1 = {}

S1["selection-sort"] = dict(file="algorithms/selection_sort.py",
starter='''def selection_sort(arr):
    """Сортировка выбором: на каждом шаге ищем минимум в неотсортированной части
    и ставим его в начало этой части. Сортирует переданный список на месте."""
    # TODO: твой код
    pass
''', demo='a = [5, 3, 8, 1, 9, 2]\nselection_sort(a)\nprint(a)   # ожидается [1, 2, 3, 5, 8, 9]',
tests=r'''
@test("не используются встроенные сортировки")
def _(): forbid(*NO_SORT)
@test("простые случаи: пусто, 1 элемент, 2 элемента")
def _():
    for c in [[], [1], [2, 1]]:
        a = c[:]; selection_sort(a); eq(a, sorted(c), f"список {c}")
@test("обратный порядок и дубликаты")
def _():
    a = [5, 4, 4, 3, 1, 1]; selection_sort(a); eq(a, [1, 1, 3, 4, 4, 5])
@test("150 случайных массивов")
def _(): check_inplace_sort(selection_sort)
''')

S1["insertion-sort"] = dict(file="algorithms/insertion_sort.py",
starter='''def insertion_sort(arr):
    """Сортировка вставками: каждый элемент сдвигаем влево, пока слева стоят большие.
    Сортирует переданный список на месте. Должна быть устойчивой."""
    # TODO: твой код
    pass
''', demo='a = [5, 2, 4, 6, 1, 3]\ninsertion_sort(a)\nprint(a)   # ожидается [1, 2, 3, 4, 5, 6]',
tests=r'''
@test("не используются встроенные сортировки")
def _(): forbid(*NO_SORT)
@test("простые случаи: пусто, 1 элемент, 2 элемента")
def _():
    for c in [[], [1], [2, 1]]:
        a = c[:]; insertion_sort(a); eq(a, sorted(c), f"список {c}")
@test("обратный порядок и дубликаты")
def _():
    a = [5, 4, 4, 3, 1, 1]; insertion_sort(a); eq(a, [1, 1, 3, 4, 4, 5])
@test("150 случайных массивов")
def _(): check_inplace_sort(insertion_sort)
@test("устойчивость: равные элементы сохраняют порядок (сравнивай строго >)")
def _(): check_stable(insertion_sort)
''')

S1["bubble-sort"] = dict(file="algorithms/bubble_sort.py",
starter='''def bubble_sort(arr):
    """Сортировка пузырьком: меняем соседей, если левый больше правого.
    Сортирует переданный список на месте."""
    # TODO: твой код
    pass
''', demo='a = [4, 3, 1, 5, 2]\nbubble_sort(a)\nprint(a)   # ожидается [1, 2, 3, 4, 5]',
tests=r'''
@test("не используются встроенные сортировки")
def _(): forbid(*NO_SORT)
@test("простые случаи: пусто, 1 элемент, 2 элемента")
def _():
    for c in [[], [1], [2, 1]]:
        a = c[:]; bubble_sort(a); eq(a, sorted(c), f"список {c}")
@test("обратный порядок и дубликаты")
def _():
    a = [5, 4, 4, 3, 1, 1]; bubble_sort(a); eq(a, [1, 1, 3, 4, 4, 5])
@test("150 случайных массивов")
def _(): check_inplace_sort(bubble_sort)
@test("устойчивость: меняй соседей только при строгом >")
def _(): check_stable(bubble_sort)
''')

S1["merge"] = dict(file="algorithms/merge.py",
starter='''def merge(a, b):
    """Слить два отсортированных списка в новый отсортированный.
    Используй два указателя i и j."""
    # TODO: твой код
    pass
''', demo='print(merge([1, 4, 7], [2, 3, 8]))   # ожидается [1, 2, 3, 4, 7, 8]',
tests=r'''
@test("не используются встроенные сортировки")
def _(): forbid(*NO_SORT)
@test("пример [1,4,7] + [2,3,8]")
def _(): eq(merge([1, 4, 7], [2, 3, 8]), [1, 2, 3, 4, 7, 8])
@test("один или оба пустые")
def _():
    eq(merge([], []), [], "merge([], [])"); eq(merge([1, 2], []), [1, 2], "merge([1,2], [])"); eq(merge([], [3]), [3], "merge([], [3])")
@test("разной длины и с повторами")
def _(): eq(merge([1, 1, 5], [1, 2, 2, 2, 9, 10]), [1, 1, 1, 2, 2, 2, 5, 9, 10])
@test("исходные списки не меняются")
def _():
    a, b = [1, 3], [2, 4]; merge(a, b); eq((a, b), ([1, 3], [2, 4]), "a и b после merge")
@test("200 случайных пар")
def _():
    for _ in range(200):
        a = sorted(_r.randint(0, 30) for _ in range(_r.randint(0, 10)))
        b = sorted(_r.randint(0, 30) for _ in range(_r.randint(0, 10)))
        eq(merge(a, b), sorted(a + b), f"merge({a}, {b})")
''')

S1["merge-sort"] = dict(file="algorithms/merge_sort.py",
starter='''def merge_sort(arr):
    """Сортировка слиянием: делим пополам, сортируем половины рекурсивно,
    сливаем обратно в arr. Сортирует переданный список."""
    # TODO: твой код
    pass
''', demo='a = [38, 27, 43, 3, 9, 82, 10]\nmerge_sort(a)\nprint(a)   # ожидается [3, 9, 10, 27, 38, 43, 82]',
tests=r'''
@test("не используются встроенные сортировки")
def _(): forbid(*NO_SORT)
@test("простые случаи: пусто, 1 элемент, 2 элемента")
def _():
    for c in [[], [1], [2, 1]]:
        a = c[:]; merge_sort(a); eq(a, sorted(c), f"список {c}")
@test("нечётная длина и дубликаты")
def _():
    a = [5, 1, 4, 1, 5, 9, 2]; merge_sort(a); eq(a, [1, 1, 2, 4, 5, 5, 9])
@test("150 случайных массивов")
def _(): check_inplace_sort(merge_sort)
@test("устойчивость: при равенстве бери из левой половины (<=)")
def _(): check_stable(merge_sort)
@test("большой массив (2000 элементов)")
def _():
    c = [_r.randint(0, 10**6) for _ in range(2000)]; a = c[:]; merge_sort(a); eq(a, sorted(c), "большой массив")
''')

S1["quick-sort-simple"] = dict(file="algorithms/quick_sort.py", only="quick_sort_simple",
starter='''def quick_sort_simple(arr):
    """Быстрая сортировка с новыми списками: pivot, затем left (< pivot),
    mid (== pivot), right (> pivot) и рекурсия. Возвращает НОВЫЙ список."""
    # TODO: твой код
    pass
''', demo='a = [3, 6, 1, 8, 2, 9, 2]\nprint(quick_sort_simple(a))   # ожидается [1, 2, 2, 3, 6, 8, 9]\nprint(a)                      # исходный не изменился',
tests=r'''
@test("не используются встроенные сортировки")
def _(): forbid(*NO_SORT)
@test("возвращает отсортированный список")
def _(): eq(quick_sort_simple([3, 6, 1, 8, 2, 9, 2]), [1, 2, 2, 3, 6, 8, 9])
@test("пусто и один элемент")
def _(): eq(quick_sort_simple([]), [], "[]"); eq(quick_sort_simple([7]), [7], "[7]")
@test("все элементы равны (нужен mid, иначе бесконечная рекурсия)")
def _(): eq(quick_sort_simple([5] * 50), [5] * 50)
@test("исходный список не меняется")
def _():
    a = [3, 1, 2]; quick_sort_simple(a); eq(a, [3, 1, 2], "исходный список")
@test("150 случайных массивов")
def _():
    for c in SORT_CASES: eq(quick_sort_simple(c[:]), sorted(c), f"quick_sort_simple({c})")
''')

S1["quick-sort-inplace"] = dict(file="algorithms/quick_sort.py", only="partition,quick_sort", header="import random\n\n\n",
starter='''import random


def partition(arr, lo, hi):
    """Разбиение Ломуто: pivot = arr[hi]. Все элементы меньше pivot переносим влево,
    затем ставим pivot на его место. Вернуть итоговый индекс pivot."""
    # TODO: твой код
    pass


def quick_sort(arr, lo=0, hi=None):
    """Быстрая сортировка на месте. Сортирует переданный список, новые списки не создаёт."""
    if hi is None:
        hi = len(arr) - 1
    # TODO: твой код
    pass
''', demo='a = [3, 6, 1, 8, 2, 9, 2]\nquick_sort(a)\nprint(a)   # ожидается [1, 2, 2, 3, 6, 8, 9]',
tests=r'''
@test("не используются встроенные сортировки")
def _(): forbid(*NO_SORT)
@test("partition ставит pivot на место и возвращает его индекс")
def _():
    for _ in range(100):
        a = [_r.randint(0, 20) for _ in range(_r.randint(1, 12))]
        b = a[:]; p = partition(b, 0, len(b) - 1)
        if not isinstance(p, int): raise AssertionError(f"partition должен вернуть индекс, получено {p!r}")
        if sorted(b) != sorted(a): raise AssertionError(f"partition потерял или добавил элементы: {a} → {b}")
        if any(x > b[p] for x in b[:p]) or any(x < b[p] for x in b[p + 1:]):
            raise AssertionError(f"после partition({a}) слева от pivot есть большие или справа меньшие: {b}, pivot на {p}")
@test("простые случаи")
def _():
    for c in [[], [1], [2, 1], [3, 3, 3]]:
        a = c[:]; quick_sort(a); eq(a, sorted(c), f"список {c}")
@test("150 случайных массивов")
def _(): check_inplace_sort(quick_sort)
@test("уже отсортированный массив из 2000 элементов (нужен случайный pivot)")
def _():
    a = list(range(2000))
    try:
        quick_sort(a)
    except RecursionError:
        raise AssertionError("RecursionError: на отсортированном массиве pivot = последний даёт глубину рекурсии n. Перед partition поменяй arr[hi] со случайным элементом")
    eq(a, list(range(2000)), "результат")
''')

S1["factorial"] = dict(file="algorithms/recursion.py", only="factorial",
starter='''def factorial(n):
    """n! рекурсивно. Для отрицательных n — ValueError."""
    # TODO: твой код
    pass
''', demo='print(factorial(5))   # ожидается 120\nprint(factorial(0))   # ожидается 1',
tests=r'''
@test("0! = 1 и 1! = 1")
def _(): eq(factorial(0), 1, "factorial(0)"); eq(factorial(1), 1, "factorial(1)")
@test("5! = 120, 10! = 3628800")
def _(): eq(factorial(5), 120, "factorial(5)"); eq(factorial(10), 3628800, "factorial(10)")
@test("значения от 0 до 20")
def _():
    r = 1
    for n in range(21):
        if n: r *= n
        eq(factorial(n), r, f"factorial({n})")
@test("отрицательное n → ValueError")
def _(): raises(ValueError, lambda: factorial(-3), "factorial(-3)")
@test("решение рекурсивное (функция вызывает сама себя)")
def _():
    calls = [0]; orig = __user_ns__["factorial"]
    def wrapped(n):
        calls[0] += 1
        return orig(n)
    __user_ns__["factorial"] = wrapped
    try: wrapped(6)
    finally: __user_ns__["factorial"] = orig
    if calls[0] < 2: raise AssertionError("factorial не вызывает сам себя — в этом задании нужна рекурсия")
''')

S1["fibonacci"] = dict(file="algorithms/recursion.py", only="fib_memo", rename=("fib_memo", "fib"),
starter='''def fib(n, memo=None):
    """n-е число Фибоначчи: F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2).
    fib(90) должно считаться мгновенно — нужна мемоизация (или цикл)."""
    # TODO: твой код
    pass
''', demo='print([fib(i) for i in range(10)])   # ожидается [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]\nprint(fib(90))                       # ожидается 2880067194370816120',
tests=r'''
@test("fib(0) = 0, fib(1) = 1")
def _(): eq(fib(0), 0, "fib(0)"); eq(fib(1), 1, "fib(1)")
@test("первые 20 чисел")
def _():
    a, b = 0, 1
    for n in range(20):
        eq(fib(n), a, f"fib({n})"); a, b = b, a + b
_fast = {"ok": False}
@test("число вызовов линейное (мемоизация работает)")
def _():
    calls = [0]; orig = __user_ns__["fib"]
    def wrapped(*args, **kw):
        calls[0] += 1
        return orig(*args, **kw)
    __user_ns__["fib"] = wrapped
    try: wrapped(25)
    finally: __user_ns__["fib"] = orig
    if calls[0] > 200:
        raise AssertionError(f"fib(25) сделал {calls[0]} вызовов — это экспоненциальная рекурсия O(2ⁿ). Запоминай посчитанные значения в словаре memo")
    _fast["ok"] = True
@test("fib(90) мгновенно")
def _():
    if not _fast["ok"]:
        raise AssertionError("пропущен: без мемоизации fib(90) считался бы тысячи лет")
    eq(fib(90), 2880067194370816120, "fib(90)")
''')

S1["palindrome"] = dict(file="algorithms/two_pointers.py", only="is_palindrome",
starter='''def is_palindrome(s):
    """Палиндром методом двух указателей: left с начала, right с конца."""
    # TODO: твой код
    pass
''', demo='print(is_palindrome("шалаш"))   # ожидается True\nprint(is_palindrome("abca"))    # ожидается False',
tests=r'''
@test("без разворота строки s[::-1] и reversed")
def _(): forbid((r"\[\s*:\s*:\s*-\s*1\s*\]", "s[::-1]"), (r"\breversed\s*\(", "reversed()"))
@test("палиндромы чётной и нечётной длины")
def _():
    for s in ["abba", "abcba", "шалаш", "aa"]: eq(is_palindrome(s), True, repr(s))
@test("не палиндромы")
def _():
    for s in ["ab", "abca", "abcab"]: eq(is_palindrome(s), False, repr(s))
@test("пустая строка и один символ — палиндромы")
def _(): eq(is_palindrome(""), True, "''"); eq(is_palindrome("x"), True, "'x'")
@test("случайные строки")
def _():
    for _ in range(300):
        s = "".join(_r.choice("ab") for _ in range(_r.randint(0, 8)))
        eq(is_palindrome(s), s == s[::-1], repr(s))
''')

S1["sliding-window"] = dict(file="algorithms/sliding_window.py", only="longest_unique_substring",
starter='''def longest_unique_substring(s):
    """Вернуть самую длинную подстроку без повторяющихся символов.
    Окно [left, right] + словарь последних позиций символов."""
    # TODO: твой код
    pass
''', demo='print(longest_unique_substring("abcabcbb"))   # ожидается "abc"\nprint(longest_unique_substring("pwwkew"))     # ожидается "wke"',
tests=r'''
def brute(s):
    best = ""
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            if len(set(s[i:j])) == j - i and j - i > len(best): best = s[i:j]
    return best
def ok(s):
    r = longest_unique_substring(s)
    if not isinstance(r, str): raise AssertionError(f"нужно вернуть строку, получено {r!r}")
    if r not in s: raise AssertionError(f"{r!r} — не подстрока {s!r}")
    if len(set(r)) != len(r): raise AssertionError(f"в {r!r} есть повторы")
    eq(len(r), len(brute(s)), f"длина ответа для {s!r}")
@test('"abcabcbb" → "abc"')
def _(): ok("abcabcbb")
@test('"bbbbb" → "b"')
def _(): ok("bbbbb")
@test('"pwwkew" → длина 3')
def _(): ok("pwwkew")
@test("пустая строка → \"\"")
def _(): eq(longest_unique_substring(""), "", "''")
@test('"abba" — старый повтор левее окна не мешает')
def _(): ok("abba")
@test("300 случайных строк")
def _():
    for _ in range(300): ok("".join(_r.choice("abcd") for _ in range(_r.randint(1, 14))))
''')

S1["binary-search"] = dict(file="algorithms/binary_search.py", only="binary_search",
starter='''def binary_search(arr, target):
    """Бинарный поиск в отсортированном arr. Вернуть индекс target или -1."""
    # TODO: твой код
    pass
''', demo='a = [1, 3, 5, 7, 9, 11]\nprint(binary_search(a, 7))   # ожидается 3\nprint(binary_search(a, 4))   # ожидается -1',
tests=r'''
@test("без in, index и bisect")
def _(): forbid((r"\.\s*index\s*\(", ".index()"), (r"\bbisect\b", "bisect"), (r"\bin\s+arr\b", "in arr"))
@test("находит каждый элемент")
def _():
    a = [1, 3, 5, 7, 9, 11]
    for i, x in enumerate(a): eq(binary_search(a, x), i, f"binary_search(a, {x})")
@test("нет элемента → -1 (меньше всех, больше всех, между)")
def _():
    a = [1, 3, 5]
    for t in [0, 2, 4, 6]: eq(binary_search(a, t), -1, f"binary_search({a}, {t})")
@test("пустой массив и один элемент")
def _(): eq(binary_search([], 1), -1, "[]"); eq(binary_search([4], 4), 0, "[4], 4"); eq(binary_search([4], 5), -1, "[4], 5")
@test("300 случайных массивов")
def _():
    for _ in range(300):
        a = sorted(set(_r.randint(0, 60) for _ in range(_r.randint(0, 25)))); t = _r.randint(-1, 61)
        eq(binary_search(a, t), a.index(t) if t in a else -1, f"binary_search({a}, {t})")
@test("скорость: массив из 10⁶ элементов, 2000 поисков")
def _():
    a = list(range(0, 2_000_000, 2))
    for _ in range(2000):
        t = _r.randint(0, 2_000_000); eq(binary_search(a, t), t // 2 if t % 2 == 0 else -1, f"t={t}")
''')

S1["array-insert-delete"] = dict(file="algorithms/array_ops.py", only="insert,delete",
starter='''def insert(arr, i, x):
    """Вставить x на позицию i, сдвинув элементы правее вправо.
    Нельзя: arr.insert. Можно: arr.append(None), чтобы получить место."""
    # TODO: твой код
    pass


def delete(arr, i):
    """Удалить элемент с позиции i, сдвинув элементы правее влево, и вернуть его.
    Нельзя: arr.pop(i), del. Можно: arr.pop() — убрать последнюю ячейку."""
    # TODO: твой код
    pass
''', demo='a = [1, 2, 4, 5]\ninsert(a, 2, 3)\nprint(a)              # ожидается [1, 2, 3, 4, 5]\nprint(delete(a, 0))   # ожидается 1\nprint(a)              # ожидается [2, 3, 4, 5]',
tests=r'''
@test("без list.insert, pop(i) и del")
def _(): forbid((r"\.\s*insert\s*\(", "list.insert()"), (r"\.\s*pop\s*\(\s*[^)\s]", "pop(i)"), (r"\bdel\b", "del"))
@test("вставка в середину")
def _(): a = [1, 2, 4, 5]; insert(a, 2, 3); eq(a, [1, 2, 3, 4, 5])
@test("вставка в начало и в конец")
def _():
    a = [2, 3]; insert(a, 0, 1); eq(a, [1, 2, 3], "в начало"); insert(a, 3, 4); eq(a, [1, 2, 3, 4], "в конец")
@test("вставка в пустой")
def _(): a = []; insert(a, 0, 7); eq(a, [7])
@test("удаление возвращает значение и сдвигает")
def _(): a = [1, 2, 3, 4]; eq(delete(a, 1), 2, "delete(a, 1)"); eq(a, [1, 3, 4], "массив")
@test("удаление первого и последнего")
def _():
    a = [1, 2, 3]; eq(delete(a, 0), 1, "первый"); eq(a, [2, 3]); eq(delete(a, 1), 3, "последний"); eq(a, [2])
@test("случайные операции против list")
def _():
    a, ref = [], []
    for _ in range(500):
        if ref and _r.random() < .45:
            i = _r.randrange(len(ref)); eq(delete(a, i), ref.pop(i), f"delete({i})")
        else:
            i = _r.randint(0, len(ref)); v = _r.randint(0, 99); insert(a, i, v); ref.insert(i, v)
        eq(a, ref, "массив")
''')

S1["linear-search"] = dict(file="algorithms/linear_search.py",
starter='''def linear_search(arr, target):
    """Линейный поиск: индекс первого вхождения target или -1."""
    # TODO: твой код
    pass
''', demo='print(linear_search([4, 2, 7, 2], 2))   # ожидается 1\nprint(linear_search([4, 2, 7], 5))      # ожидается -1',
tests=r'''
@test("без in и index")
def _(): forbid((r"\.\s*index\s*\(", ".index()"), (r"\bif\s+target\s+in\b", "target in"))
@test("находит первое вхождение")
def _(): eq(linear_search([4, 2, 7, 2], 2), 1)
@test("нет элемента → -1")
def _(): eq(linear_search([4, 2, 7], 5), -1)
@test("пустой массив")
def _(): eq(linear_search([], 1), -1)
@test("первый и последний")
def _(): eq(linear_search([9, 1, 2], 9), 0, "первый"); eq(linear_search([9, 1, 2], 2), 2, "последний")
@test("работает со строками и неотсортированными данными")
def _(): eq(linear_search(["c", "a", "b"], "b"), 2)
@test("300 случайных массивов")
def _():
    for _ in range(300):
        a = [_r.randint(0, 9) for _ in range(_r.randint(0, 15))]; t = _r.randint(0, 10)
        eq(linear_search(a, t), a.index(t) if t in a else -1, f"linear_search({a}, {t})")
''')

S1["min-max"] = dict(file="algorithms/min_max.py",
starter='''def find_min_max(arr):
    """Вернуть (минимум, максимум) неотсортированного списка за один проход.
    Пустой список — ValueError."""
    # TODO: твой код
    pass
''', demo='print(find_min_max([3, -1, 8, 0, 8]))   # ожидается (-1, 8)',
tests=r'''
@test("без min(), max() и сортировки")
def _(): forbid((r"\bmin\s*\(", "min()"), (r"\bmax\s*\(", "max()"), *NO_SORT)
@test("обычный список")
def _(): eq(find_min_max([3, -1, 8, 0, 8]), (-1, 8))
@test("один элемент")
def _(): eq(find_min_max([5]), (5, 5))
@test("все отрицательные (нельзя начинать с 0)")
def _(): eq(find_min_max([-5, -2, -9]), (-9, -2))
@test("пустой список → ValueError")
def _(): raises(ValueError, lambda: find_min_max([]), "find_min_max([])")
@test("300 случайных списков")
def _():
    for _ in range(300):
        a = [_r.randint(-100, 100) for _ in range(_r.randint(1, 20))]
        eq(find_min_max(a), (min(a), max(a)), str(a))
''')

# ---------------- LeetCode раздела 1 ----------------
P1_STARTER = {
"lc-4": ('from typing import List\n\n\nclass Solution:\n    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:\n        # твой код\n        pass\n', 'print(Solution().findMedianSortedArrays([1, 3], [2]))      # ожидается 2.0\nprint(Solution().findMedianSortedArrays([1, 2], [3, 4]))   # ожидается 2.5'),
"lc-9": ('class Solution:\n    def isPalindrome(self, x: int) -> bool:\n        # твой код\n        pass\n', 'print(Solution().isPalindrome(121))    # ожидается True\nprint(Solution().isPalindrome(-121))   # ожидается False'),
"lc-11": ('from typing import List\n\n\nclass Solution:\n    def maxArea(self, height: List[int]) -> int:\n        # твой код\n        pass\n', 'print(Solution().maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]))   # ожидается 49'),
"lc-35": ('from typing import List\n\n\nclass Solution:\n    def searchInsert(self, nums: List[int], target: int) -> int:\n        # твой код\n        pass\n', 'print(Solution().searchInsert([1, 3, 5, 6], 2))   # ожидается 1'),
"lc-58": ('class Solution:\n    def lengthOfLastWord(self, s: str) -> int:\n        # твой код\n        pass\n', 'print(Solution().lengthOfLastWord("   fly me   to   the moon  "))   # ожидается 4'),
"lc-69": ('class Solution:\n    def mySqrt(self, x: int) -> int:\n        # твой код\n        pass\n', 'print(Solution().mySqrt(8))   # ожидается 2'),
"lc-74": ('from typing import List\n\n\nclass Solution:\n    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:\n        # твой код\n        pass\n', 'm = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]\nprint(Solution().searchMatrix(m, 3))    # ожидается True\nprint(Solution().searchMatrix(m, 13))   # ожидается False'),
"lc-121": ('from typing import List\n\n\nclass Solution:\n    def maxProfit(self, prices: List[int]) -> int:\n        # твой код\n        pass\n', 'print(Solution().maxProfit([7, 1, 5, 3, 6, 4]))   # ожидается 5'),
"lc-231": ('class Solution:\n    def isPowerOfTwo(self, n: int) -> bool:\n        # твой код\n        pass\n', 'print(Solution().isPowerOfTwo(16))   # ожидается True\nprint(Solution().isPowerOfTwo(3))    # ожидается False'),
"lc-268": ('from typing import List\n\n\nclass Solution:\n    def missingNumber(self, nums: List[int]) -> int:\n        # твой код\n        pass\n', 'print(Solution().missingNumber([3, 0, 1]))   # ожидается 2'),
"lc-367": ('class Solution:\n    def isPerfectSquare(self, num: int) -> bool:\n        # твой код\n        pass\n', 'print(Solution().isPerfectSquare(16))   # ожидается True'),
"lc-392": ('class Solution:\n    def isSubsequence(self, s: str, t: str) -> bool:\n        # твой код\n        pass\n', 'print(Solution().isSubsequence("abc", "ahbgdc"))   # ожидается True'),
"lc-509": ('class Solution:\n    def fib(self, n: int) -> int:\n        # твой код\n        pass\n', 'print(Solution().fib(10))   # ожидается 55'),
"lc-643": ('from typing import List\n\n\nclass Solution:\n    def findMaxAverage(self, nums: List[int], k: int) -> float:\n        # твой код\n        pass\n', 'print(Solution().findMaxAverage([1, 12, -5, -6, 50, 3], 4))   # ожидается 12.75'),
"lc-875": ('from typing import List\n\n\nclass Solution:\n    def minEatingSpeed(self, piles: List[int], h: int) -> int:\n        # твой код\n        pass\n', 'print(Solution().minEatingSpeed([3, 6, 7, 11], 8))   # ожидается 4'),
"lc-977": ('from typing import List\n\n\nclass Solution:\n    def sortedSquares(self, nums: List[int]) -> List[int]:\n        # твой код\n        pass\n', 'print(Solution().sortedSquares([-4, -1, 0, 3, 10]))   # ожидается [0, 1, 9, 16, 100]'),
"lc-1768": ('class Solution:\n    def mergeAlternately(self, word1: str, word2: str) -> str:\n        # твой код\n        pass\n', 'print(Solution().mergeAlternately("abc", "pqr"))   # ожидается apbqcr'),
"lc-2239": ('from typing import List\n\n\nclass Solution:\n    def findClosestNumber(self, nums: List[int]) -> int:\n        # твой код\n        pass\n', 'print(Solution().findClosestNumber([-4, -2, 1, 4, 8]))   # ожидается 1'),
}
P1_FILES = {
"lc-4": "leetcode/0004_median_of_two_sorted_arrays.py", "lc-9": "leetcode/0009_palindrome_number.py", "lc-11": "leetcode/0011_container_with_most_water.py",
"lc-35": "leetcode/0035_search_insert_position.py", "lc-58": "leetcode/0058_length_of_last_word.py", "lc-69": "leetcode/0069_sqrtx.py",
"lc-74": "leetcode/0074_search_a_2d_matrix.py", "lc-121": "leetcode/0121_best_time_to_buy_and_sell_stock.py", "lc-231": "leetcode/0231_power_of_two.py",
"lc-268": "leetcode/0268_missing_number.py", "lc-367": "leetcode/0367_valid_perfect_square.py", "lc-392": "leetcode/0392_is_subsequence.py",
"lc-509": "leetcode/0509_fibonacci_number.py", "lc-643": "leetcode/0643_maximum_average_subarray_i.py", "lc-875": "leetcode/0875_koko_eating_bananas.py",
"lc-977": "leetcode/0977_squares_of_a_sorted_array.py", "lc-1768": "leetcode/1768_merge_strings_alternately.py", "lc-2239": "leetcode/2239_find_closest_number_to_zero.py",
}
P1_TESTS = {
"lc-4": r'''
def med(a, b):
    m = sorted(a + b); k = len(m)
    return float(m[k // 2]) if k % 2 else (m[k // 2 - 1] + m[k // 2]) / 2
@test("[1,3] и [2] → 2.0")
def _(): eq(Solution().findMedianSortedArrays([1, 3], [2]), 2.0)
@test("[1,2] и [3,4] → 2.5")
def _(): eq(Solution().findMedianSortedArrays([1, 2], [3, 4]), 2.5)
@test("один массив пустой")
def _(): eq(Solution().findMedianSortedArrays([], [1]), 1.0, "[], [1]"); eq(Solution().findMedianSortedArrays([2, 3], []), 2.5, "[2,3], []")
@test("300 случайных пар")
def _():
    for _ in range(300):
        a = sorted(_r.randint(-50, 50) for _ in range(_r.randint(0, 9))); b = sorted(_r.randint(-50, 50) for _ in range(_r.randint(0 if a else 1, 9)))
        eq(Solution().findMedianSortedArrays(a, b), med(a, b), f"{a}, {b}")
''',
"lc-9": r'''
@test("121 → True")
def _(): eq(Solution().isPalindrome(121), True)
@test("-121 → False")
def _(): eq(Solution().isPalindrome(-121), False)
@test("10 → False, 0 → True")
def _(): eq(Solution().isPalindrome(10), False, "10"); eq(Solution().isPalindrome(0), True, "0")
@test("1000 случайных чисел")
def _():
    for _ in range(1000):
        x = _r.choice([_r.randint(-1000, 10**9), int(str(_r.randint(1, 99999)) + str(_r.randint(1, 99999))[::-1])])
        eq(Solution().isPalindrome(x), str(x) == str(x)[::-1], str(x))
''',
"lc-11": r'''
def brute(h): return max(min(h[i], h[j]) * (j - i) for i in range(len(h)) for j in range(i + 1, len(h)))
@test("пример → 49")
def _(): eq(Solution().maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]), 49)
@test("две линии")
def _(): eq(Solution().maxArea([1, 1]), 1)
@test("200 случайных массивов против перебора")
def _():
    for _ in range(200):
        h = [_r.randint(0, 30) for _ in range(_r.randint(2, 20))]; eq(Solution().maxArea(h), brute(h), str(h))
@test("скорость: 50 000 высот (нужно O(n))")
def _():
    h = [_r.randint(0, 10**4) for _ in range(50000)]; Solution().maxArea(h)
''',
"lc-35": r'''
import bisect as _b
@test("найден → его индекс")
def _(): eq(Solution().searchInsert([1, 3, 5, 6], 5), 2)
@test("не найден → позиция вставки")
def _(): eq(Solution().searchInsert([1, 3, 5, 6], 2), 1, "2"); eq(Solution().searchInsert([1, 3, 5, 6], 7), 4, "7"); eq(Solution().searchInsert([1, 3, 5, 6], 0), 0, "0")
@test("300 случайных")
def _():
    for _ in range(300):
        a = sorted(set(_r.randint(0, 50) for _ in range(_r.randint(1, 20)))); t = _r.randint(-1, 52)
        eq(Solution().searchInsert(a, t), _b.bisect_left(a, t), f"{a}, {t}")
''',
"lc-58": r'''
@test('"Hello World" → 5')
def _(): eq(Solution().lengthOfLastWord("Hello World"), 5)
@test("пробелы в конце")
def _(): eq(Solution().lengthOfLastWord("   fly me   to   the moon  "), 4)
@test("одно слово")
def _(): eq(Solution().lengthOfLastWord("a"), 1, "'a'"); eq(Solution().lengthOfLastWord("day "), 3, "'day '")
@test("случайные строки")
def _():
    for _ in range(300):
        s = " " * _r.randint(0, 2) + " ".join("x" * _r.randint(1, 5) for _ in range(_r.randint(1, 5))) + " " * _r.randint(0, 3)
        eq(Solution().lengthOfLastWord(s), len(s.split()[-1]), repr(s))
''',
"lc-69": r'''
import math as _m
@test("4 → 2, 8 → 2")
def _(): eq(Solution().mySqrt(4), 2, "4"); eq(Solution().mySqrt(8), 2, "8")
@test("0 и 1")
def _(): eq(Solution().mySqrt(0), 0, "0"); eq(Solution().mySqrt(1), 1, "1")
@test("большое: 2³¹ − 1")
def _(): eq(Solution().mySqrt(2**31 - 1), 46340)
@test("все x до 3000")
def _():
    for x in range(3000): eq(Solution().mySqrt(x), _m.isqrt(x), f"mySqrt({x})")
''',
"lc-74": r'''
M = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
@test("есть: 3")
def _(): eq(Solution().searchMatrix(M, 3), True)
@test("нет: 13")
def _(): eq(Solution().searchMatrix(M, 13), False)
@test("все числа от 0 до 61")
def _():
    for t in range(62): eq(Solution().searchMatrix(M, t), any(t in r for r in M), f"target {t}")
@test("матрица 1×1")
def _(): eq(Solution().searchMatrix([[5]], 5), True, "5"); eq(Solution().searchMatrix([[5]], 1), False, "1")
''',
"lc-121": r'''
def brute(p): return max([0] + [p[j] - p[i] for i in range(len(p)) for j in range(i + 1, len(p))])
@test("[7,1,5,3,6,4] → 5")
def _(): eq(Solution().maxProfit([7, 1, 5, 3, 6, 4]), 5)
@test("цены только падают → 0")
def _(): eq(Solution().maxProfit([7, 6, 4, 3, 1]), 0)
@test("один день → 0")
def _(): eq(Solution().maxProfit([5]), 0)
@test("300 случайных")
def _():
    for _ in range(300):
        p = [_r.randint(0, 50) for _ in range(_r.randint(1, 15))]; eq(Solution().maxProfit(p), brute(p), str(p))
''',
"lc-231": r'''
@test("1, 2, 16, 1024 → True")
def _():
    for n in [1, 2, 16, 1024]: eq(Solution().isPowerOfTwo(n), True, str(n))
@test("0, отрицательные, 3, 6 → False")
def _():
    for n in [0, -2, -16, 3, 6, 12]: eq(Solution().isPowerOfTwo(n), False, str(n))
@test("все числа до 5000")
def _():
    for n in range(-10, 5000): eq(Solution().isPowerOfTwo(n), n > 0 and bin(n).count("1") == 1, str(n))
''',
"lc-268": r'''
@test("[3,0,1] → 2")
def _(): eq(Solution().missingNumber([3, 0, 1]), 2)
@test("пропущено последнее: [0,1] → 2")
def _(): eq(Solution().missingNumber([0, 1]), 2)
@test("пропущен 0: [1] → 0")
def _(): eq(Solution().missingNumber([1]), 0)
@test("300 случайных")
def _():
    for _ in range(300):
        n = _r.randint(1, 50); nums = list(range(n + 1)); m = nums.pop(_r.randrange(n + 1)); _r.shuffle(nums)
        eq(Solution().missingNumber(nums), m, str(nums))
''',
"lc-367": r'''
@test("16 → True, 14 → False")
def _(): eq(Solution().isPerfectSquare(16), True, "16"); eq(Solution().isPerfectSquare(14), False, "14")
@test("1 → True")
def _(): eq(Solution().isPerfectSquare(1), True)
@test("все до 5000")
def _():
    import math as _m
    for n in range(1, 5000): eq(Solution().isPerfectSquare(n), _m.isqrt(n) ** 2 == n, str(n))
@test("большое: 2147395600 = 46340²")
def _(): eq(Solution().isPerfectSquare(2147395600), True)
''',
"lc-392": r'''
def ref(s, t):
    it = iter(t); return all(c in it for c in s)
@test('"abc" в "ahbgdc" → True')
def _(): eq(Solution().isSubsequence("abc", "ahbgdc"), True)
@test('"axc" в "ahbgdc" → False')
def _(): eq(Solution().isSubsequence("axc", "ahbgdc"), False)
@test("пустая s → True")
def _(): eq(Solution().isSubsequence("", "abc"), True)
@test("500 случайных")
def _():
    for _ in range(500):
        s = "".join(_r.choice("abc") for _ in range(_r.randint(0, 4))); t = "".join(_r.choice("abc") for _ in range(_r.randint(0, 8)))
        eq(Solution().isSubsequence(s, t), ref(s, t), f"{s!r}, {t!r}")
''',
"lc-509": r'''
@test("F(0) = 0, F(1) = 1")
def _(): eq(Solution().fib(0), 0, "fib(0)"); eq(Solution().fib(1), 1, "fib(1)")
@test("F(10) = 55")
def _(): eq(Solution().fib(10), 55)
@test("F(2..25)")
def _():
    a, b = 0, 1
    for n in range(26):
        eq(Solution().fib(n), a, f"fib({n})"); a, b = b, a + b
''',
"lc-643": r'''
@test("пример → 12.75")
def _(): eq(Solution().findMaxAverage([1, 12, -5, -6, 50, 3], 4), 12.75)
@test("k = длина массива")
def _(): eq(Solution().findMaxAverage([5], 1), 5.0)
@test("300 случайных")
def _():
    for _ in range(300):
        a = [_r.randint(-50, 50) for _ in range(_r.randint(1, 15))]; k = _r.randint(1, len(a))
        exp = max(sum(a[i:i + k]) / k for i in range(len(a) - k + 1)); got = Solution().findMaxAverage(a, k)
        if abs(got - exp) > 1e-6: raise AssertionError(f"{a}, k={k}: ожидалось {exp}, получено {got}")
@test("скорость: 50 000 чисел, k = 10 000 (нужно скользящее окно)")
def _():
    a = [_r.randint(-10**4, 10**4) for _ in range(50000)]; Solution().findMaxAverage(a, 10000)
''',
"lc-875": r'''
import math as _m
def brute(p, h): return next(k for k in range(1, max(p) + 1) if sum(_m.ceil(x / k) for x in p) <= h)
@test("[3,6,7,11], h=8 → 4")
def _(): eq(Solution().minEatingSpeed([3, 6, 7, 11], 8), 4)
@test("[30,11,23,4,20], h=5 → 30")
def _(): eq(Solution().minEatingSpeed([30, 11, 23, 4, 20], 5), 30)
@test("200 случайных")
def _():
    for _ in range(200):
        p = [_r.randint(1, 40) for _ in range(_r.randint(1, 6))]; h = _r.randint(len(p), 50)
        eq(Solution().minEatingSpeed(p, h), brute(p, h), f"{p}, h={h}")
@test("большие кучки (нужен бинарный поиск)")
def _(): eq(Solution().minEatingSpeed([10**9], 2), 500000000)
''',
"lc-977": r'''
@test("[-4,-1,0,3,10]")
def _(): eq(Solution().sortedSquares([-4, -1, 0, 3, 10]), [0, 1, 9, 16, 100])
@test("все отрицательные")
def _(): eq(Solution().sortedSquares([-7, -3, -1]), [1, 9, 49])
@test("300 случайных")
def _():
    for _ in range(300):
        a = sorted(_r.randint(-30, 30) for _ in range(_r.randint(1, 15))); eq(Solution().sortedSquares(a), sorted(x * x for x in a), str(a))
''',
"lc-1768": r'''
@test('"abc", "pqr" → "apbqcr"')
def _(): eq(Solution().mergeAlternately("abc", "pqr"), "apbqcr")
@test("вторая длиннее")
def _(): eq(Solution().mergeAlternately("ab", "pqrs"), "apbqrs")
@test("первая длиннее")
def _(): eq(Solution().mergeAlternately("abcd", "pq"), "apbqcd")
@test("одна пустая")
def _(): eq(Solution().mergeAlternately("", "xyz"), "xyz")
''',
"lc-2239": r'''
@test("[-4,-2,1,4,8] → 1")
def _(): eq(Solution().findClosestNumber([-4, -2, 1, 4, 8]), 1)
@test("равные по модулю → положительное: [2,-1,1] → 1")
def _(): eq(Solution().findClosestNumber([2, -1, 1]), 1)
@test("один элемент")
def _(): eq(Solution().findClosestNumber([-5]), -5)
@test("300 случайных")
def _():
    for _ in range(300):
        a = [_r.randint(-30, 30) for _ in range(_r.randint(1, 12))]; eq(Solution().findClosestNumber(a), max(a, key=lambda x: (-abs(x), x)), str(a))
''',
}
