# у ноды всегда k + 1 детей, k - кол-во ключей узла
class BTreeNode:
    def __init__(self, leaf = True):
        self.keys = []
        self.children = []
        self.leaf = leaf
        
class BTree:
    """B-дерево минимальной степени t. Дубликаты ключей игнорируются."""
    def __init__(self, t=2):
        if t < 2:
            raise ValueError("Минимальная степень t должна быть не меньше 2")
        self.t = t
        self.root = BTreeNode()

    def search(self, key): # Поиск
        return self._search(self.root, key) # Начинает проверку с корня

    def _search(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]: 
            i += 1  # Происходит поиск диапазона 
        if i < len(node.keys) and node.keys[i] == key:
            return node
        if node.leaf:
            return None
        return self._search(node.children[i], key) # Рекурсивно запускаем поиск для диапазона, который нашли

    def insert(self, key):
        if self.search(key) is not None:
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
        middle_key = full.keys[t - 1]

        right = BTreeNode(leaf=full.leaf)
        right.keys = full.keys[t:]
        full.keys = full.keys[:t - 1]

        if not full.leaf:
            right.children = full.children[t:]
            full.children = full.children[:t]

        parent.keys.insert(index, middle_key)
        parent.children.insert(index + 1, right)

    def delete(self, key):
        self._delete(self.root, key)
        if not self.root.leaf and len(self.root.keys) == 0:
            self.root = self.root.children[0]

    def _delete(self, node, key):
        t = self.t
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and node.keys[i] == key:
            if node.leaf:
                node.keys.pop(i)
            else:
                self._delete_from_internal(node, i)
            return

        if node.leaf:
            return

        if len(node.children[i].keys) == t - 1:
            self._fill_child(node, i)
            if i > len(node.keys):
                i = len(node.keys)
        self._delete(node.children[i], key)

    def _delete_from_internal(self, node, index):
        key = node.keys[index]
        left = node.children[index]
        right = node.children[index + 1]

        if len(left.keys) >= self.t:
            predecessor = self._get_predecessor(left)
            node.keys[index] = predecessor
            self._delete(left, predecessor)
        elif len(right.keys) >= self.t:
            successor = self._get_successor(right)
            node.keys[index] = successor
            self._delete(right, successor)
        else:
            self._merge(node, index)
            self._delete(left, key)

    def _get_predecessor(self, node):
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1]

    def _get_successor(self, node):
        while not node.leaf:
            node = node.children[0]
        return node.keys[0]

    def _fill_child(self, parent, index):
        if index > 0 and len(parent.children[index - 1].keys) >= self.t:
            self._borrow_from_previous(parent, index)
        elif (index < len(parent.children) - 1
              and len(parent.children[index + 1].keys) >= self.t):
            self._borrow_from_next(parent, index)
        elif index < len(parent.children) - 1:
            self._merge(parent, index)
        else:
            self._merge(parent, index - 1)

    def _borrow_from_previous(self, parent, index):
        child = parent.children[index]
        sibling = parent.children[index - 1]
        child.keys.insert(0, parent.keys[index - 1])
        parent.keys[index - 1] = sibling.keys.pop()
        if not sibling.leaf:
            child.children.insert(0, sibling.children.pop())

    def _borrow_from_next(self, parent, index):
        child = parent.children[index]
        sibling = parent.children[index + 1]
        child.keys.append(parent.keys[index])
        parent.keys[index] = sibling.keys.pop(0)
        if not sibling.leaf:
            child.children.append(sibling.children.pop(0))

    def _merge(self, parent, index):
        child = parent.children[index]
        sibling = parent.children[index + 1]
        child.keys.append(parent.keys.pop(index))
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.children.extend(sibling.children)
        parent.children.pop(index + 1)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        for i, key in enumerate(node.keys):
            if not node.leaf:
                self._inorder(node.children[i], result)
            result.append(key)
        if not node.leaf:
            self._inorder(node.children[len(node.keys)], result)

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        print("  " * level + str(node.keys))
        for child in node.children:
            self.print_tree(child, level + 1)
