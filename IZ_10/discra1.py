from itertools import *
import time
d = ['a','b','c','d','e','f','g','h','j','k']
#длина слова
n = 7
#кол-во повторений 3-ей буквы
kn = 1

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
                    self.cur_ind_c = self.word.get_next_char_idx(-1)
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

    def init_pos(self):

        # надо нагенерить позиции таким образом
        # чтобы получилось самое младшее слово из возможных
        if self.len_word > 0:
            #Нам задали длину, что делать еще не решил
            pass
        else:
            # генерим макс возможное
            s = 0
            for i in self.dict_cnt_list:
                s+=i
            p  = [Position(None,self)]
            for i in range(1,s):
                p.append(Position(p[i-1]))
            self.pos_last = p[len(p)-1]
            return p



    def next(self):
        # переключится на след. слово
        self.is_has_next = self.pos_last.next()


    # выдает индекс след. символа разрешенного в слове после
    # символа индекс которого p_ind_c
    def get_next_char_idx(self,p_ind_c):
        for idx_c in range(p_ind_c+1,self.len_dict):
            if self.cur_cnt[idx_c] < self.dict_cnt_list[idx_c]:
                # если сменить получилось
                self.cur_cnt[idx_c]+=1
                if p_ind_c >= 0:
                    self.cur_cnt[p_ind_c]-=1
                return idx_c
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
        return [self.dict_list[p.cur_ind_c] for p in self.pos_list]


def permut_word(p_dict:str,p_dict_cnt_in_wrd:dict):
    w = Word(p_dict,p_dict_cnt_in_wrd)
    while w.is_has_next:
        yield w.get_word()
        w.next()

def comb_c(ccc,f):
    g_cnt = 0
    # в полученно ccc элемент 1 и 2 повторяются 2 раза
    # 3 элемент повторяется kn раз
    permut_str = ''.join(ccc[:2]*2)+''.join([ccc[2]]*kn)
    #словарь без букв, которые сюда пришли и объязательны
    dd = list(set(d)-set(ccc))
    # строка перебора по оставшемуся словарю
    str_var = ''.join(dd)
    #сколько еще не хватает до n?
    c = n - 2*2 - kn
    #получаем комбинации
    for x in combinations(str_var,c):
        # теперь каждую комбинацию дополняем постоянной частью что пришла сюда
        str_var_c = ''.join(ccc)+''.join(x)
        for y in permut_word(str_var_c,{ccc[0]:2,ccc[1]:2,ccc[2]:kn}):
            f.write(''.join(y)+'\n')
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
    time_start=time.perf_counter()
    if kn>n-4:
        raise Exception("кол-во повторений буквы  не может быть больше %d"%(n-4))
    if kn<1:
        raise Exception("кол-во повторений буквы не может быть меньше 1"%(kn))
    if n>4+kn+len(d)-3:
        raise Exception("n не может быть больше %d " % (kn+len(d)+1))
    f =  open('workfile','w')
    m_c(f)
    f.close()
    time_end=time.perf_counter()
    print(time_end-time_start)

main()

# cnt = 0
# for x in permut_word('12345',{'1':2,'2':2}):
#     print(x)
#     cnt+=1
# print (cnt)