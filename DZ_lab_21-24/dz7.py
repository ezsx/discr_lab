from math import *

p = 5

q = 5

edgeCount = 10

iter1 = 0


# C(C(p, 2), q) = C(C(5, 2), 5) = C(10, 5) = 2 * 7 * 2 * 9 = 63 * 4 = 252




def generateMatrix(of: str):

    offset = 0

    result = ""

    size = int(ceil(sqrt(len(of))))
    for i in  range(size):
        for j in range(i):
            # result += of[of.index(of.startIndex, offsetBy: (size - 1) * (j) - (j * (j + 1)) / 2 + i - 1 + 10)..<of.index(of.startIndex, offsetBy: (size - 1) * (j) - (j * (j + 1)) / 2 + i + 10)] + " "
            result += (of[int((size - 1) * (j) - (j * (j + 1)) / 2 + i - 1 + 10):int((size - 1) * (j) - (j * (j + 1)) / 2 + i + 10)] + " ")
            result += "0 "

        for j in range(i + 1,size):
            result += str(of[ int(j - i - 1 + offset) : int(j - i - 1 + offset + 1)])
        offset += size - i - 1
        result += "\n"
    return result

def problem7_1(i, k, prefix,f):

    newI = i + 1
    newK = k + 1
    if i == edgeCount + 1:
        f.write(generateMatrix(prefix + prefix) + "\n")
    elif (edgeCount - i + 1) - (q - k) == 0:
        newPref = prefix + "1"
        problem7_1(newI,newK,newPref,f)
    else:
        if k < 5:
            newPref = prefix + "1"
            problem7_1(newI, newK, newPref,f)
        newPref = prefix + "0"
        problem7_1(newI, k,  newPref,f)

# 1024

def problem7_2(i, prefix,f):
    newI = i + 1
    if i == edgeCount + 1:
        f.write(generateMatrix(prefix + prefix) + "\n")
    else:
        pref1 = prefix + "0"
        pref2 = prefix + "1"
        problem7_2(newI,pref1,f)
        problem7_2(newI, pref2,f)


def Problem7():
    print("Problem7:")
    f = open('workfile1', 'w')
    problem7_1(1, 0, "",f)
    f.close()

    f = open('workfile1', 'w')
    problem7_2(1,"",f)
    f.close()

Problem7()
