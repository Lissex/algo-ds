"""Бинарное дерево поиска, исправленная версия кода преподавателя."""


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self, root=None):
        self.root = None if root is None else Node(root)
        self.size = 0 if root is None else 1

    def add_node(self, val):
        if self.root is None:
            self.root = Node(val)
            self.size = 1
            return
        cur = self.root
        while True:
            if val == cur.val:
                raise ValueError(f"node {val} already in tree")
            side = "left" if val < cur.val else "right"
            child = getattr(cur, side)
            if child is None:
                setattr(cur, side, Node(val))
                self.size += 1
                return
            cur = child

    def find(self, val):
        cur = self.root
        while cur:
            if val == cur.val:
                return True
            cur = cur.left if val < cur.val else cur.right
        return False

    def remove(self, val):
        self.root, removed = self._remove(self.root, val)
        if removed:
            self.size -= 1
        return removed

    def _remove(self, node, val):
        if node is None:
            return None, False
        if val < node.val:
            node.left, removed = self._remove(node.left, val)
            return node, removed
        if val > node.val:
            node.right, removed = self._remove(node.right, val)
            return node, removed
        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True
        successor = self._min_node(node.right)
        node.val = successor.val
        node.right, _ = self._remove(node.right, successor.val)
        return node, True

    @staticmethod
    def _min_node(node):
        while node.left:
            node = node.left
        return node

    def count_nodes(self):
        return self.size

    def bfs(self):
        if self.root is None:
            return []
        from collections import deque
        result, queue = [], deque([self.root])
        while queue:
            node = queue.popleft()
            result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    def dfs(self):
        result = []
        def visit(node):
            if node:
                visit(node.left)
                result.append(node.val)
                visit(node.right)
        visit(self.root)
        return result

    def get_max(self):
        if self.root is None:
            raise ValueError("empty tree")
        cur = self.root
        while cur.right:
            cur = cur.right
        return cur.val

    def get_min(self):
        if self.root is None:
            raise ValueError("empty tree")
        cur = self.root
        while cur.left:
            cur = cur.left
        return cur.val
