def merge(left , right):
    new = []
    i,j = 0,0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            new.append(left[i])
            i = i + 1
        else:
            new.append(right[j])
            j = j + 1
    new.extend(left[i:])
    new.extend(right[j:])
    return new

def merge_sort(arr):
    n = len(arr)
    if(n <= 1):
       return arr
    mid = len(arr) // 2
    l_half = arr[:mid]
    r_half = arr[mid:]
    l_half = merge_sort(l_half)
    r_half = merge_sort(r_half)
    return merge(l_half, r_half)


arr = [7,6,5,3,23,5,8,9]

print(merge_sort(arr))