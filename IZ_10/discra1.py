from itertools import *

d = ['a','b','c','d','e','f','g','h','j','k']
#длина слова
n = 7
#кол-во повторений 3-ей буквы
kn = 1

# на входе строка ar , строка хх
# получаем сочетания (не повторяющиеся !) элементов строки ar и хх
def permut(ar,xx):
    # строка очевидно тормозит, как перебороть, не понял
    def concat():
        return ''.join(ar[0:i])+xx[0]+''.join(ar[i:len(ar)])

    # протаскиваем по одному символу xx, через ar пока все символы из xx (рекурсивно) не закончатся
    if len(xx)>1:
        x =xx[0]
        for i in range(len(ar)):
            if ar[i]==x:
                continue
            #рекурсивно вызываем, отрезая первый символ
            yield from  permut(concat(),xx[1:])
        # и надо еще  просто добавить в конец строки
        yield from permut(''.join(ar)+xx[0],xx[1:])
    else:
        x =xx[0]
        for i in range(len(ar)):
            if ar[i]==x:
                continue
            yield concat()
        yield ''.join(ar)+xx[0]


def comb_c(ccc,f):
    g_cnt = 0
    # в полученно ccc элемент 1 и 2 повторяются 2 раза
    # 3 элемент повторяется kn раз
    #мы берем три буквыб,которые встречаются обязательно в слове и рассчитываем сколько
    #встретится таких же букв в слове еще
    permut_str = ''.join(ccc[:2])+''.join([ccc[2]]*(kn-1))
    #словарь без букв, которые сюда пришли и объязательны
    dd = list(set(d)-set(ccc))
    # строка перебора по оставшемуся словарю
    str_var = ''.join(dd)
    #сколько еще не хватает до n?
    c = n - 2*2 - kn
    #получаем комбинации
    for x in combinations(str_var,c):
        # теперь каждую комбинацию дополняем постоянной частью что пришла сюда
        str_var_c = ''.join(x)
        str_cv = ''.join(ccc) + str_var_c
        # так как потом будем дополнять еще 2 буквы по разу и kn без одной
        #nc = n-2-kn+1
        nc=len(str_cv)
        #получаем все возможные сочетания из текущей комбинации
        for y in permutations(str_cv, nc):
            # домнажаем на массив входных букв
            for y1 in permut(y,tuple(permut_str)):
                f.write(''.join(y1)+'\n')
                g_cnt = g_cnt +1
                # print(''.join(y1))
    return g_cnt


def m_c(f):
    cnt = 0
    gg_cnt = 0
    #Сколько всего комбинаций из 3 объязательных бука
    # может быть на словаре ...
    for ccc in combinations(d,3):
        print(ccc)
        cnt += 1
        gg_cnt += comb_c(ccc,f)
        if gg_cnt > 10**7:
            print("Может не хватить места на диске, превышен лимит комбинаций !!!")
            break
    print ("получено всего комбинаций ",gg_cnt)



def main():
    if kn>n-4:
        raise Exception("кол-во повторений буквы  не может быть больше %d"%(n-4))
    if kn<1:
        raise Exception("кол-во повторений буквы не может быть меньше 1"%(kn))
    if n>4+kn+len(d)-3:
        raise Exception("n не может быть больше %d " % (kn+len(d)+1))
    f =  open('workfile','w')
    m_c(f)
    f.close()

# main()


for x in permut('asdf','q1'):
    print(x)