"""700. Search in a Binary Search Tree"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


class Solution:
    def searchBST(self, root, val):
        while root and root.val != val:
            root = root.left if val < root.val else root.right
        return root
