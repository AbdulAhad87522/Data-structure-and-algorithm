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

def addmatrice(a,b):
    if(len(a) != len(b) or len(a[0]) != len(b[0])):
        print("bothe the matrices should be of equal size")
        return
    ans = []
    for i in range(len(a)):
        row = []
        for j in range(len(a[i])):
            row.append(a[i][j] + b[i][j]) 
        ans.append(row)
    return ans


# a = [[1,2,3,4],
#      [4,3,2,1],
#      [7,6,5,4],
#      [56,34,2,2]]
# b = [[3,2,1,2],
#      [3,2,4,3],
#      [3,54,6,4],
#      [7,6,5,4]]

c = [[1,2,3,2],
     [3,1,3,1],
     [7,6,5,4]]
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


#4:
def MatMul(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        print("Error: Number of columns in A must equal number of rows in B")
        return None

    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]

    return C


A = [
    [1, 2, 3],
    [4, 5, 6]
]

B = [
    [7, 8],
    [9, 10],
    [11, 12]
]

C = MatMul(A, B)

for row in C:
    print(row)


#5:

def MatAdd(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def MatSub(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C


def MatMulRecursive(A, B):
    n = len(A)

    if n == 1:
        return [[A[0][0] * B[0][0]]]

    mid = n // 2

    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]

    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]

    C11 = MatAdd(MatMulRecursive(A11, B11), MatMulRecursive(A12, B21))
    C12 = MatAdd(MatMulRecursive(A11, B12), MatMulRecursive(A12, B22))
    C21 = MatAdd(MatMulRecursive(A21, B11), MatMulRecursive(A22, B21))
    C22 = MatAdd(MatMulRecursive(A21, B12), MatMulRecursive(A22, B22))

    new_matrix = []
    for i in range(mid):
        new_matrix.append(C11[i] + C12[i])
    for i in range(mid):
        new_matrix.append(C21[i] + C22[i])

    return new_matrix


A = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]]

B = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

C = MatMulRecursive(A, B)
for row in C:
    print(row)

#6:
    def MatAdd(A, B):
        n = len(A)
        C = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = A[i][j] + B[i][j]
        return C
    
    def MatSub(A, B):
        n = len(A)
        C = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                C[i][j] = A[i][j] - B[i][j]
        return C
    
    
    def MatMulStrassen(A, B):
        n = len(A)
    
        if n == 1:
            return [[A[0][0] * B[0][0]]]
    
        mid = n // 2
    
        A11 = [row[:mid] for row in A[:mid]]
        A12 = [row[mid:] for row in A[:mid]]
        A21 = [row[:mid] for row in A[mid:]]
        A22 = [row[mid:] for row in A[mid:]]
    
        B11 = [row[:mid] for row in B[:mid]]
        B12 = [row[mid:] for row in B[:mid]]
        B21 = [row[:mid] for row in B[mid:]]
        B22 = [row[mid:] for row in B[mid:]]
    
        M1 = MatMulStrassen(MatAdd(A11, A22), MatAdd(B11, B22))
        M2 = MatMulStrassen(MatAdd(A21, A22), B11)
        M3 = MatMulStrassen(A11, MatSub(B12, B22))
        M4 = MatMulStrassen(A22, MatSub(B21, B11))
        M5 = MatMulStrassen(MatAdd(A11, A12), B22)
        M6 = MatMulStrassen(MatSub(A21, A11), MatAdd(B11, B12))
        M7 = MatMulStrassen(MatSub(A12, A22), MatAdd(B21, B22))
    
        C11 = MatAdd(MatSub(MatAdd(M1, M4), M5), M7)
        C12 = MatAdd(M3, M5)
        C21 = MatAdd(M2, M4)
        C22 = MatAdd(MatSub(MatAdd(M1, M3), M2), M6)
    
        new_matrix = []
        for i in range(mid):
            new_matrix.append(C11[i] + C12[i])
        for i in range(mid):
            new_matrix.append(C21[i] + C22[i])
    
        return new_matrix
    
    
    A = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]
    
    B = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]
    
    C = MatMulStrassen(A, B)
    
    for row in C:
        print(row)