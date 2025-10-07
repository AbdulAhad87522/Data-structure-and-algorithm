#problem 2

import time
import random

def insertion(arr):
    n= len(arr)
    for i in range(1 ,  n):
        key = arr[i]
        j = i-1
        while(j >= 0 and key < arr[j]):
            arr[j + 1] = arr[j]
        j = j - 1
        arr[j+1] = key
    
    return arr


arr = [random.randint(0, 1000) for i in range(30000)]
start_time = time.time()
sorted_array = insertion(arr )

f = open(file="insertionsort.txt" , mode="w")
for i in sorted_array:
    f.write(str(i) + "\n")
end_time= time.time()

run_time= end_time - start_time

print(run_time)