# 9.1.5. Построить все подстановки на множестве цифр, содержащих 5 независимых
# цикла.
def C(n,k):
    if n==0 and k==0:
        return 1
    if k==0 or n==0:
        return 0
    #print("C(%d,%d)" % (n,k))
    #print(C(n-1,k-1)+(n-1)*C(n-1,k))
    return C(n-1,k-1)+(n-1)*C(n-1,k)
print(C(10,5))