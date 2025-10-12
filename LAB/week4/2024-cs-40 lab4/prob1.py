import random
import time
def partition(a,p,r):
    x = a[r]
    i = p-1
    for j in range(p,r):
        if(a[j] <= x):
            i= i+1
            a[i] , a[j] = a[j] , a[i]
    a[i+1] , a[r] = a[r] , a[i+1]
    return i+1

def quicksort(a , q , r):
    if(q<r):
         p=partition(a, q, r)
         quicksort(a, q, p-1)
         quicksort(a, p+1, r)
    return a
a = [random.randint(0, 10000000) for i in range(300000)]
start = time.time()
print(quicksort(a, 0, len(a) - 1))
end = time.time()
print(end - start)
