"""Задания тренажёра: заготовки, демо-код и скрытые тесты.

Тесты — обычные функции с декоратором @test("описание"). Внутри доступны:
  eq(actual, expected, what)   — сравнение с понятным сообщением
  raises(ExcType, fn, what)    — проверка, что fn() бросает исключение
  walk(head) / back(tail)      — значения связанного списка вперёд / назад
  mk(ListNode, values)         — собрать связанный список из значений
  to_list(head)                — значения связанного списка (для задач LeetCode)
и все имена из кода ученика (классы Linked_list, Solution, ...).
"""

# Для методов: из какого файла берём класс и какие методы «опустошаем».
METHOD_EX = {
    "stack-list":      ("structures/stack.py",             ["Stack.add", "Stack.remove", "Stack.peek"]),
    "queue-list":      ("structures/queue.py",             ["Queue.add", "Queue.remove", "Queue.peek"]),
    "ll-remove":       ("structures/linked_list.py",        ["Linked_list.remove"]),
    "ll-append":       ("structures/linked_list.py",        ["Linked_list.append"]),
    "ll-reverse":      ("structures/linked_list.py",        ["Linked_list.reverse"]),
    "ll-insert":       ("structures/linked_list.py",        ["Linked_list.insert"]),
    "ll-setitem":      ("structures/linked_list.py",        ["Linked_list.__setitem__", "Linked_list._get_item"]),
    "dll-pop":         ("structures/double_linked_list.py", ["Double_Linked_List.pop"]),
    "dll-getitem":     ("structures/double_linked_list.py", ["Double_Linked_List.__getitem__", "Double_Linked_List._get_node"]),
    "dll-setitem":     ("structures/double_linked_list.py", ["Double_Linked_List.__setitem__", "Double_Linked_List._get_node"]),
    "deque-popleft":   ("structures/deque_ring.py",         ["Deque.popleft"]),
    "deque-popright":  ("structures/deque_ring.py",         ["Deque.pop"]),
    "deque-append":    ("structures/deque_ring.py",         ["Deque.append"]),
    "deque-appendleft":("structures/deque_ring.py",         ["Deque.appendleft"]),
    "hs-add":          ("structures/hash_set.py",           ["Hashset.add"]),
    "hs-remove":       ("structures/hash_set.py",           ["Hashset.remove"]),
}

DEMO = {
    "stack-list": 's = Stack()\nfor x in [1, 2, 3]:\n    s.add(x)\nprint(s.peek())     # ожидается 3\nprint(s.remove())   # ожидается 3\nprint(s)            # ожидается bottom -> [1, 2] <- top',
    "queue-list": 'q = Queue()\nfor x in [1, 2, 3]:\n    q.add(x)\nprint(q.peek())     # ожидается 1\nprint(q.remove())   # ожидается 1\nprint(q)            # ожидается front -> [2, 3] <- back',
    "ll-remove": 'lst = Linked_list(1, 2, 3, 2)\nlst.remove(2)\nprint(lst)        # ожидается 1->3->2\nprint(len(lst))   # ожидается 3',
    "ll-append": 'lst = Linked_list()\nlst.append(1)\nlst.append(2)\nlst.append(3)\nprint(lst)        # ожидается 1->2->3',
    "ll-reverse": 'lst = Linked_list(1, 2, 3, 4)\nlst.reverse()\nprint(lst)        # ожидается 4->3->2->1',
    "ll-insert": 'lst = Linked_list(1, 3)\nlst.insert(1, 2)\nlst.insert(0, 0)\nlst.insert(4, 4)\nprint(lst)        # ожидается 0->1->2->3->4',
    "ll-setitem": 'lst = Linked_list(1, 2, 3)\nlst[1] = 20\nprint(lst)        # ожидается 1->20->3',
    "dll-pop": 'lst = Double_Linked_List(1, 2, 3, 4)\nprint(lst.pop())   # ожидается 4\nprint(lst.pop(0))  # ожидается 1\nprint(lst)         # ожидается 2⇔3',
    "dll-getitem": 'lst = Double_Linked_List(10, 20, 30, 40, 50)\nprint(lst[0], lst[3], lst[-1])   # ожидается 10 40 50',
    "dll-setitem": 'lst = Double_Linked_List(1, 2, 3)\nlst[0] = 100\nlst[-1] = 300\nprint(lst)        # ожидается 100⇔2⇔300',
    "deque-popleft": 'd = Deque(capacity=4)\nfor x in [1, 2, 3]:\n    d.append(x)\nprint(d.popleft())   # ожидается 1\nprint(d)             # ожидается [2, 3]',
    "deque-popright": 'd = Deque(capacity=4)\nfor x in [1, 2, 3]:\n    d.append(x)\nprint(d.pop())       # ожидается 3\nprint(d)             # ожидается [1, 2]',
    "deque-append": 'd = Deque(capacity=2)\nfor x in [1, 2, 3, 4, 5]:\n    d.append(x)\nprint(d)             # ожидается [1, 2, 3, 4, 5]\nprint(d.capacity)    # ожидается 8',
    "deque-appendleft": 'd = Deque(capacity=2)\nfor x in [1, 2, 3]:\n    d.appendleft(x)\nprint(d)             # ожидается [3, 2, 1]',
    "hs-add": 's = Hashset(capacity=1, load_factor=100)   # всё в одну корзину -> коллизии\nfor k in ["a", "b", "c", "a"]:\n    s.add(k)\nprint(s, len(s))     # ожидается 3 ключа, len = 3',
    "hs-remove": 's = Hashset()\nfor k in [1, 2, 3]:\n    s.add(k)\ns.remove(2)\nprint(s, len(s))     # ожидается {1, 3} 2',
}

COMMON_TESTS = r'''
def _fmt(x):
    if hasattr(x, "val") and hasattr(x, "next"):
        return f"узел со значением {x.val!r}"
    return repr(x)

def eq(actual, expected, what="результат"):
    if actual != expected:
        raise AssertionError(f"{what}: ожидалось {_fmt(expected)}, получено {_fmt(actual)}")

def raises(exc, fn, what="вызов"):
    try:
        fn()
    except exc:
        return
    except Exception as e:
        raise AssertionError(f"{what}: ожидалось {exc.__name__}, а получено {type(e).__name__}: {e}")
    raise AssertionError(f"{what}: ожидалось исключение {exc.__name__}, но его не было")

def walk(head, limit=10000):
    out, cur = [], head
    while cur is not None:
        out.append(cur.val)
        cur = cur.next
        if len(out) > limit:
            raise AssertionError("ссылки next зациклились — список бесконечный")
    return out

def back(tail, limit=10000):
    out, cur = [], tail
    while cur is not None:
        out.append(cur.val)
        cur = cur.prev
        if len(out) > limit:
            raise AssertionError("ссылки prev зациклились")
    return out[::-1]

def dll_ok(lst, expected):
    eq(walk(lst.head), expected, "значения от head по next")
    eq(back(lst.tail), expected, "значения от tail по prev")
    eq(len(lst), len(expected), "len(lst)")
    if expected:
        eq(lst.head.prev, None, "head.prev")
        eq(lst.tail.next, None, "tail.next")
    else:
        eq((lst.head, lst.tail), (None, None), "(head, tail) пустого списка")

def mk(cls, vals):
    dummy = cls(0)
    t = dummy
    for v in vals:
        t.next = cls(v)
        t = t.next
    return dummy.next

to_list = walk

def hkeys(s, limit=100000):
    """Все ключи хэшсета — обходим корзины напрямую (не зависит от __iter__)."""
    out = []
    for node in s.buckets:
        while node is not None:
            out.append(node.key)
            node = node.next
            if len(out) > limit:
                raise AssertionError("цепочка в корзине зациклилась")
    return out

def hset(s):
    ks = hkeys(s)
    if len(ks) != len(set(ks)):
        raise AssertionError(f"в хэшсете есть дубликаты: {sorted(map(str, ks))}")
    return set(ks)

def dq(d):
    """Содержимое кольцевого дека по полям deque/head/size/capacity."""
    return [d.deque[(d.head + i) % d.capacity] for i in range(d.size)]
import random as _r
_r.seed(7)
'''

TESTS = {
"stack-list": r'''
@test("add, затем peek показывает последний")
def _():
    s = Stack(); s.add(1); s.add(2); eq(s.peek(), 2, "peek()"); eq(len(s), 2, "len")
@test("remove возвращает в обратном порядке (LIFO)")
def _():
    s = Stack()
    for x in [1, 2, 3]: s.add(x)
    eq([s.remove(), s.remove(), s.remove()], [3, 2, 1], "три remove()")
@test("peek не удаляет элемент")
def _():
    s = Stack(); s.add(5); s.peek(); s.peek(); eq(len(s), 1, "len после двух peek")
@test("пустой стек: remove → IndexError")
def _():
    raises(IndexError, lambda: Stack().remove(), "remove() на пустом")
@test("пустой стек: peek → IndexError")
def _():
    raises(IndexError, lambda: Stack().peek(), "peek() на пустом")
@test("случайные операции против list")
def _():
    s, ref = Stack(), []
    for _ in range(2000):
        if ref and _r.random() < .45: eq(s.remove(), ref.pop(), "remove()")
        else:
            v = _r.randint(0, 99); s.add(v); ref.append(v)
        if ref: eq(s.peek(), ref[-1], "peek()")
''',
"queue-list": r'''
@test("peek показывает первый добавленный")
def _():
    q = Queue(); q.add(1); q.add(2); eq(q.peek(), 1, "peek()"); eq(len(q), 2, "len")
@test("remove в порядке добавления (FIFO)")
def _():
    q = Queue()
    for x in [1, 2, 3]: q.add(x)
    eq([q.remove(), q.remove(), q.remove()], [1, 2, 3], "три remove()")
@test("peek не удаляет элемент")
def _():
    q = Queue(); q.add(5); q.peek(); q.peek(); eq(len(q), 1, "len после двух peek")
@test("пустая очередь: remove → IndexError")
def _():
    raises(IndexError, lambda: Queue().remove(), "remove() на пустой")
@test("пустая очередь: peek → IndexError")
def _():
    raises(IndexError, lambda: Queue().peek(), "peek() на пустой")
@test("случайные операции против collections.deque")
def _():
    from collections import deque
    q, ref = Queue(), deque()
    for _ in range(2000):
        if ref and _r.random() < .45: eq(q.remove(), ref.popleft(), "remove()")
        else:
            v = _r.randint(0, 99); q.add(v); ref.append(v)
        if ref: eq(q.peek(), ref[0], "peek()")
''',
# ---------------- методы ----------------
"ll-remove": r'''
@test("удаление из середины")
def _():
    l = Linked_list(1, 2, 3); l.remove(2); eq(walk(l.head), [1, 3]); eq(len(l), 2, "len")
@test("удаление головы")
def _():
    l = Linked_list(1, 2, 3); l.remove(1); eq(walk(l.head), [2, 3]); eq(len(l), 2, "len")
@test("удаление последнего узла")
def _():
    l = Linked_list(1, 2, 3); l.remove(3); eq(walk(l.head), [1, 2])
@test("единственный элемент")
def _():
    l = Linked_list(5); l.remove(5); eq(l.head, None, "head"); eq(len(l), 0, "len")
@test("удаляется только первое вхождение")
def _():
    l = Linked_list(1, 2, 3, 2); l.remove(2); eq(walk(l.head), [1, 3, 2])
@test("значения нет → ValueError")
def _():
    l = Linked_list(1, 2); raises(ValueError, lambda: l.remove(9), "remove(9)"); eq(walk(l.head), [1, 2], "список не должен измениться")
@test("пустой список → ValueError")
def _():
    raises(ValueError, lambda: Linked_list().remove(1), "remove на пустом")
''',
"ll-append": r'''
@test("append в пустой список")
def _():
    l = Linked_list(); l.append(1); eq(walk(l.head), [1]); eq(len(l), 1, "len")
@test("append в непустой список")
def _():
    l = Linked_list(1, 2); l.append(3); eq(walk(l.head), [1, 2, 3]); eq(len(l), 3, "len")
@test("много append подряд")
def _():
    l = Linked_list()
    for i in range(50): l.append(i)
    eq(walk(l.head), list(range(50))); eq(len(l), 50, "len")
''',
"ll-reverse": r'''
@test("разворот 4 элементов")
def _():
    l = Linked_list(1, 2, 3, 4); l.reverse(); eq(walk(l.head), [4, 3, 2, 1])
@test("пустой список")
def _():
    l = Linked_list(); l.reverse(); eq(l.head, None, "head")
@test("один элемент")
def _():
    l = Linked_list(7); l.reverse(); eq(walk(l.head), [7])
@test("двойной разворот возвращает исходный список")
def _():
    l = Linked_list(*range(20)); l.reverse(); l.reverse(); eq(walk(l.head), list(range(20)))
@test("len не меняется")
def _():
    l = Linked_list(1, 2, 3); l.reverse(); eq(len(l), 3, "len")
''',
"ll-insert": r'''
@test("вставка в середину")
def _():
    l = Linked_list(1, 3); l.insert(1, 2); eq(walk(l.head), [1, 2, 3]); eq(len(l), 3, "len")
@test("вставка в начало (idx = 0)")
def _():
    l = Linked_list(1, 2); l.insert(0, 0); eq(walk(l.head), [0, 1, 2])
@test("вставка в конец (idx = size)")
def _():
    l = Linked_list(1, 2); l.insert(2, 3); eq(walk(l.head), [1, 2, 3])
@test("вставка в пустой список")
def _():
    l = Linked_list(); l.insert(0, 1); eq(walk(l.head), [1]); eq(len(l), 1, "len")
@test("idx > size → IndexError")
def _():
    l = Linked_list(1, 2); raises(IndexError, lambda: l.insert(5, 0), "insert(5, 0)")
@test("отрицательный idx → IndexError")
def _():
    l = Linked_list(1, 2); raises(IndexError, lambda: l.insert(-1, 0), "insert(-1, 0)")
@test("случайные вставки совпадают с list.insert")
def _():
    l, ref = Linked_list(), []
    for _ in range(200):
        i = _r.randint(0, len(ref)); v = _r.randint(0, 99); l.insert(i, v); ref.insert(i, v)
    eq(walk(l.head), ref)
''',
"ll-setitem": r'''
@test("lst[0] = x")
def _():
    l = Linked_list(1, 2, 3); l[0] = 10; eq(walk(l.head), [10, 2, 3])
@test("lst[1] = x (середина)")
def _():
    l = Linked_list(1, 2, 3); l[1] = 20; eq(walk(l.head), [1, 20, 3])
@test("последний элемент")
def _():
    l = Linked_list(1, 2, 3); l[2] = 30; eq(walk(l.head), [1, 2, 30])
@test("структура не меняется: len тот же")
def _():
    l = Linked_list(1, 2, 3); l[1] = 0; eq(len(l), 3, "len")
@test("idx = size → IndexError")
def _():
    l = Linked_list(1, 2, 3)
    def f(): l[3] = 0
    raises(IndexError, f, "lst[3] = 0")
@test("пустой список → IndexError")
def _():
    l = Linked_list()
    def f(): l[0] = 0
    raises(IndexError, f, "lst[0] = 0")
''',
"dll-pop": r'''
@test("pop() возвращает и удаляет последний")
def _():
    l = Double_Linked_List(1, 2, 3); eq(l.pop(), 3, "pop()"); dll_ok(l, [1, 2])
@test("pop(0) — удаление головы")
def _():
    l = Double_Linked_List(1, 2, 3); eq(l.pop(0), 1, "pop(0)"); dll_ok(l, [2, 3])
@test("pop из середины")
def _():
    l = Double_Linked_List(1, 2, 3, 4); eq(l.pop(1), 2, "pop(1)"); dll_ok(l, [1, 3, 4])
@test("отрицательный индекс")
def _():
    l = Double_Linked_List(1, 2, 3, 4); eq(l.pop(-2), 3, "pop(-2)"); dll_ok(l, [1, 2, 4])
@test("единственный элемент → head и tail = None")
def _():
    l = Double_Linked_List(9); eq(l.pop(), 9, "pop()"); dll_ok(l, [])
@test("пустой список → IndexError")
def _():
    raises(IndexError, lambda: Double_Linked_List().pop(), "pop() на пустом")
@test("индекс вне диапазона → IndexError")
def _():
    l = Double_Linked_List(1, 2); raises(IndexError, lambda: l.pop(5), "pop(5)")
@test("случайные pop совпадают с list.pop")
def _():
    ref = list(range(60)); l = Double_Linked_List(*ref)
    while ref:
        i = _r.randrange(-len(ref), len(ref)); eq(l.pop(i), ref.pop(i), f"pop({i})")
    dll_ok(l, [])
''',
"dll-getitem": r'''
@test("lst[0] и последний")
def _():
    l = Double_Linked_List(10, 20, 30, 40, 50); eq(l[0], 10, "lst[0]"); eq(l[4], 50, "lst[4]")
@test("середина (обе половины)")
def _():
    l = Double_Linked_List(10, 20, 30, 40, 50); eq(l[1], 20, "lst[1]"); eq(l[3], 40, "lst[3]")
@test("отрицательные индексы")
def _():
    l = Double_Linked_List(10, 20, 30); eq(l[-1], 30, "lst[-1]"); eq(l[-3], 10, "lst[-3]")
@test("idx = size → IndexError")
def _():
    l = Double_Linked_List(1, 2, 3); raises(IndexError, lambda: l[3], "lst[3]")
@test("idx = -size-1 → IndexError")
def _():
    l = Double_Linked_List(1, 2, 3); raises(IndexError, lambda: l[-4], "lst[-4]")
@test("пустой список → IndexError")
def _():
    raises(IndexError, lambda: Double_Linked_List()[0], "lst[0] на пустом")
@test("все индексы большого списка")
def _():
    ref = [_r.randint(0, 999) for _ in range(101)]; l = Double_Linked_List(*ref)
    for i in range(-len(ref), len(ref)): eq(l[i], ref[i], f"lst[{i}]")
''',
"dll-setitem": r'''
@test("lst[0] = x")
def _():
    l = Double_Linked_List(1, 2, 3); l[0] = 100; dll_ok(l, [100, 2, 3])
@test("последний через отрицательный индекс")
def _():
    l = Double_Linked_List(1, 2, 3); l[-1] = 300; dll_ok(l, [1, 2, 300])
@test("середина ближе к хвосту")
def _():
    l = Double_Linked_List(1, 2, 3, 4, 5); l[3] = 40; dll_ok(l, [1, 2, 3, 40, 5])
@test("idx вне диапазона → IndexError")
def _():
    l = Double_Linked_List(1, 2)
    def f(): l[2] = 0
    raises(IndexError, f, "lst[2] = 0")
@test("случайные присваивания совпадают со списком Python")
def _():
    ref = list(range(40)); l = Double_Linked_List(*ref)
    for _ in range(200):
        i = _r.randrange(-40, 40); v = _r.randint(0, 999); l[i] = v; ref[i] = v
    dll_ok(l, ref)
''',
"deque-popleft": r'''
@test("popleft возвращает первый")
def _():
    d = Deque(4)
    for x in [1, 2, 3]: d.append(x)
    eq(d.popleft(), 1, "popleft()"); eq(dq(d), [2, 3], "остаток"); eq(d.size, 2, "len")
@test("пустой дек → IndexError")
def _():
    raises(IndexError, lambda: Deque().popleft(), "popleft() на пустом")
@test("заворот head через конец массива")
def _():
    d = Deque(4)
    for x in range(4): d.append(x)
    for x in range(4): eq(d.popleft(), x, "popleft()")
    for x in range(10, 14): d.append(x)
    eq([d.popleft() for _ in range(4)], [10, 11, 12, 13], "порядок после заворота")
@test("случайные операции против collections.deque")
def _():
    from collections import deque
    d, ref = Deque(3), deque()
    for _ in range(2000):
        if ref and _r.random() < .45: eq(d.popleft(), ref.popleft(), "popleft()")
        else:
            v = _r.random(); d.append(v); ref.append(v)
    eq(dq(d), list(ref), "содержимое")
''',
"deque-popright": r'''
@test("pop возвращает последний")
def _():
    d = Deque(4)
    for x in [1, 2, 3]: d.append(x)
    eq(d.pop(), 3, "pop()"); eq(dq(d), [1, 2], "остаток"); eq(d.size, 2, "len")
@test("пустой дек → IndexError")
def _():
    raises(IndexError, lambda: Deque().pop(), "pop() на пустом")
@test("последний элемент лежит «за краем» (заворот)")
def _():
    d = Deque(4)
    for x in range(4): d.append(x)
    d.popleft(); d.popleft(); d.append(4); d.append(5)
    eq(d.pop(), 5, "pop()"); eq(d.pop(), 4, "pop()"); eq(dq(d), [2, 3], "остаток")
@test("случайные операции против collections.deque")
def _():
    from collections import deque
    d, ref = Deque(3), deque()
    for _ in range(2000):
        r = _r.random()
        if ref and r < .35: eq(d.pop(), ref.pop(), "pop()")
        elif ref and r < .5: eq(d.popleft(), ref.popleft(), "popleft()")
        else:
            v = _r.random(); d.append(v); ref.append(v)
    eq(dq(d), list(ref), "содержимое")
''',
"deque-append": r'''
@test("append сохраняет порядок")
def _():
    d = Deque(8)
    for x in [1, 2, 3]: d.append(x)
    eq(dq(d), [1, 2, 3]); eq(d.size, 3, "len")
@test("переполнение → resize")
def _():
    d = Deque(2)
    for x in range(10): d.append(x)
    eq(dq(d), list(range(10))); eq(d.size, 10, "len")
@test("заворот: свободная ячейка в начале массива")
def _():
    d = Deque(4)
    for x in [1, 2, 3]: d.append(x)
    d.popleft(); d.popleft()
    for x in [4, 5, 6]: d.append(x)
    eq(dq(d), [3, 4, 5, 6], "после заворота"); d.append(7); eq(dq(d), [3, 4, 5, 6, 7], "после resize")
@test("случайные операции против collections.deque")
def _():
    from collections import deque
    d, ref = Deque(3), deque()
    for _ in range(2000):
        if ref and _r.random() < .4: eq(d.popleft(), ref.popleft(), "popleft()")
        else:
            v = _r.random(); d.append(v); ref.append(v)
    eq(dq(d), list(ref), "содержимое")
''',
"deque-appendleft": r'''
@test("appendleft кладёт в начало")
def _():
    d = Deque(8)
    for x in [1, 2, 3]: d.appendleft(x)
    eq(dq(d), [3, 2, 1]); eq(d.size, 3, "len")
@test("head = 0 → заворот в конец массива")
def _():
    d = Deque(4); d.append(1); d.appendleft(0); eq(dq(d), [0, 1]); eq(d.head, 3, "head")
@test("переполнение → resize")
def _():
    d = Deque(2)
    for x in range(10): d.appendleft(x)
    eq(dq(d), list(range(9, -1, -1)))
@test("случайные операции против collections.deque")
def _():
    from collections import deque
    d, ref = Deque(3), deque()
    for _ in range(2000):
        r = _r.random()
        if ref and r < .3: eq(d.pop(), ref.pop(), "pop()")
        elif r < .65:
            v = _r.random(); d.appendleft(v); ref.appendleft(v)
        else:
            v = _r.random(); d.append(v); ref.append(v)
    eq(dq(d), list(ref), "содержимое")
''',
"hs-add": r'''
@test("добавление и len")
def _():
    s = Hashset()
    for k in [1, 2, 3]: s.add(k)
    eq(hset(s), {1, 2, 3}, "ключи"); eq(s.size, 3, "len")
@test("дубликаты не добавляются")
def _():
    s = Hashset()
    for k in [1, 1, 2, 2, 2]: s.add(k)
    eq(s.size, 2, "len"); eq(sorted(hset(s)), [1, 2], "ключи")
@test("коллизии: size считает ключи в цепочке")
def _():
    s = Hashset(capacity=1, load_factor=100)
    for k in "abcde": s.add(k)
    eq(s.size, 5, "len (все ключи в одной корзине)"); eq(hset(s), set("abcde"), "ключи")
@test("resize при load factor ≥ 0.75")
def _():
    s = Hashset(capacity=4)
    for k in range(20): s.add(k)
    eq(hset(s), set(range(20)), "ключи"); eq(s.size, 20, "len")
    if s.capacity <= 4: raise AssertionError("capacity не увеличился — resize не вызывается")
@test("много случайных ключей против set")
def _():
    s, ref = Hashset(capacity=2), set()
    for _ in range(1000):
        k = _r.randint(0, 300); s.add(k); ref.add(k)
    eq(hset(s), ref, "ключи"); eq(s.size, len(ref), "len")
''',
"hs-remove": r'''
@test("удаление существующего ключа")
def _():
    s = Hashset()
    for k in [1, 2, 3]: s.add(k)
    s.remove(2); eq(hset(s), {1, 3}, "ключи"); eq(s.size, 2, "len")
@test("первый ключ в цепочке")
def _():
    s = Hashset(capacity=1, load_factor=100)
    for k in "abc": s.add(k)
    s.remove("a"); eq(hset(s), set("bc"))
@test("последний ключ в цепочке")
def _():
    s = Hashset(capacity=1, load_factor=100)
    for k in "abc": s.add(k)
    s.remove("c"); eq(hset(s), set("ab"))
@test("нет ключа в непустой цепочке → KeyError")
def _():
    s = Hashset(capacity=1, load_factor=100)
    for k in "abc": s.add(k)
    raises(KeyError, lambda: s.remove("z"), "remove('z')")
@test("пустая корзина → KeyError")
def _():
    raises(KeyError, lambda: Hashset().remove(1), "remove(1)")
@test("случайные операции против set")
def _():
    s, ref = Hashset(capacity=2), set()
    for _ in range(1500):
        if ref and _r.random() < .4:
            k = _r.choice(sorted(ref)); s.remove(k); ref.remove(k)
        else:
            k = _r.randint(0, 200); s.add(k); ref.add(k)
    eq(hset(s), ref, "ключи"); eq(s.size, len(ref), "len")
''',
# ---------------- задачи ----------------
"lc-1": r'''
def check(nums, target):
    r = Solution().twoSum(list(nums), target)
    if not (isinstance(r, list) and len(r) == 2): raise AssertionError(f"twoSum({nums}, {target}): нужен список из 2 индексов, получено {r!r}")
    i, j = r
    if i == j or nums[i] + nums[j] != target: raise AssertionError(f"twoSum({nums}, {target}) = {r}: nums[{i}] + nums[{j}] != {target}")
@test("пример 1: [2,7,11,15], 9")
def _(): check([2, 7, 11, 15], 9)
@test("пример 2: [3,2,4], 6")
def _(): check([3, 2, 4], 6)
@test("одинаковые числа: [3,3], 6")
def _(): check([3, 3], 6)
@test("отрицательные числа")
def _(): check([-3, 4, 3, 90], 0)
''',
"lc-2": r'''
def num(n): return mk(ListNode, [int(c) for c in str(n)[::-1]])
def back_num(h): return int("".join(map(str, to_list(h)))[::-1] or "0")
@test("пример: 342 + 465 = 807")
def _(): eq(to_list(Solution().addTwoNumbers(num(342), num(465))), [7, 0, 8])
@test("0 + 0")
def _(): eq(to_list(Solution().addTwoNumbers(num(0), num(0))), [0])
@test("перенос в новый разряд: 9999999 + 9999")
def _(): eq(to_list(Solution().addTwoNumbers(num(9999999), num(9999))), [8, 9, 9, 9, 0, 0, 0, 1])
@test("случайные числа разной длины")
def _():
    for _ in range(200):
        a, b = _r.randint(0, 10**_r.randint(1, 30)), _r.randint(0, 10**_r.randint(1, 30))
        eq(back_num(Solution().addTwoNumbers(num(a), num(b))), a + b, f"{a} + {b}")
''',
"lc-3": r'''
def brute(s):
    return max([0] + [j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1) if len(set(s[i:j])) == j - i])
@test('"abcabcbb" → 3')
def _(): eq(Solution().lengthOfLongestSubstring("abcabcbb"), 3)
@test('"bbbbb" → 1')
def _(): eq(Solution().lengthOfLongestSubstring("bbbbb"), 1)
@test('"pwwkew" → 3')
def _(): eq(Solution().lengthOfLongestSubstring("pwwkew"), 3)
@test('пустая строка → 0')
def _(): eq(Solution().lengthOfLongestSubstring(""), 0)
@test('"abba" → 2 (старый повтор левее окна)')
def _(): eq(Solution().lengthOfLongestSubstring("abba"), 2)
@test("случайные строки против перебора")
def _():
    for _ in range(300):
        s = "".join(_r.choice("abcd ") for _ in range(_r.randint(0, 14)))
        eq(Solution().lengthOfLongestSubstring(s), brute(s), repr(s))
''',
"lc-13": r'''
def to_roman(n):
    out = ""
    for v, s in [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while n >= v: out += s; n -= v
    return out
@test('"III" → 3')
def _(): eq(Solution().romanToInt("III"), 3)
@test('"LVIII" → 58')
def _(): eq(Solution().romanToInt("LVIII"), 58)
@test('"MCMXCIV" → 1994')
def _(): eq(Solution().romanToInt("MCMXCIV"), 1994)
@test("все числа от 1 до 3999")
def _():
    for n in range(1, 4000): eq(Solution().romanToInt(to_roman(n)), n, to_roman(n))
''',
"lc-20": r'''
def ref(s):
    st = []
    for c in s:
        if c in "([{": st.append(c)
        elif not st or "([{"[")]}".index(c)] != st.pop(): return False
    return not st
@test('"()[]{}" → True')
def _(): eq(Solution().isValid("()[]{}"), True)
@test('"(]" → False')
def _(): eq(Solution().isValid("(]"), False)
@test('"([)]" → False')
def _(): eq(Solution().isValid("([)]"), False)
@test('"{[]}" → True')
def _(): eq(Solution().isValid("{[]}"), True)
@test('незакрытая "((" → False')
def _(): eq(Solution().isValid("(("), False)
@test('лишняя закрывающая "]" → False')
def _(): eq(Solution().isValid("]"), False)
@test("случайные строки")
def _():
    for _ in range(500):
        s = "".join(_r.choice("()[]{}") for _ in range(_r.randrange(0, 12, 2)))
        eq(Solution().isValid(s), ref(s), repr(s))
''',
"lc-21": r'''
def merge(a, b): return to_list(Solution().mergeTwoLists(mk(ListNode, a), mk(ListNode, b)))
@test("пример: [1,2,4] + [1,3,4]")
def _(): eq(merge([1, 2, 4], [1, 3, 4]), [1, 1, 2, 3, 4, 4])
@test("оба пустые")
def _(): eq(merge([], []), [])
@test("один пустой")
def _(): eq(merge([], [0]), [0]); eq(merge([1, 2], []), [1, 2])
@test("случайные отсортированные списки")
def _():
    for _ in range(200):
        a = sorted(_r.randint(-50, 50) for _ in range(_r.randint(0, 10)))
        b = sorted(_r.randint(-50, 50) for _ in range(_r.randint(0, 10)))
        eq(merge(a, b), sorted(a + b), f"{a} + {b}")
''',
"lc-83": r'''
def dd(v): return to_list(Solution().deleteDuplicates(mk(ListNode, v)))
@test("[1,1,2] → [1,2]")
def _(): eq(dd([1, 1, 2]), [1, 2])
@test("[1,1,2,3,3] → [1,2,3]")
def _(): eq(dd([1, 1, 2, 3, 3]), [1, 2, 3])
@test("три одинаковых подряд")
def _(): eq(dd([1, 1, 1]), [1])
@test("пустой список")
def _(): eq(dd([]), [])
@test("случайные отсортированные")
def _():
    for _ in range(200):
        v = sorted(_r.randint(0, 6) for _ in range(_r.randint(0, 15)))
        eq(dd(v), sorted(set(v)), str(v))
''',
"lc-141": r'''
def build(vals, pos):
    nodes = [ListNode(v) for v in vals]
    for a, b in zip(nodes, nodes[1:]): a.next = b
    if pos >= 0: nodes[-1].next = nodes[pos]
    return nodes[0] if nodes else None
@test("цикл на узел 1")
def _(): eq(Solution().hasCycle(build([3, 2, 0, -4], 1)), True)
@test("цикл из двух узлов")
def _(): eq(Solution().hasCycle(build([1, 2], 0)), True)
@test("один узел без цикла")
def _(): eq(Solution().hasCycle(build([1], -1)), False)
@test("пустой список")
def _(): eq(Solution().hasCycle(None), False)
@test("узел ссылается сам на себя")
def _(): eq(Solution().hasCycle(build([1], 0)), True)
@test("длинный список без цикла")
def _(): eq(Solution().hasCycle(build(list(range(5000)), -1)), False)
@test("одинаковые значения, но без цикла")
def _(): eq(Solution().hasCycle(build([1, 1, 1, 1], -1)), False)
''',
"lc-155": r'''
@test("пример из условия")
def _():
    s = MinStack(); s.push(-2); s.push(0); s.push(-3)
    eq(s.getMin(), -3, "getMin()"); s.pop(); eq(s.top(), 0, "top()"); eq(s.getMin(), -2, "getMin()")
@test("повторяющийся минимум")
def _():
    s = MinStack(); s.push(1); s.push(1); s.pop(); eq(s.getMin(), 1, "getMin()")
@test("случайные операции")
def _():
    s, ref = MinStack(), []
    for _ in range(2000):
        if ref and _r.random() < .4: s.pop(); ref.pop()
        else:
            v = _r.randint(-100, 100); s.push(v); ref.append(v)
        if ref: eq(s.getMin(), min(ref), "getMin()"); eq(s.top(), ref[-1], "top()")
''',
"lc-225": r'''
@test("пример из условия")
def _():
    s = MyStack(); s.push(1); s.push(2)
    eq(s.top(), 2, "top()"); eq(s.pop(), 2, "pop()"); eq(s.empty(), False, "empty()")
@test("опустошение")
def _():
    s = MyStack(); s.push(1); s.pop(); eq(s.empty(), True, "empty()")
@test("случайные операции (LIFO)")
def _():
    s, ref = MyStack(), []
    for _ in range(500):
        if ref and _r.random() < .45: eq(s.pop(), ref.pop(), "pop()")
        else:
            v = _r.randint(0, 99); s.push(v); ref.append(v)
        if ref: eq(s.top(), ref[-1], "top()")
        eq(s.empty(), not ref, "empty()")
''',
"lc-232": r'''
@test("пример из условия")
def _():
    q = MyQueue(); q.push(1); q.push(2)
    eq(q.peek(), 1, "peek()"); eq(q.pop(), 1, "pop()"); eq(q.empty(), False, "empty()")
@test("чередование push и pop")
def _():
    q = MyQueue(); q.push(1); q.push(2); q.pop(); q.push(3)
    eq(q.pop(), 2, "pop()"); eq(q.pop(), 3, "pop()"); eq(q.empty(), True, "empty()")
@test("случайные операции (FIFO)")
def _():
    from collections import deque
    q, ref = MyQueue(), deque()
    for _ in range(1000):
        if ref and _r.random() < .45: eq(q.pop(), ref.popleft(), "pop()")
        else:
            v = _r.randint(0, 99); q.push(v); ref.append(v)
        if ref: eq(q.peek(), ref[0], "peek()")
        eq(q.empty(), not ref, "empty()")
''',
"lc-234": r'''
def pal(v): return Solution().isPalindrome(mk(ListNode, v))
@test("[1,2,2,1] → True")
def _(): eq(pal([1, 2, 2, 1]), True)
@test("[1,2] → False")
def _(): eq(pal([1, 2]), False)
@test("нечётная длина [1,2,1] → True")
def _(): eq(pal([1, 2, 1]), True)
@test("один элемент → True")
def _(): eq(pal([7]), True)
@test("случайные списки")
def _():
    for _ in range(300):
        v = [_r.randint(0, 2) for _ in range(_r.randint(1, 9))]
        eq(pal(v), v == v[::-1], str(v))
''',
"lc-290": r'''
@test('"abba", "dog cat cat dog" → True')
def _(): eq(Solution().wordPattern("abba", "dog cat cat dog"), True)
@test('"abba", "dog cat cat fish" → False')
def _(): eq(Solution().wordPattern("abba", "dog cat cat fish"), False)
@test('"aaaa", "dog cat cat dog" → False')
def _(): eq(Solution().wordPattern("aaaa", "dog cat cat dog"), False)
@test('"abba", "dog dog dog dog" → False (нужна проверка в обе стороны)')
def _(): eq(Solution().wordPattern("abba", "dog dog dog dog"), False)
@test("разная длина → False")
def _(): eq(Solution().wordPattern("aaa", "dog dog"), False)
''',
"lc-2073": r'''
def sim(t, k):
    from collections import deque
    t = t[:]; q = deque(range(len(t))); time = 0
    while True:
        i = q.popleft(); t[i] -= 1; time += 1
        if t[i] == 0:
            if i == k: return time
        else: q.append(i)
@test("[2,3,2], k=2 → 6")
def _(): eq(Solution().timeRequiredToBuy([2, 3, 2], 2), 6)
@test("[5,1,1,1], k=0 → 8")
def _(): eq(Solution().timeRequiredToBuy([5, 1, 1, 1], 0), 8)
@test("один человек")
def _(): eq(Solution().timeRequiredToBuy([4], 0), 4)
@test("случайные очереди против моделирования")
def _():
    for _ in range(300):
        t = [_r.randint(1, 8) for _ in range(_r.randint(1, 10))]; k = _r.randrange(len(t))
        eq(Solution().timeRequiredToBuy(t, k), sim(t, k), f"tickets={t}, k={k}")
''',
}

# Заготовки для задач LeetCode (как на сайте LeetCode).
LN = '''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


'''
PROBLEM_STARTER = {
    "lc-1": ('from typing import List\n\n\nclass Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        # твой код\n        pass\n',
             'print(Solution().twoSum([2, 7, 11, 15], 9))   # ожидается [0, 1]'),
    "lc-2": (LN + 'class Solution:\n    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:\n        # твой код\n        pass\n',
             'def mk(vals):\n    d = ListNode(); t = d\n    for v in vals:\n        t.next = ListNode(v); t = t.next\n    return d.next\n\nres = Solution().addTwoNumbers(mk([2, 4, 3]), mk([5, 6, 4]))\nwhile res:\n    print(res.val, end=" ")   # ожидается 7 0 8\n    res = res.next'),
    "lc-3": ('class Solution:\n    def lengthOfLongestSubstring(self, s: str) -> int:\n        # твой код\n        pass\n',
             'print(Solution().lengthOfLongestSubstring("abcabcbb"))   # ожидается 3'),
    "lc-13": ('class Solution:\n    def romanToInt(self, s: str) -> int:\n        # твой код\n        pass\n',
              'print(Solution().romanToInt("MCMXCIV"))   # ожидается 1994'),
    "lc-20": ('class Solution:\n    def isValid(self, s: str) -> bool:\n        # твой код\n        pass\n',
              'print(Solution().isValid("()[]{}"))   # ожидается True\nprint(Solution().isValid("(]"))       # ожидается False'),
    "lc-21": (LN + 'class Solution:\n    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:\n        # твой код\n        pass\n',
              'def mk(vals):\n    d = ListNode(); t = d\n    for v in vals:\n        t.next = ListNode(v); t = t.next\n    return d.next\n\nres = Solution().mergeTwoLists(mk([1, 2, 4]), mk([1, 3, 4]))\nwhile res:\n    print(res.val, end=" ")   # ожидается 1 1 2 3 4 4\n    res = res.next'),
    "lc-83": (LN + 'class Solution:\n    def deleteDuplicates(self, head: ListNode) -> ListNode:\n        # твой код\n        pass\n',
              'def mk(vals):\n    d = ListNode(); t = d\n    for v in vals:\n        t.next = ListNode(v); t = t.next\n    return d.next\n\nres = Solution().deleteDuplicates(mk([1, 1, 2, 3, 3]))\nwhile res:\n    print(res.val, end=" ")   # ожидается 1 2 3\n    res = res.next'),
    "lc-141": ('class ListNode:\n    def __init__(self, x):\n        self.val = x\n        self.next = None\n\n\nclass Solution:\n    def hasCycle(self, head: ListNode) -> bool:\n        # твой код\n        pass\n',
               'a, b, c = ListNode(1), ListNode(2), ListNode(3)\na.next, b.next, c.next = b, c, a   # цикл\nprint(Solution().hasCycle(a))   # ожидается True'),
    "lc-155": ('class MinStack:\n    def __init__(self):\n        # твой код\n        pass\n\n    def push(self, val: int) -> None:\n        pass\n\n    def pop(self) -> None:\n        pass\n\n    def top(self) -> int:\n        pass\n\n    def getMin(self) -> int:\n        pass\n',
               's = MinStack()\ns.push(-2); s.push(0); s.push(-3)\nprint(s.getMin())   # ожидается -3\ns.pop()\nprint(s.top(), s.getMin())   # ожидается 0 -2'),
    "lc-225": ('from collections import deque\n\n\nclass MyStack:\n    """Можно использовать только операции очереди: append, popleft, q[0], len."""\n\n    def __init__(self):\n        self.q = deque()\n\n    def push(self, x: int) -> None:\n        # твой код\n        pass\n\n    def pop(self) -> int:\n        pass\n\n    def top(self) -> int:\n        pass\n\n    def empty(self) -> bool:\n        pass\n',
               's = MyStack()\ns.push(1); s.push(2)\nprint(s.top(), s.pop(), s.empty())   # ожидается 2 2 False'),
    "lc-232": ('class MyQueue:\n    """Можно использовать только списки как стеки: append, pop, [-1], len."""\n\n    def __init__(self):\n        # твой код\n        pass\n\n    def push(self, x: int) -> None:\n        pass\n\n    def pop(self) -> int:\n        pass\n\n    def peek(self) -> int:\n        pass\n\n    def empty(self) -> bool:\n        pass\n',
               'q = MyQueue()\nq.push(1); q.push(2)\nprint(q.peek(), q.pop(), q.empty())   # ожидается 1 1 False'),
    "lc-234": (LN + 'class Solution:\n    def isPalindrome(self, head: ListNode) -> bool:\n        # твой код\n        pass\n',
               'def mk(vals):\n    d = ListNode(); t = d\n    for v in vals:\n        t.next = ListNode(v); t = t.next\n    return d.next\n\nprint(Solution().isPalindrome(mk([1, 2, 2, 1])))   # ожидается True'),
    "lc-290": ('class Solution:\n    def wordPattern(self, pattern: str, s: str) -> bool:\n        # твой код\n        pass\n',
               'print(Solution().wordPattern("abba", "dog cat cat dog"))   # ожидается True'),
    "lc-2073": ('from typing import List\n\n\nclass Solution:\n    def timeRequiredToBuy(self, tickets: List[int], k: int) -> int:\n        # твой код\n        pass\n',
                'print(Solution().timeRequiredToBuy([2, 3, 2], 2))   # ожидается 6'),
}

PROBLEM_FILES = {
    "lc-1": "leetcode/0001_two_sum.py", "lc-2": "leetcode/0002_add_two_numbers.py", "lc-3": "leetcode/0003_longest_substring.py",
    "lc-13": "leetcode/0013_roman_to_integer.py", "lc-20": "leetcode/0020_valid_parentheses.py", "lc-21": "leetcode/0021_merge_two_sorted_lists.py",
    "lc-83": "leetcode/0083_remove_duplicates_sorted_list.py", "lc-141": "leetcode/0141_linked_list_cycle.py", "lc-155": "leetcode/0155_min_stack.py",
    "lc-225": "leetcode/0225_stack_using_queues.py", "lc-232": "leetcode/0232_queue_using_stacks.py", "lc-234": "leetcode/0234_palindrome_linked_list.py",
    "lc-290": "leetcode/0290_word_pattern.py", "lc-2073": "leetcode/2073_time_needed_to_buy_tickets.py",
}

# Тот же код выполняется в браузере (Pyodide) и при локальной проверке.
HARNESS = r'''
import json as _json, traceback as _tb

def __run_tests(user_code, common, tests_code):
    ns = {"__name__": "solution"}
    try:
        exec(compile(user_code, "solution.py", "exec"), ns)
    except Exception as e:
        tb = _tb.extract_tb(e.__traceback__)
        line = next((f.lineno for f in reversed(tb) if f.filename == "solution.py"), getattr(e, "lineno", None))
        return _json.dumps({"error": f"{type(e).__name__}: {e}" + (f" (строка {line})" if line else "")})
    tests = []
    def test(name):
        def deco(f):
            tests.append((name, f))
            return f
        return deco
    tns = dict(ns)
    tns["test"] = test
    tns["SOURCE"] = user_code
    tns["__user_ns__"] = ns
    exec(common, tns)
    exec(tests_code, tns)
    res = []
    for name, f in tests:
        try:
            f()
            res.append([name, True, ""])
        except AssertionError as e:
            res.append([name, False, str(e)])
        except RecursionError:
            res.append([name, False, "RecursionError: слишком глубокая рекурсия"])
        except Exception as e:
            tb = _tb.extract_tb(e.__traceback__)
            line = next((fr.lineno for fr in reversed(tb) if fr.filename == "solution.py"), None)
            res.append([name, False, f"{type(e).__name__}: {e}" + (f" (твой код, строка {line})" if line else "")])
    return _json.dumps({"results": res})
'''
