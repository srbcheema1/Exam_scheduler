from random import Random
from srblib import SrbJson

work_ratio_template = {
    1:100,
    2:150,
    3:200,
    4:250,
    5:300,
    6:350,
    7:400,
}
work_ratio = SrbJson('~/.config/exam_scheduler/work_ratio.json',work_ratio_template)

def credits_calc(rank,workratio=work_ratio):
    try: rank = int(rank)
    except: raise Exception("Rank should be integer")
    if rank == 0: return 9999999
    return (100*workratio["1"])/workratio[str(rank)]

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

def randomize(arr,seed=None):
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
    return arr

