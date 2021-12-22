from itertools import *
import time

d = ['a','b','c','d','e','f','g','h','j','k']
divided_arrs = ((7,1,1,1),(6,2,1,1),(5,3,1,1),(5,2,2,1),(4,4,1,1),(4,3,2,1),(4,2,2,2),(3,3,2,2,),(3,3,3,1))

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

# по полученному разбиению, получаем, сколько уникальных чисел разбиения
# так как по каждому уникальному числу буквы будут значимы
# каждая буква, должна побывать на каждом значимом числе
def get_uniq_cnt(ccc,divided_arr_1):
    # на вход (пример)
    # divided_arr_1 => (4,2,2,2)
    # ccc => ('g', 'h', 'j', 'k')
    # на выход (пример)
    # {'g': 4,'h':2,'j':2,'k':2}
    # {'h': 4,'g':2,'j':2,'k':2}
    # {'j': 4,'h':2,'g':2,'k':2}
    # {'k': 4,'h':2,'j':2,'g':2}
    a = set(divided_arr_1)
    x = len(a)-1
    # print('x ',x)
    # print(divided_arr_1)
    for c in permutations(ccc,x):
        print(c)
        union_cc = list(c)
        union_cc.extend(tuple(set(ccc) - set(c)))
        # print(union_cc)
        dict_union = {}
        for uc,da in zip (union_cc,divided_arr_1):
            dict_union.update({uc:da})
        yield dict_union

def main(f):
    g_cnt = 0
    cc_cnt = 0
    # Сперва получим все сочетания из 10 по 4
    for ccc in combinations(d,4):
        cc_cnt += 1;print(cc_cnt, ' -> ', ccc," комбинаций: ",g_cnt)
        # Дальше с каждым из этих сочетаний, мы проходим через все разбиения
        for divide_arr in divided_arrs:
            print(divide_arr," комбинаций: ",g_cnt)
            # получаем комбинации букв по кол-ву значимых позиций и
            # генерим через перестановки с повторениями поток в файл
            for dd in get_uniq_cnt(ccc,divide_arr):
                str_var_c = ''.join(ccc)
                for y in permut_word(str_var_c, dd):
                    # print(" y ",y)
                    f.write(str(y) + '\n')
                    g_cnt = g_cnt + 1
                    # print(''.join(y1))
        if g_cnt > 10**7:
            print("Может не хватить места на диске, превышен лимит комбинаций !!!")
            break

    print ("получено всего комбинаций ",g_cnt)


time_start=time.perf_counter()
f = open('workfile', 'w')
main(f)
f.close()
time_end = time.perf_counter()
# print(time_end - time_start)
# get_uniq_cnt(('g', 'h', 'j', 'k',),(5,3,2,1))
# get_uniq_cnt(('g', 'h', 'j', 'k',),(4,2,2,2))
# get_uniq_cnt(('g', 'h', 'j', 'k',),(6,2,1,1))



