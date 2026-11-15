"""AVL-дерево; высота листа 0, дубликаты игнорируются."""


class Node:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None
        self.height = 0


class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return -1 if node is None else node.height

    def get_balance(self, node):
        return 0 if node is None else self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def rotate_right(self, a):
        b, middle = a.left, a.left.right
        b.right, a.left = a, middle
        self.update_height(a)
        self.update_height(b)
        return b

    def rotate_left(self, a):
        b, middle = a.right, a.right.left
        b.left, a.right = a, middle
        self.update_height(a)
        self.update_height(b)
        return b

    def rebalance(self, node):
        if node is None:
            return None
        self.update_height(node)
        balance = self.get_balance(node)
        if balance > 1:
            if self.get_balance(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1:
            if self.get_balance(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node
        return self.rebalance(node)

    def search(self, key):
        cur = self.root
        while cur:
            if key == cur.key:
                return cur
            cur = cur.left if key < cur.key else cur.right
        return None

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        elif node.left is None:
            return node.right
        elif node.right is None:
            return node.left
        else:
            successor = self._min_node(node.right)
            node.key = successor.key
            node.right = self._delete(node.right, successor.key)
        return self.rebalance(node)

    @staticmethod
    def _min_node(node):
        while node.left:
            node = node.left
        return node

    def inorder(self):
        result = []
        def walk(node):
            if node:
                walk(node.left)
                result.append(node.key)
                walk(node.right)
        walk(self.root)
        return result
