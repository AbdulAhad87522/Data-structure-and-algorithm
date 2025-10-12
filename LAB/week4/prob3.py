# # Linear time sorting

# def countingsort(a):
#     k = max(a)
#     count = [0] * (k+1)
#     output = [0] * len(a)
#     for i in range(len(a)):
#         count[a[i]] += 1
#     for i in range(1,k + 1):
#         count[i] += count[i - 1]
#     for i in range(len(a) -1 , -1, -1):
#         output[count[a[i]] - 1] = a[i]
#         count[a[i]] -= 1
    
#     return output
        
# a = [5,4,3,3,2,54,56,6,4,3,5,55]
# print("Original:", a)
# print("Sorted:", countingsort(a))


# radix sort

def counting_sort_by_digit(a , exp):
    n = len(a)
    output = [0]*n
    count = [0] * 10
    for i in range(n):
        digit = (a[i] // exp) % 10
        count[digit] = count[digit] + 1
    for i in range(1,10):
        count[i] = count[i] + count[i - 1]
    for i in range(n-1 , -1 , -1):
        digit =(a[i]//exp) % 10
        output[count[digit] -1] = a[i]
        count[digit] = count[digit] - 1
    for i in range(n):
        a[i] = output[i]
    return a
    
def redix_sort(a):
    maxe = max(a)
    exp = 1
    while (maxe//exp) > 0:
        counting_sort_by_digit(a,exp)
        exp = exp*10
    return a


a = [5,3,2,4,5,3,1,3,45,5]
print(redix_sort(a))