from math import *
# 9.2.1. Сколько существует связных графов из 8 вершин?
def fac(n):
    if n == 0:
        return 1
    return fac(n-1) * n

def G(n):
    return pow(2,(n*(n-1))/2)

def sum(n):
    s=0
    for i in range(1,n):
        s+=i*comb(n,i)*Gcon(i)*G(n-i)
    return s

def Gcon(n):
    return G(n)-(1/n)*sum(n)

print(Gcon(5))