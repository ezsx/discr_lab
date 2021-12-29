from itertools import *

# вычисление возможных комбинаций из n элементов по k подмножествам
def s(k,n):
    if k ==0:
        return 0
    if k>n:
        return 0
    if k==n:
        return 1
    return s(k-1,n-1) + k*s(k,n-1)

# генерация возмжных разбиений n элементов по k подмножествам
def get_div(k,n):
    lst = []
    for i in range(1,n+1):
        c = 0
        for j in range(k):
            c+=i
            if c <= n:
                lst.append(i)
            else:
                break
    r = set()
    for a in combinations(lst,k):
        #print(a)
        if sum(a)==n:
            r.add(a)
    # print(r)
    rr = list()
    for a in r:
        d = dict()
        for b in a:
            d[b]=d.get(b,0)+1
        # print(d)
        r1 = list()
        for k,v in d.items():
            r1.append((v,k,))
        rr.append(tuple(r1))
    return tuple(rr)

# Класс генератор для одной группы множеств, одинаковго размера
class C:
    def __init__(self,ch,cnt=(0,0,),d=None):
        self._is_has_next=True
        self.cnt = cnt[1] # это сколько символов в этом подмножестве
        self.cntg = cnt[0] # это сколько таких подмножеств
        self.ch=ch
        self.cl=None
        self.cur_comb = []
        self.dict_cmb = []
        self.comb_gen = None
        if ch is None:
            self.dd=set(d)
        else:
            ch.cl=self

    def init_gen(self):
        if self.ch is not None:
            self.dd = set(self.ch.get_rest())
        self.dict_cmb = [a for a in combinations(tuple(self.dd), self.cnt)]
        self.comb_gen = combinations(self.dict_cmb,self.cntg)
        self._is_has_next=True

    def is_has_next(self):
        return self._is_has_next

    def get_rest(self):
        if self.ch is not None:
            rest_c = self.ch.get_rest()
        else:
            rest_c =  self.dd

        r=set()
        for aa in self.cur_comb:
            for bb in aa:
                r= r.union(set(bb))
        rr = rest_c-r
        return rr

    def check(self):
        # надо проверить что в текущем сочетании множетсв
        # ни один символ не повторяется.
        c = dict()
        for set_a in self.cur_comb:
            for b in set_a:
                if c.get(b,-1) == -1:
                    c.update({b:1})
                else:
                    return False
        return True

    def get_next(self):
        try:
            self.cur_comb = next(self.comb_gen)
            while not self.check():
                self.cur_comb = next(self.comb_gen)
        except StopIteration:
            self._is_has_next = False
        if self.cl:
               self.cl.init_gen()
               self.cl.get_next()


    def get_set(self):
        r=[]
        for i in self.cur_comb:
            r.append(set(i))
        return r

# Класс который согласовано управляет   классами C (оркестратор)
class P:

    def __init__(self,razb,d):
        self.c_cnt=[]
        self.c_main=C(None,razb[0],d)
        self.c_main.init_gen()
        self.c_cnt.append(self.c_main)
        c=self.c_main
        for i in range(1,len(razb)):
            c=C(c,razb[i])
            self.c_cnt.append(c)

    def get_next(self):
        self.c_main.get_next()
        while True:
            c = self.c_cnt[len(self.c_cnt) - 1]
            r=[]
            for cc in self.c_cnt:
                r+=cc.get_set()
            yield r
            c.get_next()
            while not c.is_has_next():
                c = c.ch
                if c is None:
                    break
                c.get_next()
            if c is None:
                break

# собственно генератор
# перебирает возможные разбиения на k множества из n элементов и для каждого генерит комбинации
def get_permut_set(k,n,p_dict):
    for div_p in get_div(k,n):
        p = P(div_p, p_dict)
        for a in p.get_next():
            yield a
#
cnt_g = 0
# Кол-во подмножеств
k = 5
# кол-во элементов ( не больше 10)
n = 10
print(" Всего ожидаем ",s(k,n))
for p in get_permut_set(k,n,"abcdefghjk"[:n]):
     cnt_g += 1
     print(p)
print('Всего полученно комбинаций ',cnt_g)
