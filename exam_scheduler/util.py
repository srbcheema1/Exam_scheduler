from random import randint

def credits_calc(rank):
    try:
        rank = int(rank)
    except:
        raise Exception("Rank should be integer")
    if rank == 0:
        return 9999999

    workratio = {
        1:100,
        2:150,
        3:200,
        4:250,
        5:300,
    }
    return (100*workratio[1])/workratio[rank]

def randomize(arr):
    n = len(arr)
    for i in range(n-1,0,-1):
        j = randint(0,i)
        arr[i],arr[j] = arr[j],arr[i]
    return arr
