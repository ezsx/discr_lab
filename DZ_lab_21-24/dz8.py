from math import *

alphabet= ["0", "1", "2", "3"]
wasAutomorfizm: bool = False

matrix1: str = ""
matrix2: str = ""
n: int = 0

def convertToArray(matrix: str):

    result:[(int,[int])] = []
    size = int(sqrt(float(len(matrix))))

    for i in range(size):
        result.append((i, []))
    for i in range(size):
        for j in range(size):
            if (j != i) and (matrix[i * size + j] == "1"):
                if not (j in result[i][1]):
                    result[i][1].append(j)

    # print(result)
    return result

def convertToMatrix(m: [(int, [int])]):
    result = ""
    size = len(m)
    for i in range(size):
        for j in range(size):
            result += j in m[i][1] if "1" else "0"

    return result

def replace(matrix: [(int, [int])], from1: int, to: int):
    result = matrix

    result[from1] = to
    result[to] = from1

    for j in range(len(result)):
        for i in range(len(result[j])):
            if result[j][1][i] == from1:
                result[j][1][i] = to
            elif result[j][1][i] == to:
                result[j][1][i] = from1
    result.sort()
    return result

def printMatrix(matrix: str):
    size = int(sqrt(float(len(matrix))))

    for i in range(size):
        print(matrix[i * size: i * size + size])

def toTransArray(value: str):

    result: [(int, int)] = []

    for i in range(len(value)):
        subArray: [(int, int)] = []
        for j in range(len(value)):
            if int(value[j]) < int(value[i]):
                subArray.append((int(value[i]), int(value[j])))

        subArray.sort()
        result.append(subArray)

    return result

def problem8(i: int, prefix: str):
    global alphabet
    global wasAutomorfizm
    if i == len(alphabet) + 1:
        if not wasAutomorfizm:
            transMatrix = convertToArray(matrix2)

            for p in toTransArray(prefix):
                transMatrix = replace(transMatrix,p[0][1],p[0][0])

            if convertToMatrix(transMatrix) == matrix1:
                wasAutomorfizm = True
    else:
        for i in alphabet:
            if not i in prefix:
                newI = i + "1"
                newPref = prefix + i
                problem8(newI,newPref)


def Problem8():
    global matrix1
    global matrix2
    global alphabet
    print("Problem8:")

    print("Введите размерность матрицы:")
    n = int(input())

    print("Введите первую матрицу:")
    for _ in range(n):
        matrix1 += input()


    print("Введите вторую матрицу:")
    for _ in range(n):
        matrix2 += input()

    alphabet = []
    for i in range(n):
        alphabet.append(str(i))


Problem8()
print(wasAutomorfizm)

# 1 2 3 4    3 2 1 4

# 0 1 1 1    0 0 1 0
# 1 0 0 0 -> 0 0 1 0
# 1 0 0 0    1 1 0 1
# 1 0 0 0    0 0 1 0

# 0 1 0 1    0 0 0 0
# 1 0 0 0 -> 0 0 1 0
# 0 0 0 0    0 1 0 1
# 1 0 0 0    0 0 1 0