import numpy as np 
array = np.zeros([10])
print(array)

array2d = [[0 for x in range(4)] for x in range (3)]
print (array2d)

str = [1,2,4,5,5]
for x in range(len(str)):
    print(str[x])
     

arr = [1,2,3,4,5,6]
print(arr[:2])
print(arr[3:])
print(arr[-2])
print(arr[1:3])

#example 1.5 using np
import numpy as np
array = []
min = 0
max = 20
n = 5
for i in range(0,n):
        num = random.randint(min,max)
    array. append(num)