def indertionsortarr(arr):
    n = len(arr)
    for i in range(1,n):
        key = arr[i]
        j = i - 1
        while j>= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j= j - 1
        arr[j+1] = key
    return arr


arr = [6,5,4,3,2,1,3,4,5,6,8,6,5,4,44,4,34,3,32,2,2]
print(indertionsortarr(arr))        