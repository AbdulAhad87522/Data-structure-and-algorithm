
import random
import time

#problem 2

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

#problem 3

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

# def buublesort(arr , st , end):
#     n= end - st
#     for i in range(n - 1):
#         for j in range( st ,end - i - 1):
#             if(arr[j] > arr[j + 1]):
#                 temp = arr[j]
#                 arr[j] = arr[j + 1]
#                 arr[j + 1] = temp
#     return arr


# arr = [random.randint(0, 1000) for i in range(30000)]
# start_time = time.time()
# sorted_array = buublesort(arr , 0 , len(arr))

# f = open(file="bubblesort.txt" , mode="w")
# for i in sorted_array:
#     f.write(str(i) + "\n")
# end_time= time.time()

# run_time= end_time - start_time

# print(run_time)

#priblem 6

# def selectionsort(arr):
#     n = len(arr)
#     for i in range(n-1):
#         for j in range(i+1 , n):
#             if(arr[j] < arr[i]):
#                 arr[j] , arr[i] = arr[i] , arr[j]
#     return arr

# # arr = [random.randint(0, 1000) for i in range(30000)]
# arr = [random.randint(0, 1000) for i in range(30000)]
# start_time = time.time()
# sorted_array = selectionsort(arr )

# f = open(file="selectionsort.txt" , mode="w")
# for i in sorted_array:
#     f.write(str(i) + "\n")
# end_time= time.time()

# run_time= end_time - start_time

# print(run_time)