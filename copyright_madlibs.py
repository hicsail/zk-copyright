from picozk import *
from utils.datatypes import Instr
from utils.steps import step
from utils.functions import make_program, int_to_string, string_to_int


def make_X(madlibs, nouns):
    X = madlibs.split()
    i = 0
    idx = [0,1,2,5,6]

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
        


def main():

    madlibs = "I have a _ and _ , and every _ I walk _ to the _"
    nouns = ['dog', 'cat', 'day', 'her', 'park', 'them', 'beach', 'school', 'like', 'hour', 'tree', 'car', 'house', 'week', 'shoe', 'beach']
    exp_Y = "I have a dog and cat , and every day I walk her to the park"
    print('Y: ', exp_Y, '\n')
    X = make_X(madlibs, nouns)
    print('X: ', X, '\n')

    X_list = [string_to_int(_str) for _str in X.split()]
    nouns_list = [string_to_int(_str) for _str in nouns]
    madlibs_list = [string_to_int(_str) for _str in madlibs.split()]

    n_iter = 1500
    lim = 10
    threshold = 300 # The program has to be performed within this (weight < )

    us = string_to_int("_")
    
    with PicoZKCompiler('irs/picozk_test', options=['ram']):

        # Producer
        nouns_list = nouns_list #0-15
        madlibs_list = madlibs_list #17 - 32
        X_list = X_list #34 - 49
        res_list = [0] * 16 #51 - 66

        reg1 = 0 #68
        reg2 = 0 #70
        reg3 = 0 #72
        reg4 = 0 #74
        dummy_int = 0 #76
        
        bot = 0

        mem = ZKList(nouns_list + [bot] + madlibs_list + [bot] + X_list + [bot] + res_list + [bot] + [reg1] + [bot] + [reg2] + [bot] + [reg3] + [bot] + [reg4] + [bot] + [dummy_int])

        X_len = len(X_list)

        program = [

            # Take the first three nouns from X and hard-code the rest from the fill list
            
                ## FIRST IF curr madlibs_words is equal to "_"
                    Instr(5, 76, 68, 76, 76, 76, 76, 72, 76, 0),    ## Step0   #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76, 17, 76, 76, 72, 76, 0),    ## Step1   #2: Add 17 to idx72 (temp-idx/reg3) = Shifting pointer idx-i to madlibs list by 17
                    Instr(6, 76, 72, 76, 76, 76, 76, 70, 76, 0),    ## Step2   #6: Set idx72 (temp-idx/reg3) of madlibs list to idx70 (reg2)
                    Instr(3, 76, 76, 76,  0, us, 70, 70, 76, 0),    ## Step3   #3: Compare idx70 (reg2) and "_" and assign result to idx70 (reg2)
                    Instr(4, 76, 76, 70,  5, 16, 76, 76, 76, 1),    ## Step4   #4: Cond jump to Step5/Step16 if true/false

                ## SECOND IF index of madlibs_words is less than lim (upto idx of third)
                    Instr(3, 76, 76, 76,  2,lim, 68, 70, 76, 0),    ## Step5   #3: Compare idx 68(idx-i/reg1) < fill_upto (10 for now) and set the result to idx70 (reg2)
                    Instr(4, 76, 76, 70,  7, 11, 76, 76, 76, 1),    ## Step6   #4: Cond jump to Step7/Step11 if true/false

                ## IF Both TRUE (Append from X list)
                    Instr(5, 76, 68, 76, 76, 76, 76, 72, 76, 0),    ## Step7   #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76, 34, 76, 76, 72, 76, 0),    ## Step8   #2: Add 34 to idx72 (temp-idx/reg3) = Shifting pointer to X_list idx-i by 34
                    Instr(6, 76, 72, 76, 76, 76, 76, 70, 76, 0),    ## Step9   #6: Set idx72 (temp-idx/reg3) of X_words to idx70 (reg2)
                    Instr(4, 76, 76, 76, 19, 76, 76, 76, 76, 0),    ## Step10  #4: jump to Step19

                ## IF only the former TRUE (Append from nouns list)
                    Instr(5, 76, 74, 76, 76, 76, 76, 72, 76, 0),    ## Step11  #5: Copy idx74 (idx-k/reg2) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76,  3, 76, 76, 72, 76, 0),    ## Step12  #2: Add 3 to idx72 (temp-idx/reg3) = Shifting pointer idx-k to nouns list by 3
                    Instr(6, 76, 72, 76, 76, 76, 76, 70, 76, 1),    ## Step13  #6: Set idx72 (temp-idx/reg3) of nouns list to idx70 (reg2)
                    Instr(2, 76, 76, 76,  1, 76, 76, 74, 76, 0),    ## Step14  #2: Add 1 to idx74 (idx-k/reg3)
                    Instr(4, 76, 76, 76, 19, 76, 76, 76, 76, 0),    ## Step15  #4: jump to Step19

                ## ELSE (Append from madlibs list)
                    Instr(5, 76, 68, 76, 76, 76, 76, 72, 76, 0),    ## Step16  #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76, 17, 76, 76, 72, 76, 0),    ## Step17  #2: Add 17 to idx72 (temp-idx/reg3) = Shifting pointer idx-i to madlibs list by 17
                    Instr(6, 76, 72, 76, 76, 76, 76, 70, 76, 0),    ## Step18  #6: Set idx72 (temp-idx/reg3) of madlibs list to idx70 (reg2)

                ## APPEND and INCREMENT
                    Instr(5, 76, 68, 76, 76, 76, 76, 72, 76, 0),    ## Step19  #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76, 51, 76, 76, 72, 76, 0),    ## Step20  #2: Add 51 to idx72 (temp-idx/reg3) = Shifting pointer idx-i to res list by 51
                    Instr(7, 76, 76, 76, 70, 76, 76, 76, 72, 1),    ## Step21  #6: Set idx70 (reg2) to idx72 (temp-idx/reg3) of res list
                    Instr(2, 76, 76, 76,  1, 76, 76, 68, 76, 0),    ## Step22  #2: Add 1 to idx 68 (idx-i)
                    
                ## CHECK IF ITERATE OR NEXT
                    Instr(3, 76, 76, 76, 2, X_len, 68, 72, 76, 0),  ## Step23  #3: Compare idx68 (idx-i) < p5 (X_len) and assign result to idx72 (reg3)
                    Instr(4, 76, 76, 72, 0, 25, 76, 76, 76, 1),     ## Step24  #4: Cond jump to Step0/25 if true/false

            # END
                    Instr(100, 76, 76, 76, 76, 76, 76, 76, 76, 0),   ## Step25  #100: Terminal
                    ]
        pro_prog = make_program(program)

        pc = 0
        weight = 0
        for i in range(n_iter):
            pc, weight = step(pro_prog, pc, mem, weight)
        
        prod_Y = reveal(mem, 51, 67)

        print('prod_Y:', prod_Y, '\n')

        res = mux(exp_Y == prod_Y,
                  mux(weight <= threshold, SecretInt(0), SecretInt(1))
                  , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)


        # Reproducer
        nouns_list = nouns_list #0-15
        madlibs_list = madlibs_list #17 - 32
        hardcode_idx = [0, 1, 2, 3, 4] #34 - 38 TODO: Might need fix
        bots_list = [0] * (16 - 6) #40 - 49
        res_list = [0] * 16 #51 - 66

        reg1 = 0 #68
        reg2 = 0 #70
        reg3 = 0 #72
        reg4 = 0 #74
        dummy_int = 0 #76
        
        bot = 0

        repro_mem = ZKList(nouns_list + [bot] + madlibs_list + [bot] + hardcode_idx + [bot] + bots_list + [bot] + res_list + [bot] + [reg1] + [bot] + [reg2] + [bot] + [reg3] + [bot] + [reg4] + [bot] + [dummy_int])


        lim = len(madlibs_list)

        program = [

            # Hard-Code all blanks from the nouns list
                
                ## IF madlibs_words[curr] == "_"
                    Instr(5, 76, 68, 76, 76, 76, 76, 72, 76, 0),    ## Step0   #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76, 17, 76, 76, 72, 76, 0),    ## Step1   #2: Add 17 to idx72 (temp-idx/reg3) = Shifting pointer idx-i to madlibs list by 17
                    Instr(6, 76, 72, 76, 76, 76, 76, 70, 76, 0),    ## Step2   #6: Set idx72 (temp-idx/reg3) of madlibs list to idx70 (reg2)
                    Instr(3, 76, 76, 76,  0, us, 70, 70, 76, 0),    ## Step3   #3: Compare idx70 (reg2) and "_" and assign result to idx70 (reg2)
                    Instr(4, 76, 76, 70,  5, 8, 76, 76, 76, 1),     ## Step4   #4: Cond jump to Step5/Step8 if true/false

                    ## TRUE: Append from nouns_list[idx-k] to res_list
                    Instr(6, 76, 74, 76, 76, 76, 76, 70, 76, 0),    ## Step5   #6: Set idx74 (idx-k/reg4) of nouns list to idx70 (reg2)
                    Instr(2, 76, 76, 76,  1, 76, 76, 74, 76, 0),    ## Step6   #2: add 1 to idx74 (idx-k)
                    Instr(4, 76, 76, 76, 11, 76, 76, 76, 76, 0),    ## Step7   #4: jump to Step11

                    ## ELSE: Append from madlibs_list[idx-k] to res_list
                    Instr(5, 76, 68, 76, 76, 76, 76, 72, 76, 0),    ## Step8   #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76, 17, 76, 76, 72, 76, 0),    ## Step9   #2: Add 17 to idx72 (temp-idx/reg3) = Shifting pointer idx-i to madlibs list by 17
                    Instr(6, 76, 72, 76, 76, 76, 76, 70, 76, 0),    ## Step10  #6: Set idx72 (temp-idx/reg3) of madlibs list to idx70 (reg2)
                    
                ## APPEND and INCREMENT
                    Instr(5, 76, 68, 76, 76, 76, 76, 72, 76, 0),    ## Step11  #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76, 51, 76, 76, 72, 76, 0),    ## Step12  #2: Add 51 to idx72 (temp-idx/reg3) = Shifting pointer idx-i to res list by 51
                    Instr(7, 76, 76, 76, 70, 76, 76, 76, 72, 1),    ## Step13  #6: Set idx70 (reg2) to idx72 (temp-idx/reg3) of res list
                    Instr(2, 76, 76, 76,  1, 76, 76, 68, 76, 0),    ## Step14  #2: Add 1 to idx 68 (idx-i)

                ## Determine whether or not to iterate over again depending idx-i< len(madlibs_words)
                    Instr(3, 76, 76, 76, 2, lim, 68, 72, 76, 0),    ## Step15  #3: Compare idx68 (idx-i) < p5 (X_len) and assign result to idx72 (reg3)
                    Instr(4, 76, 76, 72, 0, 17, 76, 76, 76, 1),    ## Step16  #4: Cond jump to -16/+1 if true/false

            # END
                    Instr(100, 76, 76, 76, 76, 76, 76, 76, 76, 0),   ## Step17  #100: Terminal
                    ]
        repro_prog = make_program(program)

        pc = 0
        weight = 0

        for i in range(n_iter):
            pc, weight = step(repro_prog, pc, repro_mem, weight)

        reprod_Y = reveal(repro_mem, 51, 67)
        print('reprod_Y: ', reprod_Y, '\n')
        res = mux(exp_Y == reprod_Y, 
                  mux(weight <= threshold, SecretInt(0), SecretInt(1))
                  , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)

if __name__ == "__main__":
    main()