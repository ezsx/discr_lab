from math import *
# 9.2.2. Сколько существует эйлеровых графов из 8 вершин?
def W(p):
    return pow(2, (p*(p-1)/2))

def summ(p):
    s=0
    for i in range(1,p):
        s+=comb(p,i)*E(i)*W(p-i)
    return s
def E(p):
    return W(p)-(1/p)*summ(p)

print(E(5))
