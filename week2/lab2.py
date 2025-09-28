#problem 3

import random
import time


# def merge(arr , st , mid , end):
#     temp  = []
#     i = st 
#     j = mid+1
#     while(i <= mid and j <= end):
#         if(arr[i] <= arr[j]):
#             temp.append(arr[i])
#             i = i + 1
#         else:
#             temp.append(arr[j])
#             j = j + 1
#     while(i <= mid):
#         temp.append(arr[i])
#         i = i + 1
                
#     while(j <= end):
#         temp.append(arr[j])
#         j = j + 1
    
#     for i in range (len(temp)):
#         arr[i + st] = temp[i]
        
    
    
#     # return arr
    
    
# def mergesort(arr , st , end):
#     if(st < end):
#         mid = st + (end-st) //2
    
#         mergesort(arr, st, mid)
#         mergesort(arr, mid+1, end)
        
#         merge(arr, st, mid, end)
#     return arr


# arr = [random.randint(0, 1000) for i in range(30000)]
# start_time = time.time()
# sorted_arr = mergesort(arr, 0, len(arr) - 1)
# end_time = time.time()

# f = open(file = 'test.txt' , mode= "w")
# for i in sorted_arr:
#     f.write(str(sorted_arr[i])+ "\n")

# run_time = end_time - start_time

# print(run_time)


#problem 5

def buublesort(arr , st , end):
    for i in range(st , end - 1):
        for j in range( 0 ,end - i - 1):
            if(arr[j] > arr[j + 1]):
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
    return arr


arr = [random.randint(0, 1000) for i in range(30000)]
start_time = time.time()
sorted_array = buublesort(arr , 0 , len(arr))

f = open(file="bubblesort.txt" , mode="w")
for i in sorted_array:
    f.write(str(sorted_array[i]) + "\n")
end_time= time.time()

run_time= end_time - start_time

print(run_time)

#priblem 6

