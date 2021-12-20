from itertools import *
import time

d = ['a','b','c','d','e','f']
n=5

class Position:

    def __init__(self,pos_l,p_word=None):
        # pos_l это ссылка на старшую (левую) позицию
        if pos_l:
            # ссылка на старшую (левую) позицию
            self.pos_l = pos_l
            # индекс позиции в этом слове (слева на право)
            self.ind_x = pos_l.ind_x+1
            # слово в котором представлена эта позиция
            self.word:Word = pos_l.word
        # Здесь когда pos_l = None, а слово задано.
        # Это случай самой старшей позиции (самая левая)
        else:
            #(в слове крайняя левая, самая старшая, тут будет None)
            self.pos_l = None
            self.ind_x = 0
            self.word:Word = p_word
        # индекс текущего символа в данной позиции из словаря слова
        self.cur_ind_c = self.word.get_next_char_idx(-1)


    # выбрать следующий разрешенный на сейчас символ
    def next(self,pos_r=None):
        # если текуший символ из словаря не последний
        if self.cur_ind_c < self.word.len_dict -1:
            #возьмем следующий разрешенный символ из словаря в этом слове
            idx = self.word.get_next_char_idx(self.cur_ind_c)
        else:
            # если последний, то с него надо уйти по любому
            # чтобы освободить его для других позиций
            self.word.cur_cnt[self.cur_ind_c] -=1
            idx = -1

        if idx < 0:
            # Если след. символа нет, надо пойти с низу словаря
            # но сначала спросим разрешния у левой позиции, если она есть
            if self.pos_l:
                # т.е. вызваем тот же самый метод, в котором находимся
                # но для левой позиции, выглядит как рекурсия .
                if self.pos_l.next(self):
                    #левая позиция смогла переключится, и мы переключимся
                    self.cur_ind_c =  self.word.get_next_char_idx(-1)
                    return self.cur_ind_c >= 0
                else:
                    #похоже приехали! не смогли найти свободный символ для этой позиции
                    # или входные данные кривые или ошибка в логике.
                    # Другой причины быть в этой части кода нет ((
                    return False
            else:
                # здесь будем, когда уже потребовалось пойти с низу словаря (самый первый в списке - самый нижний)
                # для самой левой (старшей) позиции, т.е. приехали, перебор закончен
                self.word.stop()
                return False
        else:
            self.cur_ind_c = idx
            return True
        return False


    def __str__(self):
        return self.word.dict_list[self.cur_ind_c]


    def __repr__(self):
        return self.word.dict_list[self.cur_ind_c]

class Word:

    def __init__(self,p_dict:str,p_dict_cnt_in_wrd:dict,p_len_word=0):
        # длина слов которые надо генерить на переданных данных
        self.len_word = p_len_word
        # словарь
        self.dict_list = list(p_dict)
        self.len_dict = len(self.dict_list)
        # сколько раз символы в словаре должны  повторятся, по умолчанию 1
        self.dict_cnt_list = [p_dict_cnt_in_wrd.get(c,1) for c in self.dict_list]
        # текущее число повторов в слове для символов из словаря
        self.cur_cnt = [0]*len(self.dict_list)
        #Позиции list
        self.pos_list = self.init_pos()
        #самая крайняя правая (последня в слове позиция)
        self.pos_last = self.pos_list[len(self.pos_list)-1]
        self.is_has_next = True
        self._word = tuple([p for p in self.pos_list])

    def init_pos(self):
        # надо нагенерить позиции таким образом
        # чтобы получилось самое младшее слово из возможных
        if self.len_word == 0:
            # генерим макс возможное
            s = 0
            for i in self.dict_cnt_list:
                s+=i
            self.len_word = s
        p  = [Position(None,self)]
        for i in range(1,self.len_word):
            p.append(Position(p[i-1]))
        self.pos_last = p[len(p)-1]
        return p

    def next(self):
        # переключится на след. слово
        self.is_has_next = self.pos_last.next()

    # выдает индекс след. символа разрешенного в слове после
    # символа индекс которого p_ind_c
    def get_next_char_idx(self,p_ind_c):
        # for idx_c in range(p_ind_c+1,self.len_dict):
        idx_c = p_ind_c+1
        while idx_c < self.len_dict:
            if self.cur_cnt[idx_c] < self.dict_cnt_list[idx_c]:
                # если сменить получилось
                self.cur_cnt[idx_c]+=1
                if p_ind_c >= 0:
                    self.cur_cnt[p_ind_c]-=1
                return idx_c
            idx_c +=1
        if p_ind_c < 0:
            #что-то пошло не так, надо было перейти на новый символ
            # но свободных нет ((
            self.word.stop()
        else:
            # с текущего символа уходим по любому, так как
            # вынуждены вернуть -1
            self.cur_cnt[p_ind_c] -= 1
        return -1

    def stop(self):
        self.is_has_next = False

    def get_word(self):
        # return  [self.dict_list[p.cur_ind_c] for p in self.pos_list]
        return  self._word


def permut_word(p_dict:str,p_dict_cnt_in_wrd:dict,p_len_word=0):
    w = Word(p_dict,p_dict_cnt_in_wrd,p_len_word)
    while w.is_has_next:
        yield w.get_word()
        # yield '1'
        w.next()



def comb_c(ccc,f):
    g_cnt = 0
    f.write("без повтора")
    # в полученно ccc элемент 1 и 2 повторяются 2 раза
    # 3 элемент повторяется kn раз
    #словарь без букв, которые сюда пришли и объязательны
    dd = list(set(d)-set(ccc))
    print(dd)
    # строка перебора по оставшемуся словарю
    str_var = ''.join(dd)
    #сколько еще не хватает до n?
    c = 5 - 2
    dict_n = {ccc[0]:2}
    #получаем комбинации
    for x in combinations(str_var,c):
        # print('x', x)
        # теперь каждую комбинацию дополняем постоянной частью что пришла сюда
        str_var_c = ''.join(ccc)+''.join(x)
        # f.write('-------------------------------- %s ----------------------------'%str_var_c)
        for y in permut_word(str_var_c,dict_n):
            # print(" y ",y)
            f.write(str(y)+'\n')
            g_cnt = g_cnt +1
            # print(''.join(y1))
    return g_cnt

def comb_c_rrr(ccc,f):
    g_cnt = 0
    f.write("с повтором")
    # в полученно ccc элемент 1 и 2 повторяются 2 раза
    # 3 элемент повторяется kn раз
    #словарь без букв, которые сюда пришли и объязательны
    dd = list(set(d)-set(ccc))
    print(dd)
    # строка перебора по оставшемуся словарю
    str_var = ''.join(dd)
    #сколько еще не хватает до n?
    c = 5 - 2
    dict_n = {ccc[0]:2}
    a=[]
    b=[]
    #получаем комбинации
    for x in combinations_with_replacement(str_var,c):
        # print('x', x)
        # теперь каждую комбинацию дополняем постоянной частью что пришла сюда
        str_var_c = ''.join(ccc)+''.join(x)
        # f.write('-------------------------------- %s ----------------------------'%str_var_c)
        for y in permut_word(str_var_c,dict_n):
            # print(" y ",y)
            a.append(str(y))
    a = set(a)
    for i in a:
        f.write(str(i)+"\n")
    return len(a)

def m_c(f):
    gg_cnt = 0
    gg_cnt1 = 0
    #Сколько всего комбинаций из 3 объязательных бука
    # может быть на словаре ...
    dc=('a')
    gg_cnt += comb_c(dc,f)

    gg_cnt1+= comb_c_rrr(dc,f)
    print("получено всего комбинаций ", gg_cnt)
    print("получено всего комбинаций с повтором", gg_cnt1)

def main():
    f = open('workfile', 'w')
    f.write("")
    f.close()
    f = open('workfile', 'a')
    m_c(f)
    f.close()

# формальная запись: если не повторяются C(5_2)*P(5!/2!) = 600
#                    если повторяются    C(5_3)*P(5!/2)+    = 1200
time_start=time.perf_counter()
main()
time_end = time.perf_counter()
print(time_end - time_start)