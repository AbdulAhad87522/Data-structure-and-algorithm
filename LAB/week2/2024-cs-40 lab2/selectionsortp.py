def selectionsort(arr):
    n= len(arr)
    for i in range(n-1):
        for j in range(i+ 1 , n):
            if arr[j]< arr[i]:
               arr[i] , arr[j] = arr[j] , arr[i]
    return arr


arr = [8,7,6,5,4,3,2,34,5,6,7,6]
print(selectionsort(arr))