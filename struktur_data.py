from collections import deque..........


class Queue:
    
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue kosong, tidak bisa dequeue")
        return self._items.popleft()

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)


class PriorityQueue:

    def __init__(self):
        self._heap = []  # setiap elemen: (key, item)

    def is_empty(self):
        return len(self._heap) == 0

    def __len__(self):
        return len(self._heap)

    def insert(self, item, key):
        self._heap.append((key, item))
        self._heapify_up(len(self._heap) - 1)

    def extract_min(self):
        if self.is_empty():
            raise IndexError("PriorityQueue kosong, tidak bisa extract_min")
        self._swap(0, len(self._heap) - 1)
        _, item = self._heap.pop()
        if not self.is_empty():
            self._heapify_down(0)
        return item

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _heapify_up(self, i):
        while i > 0 and self._heap[i][0] < self._heap[self._parent(i)][0]:
            p = self._parent(i)
            self._swap(i, p)
            i = p

    def _heapify_down(self, i):
        n = len(self._heap)
        while True:
            kiri, kanan = self._left(i), self._right(i)
            terkecil = i
            if kiri < n and self._heap[kiri][0] < self._heap[terkecil][0]:
                terkecil = kiri
            if kanan < n and self._heap[kanan][0] < self._heap[terkecil][0]:
                terkecil = kanan
            if terkecil == i:
                break
            self._swap(i, terkecil)
            i = terkecil
