# 9.1.4. Дано множество A = { a, a, a, a, a, a, a, a, a, a}. Сколько существует способов
# разбить его на 5 именованных множеств?
from math import *
def count(n,k):
    kof=int(n/k)
    s=0
    s1=0
    for i in range(1,n+1):
        s+=1
        if s%kof==0:
            s1+=1
    print(s+s1)
    print(kof-1)
    return comb(s+s1-1,kof-1)

print(count(10,5))