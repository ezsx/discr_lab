#9.1.3. Дано множество A = { a, a, a, a, a, a, a, a, a, a}. Сколько существует способов
#разбить его на 5 неименованных множеств?

def P_(k,n):
    s=0
    for i in range(1,k+1):
        s+=P(i,n)
    return s

def P(k,n):
    if k==n:
        return 1
    if k==1:
        return 1
    if k>n:
        return 0
    if k==2:
        return int(n/2)
    return P_(k,n-k)

print(P_(5,10))