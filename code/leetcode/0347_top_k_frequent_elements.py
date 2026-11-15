"""347. Top K Frequent Elements"""
from collections import Counter
import heapq


class Solution:
    def topKFrequent(self, nums, k):
        return [value for value, _ in heapq.nlargest(k, Counter(nums).items(), key=lambda item: item[1])]
