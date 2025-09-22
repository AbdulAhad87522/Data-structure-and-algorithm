#task 1

# array = [22,2,2,3,4,2,5,4,2]
# x = int(input("Enter the number you want to check"))
# ans = []
# for i in range(0,len(array)):
#     if(array[i] == x):
#         ans.append(i)    
# print(ans)

#task 2

# array = [1,2,3,4,5,6,7,8,8,8,8]
# x = int(input("Enter the number you want to check"))
# ans = []
# index = 0
# for i in range(0,len(array)):
#     if(array[i] == x):
#         ans.append(i)
#         index = i
    
# print(ans)
# print("the loop ran " ,{index})

#task 3

# arrr = list(map(int, input("Enter the array").split()))
# start = 4
# ending = 7
# ans = -99999999999999999999999999999999999
# for i in range (start , ending+1):
#     if(arrr[i] < arrr[i+1]):
#         ans = arrr[i]        
# print(ans)


#task4

# def sorting(arr):
#     for i in range (0 , len(arr) -1):
#         for j in range(0 , (len(arr) - i - 1)):
#             if(arr[j] > arr[j+1]):
#                 arr[j], arr[j+1] = arr[j+1], arr[j]
#     return arr

# inout = list(map(int, input("Enter the array").split()))

# print(sorting(inout))

#task 5

# def stringreverse(arr):
#     arr = list(arr)
#     for i in range(0 , len(arr)):
#         for j in range(0 , len(arr) - i - 1):
#             arr[j], arr[j+1] = arr[j+1], arr[j]
#     return "".join(arr)



# inp = "adbaucasouvauvweuh"
# print(stringreverse(inp))

#task 6

# def sumiteratively(arr):
#     ans = 0
#     for i in range(len(arr)):
#         ans = ans + arr[i]
#     return ans



# ino = list(map(int, input("enter the number: ").split()))
# print(sumiteratively(ino))

#task6 (b)

def sumrecursively(arr):
    