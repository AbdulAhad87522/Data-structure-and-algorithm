# # 1

# def printmatrix(a, starting_index , rows , column):
#     ans = []
#     start_row , start_col = starting_index
#     for i in range(start_row , start_row+rows):
#         row = []
#         for j in range(start_col , start_col + column):
#             row.append(a[i][j])
#         ans.append(row)
#     return ans


# a = [[1,2,3,4],
#      [4,3,2,1],
#      [7,6,5,4],
#      [56,34,2,2]]
# print(printmatrix(a, (2,1), 2, 3))

# 2

# def addmatrice(a,b):
#     if(len(a) != len(b) or len(a[0]) != len(b[0])):
#         print("bothe the matrices should be of equal size")
#         return
#     ans = []
#     for i in range(len(a)):
#         row = []
#         for j in range(len(a[i])):
#             row.append(a[i][j] + b[i][j]) 
#         ans.append(row)
#     return ans


# a = [[1,2,3,4],
#      [4,3,2,1],
#      [7,6,5,4],
#      [56,34,2,2]]
# b = [[3,2,1,2],
#      [3,2,4,3],
#      [3,54,6,4],
#      [7,6,5,4]]


# print(addmatrice(a, b))

# 3

def partialaddmatrices(a, b, start, size):
    start_row , start_col = start
    ans = []
    for i in range(start_row, start_row + size):
        row = []
        for j in range(start_col , start_col+size):
            row.append(a[i][j] + b[i][j])
        ans.append(row)
    return ans

a = [[1,2,3,4],
     [4,3,2,1],
     [7,6,5,4],
     [56,34,2,2]]
b = [[3,2,1,2],
     [3,2,4,3],
     [3,54,6,4],
     [7,6,5,4]]
print(partialaddmatrices(a, b, (2,1), 2))

