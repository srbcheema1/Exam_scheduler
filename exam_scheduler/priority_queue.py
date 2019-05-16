import heapq
import queue

class EmptyQueue(Exception):
    pass

class PriorityQueue:
    def __init__(self, data=None, key=lambda x:0):
        self.empty = True
        self.key = key
        if data:
            self._data = [(key(item), item) for item in data]
            heapq.heapify(self._data)
            self.empty = False
        else:
            self._data = []

    def sync(self):
        heapq.heapify(self._data)

    def push(self, item):
        heapq.heappush(self._data, (self.key(item), item))
        self.empty = False

    def pop(self):
        if(len(self._data) == 0): raise EmptyQueue('queue empty !! unable to pop')
        ret = heapq.heappop(self._data)[1]
        if(len(self._data) == 0): self.empty = True
        return ret

    def top(self):
        if(len(self._data) == 0): raise EmptyQueue('queue empty !! unable to top')
        return self._data[0][1]

    def __len__(self):
        return len(self._data)

    def __str__(self):
        arr = [x[1] for x in self._data]
        return arr.__str__()

class Queue:
    def __init__(self, data=None):
        self.empty = True
        if data:
            self._data = queue.Queue()
            for item in data:
                self._data.put(item)
            self.empty = False
        else:
            self._data = []

    def push(self, item):
        self._data.put(item)
        self.empty = False

    def pop(self):
        if(self._data.qsize() == 0): raise EmptyQueue('queue empty !! unable to pop')
        ret = self._data.get()
        if(self._data.qsize() == 0): self.empty = True
        return ret

    def top(self):
        if(self._data.qsize() == 0): raise EmptyQueue('queue empty !! unable to top')
        return self._data.get()

    def __len__(self):
        return self._data.qsize()

    def __str__(self):
        arr = []
        while self._data.qsize:
            arr.append(self._data.get())
        for item in arr:
            self._data.put(item)
        return arr.__str__()
