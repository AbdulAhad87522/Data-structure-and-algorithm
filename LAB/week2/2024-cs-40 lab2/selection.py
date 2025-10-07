#priblem 6

import time
import random

def selectionsort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(i+1 , n):
            if(arr[j] < arr[i]):
                arr[j] , arr[i] = arr[i] , arr[j]
    return arr

# arr = [random.randint(0, 1000) for i in range(30000)]
arr = [random.randint(0, 1000) for i in range(30000)]
start_time = time.time()
sorted_array = selectionsort(arr )

f = open(file="selectionsort.txt" , mode="w")
for i in sorted_array:
    f.write(str(i) + "\n")
end_time= time.time()

run_time= end_time - start_time

print(run_time)