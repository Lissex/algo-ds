# Время O(n): заяц либо доходит до конца, либо догоняет черепаху в цикле.
# Память O(1): два указателя (решение через set заняло бы O(n)).

from typing import Optional


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        # Алгоритм Флойда «черепаха и заяц»
        slow = fast = head
        while fast and fast.next:
            slow = slow.next           # 1 шаг
            fast = fast.next.next      # 2 шага
            if slow is fast:           # заяц догнал черепаху — есть цикл
                return True
        return False                   # заяц дошёл до конца — цикла нет
