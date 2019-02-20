from random import randint
from srblib import SrbJson

work_ratio_template = {
    1:100,
    2:150,
    3:200,
    4:250,
    5:300,
}
work_ratio = SrbJson('~/.config/exam_scheduler/work_ratio.json',work_ratio_template)

def credits_calc(rank,workratio=work_ratio):
    try: rank = int(rank)
    except: raise Exception("Rank should be integer")
    if rank == 0: return 9999999
    return (100*workratio["1"])/workratio[str(rank)]

def randomize(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(0,n-1):
        j = randint(i,n-1)
        arr[i],arr[j] = arr[j],arr[i]
    for i in range(n-1,0,-1):
        j = randint(0,i)
        arr[i],arr[j] = arr[j],arr[i]
    return arr
