#problem 5

import time
import random

def buublesort(arr , st , end):
    n= end - st
    for i in range(0,n-1):
        for j in range( st ,end-i-1):
            if(arr[j] > arr[j + 1]):
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
    return arr


arr = [random.randint(0, 30) for i in range(30)]
start_time = time.time()
sorted_array = buublesort(arr , 0 , len(arr))
print (sorted_array)

""" f = open(file="bubblesort.txt" , mode="w")
for i in sorted_array:
    f.write(str(i) + "\n")
end_time= time.time()

run_time= end_time - start_time

print(run_time)"""