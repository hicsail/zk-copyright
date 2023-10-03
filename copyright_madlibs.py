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



def reveal(list, st, end):
    res = ""
    for i in range(st, end):
        res += int_to_string(val_of(list[i])) + " "
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

    if DEBUG==True:
       exp_Y, X, madlibs, nouns, indexes = debug()

    else:
        scale = 12
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

    n_iter = 1500
    lim = max(indexes) + 1
    threshold = 300 # The program has to be performed within this (weight < )

    us = string_to_int("_")

    p = pow(2,256) - pow(2,32) - pow(2,9) - pow(2,8) - pow(2,7) - pow(2,6) - pow(2,4) - 1
    
    X_len = len(X_list)
    ml_len = len(madlibs_list)
    s_ml = len(nouns_list) + 1
    s_xl = len(nouns_list) + 1 + ml_len + 1
    sr1 = len(nouns_list) + 1 + ml_len + 1 + X_len + 1
    sr2 = len(nouns_list) + 1 + ml_len + 1 + X_len + 3
    sr3 = len(nouns_list) + 1 + ml_len + 1 + X_len + 5
    sr4 = len(nouns_list) + 1 + ml_len + 1 + X_len + 7
    di = len(nouns_list) + 1 + ml_len + 1 + X_len + 9
    s_rs = len(nouns_list) + 1 + ml_len + 1 + X_len + 11
    s_nn = 0

    with PicoZKCompiler('irs/picozk_test', field=[p], options=['ram']):

        # Producer
        nouns_list = nouns_list #0-15
        madlibs_list = madlibs_list #17 - 32
        X_list = X_list #34 - 49
        
        reg1 = 0 #51
        reg2 = 0 #53
        reg3 = 0 #55
        reg4 = 0 #57
        dummy_int = 0 #59
        res_list = [0] * ml_len #61 - 76
        
        bot = 0

        mem = ZKList(nouns_list + [bot] + madlibs_list + [bot] + X_list
                     + [bot] + [reg1] + [bot] + [reg2] + [bot] + [reg3]
                     + [bot] + [reg4] + [bot] + [dummy_int] + [bot] + res_list)

        program = [

            # Take the first three nouns from X and hard-code the rest from the fill list
            
                ## FIRST IF curr madlibs_words is equal to "_"
                    Instr(5, sr1, di, di, di, di, di, sr3, di, 0),    ## Step0   #5: Copy idx51 (idx-i/reg1) to idx55 (temp-idx/reg3)
                    Instr(2, di, di, s_ml, di, di, di, sr3, di, 0),   ## Step1   #2: Add 17 to idx55 (temp-idx/reg3) = Shifting pointer idx-i to madlibs list by 17
                    Instr(6, sr3, di, di, di, di, di, sr2, di, 0),    ## Step2   #6: Set idx55 (temp-idx/reg3) of madlibs list to idx53 (reg2)
                    Instr(3, di, di,  0, us, sr2, di, sr2, di, 0),    ## Step3   #3: Compare idx53 (reg2) and "_" and assign result to idx53 (reg2)
                    Instr(4, di, sr2,  1, 12, di, di, di, di, 2),     ## Step4   #4: Cond jump to Step5/Step16 if true/false

                ## SECOND IF index of madlibs_words is less than lim (upto idx of third)
                    Instr(3, di, di,  2,lim, sr1, di, sr2, di, 0),    ## Step5   #3: Compare idx 51(idx-i/reg1) < fill_upto (10 for now) and set the result to idx53 (reg2)
                    Instr(4, di, sr2,  1,  5, di, di, di, di, 2),     ## Step6   #4: Cond jump to Step7/Step11 if true/false

                ## IF Both TRUE (Append from X list)
                    Instr(5, sr1, di, di, di, di, di, sr3, di, 0),    ## Step7   #5: Copy idx51 (idx-i/reg1) to idx55 (temp-idx/reg3)
                    Instr(2, di, di, s_xl, di, di, di, sr3, di, 0),   ## Step8   #2: Add 34 to idx55 (temp-idx/reg3) = Shifting pointer to X_list idx-i by 34
                    Instr(6, sr3, di, di, di, di, di, sr2, di, 0),    ## Step9   #6: Set idx55 (temp-idx/reg3) of X_words to idx53 (reg2)
                    Instr(4, di, di,  9, di, di, di, di, di, 0),      ## Step10  #4: jump to Step19

                ## IF only the former TRUE (Append from nouns list)
                    Instr(5, sr2, di, di, di, di, di, sr3, di, 0),    ## Step11  #5: Copy idx57 (idx-k/reg2) to idx55 (temp-idx/reg3)
                    Instr(2, di, di, s_nn, di, di, di, sr3, di, 0),   ## Step12  #2: Add 3 to idx55 (temp-idx/reg3) = Shifting pointer idx-k to nouns list by 3
                    Instr(6, sr3, di, di, di, di, di, sr2, di, 1),    ## Step13  #6: Set idx55 (temp-idx/reg3) of nouns list to idx53 (reg2)
                    Instr(2, di, di,  1, di, di, di, sr3, di, 0),     ## Step14  #2: Add 1 to idx57 (idx-k/reg3)
                    Instr(4, di, di,  4, di, di, di, di, di, 0),      ## Step15  #4: jump to Step19

                ## ELSE (Append from madlibs list)
                    Instr(5, sr1, di, di, di, di, di, sr3, di, 0),    ## Step16  #5: Copy idx51 (idx-i/reg1) to idx55 (temp-idx/reg3)
                    Instr(2, di, di, s_ml, di, di, di, sr3, di, 0),   ## Step17  #2: Add 17 to idx55 (temp-idx/reg3) = Shifting pointer idx-i to madlibs list by 17
                    Instr(6, sr3, di, di, di, di, di, sr2, di, 0),    ## Step18  #6: Set idx55 (temp-idx/reg3) of madlibs list to idx53 (reg2)

                ## APPEND and INCREMENT
                    Instr(5, sr1, di, di, di, di, di, sr3, di, 0),    ## Step19  #5: Copy idx51 (idx-i/reg1) to idx55 (temp-idx/reg3)
                    Instr(2, di, di, s_rs, di, di, di, sr3, di, 0),   ## Step20  #2: Add 61 to idx55 (temp-idx/reg3) = Shifting pointer idx-i to res list by 61
                    Instr(7, di, di, sr2, di, di, di, di, sr3, 1),    ## Step21  #6: Set idx53 (reg2) to idx55 (temp-idx/reg3) of res list
                    Instr(2, di, di,  1, di, di, di, sr1, di, 0),     ## Step22  #2: Add 1 to idx51 (idx-i/reg1)
                    
                ## CHECK IF ITERATE OR NEXT
                    Instr(3, di, di, 2, X_len, sr1, di, sr3, di, 0),  ## Step23  #3: Compare idx51 (idx-i) < p5 (X_len) and assign result to idx55 (reg3)
                    Instr(4, di, sr3, 24,  1, di, di, di, di, 1),     ## Step24  #4: Cond jump to Step0/25 if true/false

            # END
                    Instr(100, di, di, di, di, di, di, di, di, 0),    ## Step25  #100: Terminal
                    ]
        pro_prog = make_program(program)

        pc = 0
        weight = 0
        for i in range(n_iter):
            pc, weight = step(pro_prog, pc, mem, weight)

        prod_Y = reveal(mem, s_rs, s_rs + ml_len)

        print('prod_Y:', prod_Y, '\n')
        print(exp_Y == prod_Y)
        print(val_of(weight), val_of(threshold))
        res = mux(exp_Y == prod_Y,
                  mux(weight <= threshold, SecretInt(0), SecretInt(1))
                  , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)


        # Reproducer
        nouns_list = nouns_list #0-15
        madlibs_list = madlibs_list #17 - 32
        bots_list = [0] * 16 #33 - 49
        
        reg1 = 0 #51
        reg2 = 0 #53
        reg3 = 0 #55
        reg4 = 0 #57
        dummy_int = 0 #59
        res_list = [0] * 16 #61 - 76
        
        hc0 = nouns_list[0]
        hc1 = nouns_list[1]
        hc2 = nouns_list[2]
        hc3 = nouns_list[3]
        hc4 = nouns_list[4]

        bot = 0

        repro_mem = ZKList(nouns_list + [bot] + madlibs_list + [bot] + bots_list
                           + [bot] + [reg1] + [bot] + [reg2] + [bot] + [reg3] + [bot] + [reg4]
                           + [bot] + [dummy_int]  + [bot] + res_list)


        lim = len(madlibs_list)

        program = [

            # Hard-Code all blanks from the nouns list
                
                ## IF madlibs_words[curr] == "_"
                    Instr(5, 51, di, di, di, di, di, 55, di, 0),    ## Step0   #5: Copy idx51 (idx-i/reg1) to idx55 (temp-idx/reg3)
                    Instr(2, di, di, 17, di, di, di, 55, di, 0),    ## Step1   #2: Add 17 to idx55 (temp-idx/reg3) = Shifting pointer idx-i to madlibs list by 17
                    Instr(6, 55, di, di, di, di, di, 53, di, 0),    ## Step2   #6: Set idx55 (temp-idx/reg3) of madlibs list to idx53 (reg2)
                    Instr(3, di, di,  0, us, 53, di, 53, di, 0),    ## Step3   #3: Compare idx53 (reg2) and "_" and assign result to idx53 (reg2)
                    Instr(4, di, 53,  1, 23, di, di, di, di, 2),    ## Step4   #4: Cond jump to Step5/Step27 if true/false

                    ## TRUE: Check k and jump to respective step
                    Instr(3, di, di,  0,  0, 57, di, 55, di, 0),    ## Step5   #3: Compare idx57 (idx-k) == 0 and assign result to idx55 (reg3)
                    Instr(4, di, 55,  9,  1, di, di, di, di, 2),    ## Step6   #4: Cond jump to  +9/+1 if true/false
                    Instr(3, di, di,  0,  1, 57, di, 55, di, 0),    ## Step7   #3: Compare idx57 (idx-k) == 1 and assign result to idx55 (reg3)
                    Instr(4, di, 55,  9,  1, di, di, di, di, 2),    ## Step8   #4: Cond jump to  +9/+1 if true/false
                    Instr(3, di, di,  0,  2, 57, di, 55, di, 0),    ## Step9   #3: Compare idx57 (idx-k) == 2 and assign result to idx55 (reg3)
                    Instr(4, di, 55,  9,  1, di, di, di, di, 2),    ## Step10  #4: Cond jump to  +9/+1 if true/false
                    Instr(3, di, di,  0,  3, 57, di, 55, di, 0),    ## Step11  #3: Compare idx57 (idx-k) == 3 and assign result to idx55 (reg3)
                    Instr(4, di, 55,  9,  1, di, di, di, di, 2),    ## Step12  #4: Cond jump to  +9/+1 if true/false
                    Instr(3, di, di,  0,  4, 57, di, 55, di, 0),    ## Step13  #3: Compare idx57 (idx-k) == 4 and assign result to idx55 (reg3)
                    Instr(4, di, 55,  9, 22, di, di, di, di, 2),    ## Step14  #4: Cond jump to  +9/+22 if true/false (sending to terminal if false as its error)

                    ## k = 0: Set hc0 to reg2
                    Instr(1, di, di, di, di, di,hc0, 53, di, 0),    ## Step15  #6: Set hc0 to idx53 (reg2)
                    Instr(4, di, di,  9, di, di, di, di, di, 0),    ## Step16  #4: jump to Step25

                    ## k = 1: Set hc1 to reg2
                    Instr(1, di, di, di, di, di,hc1, 53, di, 0),    ## Step17  #6: Set hc1 to idx53 (reg2)
                    Instr(4, di, di,  7, di, di, di, di, di, 0),    ## Step18  #4: jump to Step25

                    ## k = 2: Set hc2 to reg2
                    Instr(1, di, di, di, di, di,hc2, 53, di, 0),    ## Step19  #6: Set hc2 to idx53 (reg2)
                    Instr(4, di, di,  5, di, di, di, di, di, 0),    ## Step20  #4: jump to Step25

                    ## k = 3: Set hc3 to reg2
                    Instr(1, di, di, di, di, di,hc3, 53, di, 0),    ## Step21  #6: Set hc3 to idx53 (reg2)
                    Instr(4, di, di,  3, di, di, di, di, di, 0),    ## Step22  #4: jump to Step25

                    ## k = 4: Set hc4 to reg2
                    Instr(1, di, di, di, di, di,hc4, 53, di, 0),    ## Step23  #6: Set hc4 to idx53 (reg2)
                    Instr(4, di, di,  1, di, di, di, di, di, 0),    ## Step24  #4: jump to Step25
                    
                    ## (Common) Increment k by 1 and jump to Step30
                    Instr(2, di, di,  1, di, di, di, 57, di, 0),    ## Step25  #2: add 1 to idx57 (idx-k)
                    Instr(4, di, di,  4, di, di, di, di, di, 0),    ## Step26  #4: jump to Step30

                    ## ELSE: Append from madlibs_list[idx-k] to res_list
                    Instr(5, 51, di, di, di, di, di, 55, di, 0),    ## Step27  #5: Copy idx51 (idx-i/reg1) to idx55 (temp-idx/reg3)
                    Instr(2, di, di, 17, di, di, di, 55, di, 0),    ## Step28  #2: Add 17 to idx55 (temp-idx/reg3) = Shifting pointer idx-i to madlibs list by 17
                    Instr(6, 55, di, di, di, di, di, 53, di, 0),    ## Step29  #6: Set idx55 (temp-idx/reg3) of madlibs list to idx53 (reg2)
                    
                ## APPEND and INCREMENT
                    Instr(5, 51, di, di, di, di, di, 55, di, 0),    ## Step30  #5: Copy idx51 (idx-i/reg1) to idx55 (temp-idx/reg3)
                    Instr(2, di, di, 61, di, di, di, 55, di, 0),    ## Step31  #2: Add 61 to idx55 (temp-idx/reg3) = Shifting pointer idx-i to res list by 61
                    Instr(7, di, di, 53, di, di, di, di, 55, 1),    ## Step32  #6: Set idx53 (reg2) to idx55 (temp-idx/reg3) of res list
                    Instr(2, di, di,  1, di, di, di, 51, di, 0),    ## Step33  #2: Add 1 to idx 51 (idx-i)

                ## Determine whether or not to iterate over again depending idx-i< len(madlibs_words)
                    Instr(3, di, di, 2, lim, 51, di, 55, di, 0),    ## Step34  #3: Compare idx51 (idx-i) < p5 (X_len) and assign result to idx55 (reg3)
                    Instr(4, di, 55, 35,  1, di, di, di, di, 1),    ## Step35  #4: Cond jump to -16/+1 if true/false

            # END
                    Instr(100, di, di, di, di, di, di, di, di, 0),  ## Step36  #100: Terminal
                    ]
        repro_prog = make_program(program)

        pc = 0
        weight = 0

        for i in range(n_iter):
            pc, weight = step(repro_prog, pc, repro_mem, weight)

        reprod_Y = reveal(repro_mem, 61, 77)
        print('reprod_Y: ', reprod_Y, '\n')
        res = mux(exp_Y == reprod_Y, 
                  mux(weight <= threshold, SecretInt(0), SecretInt(1))
                  , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)

if __name__ == "__main__":
    main()