"""653. Two Sum IV - Input is a BST"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


class Solution:
    def findTarget(self, root, k):
        seen = set()
        def visit(node):
            if node is None:
                return False
            if k - node.val in seen:
                return True
            seen.add(node.val)
            return visit(node.left) or visit(node.right)
        return visit(root)
