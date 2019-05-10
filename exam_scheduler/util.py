from random import Random
from srblib import Tabular


def fabricate(arr,seed=5):
    seed = int(seed)
    if seed >= len(arr)/2: seed = len(arr)//3
    ret = []
    i = seed
    while i > 0:
        j = i - 1
        while j < len(arr):
            ret.append(arr[j])
            j += seed
        i -= 1
    return ret


def fabricate_adv(arr,key,seed=5):
    lists = dict()
    for item in arr:
        if not key(item) in lists:
            lists[key(item)] = [item]
            continue
        lists[key(item)].append(item)
    ret = []
    for k in lists:
        ret.extend(fabricate(lists[k],seed))
    return ret


def randomize(arr,seed=5):
    r = Random()
    if seed: r.seed(str(seed))
    arr = fabricate(arr,7)
    n = len(arr)
    for i in range(0,n-1):
        j = r.randint(i,n-1)
        arr[i],arr[j] = arr[j],arr[i]
    for i in range(n-1,0,-1):
        j = r.randint(0,i)
        arr[i],arr[j] = arr[j],arr[i]
    r.shuffle(arr)
    return arr


class Response:
    def __init__(self,execption=None):
        self.__message = []
        self.exception = execption

    def addMessage(self, msg):
        self.__message.append(msg)
        return self

    def __str__(self):
        ans = ""
        # if len(self.__message) > 0:
            # ans += "[ERROR]\n\n"
        ans += '\n'.join(self.__message)
        # if len(self.__message) > 0:
            # ans += "\n[NOTE] Row nums are not exact, Empty rows are not counted\n"
        return ans

    def __bool__(self):
        return len(self.__message)==0 and not self.exception

    def safe(self):
        if self.exception:
            print(Tabular([[str(self)]]))
            raise self.exception
        return bool(self)

    def json(self):
        return {
            'message':str(self),
            'status':bool(self)
        }
