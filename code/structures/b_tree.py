"""B-дерево минимальной степени t (код преподавателя, приведён в порядок)."""


class BTreeNode:
    def __init__(self, leaf=True):
        self.keys = []
        self.children = []
        self.leaf = leaf


class BTree:
    def __init__(self, t=2):
        if t < 2:
            raise ValueError("Минимальная степень t должна быть не меньше 2")
        self.t = t
        self.root = BTreeNode()

    def search(self, key):
        node = self.root
        while True:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if i < len(node.keys) and node.keys[i] == key:
                return node
            if node.leaf:
                return None
            node = node.children[i]

    def insert(self, key):
        if self.search(key):
            return
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(root)
            self.root = new_root
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, key)
        else:
            self._insert_non_full(root, key)

    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(key)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
            return
        while i >= 0 and key < node.keys[i]:
            i -= 1
        i += 1
        if len(node.children[i].keys) == 2 * self.t - 1:
            self._split_child(node, i)
            if key > node.keys[i]:
                i += 1
        self._insert_non_full(node.children[i], key)

    def _split_child(self, parent, index):
        t = self.t
        full = parent.children[index]
        right = BTreeNode(leaf=full.leaf)
        middle = full.keys[t - 1]
        right.keys, full.keys = full.keys[t:], full.keys[:t - 1]
        if not full.leaf:
            right.children, full.children = full.children[t:], full.children[:t]
        parent.keys.insert(index, middle)
        parent.children.insert(index + 1, right)

    def inorder(self):
        result = []
        def walk(node):
            for i, key in enumerate(node.keys):
                if not node.leaf:
                    walk(node.children[i])
                result.append(key)
            if not node.leaf:
                walk(node.children[-1])
        walk(self.root)
        return result
