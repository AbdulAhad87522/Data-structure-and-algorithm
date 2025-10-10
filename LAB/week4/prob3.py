# Linear time sorting

def countingsort(a):
    k = max(a)
    count = [0]* (k+1)
    output = [0] * (len(a))
    for i in range(len(a)):
        j = (a[i])
        count[j] += 1
        
    for j in range(1,k + 1):
        count[j] += count[j -1]
        
    for i in range(len(a)-1, -1,-1):
        j = a[i]
        count[j] -= 1
        output[count[j]] = a[i]
    return output




a = [5,4,3,3,2,54,56,6,4,3,5,55]
print(countingsort(a))