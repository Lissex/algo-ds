"""Тесты кода раздела 1: алгоритмы и задачи LeetCode."""
import importlib.util, random, math, itertools
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "code"
def load(p):
    spec = importlib.util.spec_from_file_location(p.stem, p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
A = {p.stem: load(p) for p in (ROOT / "algorithms").glob("*.py")}
L = {p.stem.split("_")[0]: load(p) for p in (ROOT / "leetcode").glob("*.py")}
random.seed(3)
cases = [[], [1], [2, 1], [1, 2], [3, 3, 3], [5, 4, 3, 2, 1], list(range(10))] + \
        [[random.randint(-20, 20) for _ in range(random.randint(0, 30))] for _ in range(400)]

class K:  # для проверки устойчивости
    def __init__(s, k, tag): s.k, s.tag = k, tag
    def __lt__(s, o): return s.k < o.k
    def __gt__(s, o): return s.k > o.k
    def __le__(s, o): return s.k <= o.k
    def __ge__(s, o): return s.k >= o.k
    def __eq__(s, o): return s.k == o.k

# сортировки на месте
for name, fn in [("selection_sort", A["selection_sort"].selection_sort), ("insertion_sort", A["insertion_sort"].insertion_sort),
                 ("bubble_sort", A["bubble_sort"].bubble_sort), ("merge_sort", A["merge_sort"].merge_sort),
                 ("quick_sort", A["quick_sort"].quick_sort)]:
    for c in cases:
        a = c[:]; r = fn(a); assert a == sorted(c), (name, c); assert r is None, name
for name, fn in [("insertion", A["insertion_sort"].insertion_sort), ("bubble", A["bubble_sort"].bubble_sort), ("merge", A["merge_sort"].merge_sort)]:
    for _ in range(100):
        items = [K(random.randint(0, 5), i) for i in range(random.randint(0, 25))]
        a = items[:]; fn(a)
        assert [x.tag for x in a] == [x.tag for x in sorted(items, key=lambda x: x.k)], name + " не устойчива"
for c in cases:
    orig = c[:]
    assert A["quick_sort"].quick_sort_simple(c) == sorted(c) and c == orig
    assert A["merge_sort"].merge_sort_new(c) == sorted(c) and c == orig
# merge
for _ in range(300):
    a = sorted(random.randint(0, 30) for _ in range(random.randint(0, 10)))
    b = sorted(random.randint(0, 30) for _ in range(random.randint(0, 10)))
    assert A["merge"].merge(a, b) == sorted(a + b)
# рекурсия
R = A["recursion"]
for n in range(0, 20):
    assert R.factorial(n) == math.factorial(n) == R.factorial_iter(n)
    assert R.fib(n) == R.fib_memo(n) == R.fib_iter(n)
assert R.fib_memo(90) == R.fib_iter(90) == 2880067194370816120
# два указателя, окно
T = A["two_pointers"]
for s, e in [("", True), ("a", True), ("abba", True), ("abcba", True), ("abca", False), ("ab", False)]:
    assert T.is_palindrome(s) == e
assert T.is_palindrome_phrase("А роза упала на лапу Азора") and not T.is_palindrome_phrase("race a car")
W = A["sliding_window"]
def brute(s):
    best = ""
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            if len(set(s[i:j])) == j - i and j - i > len(best): best = s[i:j]
    return best
for _ in range(300):
    s = "".join(random.choice("abcd") for _ in range(random.randint(0, 14)))
    r1, r2 = W.longest_unique_substring(s), W.longest_unique_substring_set(s)
    for r in (r1, r2):
        assert len(r) == len(brute(s)) and r in s and len(set(r)) == len(r), s
# поиск
B = A["binary_search"]
for _ in range(300):
    arr = sorted(set(random.randint(0, 50) for _ in range(random.randint(0, 20))))
    t = random.randint(-2, 52)
    exp = arr.index(t) if t in arr else -1
    assert B.binary_search(arr, t) == exp == B.binary_search_rec(arr, t)
    arr2 = [random.randint(0, 9) for _ in range(random.randint(0, 15))]
    assert A["linear_search"].linear_search(arr2, t % 10) == (arr2.index(t % 10) if t % 10 in arr2 else -1)
MM = A["min_max"]
for c in cases:
    if c: assert MM.find_min_max(c) == (min(c), max(c))
try: MM.find_min_max([]); assert False
except ValueError: pass
AO = A["array_ops"]
for _ in range(200):
    a = [random.randint(0, 9) for _ in range(random.randint(1, 10))]; ref = a[:]
    i = random.randint(0, len(a)); AO.insert(a, i, 99); ref.insert(i, 99); assert a == ref
    i = random.randrange(len(a)); assert AO.delete(a, i) == ref.pop(i); assert a == ref
BO = A["big_o_examples"]
assert BO.logarithmic(1024) == 10 and BO.quadratic([1, 2, 3]) == 9 and len(BO.factorial_time([1, 2, 3, 4])) == 24 and BO.exponential(10) == 55

# ---------- LeetCode ----------
S = lambda k: L[k].Solution()
for _ in range(500):
    a = sorted(random.randint(-50, 50) for _ in range(random.randint(0, 9)))
    b = sorted(random.randint(-50, 50) for _ in range(random.randint(0 if a else 1, 9)))
    m = sorted(a + b); k = len(m); med = m[k // 2] if k % 2 else (m[k // 2 - 1] + m[k // 2]) / 2
    assert S("0004").findMedianSortedArrays(a, b) == med == S("0004").findMedianMerge(a, b), (a, b)
for x in [-121, 0, 1, 10, 121, 1221, 12321, 123, 1000021] + [random.randint(-10**6, 10**9) for _ in range(500)]:
    assert S("0009").isPalindrome(x) == (str(x) == str(x)[::-1]) == S("0009").isPalindromeStr(x), x
for _ in range(300):
    h = [random.randint(0, 20) for _ in range(random.randint(2, 15))]
    assert S("0011").maxArea(h) == max(min(h[i], h[j]) * (j - i) for i in range(len(h)) for j in range(i + 1, len(h)))
for _ in range(300):
    a = sorted(set(random.randint(0, 40) for _ in range(random.randint(1, 15)))); t = random.randint(-1, 42)
    import bisect; assert S("0035").searchInsert(a, t) == bisect.bisect_left(a, t)
for s, e in [("Hello World", 5), ("   fly me   to   the moon  ", 4), ("luffy is still joyboy", 6), ("a", 1)]:
    assert S("0058").lengthOfLastWord(s) == e
for x in list(range(0, 2000)) + [2**31 - 1]:
    assert S("0069").mySqrt(x) == math.isqrt(x)
mat = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
for t in range(0, 65): assert S("0074").searchMatrix(mat, t) == any(t in r for r in mat)
for _ in range(300):
    p = [random.randint(0, 50) for _ in range(random.randint(1, 15))]
    assert S("0121").maxProfit(p) == max([0] + [p[j] - p[i] for i in range(len(p)) for j in range(i + 1, len(p))])
for n in range(-5, 5000):
    e = n > 0 and bin(n).count("1") == 1
    assert S("0231").isPowerOfTwo(n) == e == S("0231").isPowerOfTwoRec(n)
for _ in range(300):
    n = random.randint(1, 30); nums = list(range(n + 1)); miss = nums.pop(random.randrange(n + 1)); random.shuffle(nums)
    assert S("0268").missingNumber(nums) == miss == S("0268").missingNumberXor(nums)
for n in range(1, 5000): assert S("0367").isPerfectSquare(n) == (math.isqrt(n) ** 2 == n)
def is_sub(s, t):
    it = iter(t); return all(c in it for c in s)
for _ in range(500):
    s = "".join(random.choice("abc") for _ in range(random.randint(0, 4))); t = "".join(random.choice("abc") for _ in range(random.randint(0, 8)))
    assert S("0392").isSubsequence(s, t) == is_sub(s, t)
for n in range(31): assert S("0509").fib(n) == R.fib_iter(n) == S("0509").fibMemo(n)
for _ in range(300):
    nums = [random.randint(-50, 50) for _ in range(random.randint(1, 15))]; k = random.randint(1, len(nums))
    assert abs(S("0643").findMaxAverage(nums, k) - max(sum(nums[i:i + k]) / k for i in range(len(nums) - k + 1))) < 1e-9
for _ in range(300):
    piles = [random.randint(1, 30) for _ in range(random.randint(1, 6))]; h = random.randint(len(piles), 40)
    best = next(k for k in range(1, 31) if sum(math.ceil(p / k) for p in piles) <= h)
    assert S("0875").minEatingSpeed(piles, h) == best
for _ in range(300):
    a = sorted(random.randint(-20, 20) for _ in range(random.randint(1, 12)))
    assert S("0977").sortedSquares(a) == sorted(x * x for x in a)
for w1, w2, e in [("abc", "pqr", "apbqcr"), ("ab", "pqrs", "apbqrs"), ("abcd", "pq", "apbqcd")]:
    assert S("1768").mergeAlternately(w1, w2) == e
for _ in range(300):
    nums = [random.randint(-30, 30) for _ in range(random.randint(1, 12))]
    assert S("2239").findClosestNumber(nums) == max(nums, key=lambda x: (-abs(x), x))
print("SECTION 1 OK")
