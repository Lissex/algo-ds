"""Регрессионные и property-based проверки кода раздела 3."""
import importlib.util
import random
from collections import Counter, deque
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "code"
random.seed(33)


def load(rel):
    path = ROOT / rel
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BST = load("structures/binary_search_tree.py")
AVL = load("structures/avl_tree.py")
HEAP = load("structures/heap.py")
BTREE = load("structures/b_tree.py")
TRIE = load("structures/trie.py")
HEAPSORT = load("algorithms/heap_sort.py")
TRAVERSAL = load("algorithms/tree_traversal.py")
LC = {
    n: load(f"leetcode/{n}_{suffix}.py")
    for n, suffix in [
        ("0100", "same_tree"),
        ("0104", "maximum_depth_of_binary_tree"),
        ("0108", "convert_sorted_array_to_binary_search_tree"),
        ("0109", "convert_sorted_list_to_binary_search_tree"),
        ("0347", "top_k_frequent_elements"),
        ("0543", "diameter_of_binary_tree"),
        ("0653", "two_sum_iv_input_is_a_bst"),
        ("0700", "search_in_a_binary_search_tree"),
        ("0703", "kth_largest_element_in_a_stream"),
        ("0973", "k_closest_points_to_origin"),
    ]
}


def check_bst(node, low=None, high=None):
    if node is None:
        return []
    assert low is None or low < node.val
    assert high is None or node.val < high
    return check_bst(node.left, low, node.val) + [node.val] + check_bst(node.right, node.val, high)


def check_avl(node, low=None, high=None):
    if node is None:
        return -1
    assert low is None or low < node.key
    assert high is None or node.key < high
    lh = check_avl(node.left, low, node.key)
    rh = check_avl(node.right, node.key, high)
    assert abs(lh - rh) <= 1, f"AVL balance broken at {node.key}"
    assert node.height == 1 + max(lh, rh), f"wrong height at {node.key}"
    return node.height


def check_btree(tree):
    t = tree.t
    leaf_depths = set()

    def walk(node, depth, low=None, high=None, is_root=False):
        assert node.keys == sorted(node.keys)
        assert len(node.keys) <= 2 * t - 1
        if is_root:
            assert node.leaf or len(node.keys) >= 1
        else:
            assert len(node.keys) >= t - 1
        assert all(low is None or low < k for k in node.keys)
        assert all(high is None or k < high for k in node.keys)
        if node.leaf:
            assert not node.children
            leaf_depths.add(depth)
            return node.keys[:]
        assert len(node.children) == len(node.keys) + 1
        values = []
        for i, child in enumerate(node.children):
            child_low = low if i == 0 else node.keys[i - 1]
            child_high = high if i == len(node.keys) else node.keys[i]
            values.extend(walk(child, depth + 1, child_low, child_high))
            if i < len(node.keys):
                values.append(node.keys[i])
        return values

    values = walk(tree.root, 0, is_root=True)
    assert len(leaf_depths) <= 1, f"B-tree leaves have different depths: {leaf_depths}"
    return values


def test_bst():
    values = list(range(-80, 81))
    random.shuffle(values)
    tree, ref = BST.BinaryTree(values[0]), {values[0]}
    for value in values[1:]:
        tree.add_node(value)
        ref.add(value)
        assert tree.size == len(ref)
        assert tree.dfs() == sorted(ref)
        assert tree.find(value)
        check_bst(tree.root)
    try:
        tree.add_node(0)
        assert False, "BST must reject duplicate keys"
    except ValueError:
        pass
    random.shuffle(values)
    for value in values:
        assert tree.find(value)
        tree.remove(value)
        ref.remove(value)
        assert tree.size == len(ref)
        assert tree.dfs() == sorted(ref)
        check_bst(tree.root)
    tree.remove(1000)
    assert tree.size == 0 and tree.dfs() == []
    tree.add_node(42)
    assert tree.root.val == 42 and tree.size == 1
    tree.remove(42)
    for fn in (tree.get_min, tree.get_max):
        try:
            fn()
            assert False, "min/max on an empty BST must fail"
        except ValueError:
            pass


def test_avl():
    for _ in range(20):
        values = random.sample(range(-500, 501), 100)
        tree, ref = AVL.AVLTree(), set()
        for value in values:
            tree.insert(value)
            ref.add(value)
            assert tree.inorder() == sorted(ref)
            check_avl(tree.root)
        for value in random.sample(values, 65):
            tree.delete(value)
            ref.remove(value)
            assert tree.inorder() == sorted(ref)
            check_avl(tree.root)
        tree.insert(7)
        tree.insert(7)
        assert tree.inorder().count(7) == 1


def is_heap(values, is_min):
    return all((values[(i - 1) // 2] <= values[i] if is_min else values[(i - 1) // 2] >= values[i])
               for i in range(1, len(values)))


def test_heap():
    for is_min in (False, True):
        for _ in range(20):
            values = [random.randint(-100, 100) for _ in range(random.randrange(0, 80))]
            heap = HEAP.Heap()
            heap._is_min = is_min
            heap.heapify(values)
            ref = values[:]
            assert is_heap(heap.heap, is_min)
            while ref:
                target = min(ref) if is_min else max(ref)
                assert heap.peek() == target
                assert heap.pop() == target
                ref.remove(target)
                assert is_heap(heap.heap, is_min)
            for name, fn in (("peek", heap.peek), ("pop", heap.pop)):
                try:
                    fn()
                    assert False, f"{name} on empty heap must fail"
                except ValueError:
                    pass
            for value in [5, -2, 5, 0]:
                heap.append(value)
                assert is_heap(heap.heap, is_min)


def test_btree():
    try:
        BTREE.BTree(1)
        assert False, "B-tree degree below 2 must be rejected"
    except ValueError:
        pass
    for degree in (2, 3, 4):
        tree, ref = BTREE.BTree(degree), set()
        values = list(range(-180, 181))
        random.shuffle(values)
        for value in values:
            tree.insert(value)
            ref.add(value)
            assert check_btree(tree) == sorted(ref)
            assert tree.search(value) is not None
        for value in values:
            assert tree.search(value) is not None
        assert tree.search(10_000) is None
        for value in values[:20]:
            tree.insert(value)
        assert check_btree(tree) == sorted(ref)


def test_trie():
    trie, ref = TRIE.Trie(), set()
    words = [""] + ["".join(random.choice("abcd") for _ in range(n)) for n in range(1, 9) for _ in range(30)]
    for word in words:
        trie.insert(word)
        ref.add(word)
        assert trie.search(word)
    for _ in range(1200):
        word = random.choice(words + ["missing", "abcx"])
        if random.random() < 0.45:
            assert trie.delete(word) is (word in ref)
            ref.discard(word)
        else:
            trie.insert(word)
            ref.add(word)
        for probe in (word, "", "a", "ab"):
            assert trie.search(probe) is (probe in ref)
            assert trie.start_width(probe) is any(item.startswith(probe) for item in ref)


def test_heap_sort_and_traversals():
    for _ in range(400):
        values = [random.randint(-1000, 1000) for _ in range(random.randrange(0, 100))]
        expected = sorted(values)
        HEAPSORT.heap_sort(values)
        assert values == expected

    class Node:
        def __init__(self, val, left=None, right=None):
            self.val, self.left, self.right = val, left, right

    def make_tree(depth=0):
        if depth >= 7 or random.random() < 0.28:
            return None
        return Node(random.randint(-30, 30), make_tree(depth + 1), make_tree(depth + 1))

    def preorder(node):
        return [] if node is None else [node.val] + preorder(node.left) + preorder(node.right)

    def breadth_first(root):
        if root is None:
            return []
        result, queue = [], deque([root])
        while queue:
            node = queue.popleft()
            result.append(node.val)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return result

    for _ in range(250):
        root = make_tree()
        assert TRAVERSAL.preorder(root) == preorder(root)
        assert TRAVERSAL.bfs_binary_tree(root) == breadth_first(root)
    assert TRAVERSAL.preorder(None) == []
    assert TRAVERSAL.bfs_binary_tree(None) == []


def test_leetcode_trees():
    n100, n104, n108, n109, n543 = (LC[x] for x in ("0100", "0104", "0108", "0109", "0543"))

    same = n100.Solution()
    a = n100.TreeNode(1, n100.TreeNode(2), n100.TreeNode(3))
    b = n100.TreeNode(1, n100.TreeNode(2), n100.TreeNode(3))
    assert same.isSameTree(a, b)
    assert not same.isSameTree(a, n100.TreeNode(1, n100.TreeNode(3), n100.TreeNode(2)))
    assert same.isSameTree(None, None) and not same.isSameTree(a, None)

    depth = n104.Solution()
    assert depth.maxDepth(None) == 0
    assert depth.maxDepth(n104.TreeNode(3, n104.TreeNode(9), n104.TreeNode(20, n104.TreeNode(15), n104.TreeNode(7)))) == 3

    def tree_values(root):
        return [] if root is None else tree_values(root.left) + [root.val] + tree_values(root.right)

    def tree_height(root):
        return 0 if root is None else 1 + max(tree_height(root.left), tree_height(root.right))

    for size in range(0, 80):
        values = list(range(-size, size * 2, 3))[:size]
        root = n108.Solution().sortedArrayToBST(values)
        assert tree_values(root) == values
        assert abs(tree_height(root.left) - tree_height(root.right)) <= 1 if root else not values

        dummy = n109.ListNode()
        tail = dummy
        for value in values:
            tail.next = n109.ListNode(value)
            tail = tail.next
        list_root = n109.Solution().sortedListToBST(dummy.next)
        assert tree_values(list_root) == values
        assert abs(tree_height(list_root.left) - tree_height(list_root.right)) <= 1 if list_root else not values

    diameter = n543.Solution()
    assert diameter.diameterOfBinaryTree(None) == 0
    assert diameter.diameterOfBinaryTree(n543.TreeNode(1, n543.TreeNode(2, n543.TreeNode(4), n543.TreeNode(5)), n543.TreeNode(3))) == 3


def test_leetcode_bst_and_heaps():
    n653, n700, n347, n703, n973 = (LC[x] for x in ("0653", "0700", "0347", "0703", "0973"))

    root = n653.TreeNode(5, n653.TreeNode(3, n653.TreeNode(2), n653.TreeNode(4)), n653.TreeNode(6, None, n653.TreeNode(7)))
    for target in range(0, 18):
        values = [2, 3, 4, 5, 6, 7]
        expected = any(a + b == target for a, b in combinations(values, 2))
        assert n653.Solution().findTarget(root, target) is expected
    assert n653.Solution().findTarget(None, 0) is False

    search_root = n700.TreeNode(4, n700.TreeNode(2, n700.TreeNode(1), n700.TreeNode(3)), n700.TreeNode(7))
    for value in range(0, 9):
        found = n700.Solution().searchBST(search_root, value)
        assert (found.val if found else None) == (value if value in {1, 2, 3, 4, 7} else None)

    topk = n347.Solution()
    for _ in range(250):
        nums = [random.randint(-8, 8) for _ in range(random.randint(1, 60))]
        freq = Counter(nums)
        k = random.randint(1, len(freq))
        result = topk.topKFrequent(nums, k)
        threshold = sorted(freq.values(), reverse=True)[k - 1]
        assert len(result) == len(set(result)) == k
        assert all(value in freq and freq[value] >= threshold for value in result)

    for k in range(1, 9):
        initial = [random.randint(-50, 50) for _ in range(20)]
        stream = n703.KthLargest(k, initial)
        values = initial[:]
        for _ in range(100):
            value = random.randint(-50, 50)
            values.append(value)
            assert stream.add(value) == sorted(values, reverse=True)[k - 1]

    closest = n973.Solution()
    for _ in range(250):
        points = [[random.randint(-30, 30), random.randint(-30, 30)] for _ in range(random.randint(1, 40))]
        k = random.randint(1, len(points))
        result = closest.kClosest(points, k)
        distances = [x * x + y * y for x, y in points]
        threshold = sorted(distances)[k - 1]
        assert len(result) == k
        assert all(point in points and point[0] ** 2 + point[1] ** 2 <= threshold for point in result)


if __name__ == "__main__":
    for test in (
        test_bst,
        test_avl,
        test_heap,
        test_btree,
        test_trie,
        test_heap_sort_and_traversals,
        test_leetcode_trees,
        test_leetcode_bst_and_heaps,
    ):
        test()
        print(f"OK {test.__name__}")
    print("SECTION 3 OK")
