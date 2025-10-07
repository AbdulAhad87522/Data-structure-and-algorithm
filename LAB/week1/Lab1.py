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

# def sumrecursively(arr):

#task7

# def columnwisesum(Mat):
#     row = len(Mat)
#     col = len (Mat[0])
#     ans = [0] * col
#     for i in range(col):
#         for j in range(row):
#             ans[i] = ans[i] + Mat[j][i]
#     return ans   
        
        
# Mat = [1,2,3],[4,5,6],[1,2,3]
# print(columnwisesum(Mat))


# def rowwisesum(Mat):
#     row = len(Mat[0])
#     col = len(Mat)
#     ans = [0] * row
#     for i in range(col):
#         for j in range(row):
#             ans[i] = ans[i] + Mat[i][j]
#     return ans


# Mat = [1,2,3],[4,5,6],[1,2,3]
# print(rowwisesum(Mat))

#task 8

# def sortedmerge(arr1 , arr2):
#     for i in range(len(arr2)):
#         arr1.append(arr2[i])
#     for i in range(len(arr1) - 1):
#         for j in range((len(arr1) - i - 1)):
#             if(arr1[j] > arr1[j+1]):
#                 arr1[j] , arr1[j+1] = arr1[j+1] , arr1[j]
#     return arr1

# arr1 = [1 ,2,3,4,4]
# arr2 = [6,4,2,2]
# print(sortedmerge(arr1 , arr2))

#task 9

# def Palindromerecursive(str):
#     if(len(str) < 1):
#         return str
#     else:
#         return Palindromerecursive(str[1:]) + str[0]
        
# str = "ahad"
# print(Palindromerecursive(str))

#task 10

def sort10(arr):
    arr.sort()
    neg_arr = []
    pos_arr = []
    for i in range(len(arr)):
        if(arr[i] < 0):
            neg_arr.append(arr[i])
        else:
            pos_arr.append(arr[i])
    # return neg_arr
    i = 0 
    j = 0
    result = []
    while(i < len(neg_arr) or j< len(pos_arr)):
        result.append(neg_arr[i])
        result.append(pos_arr[j])
        i = i + 1
        j = j + 1
    return result
arr = [1,5,7,3,3,5,12,33,2,-20,-9,-9,-98]
print(sort10(arr))