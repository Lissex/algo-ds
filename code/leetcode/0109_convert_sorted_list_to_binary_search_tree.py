"""109. Convert Sorted List to Binary Search Tree"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


class Solution:
    def sortedListToBST(self, head):
        values = []
        while head:
            values.append(head.val)
            head = head.next
        def build(lo, hi):
            if lo >= hi:
                return None
            mid = (lo + hi) // 2
            return TreeNode(values[mid], build(lo, mid), build(mid + 1, hi))
        return build(0, len(values))
