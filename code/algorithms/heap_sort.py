"""Heapsort по возрастанию, на месте, O(n log n) времени и O(1) памяти."""


def heap_sort(arr):
    # Сначала строим max-heap, затем фиксируем максимумы справа налево.
    n = len(arr)

    def sift_down(root, end):
        # end — граница кучи; элементы справа уже отсортированы.
        while 2 * root + 1 < end:
            child = 2 * root + 1
            if child + 1 < end and arr[child] < arr[child + 1]:
                child += 1
            if arr[root] >= arr[child]:
                return
            arr[root], arr[child] = arr[child], arr[root]
            root = child

    # Листья уже являются кучами, поэтому начинаем с последнего родителя.
    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n)
    for end in range(n - 1, 0, -1):
        # Переносим корневой максимум в конец активной части массива.
        arr[0], arr[end] = arr[end], arr[0]
        sift_down(0, end)
