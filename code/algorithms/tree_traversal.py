"""Обходы бинарного дерева: DFS в глубину и BFS по уровням."""
from collections import deque


def dfs_preorder(root):
    result = []
    def visit(node):
        if node is not None:
            result.append(node.val)
            visit(node.left)
            visit(node.right)
    visit(root)
    return result


def bfs(root):
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
