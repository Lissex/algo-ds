"""543. Diameter of Binary Tree"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


class Solution:
    def diameterOfBinaryTree(self, root):
        diameter = 0
        def height(node):
            nonlocal diameter
            if node is None:
                return 0
            left, right = height(node.left), height(node.right)
            diameter = max(diameter, left + right)
            return 1 + max(left, right)
        height(root)
        return diameter
