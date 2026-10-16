# Время O(n): один проход по формуле. Память O(1).
# (Моделирование очередью: время O(n * max(tickets)), память O(n).)

from typing import List


class Solution:
    def timeRequiredToBuy(self, tickets: List[int], k: int) -> int:
        # Человек i до ухода человека k купит:
        #  - не больше tickets[k] билетов, если стоит до k (включительно)
        #  - не больше tickets[k] - 1, если стоит после k
        time = 0
        for i, t in enumerate(tickets):
            if i <= k:
                time += min(t, tickets[k])
            else:
                time += min(t, tickets[k] - 1)
        return time

    def timeRequiredToBuySimulation(self, tickets: List[int], k: int) -> int:
        # Прямое моделирование очереди (FIFO)
        from collections import deque
        q = deque(range(len(tickets)))
        tickets = tickets[:]
        time = 0
        while q:
            i = q.popleft()
            tickets[i] -= 1
            time += 1
            if tickets[i] == 0:
                if i == k:
                    return time
            else:
                q.append(i)
        return time
