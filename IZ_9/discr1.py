s="_"
# 9.1.1. Дано множество A = { a, b, c, d, e, f, g, h, j, k}. Сколько существует способов
# разбить его на 5 неименованных множеств?
def S(k,n,m):
    m+=1
    print("(",m,s*m,")","S(%d,%d)=" % (k, n),"S(%d, %d)+%d*S(%d, %d)" % (k - 1, n - 1,k, k, n - 1))
    if k > n:
        print("S(%d,%d)=0" % (k, n))
        return 0
    if k == n:
        print("S(%d,%d)=1" % (k, n))
        return 1
    if k == 1:
        print("S(%d,%d)=1" % (k, n))
        return 1

    return S(k-1, n-1,m)+k*S(k, n-1,m)
m = 0
print(S(5,10,m))