from itertools import product
from itertools import *
from itertools import chain, combinations
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

word="abc"
#размещения без повторений
acc_r=[]
for i in product(word,repeat=len(word)):
    acc_r.append(i)
print(acc_r)
#перестановки
rep=[]
for i in permutations(word,len(word)):
    rep.append(i)
print(rep)
#размещения с повтроениями
per=[]

#все подмножества
def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
pod=powerset(word)
print(list(pod))
#все сочетания
com=[]
for i in combinations(word,2):
    com.append(i)
print(com)
#все сочетания с повторениями
com_r=[]
for i in combinations_with_replacement(word,2):
    com_r.append(i)
print(com_r)
