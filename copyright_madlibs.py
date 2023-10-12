from picozk import *
from utils.datatypes import Instr
from utils.steps import step
from utils.functions import make_program, int_to_string, string_to_int
import random
from faker import Faker


def make_exp_y(scale):
  
  fake = Faker() # Create an instance of Faker

  exp_Y = fake.sentence(nb_words=scale)

  return exp_Y[:-1]


def get_blanks(exp_Y):

  # Using integer division to ensure the second argument is an integer
  indexes = random.sample(range(0, len(exp_Y)), len(exp_Y) // 3)
  indexes.sort()
  return indexes


def make_madlibs(exp_Y, indexes):


  # Making madlibs
  madlibs = ['_' if i in indexes else exp_Y[i] for i in range(len(exp_Y))]
  
  return madlibs


def make_nouns(exp_Y, indexes):

  # Using list comprehension to get words at specific indices
  nouns = [exp_Y[i] for i in indexes]

  # Generate random words
  fake_add = Faker()

  addition = fake_add.words(nb=3, unique=False)
  nouns += addition
  return nouns


def make_X(madlibs, nouns, indexes):
    X = madlibs.copy()
    i = 0
    idx = range(len(indexes))

    for k in range(len(X)):
        if X[k] == '_':
            X[k] = nouns[idx[i]]
            i+=1

    X = ' '.join(X) # This is the madlibs text with all blanks are filled

    return X



def reveal(mem, st, end):
    if not (0 <= st <= len(mem)) or not (end == len(mem)):
        raise ValueError("Start and end indices must be within the bounds of the list.")
    
    res = ""
    for i in range(st, end):
        res += int_to_string(val_of(mem[i])) + " "
    
    return res[:-1]
        
def debug():
   
    exp_Y = "I have a dog and cat , and every day I walk her to the park"
    print("\nexp_y:", exp_Y)

    indexes = [3, 5, 9, 12, 15]

    madlibs = "I have a _ and _ , and every _ I walk _ to the _".split()
    print("\nmadlibs:", madlibs)

    nouns = ['dog', 'cat', 'day', 'her', 'park', 'them', 'beach', 'school', 'like', 'hour', 'tree', 'car', 'house', 'week', 'shoe', 'beach']
    print("\nnouns:", nouns)

    X = make_X(madlibs, nouns, indexes)
    print('\nX: ', X)

    return exp_Y, X, madlibs, nouns, indexes

def main():
    
    DEBUG=False
    scale = 5
    n_iter = (scale*26) ** 2
    threshold = n_iter # The program has to be performed within this (weight < )

    if DEBUG==True:
       exp_Y, X, madlibs, nouns, indexes = debug()

    else:
        exp_Y = make_exp_y(scale)
        print("\nexp_y:", exp_Y)

        _exp_Y = exp_Y.split()  # Splitting the sentence into words
        indexes = get_blanks(_exp_Y)

        madlibs = make_madlibs(_exp_Y, indexes)
        print("\nmadlibs:", madlibs)

        nouns = make_nouns(_exp_Y, indexes)
        print("\nnouns:", nouns)

        X = make_X(madlibs, nouns, indexes)
        print('\nX: ', X)

    X_list = [string_to_int(_str) for _str in X.split()]
    nouns_list = [string_to_int(_str) for _str in nouns]
    madlibs_list = [string_to_int(_str) for _str in madlibs]

    lim = max(indexes) + 1

    us = string_to_int("_")

    p = pow(2,256) - pow(2,32) - pow(2,9) - pow(2,8) - pow(2,7) - pow(2,6) - pow(2,4) - 1
    
    
    X_len = len(X_list)
    ml_len = len(madlibs_list)
    
    s_nl = 10
    s_nn = s_nl + 3
    s_ml = s_nl + len(nouns_list) + 1
    s_xl = s_ml + ml_len + 1
    s_rs = s_xl + X_len + 1

    with PicoZKCompiler('irs/picozk_test', field=[p], options=['ram']):

        # Producer
        reg1 = 0 #0
        reg2 = 0 #2
        reg3 = 0 #4
        reg4 = 0 #6
        dummy_int = 0 #8

        nouns_list = nouns_list #10-25
        madlibs_list = madlibs_list #27 - 42
        X_list = X_list #44 - 59
        
        res_list = [0] * ml_len #61 - 76
        
        bot = 0

        mem = ZKList([reg1] + [bot] + [reg2] + [bot] + [reg3] + [bot] + [reg4]
                      + [bot] + [dummy_int] + [bot] + nouns_list + [bot] 
                      + madlibs_list + [bot] + X_list + [bot] + res_list)

        program = [

            # Take the first three nouns from X and hard-code the rest from the fill list
            
                ## FIRST IF curr madlibs_words is equal to "_"
                    Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),     ## Step0   #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                    Instr(2, 8, 8, s_ml, 8, 8, 8, 4, 8, 0),  ## Step1   #2: Add s_ml to idx4 (temp-idx/reg3) and shift the pointer (temp-idx) to an appropriate position of the madlibs list
                    Instr(6, 4, 8, 8, 8, 8, 8, 2, 8, 0),     ## Step2   #6: Set idx4 (temp-idx/reg3) of madlibs list to idx2 (reg2)
                    Instr(3, 8, 8,  0, us, 2, 8, 2, 8, 0),   ## Step3   #3: Compare idx2 (reg2) and "_" and assign result to idx2 (reg2)
                    Instr(4, 8, 2,  1, 12, 8, 8, 8, 8, 2),   ## Step4   #4: Cond jump to Step5/Step16 if true/false

                ## SECOND IF index of madlibs_words is less than lim (upto idx of third)
                    Instr(3, 8, 8,  2,lim, 0, 8, 2, 8, 0),   ## Step5   #3: Compare idx0 (idx-i/reg1) < fill_upto and set the result to idx2 (reg2)
                    Instr(4, 8, 2,  1,  5, 8, 8, 8, 8, 2),   ## Step6   #4: Cond jump to Step7/Step11 if true/false

                ## IF Both TRUE (Append from X list)
                    Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),     ## Step7   #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                    Instr(2, 8, 8, s_xl, 8, 8, 8, 4, 8, 0),  ## Step8   #2: Add s_xl to idx4 (temp-idx/reg3) and shift the pointer (temp-idx) to an appropriate position of the X_list
                    Instr(6, 4, 8, 8, 8, 8, 8, 2, 8, 0),     ## Step9   #6: Set idx4 (temp-idx/reg3) of X_words to idx2 (reg2)
                    Instr(4, 8, 8,  9, 8, 8, 8, 8, 8, 0),    ## Step10  #4: jump to Step19

                ## IF only the former TRUE (Append from nouns list)
                    Instr(5, 2, 8, 8, 8, 8, 8, 4, 8, 0),     ## Step11  #5: Copy idx2 (idx-k/reg2) to idx4 (temp-idx/reg3)
                    Instr(2, 8, 8, s_nn, 8, 8, 8, 4, 8, 0),  ## Step12  #2: Add s_nn to idx4 (temp-idx/reg3) and shift the pointer (idx-k) to an appropriate position of the nouns list
                    Instr(6, 4, 8, 8, 8, 8, 8, 2, 8, 1),     ## Step13  #6: Set idx4 (temp-idx/reg3) of the nouns list to idx2 (reg2)
                    Instr(2, 8, 8,  1, 8, 8, 8, 4, 8, 0),    ## Step14  #2: Add 1 to idx4 (idx-k/reg3)
                    Instr(4, 8, 8,  4, 8, 8, 8, 8, 8, 0),    ## Step15  #4: jump to Step19

                ## ELSE (Append from madlibs list)
                    Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),     ## Step16  #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                    Instr(2, 8, 8, s_ml, 8, 8, 8, 4, 8, 0),  ## Step17  #2: Add s_ml to idx4 (temp-idx/reg3) and shift the pointer (idx-i) to an appropriate position of the madlibs list
                    Instr(6, 4, 8, 8, 8, 8, 8, 2, 8, 0),     ## Step18  #6: Set idx4 (temp-idx/reg3) of the madlibs list to idx2 (reg2)

                ## APPEND and INCREMENT
                    Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),     ## Step19  #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                    Instr(2, 8, 8, s_rs, 8, 8, 8, 4, 8, 0),  ## Step20  #2: Add s_rs to idx4 (temp-idx/reg3) and shift the pointer (idx-i) to an appropriate position of the res list
                    Instr(7, 8, 8, 2, 8, 8, 8, 8, 4, 1),     ## Step21  #6: Set idx2 (reg2) to idx4 (temp-idx/reg3) of the res list
                    Instr(2, 8, 8,  1, 8, 8, 8, 0, 8, 0),    ## Step22  #2: Add 1 to idx0 (idx-i/reg1)
                    
                ## CHECK IF ITERATE OR NEXT
                    Instr(3, 8, 8, 2, X_len, 0, 8, 4, 8, 0), ## Step23  #3: Compare idx0 (idx-i) < p5 (X_len) and assign the result to idx4 (reg3)
                    Instr(4, 8, 4, 24,  1, 8, 8, 8, 8, 1),   ## Step24  #4: Cond jump to Step0/25 if true/false

            # END
                    Instr(100, 8, 8, 8, 8, 8, 8, 8, 8, 0),   ## Step25  #100: Terminal
                    ]
        pro_prog = make_program(program)

        pc = 0
        weight = 0
        for i in range(n_iter):
            pc, weight = step(pro_prog, pc, mem, weight)
        
        prod_Y = reveal(mem, s_rs, s_rs + ml_len)

        print('prod_Y:', prod_Y, '\n')

        res = mux(exp_Y == prod_Y,
                  mux(weight <= threshold, SecretInt(0), SecretInt(1))
                  , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)


        # Reproducer
        
        reg1 = 0 #0
        reg2 = 0 #2
        reg3 = 0 #4
        reg4 = 0 #6
        dummy_int = 0 #8

        nouns_list = nouns_list #10-25
        madlibs_list = madlibs_list #27 - 42
        bots_list = [0] * X_len #44 - 59
        res_list = [0] * ml_len #61 - 76

        hc_size = len(indexes)
        hcs = [nouns_list[i] for i in range(hc_size)]
        bot = 0

        repro_mem = ZKList([reg1] + [bot] + [reg2] + [bot] + [reg3] + [bot] + [reg4]
                      + [bot] + [dummy_int] + [bot] + nouns_list + [bot] 
                      + madlibs_list + [bot] + bots_list + [bot] + res_list)
        lim = len(madlibs_list)

        # Hard-Code all blanks from the nouns list
        header = [

                ## IF madlibs_words[curr] == "_"
                    Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),                       #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                    Instr(2, 8, 8, s_ml, 8, 8, 8, 4, 8, 0),                    #2: Add s_ml to idx4 (temp-idx/reg3) and shift the pointer (temp-idx) to the madlibs list
                    Instr(6, 4, 8, 8, 8, 8, 8, 2, 8, 0),                       #6: Set idx4 (temp-idx/reg3) of madlibs list to idx2 (reg2)
                    Instr(3, 8, 8,  0, us, 2, 8, 2, 8, 0),                     #3: Compare idx2 (reg2) and "_" and assign result to idx2 (reg2)
                    Instr(4, 8, 2,  1, hc_size*4+3, 8, 8, 8, 8, 2),            #4: Cond jump to the first step in the dynamic part/Point2 if true/false
                ]


        dynamic = []
        for i in range(hc_size, 0, -1):
                ## TRUE: Check k and jump to respective step
                dynamic += [
                    Instr(3, 8, 8,  0, hc_size-i, 6, 8, 4, 8, 0),              #3: Compare idx6 (idx-k) == 0 ~ hc_size and assign result to idx4 (reg3)
                    Instr(4, 8, 4, hc_size*2-1,  1, 8, 8, 8, 8, 2)             #4: Cond jump to respective step/next in dynamic
                ]


        for i in range(hc_size):
                dynamic += [
                    Instr(1, 8, 8, 8, 8, 8,hcs[i], 2, 8, 0),                   #1: set i of hard code nouns to idx2 (reg2)
                    Instr(4, 8, 8,  hc_size*2-i*2-1, 8, 8, 8, 8, 8, 0)         #4: jump to "Point1" (The steps of jump changes depending on the size of the list of hard coded nouns)
                    ]


        footter = [
                    ## (Common) Increment k by 1 and jump to Step30
                    Instr(2, 8, 8,  1, 8, 8, 8, 6, 8, 0),            ## Point1  #2: add 1 to idx6 (idx-k)
                    Instr(4, 8, 8,  4, 8, 8, 8, 8, 8, 0),                       #4: jump to Point3

                    ## ELSE: Append from madlibs_list[idx-k] to res_list
                    Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),             ## Point2  #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                    Instr(2, 8, 8, s_ml, 8, 8, 8, 4, 8, 0),                     #2: Add s_ml to idx4 (temp-idx/reg3) and shift the pointer (temp-idx) to an appropriate position of the madlibs list
                    Instr(6, 4, 8, 8, 8, 8, 8, 2, 8, 0),                        #6: Set idx4 (temp-idx/reg3) of the madlibs list to idx2 (reg2)
                    
                ## APPEND and INCREMENT
                    Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),             ## Point3  #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                    Instr(2, 8, 8, s_rs, 8, 8, 8, 4, 8, 0),                     #2: Add s_rs to idx4 (temp-idx/reg3) and shift the pointer (temp-idx) to an approproate position of the res list
                    Instr(7, 8, 8, 2, 8, 8, 8, 8, 4, 1),                        #6: Set idx2 (reg2) to idx4 (temp-idx/reg3) of the res list
                    Instr(2, 8, 8,  1, 8, 8, 8, 0, 8, 0),                       #2: Add 1 to idx 0 (idx-i)

                ## Determine whether or not to iterate over again depending idx-i< len(madlibs_words)
                    Instr(3, 8, 8, 2, lim, 0, 8, 4, 8, 0),                      #3: Compare idx0 (idx-i) < p5 (X_len) and assign the result to idx4 (reg3)
                    Instr(4, 8, 4, hc_size*4+15, 1, 8, 8, 8, 8, 1),             #4: Cond jump to the very beginning/end if true/false

            # END
                    Instr(100, 8, 8, 8, 8, 8, 8, 8, 8, 0),                      #100: Terminal
                    ]
        
        program = header + dynamic + footter
        repro_prog = make_program(program)

        pc = 0
        weight = 0

        for i in range(n_iter):
            pc, weight = step(repro_prog, pc, repro_mem, weight)

        reprod_Y = reveal(repro_mem, s_rs, s_rs + ml_len)
        print('reprod_Y: ', reprod_Y, '\n')
        res = mux(exp_Y == reprod_Y, 
                  mux(weight <= threshold, SecretInt(0), SecretInt(1))
                  , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)

if __name__ == "__main__":
    main()