from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        cur = head
        while cur and cur.next:
            if cur.val == cur.next.val:    # дубликат стоит сразу за cur (список отсортирован)
                cur.next = cur.next.next   # выкидываем его, cur не двигаем
            else:
                cur = cur.next
        return head
