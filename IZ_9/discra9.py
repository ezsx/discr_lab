from math import *

def sum(p,k):
    s=0
    for i in range(1,p):
        s+=comb(p,i)*pow(2,(i*(p-i)))*C(i,k-1)
    return s
def C(p,k):
    if k==1:
        return 1
    if k>p:
        return 0
    return (1/k)*sum(p,k)
print(C(8,8))