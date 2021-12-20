from itertools import *


class C:
    def __init__(self,ch,cnt=(0,0,),d=None):
        self._is_has_next=True
        self.cnt = cnt[0] # это сколько символов в этом подмножестве
        self.cntg = cnt[1] # это сколько таких подмножеств
        self.ch=ch
        self.cl=None
        self.cur_comb = []
        if ch is None:
            self.dd=set(d)
        else:
            ch.cl=self

    def init_gen(self):
        self._is_has_next = True
        if self.ch is not None:
            self.dd = set(self.ch.get_rest())
        self.comb_gen = combinations(tuple(self.dd), self.cnt)

    def is_has_next(self):
        return self._is_has_next

    def get_rest(self):
        if self.ch is not None:
            rest_c = self.ch.get_rest()
        else:
            rest_c =  self.dd

        r=set()
        for aa in self.cur_comb:
           r= r.union(set(aa))
        rr = rest_c-r
        return rr

    def get_next(self):
        self.cur_comb.clear()
        for i in range(self.cntg):
            try:
                self.cur_comb.append(self.comb_gen.__next__())
            except StopIteration:
                self._is_has_next = False
                break
        if self.cl:
               self.cl.init_gen()
               self.cl.get_next()


    def get_set(self):
        r=[]
        for i in self.cur_comb:
            r.append(set(i))
        return r

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

divided_arrs = ((6,1,1,1,1),(5,2,1,1,1),(4,3,1,1,1),(4,2,2,1,1),(3,3,2,1,1),(3,2,2,2,1),(2,2,2,2,2))

#p=P((6,1,1,1,1,),"abcdefghjk")
#p=P(((6,1,),(1,4,),), "abcdefghjk")
a1=P(((6,1,),(1,4,)), "abcdefghjk")
a2=P(((5,1,),(2,1,),(1,3,)), "abcdefghjk")
a3=P(((4,3,),(3,1,),(1,3,)), "abcdefghjk")
a4=P(((4,1,),(2,2,),(1,2,)), "abcdefghjk")
a5=P(((3,2,),(2,1,),(1,2,)), "abcdefghjk")
a6=P(((3,1,),(2,3,),(1,1,)), "abcdefghjk")
a7=P(((2,5,),), "abcdefghjk")
p =P(((5,1,),(2,1,),(1,3,)), "abcdefghjk")
c=0
pp=[a1,a2,a3,a4,a5,a6,a7]
for ll in pp:
    for a in ll.get_next():
        c+=1
        print(c)
        print(a) # tupple с 5 множествами (разбиениями)