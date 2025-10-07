import time
import random

def randomarray(size):
    array = [random.randint(0,1000) for i in range(size)]
    return array


# arr1 = [100,3000,40000,50000]    
# f = open(file = "prob7.txt" , mode="w")
# for i in arr1:
#     f.write(str(i) + "\n")
#     print("done")
    
    
    
def buublesort(arr , st , end):
    n= end - st
    for i in range(n - 1):
        for j in range( st ,end - i - 1):
            if(arr[j] > arr[j + 1]):
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
    return arr

def selectionsort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(i+1 , n):
            if(arr[j] < arr[i]):
                arr[j] , arr[i] = arr[i] , arr[j]
    return arr

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

def merge(arr , st , mid , end):
    temp  = []
    i = st 
    j = mid+1
    while(i <= mid and j <= end):
        if(arr[i] <= arr[j]):
            temp.append(arr[i])
            i = i + 1
        else:
            temp.append(arr[j])
            j = j + 1
    while(i <= mid):
        temp.append(arr[i])
        i = i + 1
                
    while(j <= end):
        temp.append(arr[j])
        j = j + 1
    
    for i in range (len(temp)):
        arr[i + st] = temp[i]
    
def mergesort(arr , st , end):
    if(st < end):
        mid = st + (end-st) //2
    
        mergesort(arr, st, mid)
        mergesort(arr, mid+1, end)
        
        merge(arr, st, mid, end)
    return arr

    
f = open(file="prob7.txt" , mode = "r")
lines = f.read()
numbers = []
arr = lines.split()

for i in arr:
    num = int(i)
    numbers.append(num)
    
print(numbers)

for i in range(len(numbers)):
    array = randomarray(numbers[i])
    start_time = 0
    end_time = 0
    run_time= 0
    
    start_time = time.time()
    sorted_array = (buublesort(array, 0,len(array)))
    end_time = time.time()
    run_time = end_time - start_time
    print("runtime of bubblesort for" , i ," iteration", run_time)
    
    start_time = time.time()
    sorted_array = (selectionsort(array))
    end_time = time.time()
    run_time = end_time - start_time
    
    print("runtime of selectionsrt is " , i ," iteration", run_time)
    
    start_time = time.time()
    sorted_array = (insertion(array))
    end_time = time.time()
    run_time = end_time - start_time
    
    print("runtime of insertion sort is " , i ," iteration", run_time)
    
    start_time = time.time()
    sorted_array = (mergesort(array , 0, len(array) - 1))
    end_time = time.time()
    run_time = end_time - start_time
    
    print("runtime of merge sort is " , i ," iteration", run_time)
    
    # print(sorted_array)