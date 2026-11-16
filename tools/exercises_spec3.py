"""Задания тренажёра для билетов раздела 3."""

COMMON3 = r'''
def make_tree(values, cls=None):
    if cls is None: cls = __user_ns__.get("TreeNode")
    if cls is None: raise AssertionError("для этой задачи нужен TreeNode")
    if not values or values[0] is None: return None
    nodes = [None if v is None else cls(v) for v in values]
    kids = iter(nodes[1:])
    for node in nodes:
        if node is not None:
            node.left = next(kids, None); node.right = next(kids, None)
    return nodes[0]

def inorder_values(node):
    if node is None: return []
    return inorder_values(node.left) + [node.val] + inorder_values(node.right)

def tree_depth(node):
    if node is None: return 0
    return 1 + max(tree_depth(node.left), tree_depth(node.right))

def list_node(values):
    dummy = ListNode(); tail = dummy
    for value in values:
        tail.next = ListNode(value); tail = tail.next
    return dummy.next

def assert_bst(node, lo=None, hi=None):
    if node is None: return
    if lo is not None: assert lo < node.val
    if hi is not None: assert node.val < hi
    assert_bst(node.left, lo, node.val); assert_bst(node.right, node.val, hi)

def assert_avl(node):
    if node is None: return -1
    lh, rh = assert_avl(node.left), assert_avl(node.right)
    assert abs(lh-rh) <= 1, f"узел {node.key}: баланс нарушен"
    assert node.height == max(lh, rh)+1, f"узел {node.key}: высота некорректна"
    return node.height
'''

METHOD_EX = {
    "bst-add": ("structures/binary_search_tree.py", ["BinaryTree.add_node"]),
    "bst-remove": ("structures/binary_search_tree.py", ["BinaryTree.remove", "BinaryTree._remove"]),
    "avl-add": ("structures/avl_tree.py", ["AVLTree.insert", "AVLTree._insert"]),
    "heapify": ("structures/heap.py", ["Heap.heapify"]),
    "heap-add": ("structures/heap.py", ["Heap.append"]),
    "heap-remove": ("structures/heap.py", ["Heap.pop"]),
    "trie-add": ("structures/trie.py", ["Trie.insert"]),
    "trie-delete": ("structures/trie.py", ["Trie.delete"]),
    "avl-rotate": ("structures/avl_tree.py", ["AVLTree.rotate_right", "AVLTree.rotate_left", "AVLTree.rebalance"]),
}

DEMO = {
    "bst-add": 'tree = BinaryTree(8)\nfor x in [3, 10, 1, 6]: tree.add_node(x)\nprint(tree.dfs(), tree.size)  # [1, 3, 6, 8, 10], 5',
    "bst-remove": 'tree = BinaryTree(8)\nfor x in [3, 10, 1, 6, 14, 4, 7, 13]: tree.add_node(x)\ntree.remove(3)\nprint(tree.dfs(), tree.size)',
    "avl-add": 'tree = AVLTree()\nfor x in [10, 20, 30, 40, 50, 25]: tree.insert(x)\nprint(tree.inorder(), tree.root.key)',
    "heapify": 'h = Heap()\nh.heapify([3, 1, 6, 5, 2, 4])\nprint(h.heap, h.peek())  # max-heap, максимум 6',
    "heap-add": 'h = Heap()\nh.heapify([8, 5, 3])\nh.append(10)\nprint(h.heap, h.peek())  # максимум 10',
    "heap-remove": 'h = Heap()\nh.heapify([8, 5, 3, 10])\nprint(h.pop(), h.peek())  # 10, затем 8',
    "trie-add": 't = Trie()\nt.insert("cat"); t.insert("car")\nprint(t.search("cat"), t.start_width("ca"))',
    "trie-delete": 't = Trie()\nt.insert("car"); t.insert("cart")\nprint(t.delete("car"), t.search("cart"), t.search("car"))',
    "avl-rotate": 'tree = AVLTree()\nfor x in [30, 20, 10]: tree.insert(x)\nprint(tree.root.key, tree.inorder())  # 20, [10, 20, 30]',
}

TESTS = {
"bst-add": r'''
@test("вставка и inorder")
def _():
    t=BinaryTree(8); [t.add_node(x) for x in [3,10,1,6]]; eq(t.dfs(),[1,3,6,8,10]); eq(t.size,5)
@test("корень и дубликат")
def _():
    t=BinaryTree(5); eq(t.root.val,5); raises(ValueError,lambda:t.add_node(5))
''',
"bst-remove": r'''
@test("удаление листа, одного и двух детей")
def _():
    t=BinaryTree(8)
    for x in [3,10,1,6,14,4,7,13]: t.add_node(x)
    for x in [1,14,3,8]: t.remove(x); assert_bst(t.root)
    eq(t.dfs(),[4,6,7,10,13]); eq(t.size,5)
@test("отсутствующий ключ")
def _():
    t=BinaryTree(2); t.remove(9); eq(t.size,1)
''',
"avl-add": r'''
@test("повороты и отсортированный порядок")
def _():
    t=AVLTree()
    for x in [10,20,30,40,50,25]: t.insert(x); assert_avl(t.root)
    eq(t.inorder(),[10,20,25,30,40,50])
@test("дубликат игнорируется")
def _():
    t=AVLTree(); t.insert(4); t.insert(4); eq(t.inorder(),[4])
''',
"heapify": r'''
@test("max-heap")
def _():
    h=Heap(); h.heapify([3,1,6,5,2,4])
    eq(h.heap[0],6)
    for i in range(1,len(h.heap)): assert h.heap[(i-1)//2] >= h.heap[i]
@test("min-heap, пустой и singleton")
def _():
    for a in [[],[7],[8,2,5,1,9]]:
        h=Heap(); h._is_min=True; h.heapify(a)
        for i in range(1,len(h.heap)): assert h.heap[(i-1)//2] <= h.heap[i]
''',
"heap-add": r'''
@test("добавление в max-heap")
def _():
    h=Heap(); h.heapify([7,4,5]); h.append(9); eq(h.peek(),9)
    for i in range(1,len(h.heap)): assert h.heap[(i-1)//2] >= h.heap[i]
@test("min-heap")
def _():
    h=Heap(); h._is_min=True; h.heapify([7,4,5]); h.append(2); eq(h.peek(),2)
''',
"heap-remove": r'''
@test("извлекает значения по убыванию")
def _():
    h=Heap(); h.heapify([3,1,6,5,2,4]); eq([h.pop() for _ in range(6)],[6,5,4,3,2,1])
@test("ошибка на пустой куче")
def _(): raises(ValueError,lambda:Heap().pop())
''',
"trie-add": r'''
@test("поиск и префикс")
def _():
    t=Trie(); t.insert("car"); t.insert("cart"); eq(t.search("car"),True); eq(t.search("ca"),False); eq(t.start_width("ca"),True)
@test("пустое слово и дубликат")
def _():
    t=Trie(); t.insert(""); t.insert(""); eq(t.search(""),True)
''',
"trie-delete": r'''
@test("удаление одного из общих префиксов")
def _():
    t=Trie(); t.insert("car"); t.insert("cart"); eq(t.delete("car"),True); eq(t.search("car"),False); eq(t.search("cart"),True)
@test("несуществующее слово")
def _(): eq(Trie().delete("no"),False)
''',
"avl-rotate": r'''
@test("LL, RR, LR и RL")
def _():
    for vals in ([30,20,10],[10,20,30],[30,10,20],[10,30,20]):
        t=AVLTree()
        for v in vals: t.root=t._insert(t.root,v); assert_avl(t.root)
        eq(t.root.key,20)
@test("ребалансировка без поворота")
def _():
    t=AVLTree()
    for v in [8,3,10,1,6]: t.root=t._insert(t.root,v)
    t.root=t.rebalance(t.root)
    eq(t.inorder(),[1,3,6,8,10]); assert_avl(t.root)
''',
}

FUNCTION_EX = {
"heap-sort": ("algorithms/heap_sort.py", "def heap_sort(arr):\n    # TODO: отсортируй массив на месте\n    pass", 'a = [5, 1, 4, 2, 8]\nheap_sort(a)\nprint(a)  # [1, 2, 4, 5, 8]', r'''
@test("обычный массив")
def _():
    a=[5,1,4,2,8]; heap_sort(a); eq(a,[1,2,4,5,8])
@test("пустой, дубликаты, отрицательные")
def _():
    for a in [[],[1],[3,3,1,2],[-4,0,-9,2]]:
        expected=sorted(a); heap_sort(a); eq(a,expected)
'''),
}

PROBLEM_FILES = {"lc-100":"leetcode/0100_same_tree.py", "lc-104":"leetcode/0104_maximum_depth_of_binary_tree.py", "lc-109":"leetcode/0109_convert_sorted_list_to_binary_search_tree.py", "lc-653":"leetcode/0653_two_sum_iv_input_is_a_bst.py", "lc-347":"leetcode/0347_top_k_frequent_elements.py", "lc-703":"leetcode/0703_kth_largest_element_in_a_stream.py", "lc-973":"leetcode/0973_k_closest_points_to_origin.py", "lc-700":"leetcode/0700_search_in_a_binary_search_tree.py", "lc-543":"leetcode/0543_diameter_of_binary_tree.py", "lc-108":"leetcode/0108_convert_sorted_array_to_binary_search_tree.py"}

PROBLEM_STARTER = {
"lc-100": ('class TreeNode:\n    def __init__(self, val=0, left=None, right=None): self.val, self.left, self.right = val, left, right\n\nclass Solution:\n    def isSameTree(self, p, q):\n        # TODO\n        pass', 'p=TreeNode(1,TreeNode(2),TreeNode(3)); q=TreeNode(1,TreeNode(2),TreeNode(3))\nprint(Solution().isSameTree(p,q))'),
"lc-104": ('class TreeNode:\n    def __init__(self, val=0, left=None, right=None): self.val, self.left, self.right = val, left, right\n\nclass Solution:\n    def maxDepth(self, root):\n        # TODO\n        pass', 'root=TreeNode(3,TreeNode(9),TreeNode(20,TreeNode(15),TreeNode(7)))\nprint(Solution().maxDepth(root))'),
"lc-109": ('class ListNode:\n    def __init__(self,val=0,next=None): self.val,self.next=val,next\nclass TreeNode:\n    def __init__(self,val=0,left=None,right=None): self.val,self.left,self.right=val,left,right\nclass Solution:\n    def sortedListToBST(self, head):\n        # TODO\n        pass', 'head=ListNode(-10,ListNode(-3,ListNode(0,ListNode(5,ListNode(9)))))\nprint(Solution().sortedListToBST(head).val)  # корень 0'),
"lc-653": ('class TreeNode:\n    def __init__(self,val=0,left=None,right=None): self.val,self.left,self.right=val,left,right\nclass Solution:\n    def findTarget(self, root, k):\n        # TODO\n        pass', 'root=TreeNode(5,TreeNode(3,TreeNode(2),TreeNode(4)),TreeNode(6,None,TreeNode(7)))\nprint(Solution().findTarget(root,9))'),
"lc-347": ('class Solution:\n    def topKFrequent(self, nums, k):\n        # TODO\n        pass', 'print(Solution().topKFrequent([1,1,1,2,2,3],2))'),
"lc-703": ('class KthLargest:\n    def __init__(self, k, nums):\n        # TODO\n        pass\n    def add(self, val):\n        # TODO\n        pass', 'k=KthLargest(3,[4,5,8,2])\nprint(k.add(3), k.add(5))'),
"lc-973": ('class Solution:\n    def kClosest(self, points, k):\n        # TODO\n        pass', 'print(Solution().kClosest([[1,3],[-2,2]],1))'),
"lc-700": ('class TreeNode:\n    def __init__(self,val=0,left=None,right=None): self.val,self.left,self.right=val,left,right\nclass Solution:\n    def searchBST(self, root, val):\n        # TODO\n        pass', 'root=TreeNode(4,TreeNode(2,TreeNode(1),TreeNode(3)),TreeNode(7))\nprint(Solution().searchBST(root,2).val)'),
"lc-543": ('class TreeNode:\n    def __init__(self,val=0,left=None,right=None): self.val,self.left,self.right=val,left,right\nclass Solution:\n    def diameterOfBinaryTree(self, root):\n        # TODO\n        pass', 'root=TreeNode(1,TreeNode(2,TreeNode(4),TreeNode(5)),TreeNode(3))\nprint(Solution().diameterOfBinaryTree(root))'),
"lc-108": ('class TreeNode:\n    def __init__(self,val=0,left=None,right=None): self.val,self.left,self.right=val,left,right\nclass Solution:\n    def sortedArrayToBST(self, nums):\n        # TODO\n        pass', 'root=Solution().sortedArrayToBST([-10,-3,0,5,9])\nprint(root.val)'),
}

PROBLEM_TESTS = {
"lc-100": r'''@test("одинаковые структуры и значения")\ndef _(): eq(Solution().isSameTree(make_tree([1,2,3]),make_tree([1,2,3])),True)\n@test("разная структура")\ndef _(): eq(Solution().isSameTree(make_tree([1,2]),make_tree([1,None,2])),False)\n@test("пустые")\ndef _(): eq(Solution().isSameTree(None,None),True)''',
"lc-104": r'''@test("глубина 3")\ndef _(): eq(Solution().maxDepth(make_tree([3,9,20,None,None,15,7])),3)\n@test("пустое дерево")\ndef _(): eq(Solution().maxDepth(None),0)''',
"lc-109": r'''@test("сбалансированное дерево из списка")\ndef _():\n root=Solution().sortedListToBST(list_node([-10,-3,0,5,9])); eq(inorder_values(root),[-10,-3,0,5,9]); assert abs(tree_depth(root.left)-tree_depth(root.right))<=1\n@test("пустой список")\ndef _(): eq(Solution().sortedListToBST(None),None)''',
"lc-653": r'''@test("пара найдена")\ndef _(): eq(Solution().findTarget(make_tree([5,3,6,2,4,None,7]),9),True)\n@test("пары нет и нельзя использовать один узел дважды")\ndef _(): eq(Solution().findTarget(make_tree([1]),2),False)''',
"lc-347": r'''@test("частоты")\ndef _(): eq(set(Solution().topKFrequent([1,1,1,2,2,3],2)),{1,2})\n@test("отрицательные числа")\ndef _(): eq(set(Solution().topKFrequent([-1,-1,2,2,2],1)),{2})''',
"lc-703": r'''@test("поток примера")\ndef _():\n k=KthLargest(3,[4,5,8,2]); eq([k.add(x) for x in [3,5,10,9,4]],[4,5,5,8,8])\n@test("начало с пустого потока")\ndef _():\n k=KthLargest(1,[]); eq(k.add(-3),-3)''',
"lc-973": r'''@test("ближайшая точка")\ndef _(): eq(Solution().kClosest([[1,3],[-2,2]],1),[[-2,2]])\n@test("k равно числу точек")\ndef _(): eq(set(map(tuple,Solution().kClosest([[3,3],[5,-1],[-2,4]],3))),{(3,3),(5,-1),(-2,4)})''',
"lc-700": r'''@test("узел найден")\ndef _(): eq(Solution().searchBST(make_tree([4,2,7,1,3]),2).val,2)\n@test("значение отсутствует")\ndef _(): eq(Solution().searchBST(make_tree([4,2,7]),5),None)''',
"lc-543": r'''@test("диаметр проходит через корень")\ndef _(): eq(Solution().diameterOfBinaryTree(make_tree([1,2,3,4,5])),3)\n@test("одно дерево и пустое")\ndef _(): eq(Solution().diameterOfBinaryTree(make_tree([1])),0); eq(Solution().diameterOfBinaryTree(None),0)''',
"lc-108": r'''@test("сбалансированное BST")\ndef _():\n a=[-10,-3,0,5,9]; root=Solution().sortedArrayToBST(a); eq(inorder_values(root),a); assert abs(tree_depth(root.left)-tree_depth(root.right))<=1\n@test("пустой массив")\ndef _(): eq(Solution().sortedArrayToBST([]),None)''',
}
