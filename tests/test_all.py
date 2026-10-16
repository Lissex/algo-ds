import sys, importlib.util, random, collections
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent / 'code'
def load(p):
    spec = importlib.util.spec_from_file_location(p.stem, p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
S = {p.stem: load(p) for p in (ROOT/'structures').glob('*.py')}
L = {p.stem.split('_')[0]: load(p) for p in (ROOT/'leetcode').glob('*.py')}
random.seed(1)

# Stack / Queue
for cls in (S['stack'].Stack, S['stack'].ArrayStack):
    st, ref = cls(), []
    for _ in range(2000):
        if ref and random.random() < .45:
            assert st.peek() == ref[-1]; assert st.remove() == ref.pop()
        else:
            v = random.randint(0, 99); st.add(v); ref.append(v)
        assert len(st) == len(ref)
q, ref = S['queue'].Queue(), collections.deque()
for _ in range(2000):
    if ref and random.random() < .45:
        assert q.peek() == ref[0]; assert q.remove() == ref.popleft()
    else:
        v = random.randint(0, 99); q.add(v); ref.append(v)
    assert len(q) == len(ref)
for e in (S['stack'].Stack().remove, S['queue'].Queue().peek):
    try: e(); assert False
    except IndexError: pass

# Linked lists
for mod, cls in (('linked_list', 'Linked_list'), ('double_linked_list', 'Double_Linked_List')):
    C = getattr(S[mod], cls)
    for _ in range(300):
        ref = [random.randint(0, 9) for _ in range(random.randint(0, 8))]
        ll = C(*ref)
        for _ in range(15):
            op = random.choice(['append', 'insert', 'remove', 'pop', 'set', 'get', 'reverse'])
            if op == 'append':
                v = random.randint(0, 9); ll.append(v); ref.append(v)
            elif op == 'insert':
                i = random.randint(0, len(ref)); v = random.randint(0, 9); ll.insert(i, v); ref.insert(i, v)
            elif op == 'remove' and ref:
                v = random.choice(ref); ll.remove(v); ref.remove(v)
            elif op == 'pop' and ref:
                i = random.randrange(len(ref)); assert ll.pop(i) == ref.pop(i)
            elif op == 'set' and ref:
                i = random.randrange(len(ref)); ll[i] = 42; ref[i] = 42
            elif op == 'get' and ref:
                i = random.randrange(len(ref)); assert ll[i] == ref[i]
            elif op == 'reverse':
                ll.reverse(); ref.reverse()
            assert list(ll) == ref and len(ll) == len(ref), (cls, op)
        if mod == 'double_linked_list' and ref:
            # tail и prev-ссылки корректны
            back, cur = [], ll.tail
            while cur: back.append(cur.val); cur = cur.prev
            assert back == ref[::-1]
            assert ll.pop() == ref.pop(); assert ll[-1] == ref[-1] if ref else True

# Deques
for C in (S['deque_ring'].Deque, S['deque_dll'].LinkedDeque):
    d, ref = C(), collections.deque()
    for _ in range(5000):
        r = random.random()
        if ref and r < .25: assert d.popleft() == ref.popleft()
        elif ref and r < .5: assert d.popright() == ref.pop()
        elif r < .75: v = random.random(); d.append(v); ref.append(v)
        else: v = random.random(); d.appendleft(v); ref.appendleft(v)
        assert list(d) == list(ref) and len(d) == len(ref)

# Hashset / Hashtable
hs, ref = S['hash_set'].Hashset(capacity=4), set()
for _ in range(5000):
    k = random.randint(0, 300)
    if random.random() < .4 and ref:
        k = random.choice(list(ref)); hs.remove(k); ref.remove(k)
    else:
        hs.add(k); ref.add(k)
    assert len(hs) == len(ref)
assert set(hs) == ref and all(k in hs for k in ref)
try: hs.remove(-1); assert False
except KeyError: pass
ht, ref = S['hash_table'].Hashtable(capacity=4), {}
for _ in range(5000):
    k = random.choice([random.randint(0, 300), f"k{random.randint(0,50)}"])
    if random.random() < .3 and ref:
        k = random.choice(list(ref)); ht.remove(k); del ref[k]
    else:
        v = random.random(); ht[k] = v; ref[k] = v
    assert len(ht) == len(ref)
for k, v in ref.items(): assert ht[k] == v
assert sorted(map(str, ht.keys())) == sorted(map(str, ref)) and dict(ht.items()) == ref
try: ht['nope']; assert False
except KeyError: pass

# LeetCode
def mk(mod, vals):
    d = mod.ListNode(0); t = d
    for v in vals: t.next = mod.ListNode(v); t = t.next
    return d.next
def tl(n):
    r = []
    while n: r.append(n.val); n = n.next
    return r
s = L['0001'].Solution(); assert s.twoSum([2,7,11,15], 9) == [0,1]; assert s.twoSum([3,3], 6) == [0,1]; assert s.twoSum([3,2,4], 6) == [1,2]
m = L['0002']; assert tl(m.Solution().addTwoNumbers(mk(m,[2,4,3]), mk(m,[5,6,4]))) == [7,0,8]
assert tl(m.Solution().addTwoNumbers(mk(m,[9]*7), mk(m,[9]*4))) == [8,9,9,9,0,0,0,1]
s = L['0003'].Solution()
def brute(x):
    return max([0]+[j-i for i in range(len(x)) for j in range(i+1,len(x)+1) if len(set(x[i:j]))==j-i])
for t in ['abcabcbb','bbbbb','pwwkew','','abba','dvdf'] + [''.join(random.choice('abcd') for _ in range(random.randint(0,12))) for _ in range(300)]:
    assert s.lengthOfLongestSubstring(t) == brute(t), t
s = L['0013'].Solution(); assert s.romanToInt('III')==3 and s.romanToInt('LVIII')==58 and s.romanToInt('MCMXCIV')==1994
s = L['0020'].Solution(); assert s.isValid('()[]{}') and not s.isValid('(]') and not s.isValid('([)]') and s.isValid('{[]}') and not s.isValid('(') and not s.isValid(']')
m = L['0021']; assert tl(m.Solution().mergeTwoLists(mk(m,[1,2,4]), mk(m,[1,3,4]))) == [1,1,2,3,4,4]; assert tl(m.Solution().mergeTwoLists(None, mk(m,[0]))) == [0]
m = L['0083']; assert tl(m.Solution().deleteDuplicates(mk(m,[1,1,2,3,3,3]))) == [1,2,3]
m = L['0141']; a=[m.ListNode(i) for i in range(4)]
for x,y in zip(a,a[1:]): x.next=y
assert not m.Solution().hasCycle(a[0]); a[-1].next=a[1]; assert m.Solution().hasCycle(a[0])
ms = L['0155'].MinStack(); ms.push(-2); ms.push(0); ms.push(-3); assert ms.getMin()==-3; ms.pop(); assert ms.top()==0 and ms.getMin()==-2
st = L['0225'].MyStack(); st.push(1); st.push(2); assert st.top()==2 and st.pop()==2 and not st.empty()
qq = L['0232'].MyQueue(); qq.push(1); qq.push(2); assert qq.peek()==1 and qq.pop()==1 and not qq.empty()
m = L['0234']
for v in [[1,2,2,1],[1,2],[1],[1,2,1],[1,2,3,2,1],[1,2,3]]: assert m.Solution().isPalindrome(mk(m,v)) == (v==v[::-1])
s = L['0290'].Solution(); assert s.wordPattern('abba','dog cat cat dog') and not s.wordPattern('abba','dog cat cat fish') and not s.wordPattern('aaaa','dog cat cat dog') and not s.wordPattern('abba','dog dog dog dog')
s = L['2073'].Solution()
for _ in range(500):
    t = [random.randint(1,6) for _ in range(random.randint(1,8))]; k = random.randrange(len(t))
    assert s.timeRequiredToBuy(t,k) == s.timeRequiredToBuySimulation(t,k)
assert s.timeRequiredToBuy([2,3,2],2)==6 and s.timeRequiredToBuy([5,1,1,1],0)==8
print("ALL OK")
