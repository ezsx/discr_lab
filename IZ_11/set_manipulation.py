from itertools import *


class C:
    def __init__(self,ch,cnt=0,d=None):
        self._is_has_next=True
        self.cnt = cnt
        self.ch=ch
        self.cl=None
        if ch is None:
            self.dd=set(d)
        else:
            ch.cl=self

    def init_gen(self):
        if self.ch is not None:
            self.dd = self.ch.get_rest()
        self.comb_gen = combinations(tuple(self.dd), self.cnt)

    def is_has_next(self):
        return self._is_has_next

    def get_rest(self):
        return self.dd-set(self.cur_comb)

    def get_next(self):
        try:
           self.cur_comb = self.comb_gen.__next__()
           if self.cl:
               self.cl.init_gen()
               self.cl.get_next()

        except StopIteration:
            self._is_has_next=False

    def get_set(self):
        return set(self.cur_comb)

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
            yield [cc.get_set() for cc in self.c_cnt]
            while not c.is_has_next():
                c = c.ch
                if c is None:
                    break
            if c is None:
                break
            c.get_next()


p=P((6,1,1,1,1,),"abcdefghjk")

for a in p.get_next():
    print(a) # tupple с 5 множествами (разбиениями)
