import heapq

class PriorityQueue:
    def __init__(self, data=None, key=lambda x:x):
        self.empty = True
        self.key = key
        if data:
            self._data = [(key(item), item) for item in data]
            heapq.heapify(self._data)
            self.empty = False
        else:
            self._data = []

    def push(self, item):
        heapq.heappush(self._data, (self.key(item), item))
        self.empty = False

    def pop(self):
        if(len(self._data) == 0): raise Exception('queue empty !! unable to pop')
        ret = heapq.heappop(self._data)[1]
        if(len(self._data) == 0): self.empty = True
        return ret

    def top(self):
        if(len(self._data) == 0): raise Exception('queue empty !! unable to top')
        ret = heapq.heappop(self._data)[1]
        heapq.heappush(self._data, (self.key(ret), ret))
        return ret

    def __len__(self):
        return len(self._data)

    def __str__(self):
        arr = [x[1] for x in self._data]
        return arr.__str__()
