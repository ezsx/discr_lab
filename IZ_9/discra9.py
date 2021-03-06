
from math import *

# 9.2.3. Сколько существует графов из 8 вершин, которые можно раскрасить в 8
# цветов?
ss="_"
def sum(p,k,m):
    s=0
    for i in range(1,p):
        s+=comb(p,i)*pow(2,(i*(p-i)))*C(i,k-1,m)
    return s
def C(p,k,m):
    m += 1
    if k==1:
        return 1
    if k>p:
        return 0

    print("(",m,ss*k*2,")","C(%d,%d)=%d" % (p, k, (1 / k) * sum(p, k,m)))
    return (1/k)*sum(p,k,m)

print(C(8,8,0))