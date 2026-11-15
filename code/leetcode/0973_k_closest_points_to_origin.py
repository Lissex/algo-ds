"""973. K Closest Points to Origin"""
import heapq


class Solution:
    def kClosest(self, points, k):
        return heapq.nsmallest(k, points, key=lambda point: point[0] ** 2 + point[1] ** 2)
