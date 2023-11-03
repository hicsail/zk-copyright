from picozk import *
from utils.datatypes import Instr
from utils.steps import step
from utils.functions import make_program
from .helpers import reveal

def producer(nouns_list, madlibs_list, X_list,  ml_len, s_ml, us, hc_size, from_x, s_xl, hcs, s_rs, n_iter, exp_Y, threshold):

    reg1 = 0 #0
    reg2 = 0 #2
    reg3 = 0 #4
    reg4 = 0 #6
    dummy_int = 0 #8

    nouns_list = nouns_list #10-25
    madlibs_list = madlibs_list #27 - 42
    X_list = X_list #44 - 59
    res_list = [0] * max(7, ml_len) #61 - 76 Need min 4 space so that a program pointer at the final step does not exceed memory length

    bot = 0

    mem = ZKList([reg1] + [bot] + [reg2] + [bot] + [reg3] + [bot] + [reg4]
                    + [bot] + [dummy_int] + [bot] + nouns_list + [bot] 
                    + madlibs_list + [bot] + X_list + [bot] + res_list)

    header = [

        # Take the first three nouns from X and hard-code the rest from the fill list
        
            ## FIRST IF curr madlibs_words is equal to "_"
                Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),                            #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                Instr(2, 8, 8, s_ml, 8, 8, 8, 4, 8, 0),                         #2: Add s_ml to idx4 (temp-idx/reg3) and shift the pointer (temp-idx) to an appropriate position of the madlibs list
                Instr(6, 4, 8, 8, 8, 8, 8, 2, 8, 0),                            #6: Set idx4 (temp-idx/reg3) of madlibs list to idx2 (reg2)
                Instr(3, 8, 8, 0, us, 2, 8, 2, 8, 0),                           #3: Compare idx2 (reg2) and "_" and assign result to idx2 (reg2)
                Instr(4, 8, 2, 1, hc_size*4+9, 8, 8, 8, 8, 2),                  #4: Cond jump to Next/Point2 if true/false

            ## SECOND IF index of madlibs_words is less than lim (upto idx of third)
                Instr(3, 8, 8,  2,from_x, 0, 8, 2, 8, 0),                       #3: Compare idx0 (idx-i/reg1) < from_x and set the result to idx2 (reg2)
                Instr(4, 8, 2,  1,  5, 8, 8, 8, 8, 2),                          #4: Cond jump to Next/Dynamic if true/false

            ## IF Both TRUE (Append from X list)
                Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),                            #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                Instr(2, 8, 8, s_xl, 8, 8, 8, 4, 8, 0),                         #2: Add s_xl to idx4 (temp-idx/reg3) and shift the pointer (temp-idx) to an appropriate position of the X_list
                Instr(6, 4, 8, 8, 8, 8, 8, 2, 8, 0),                            #6: Set idx4 (temp-idx/reg3) of X_words to idx2 (reg2)
                Instr(4, 8, 2, 1, hc_size*4+6, 8, 8, 8, 8, 2),                  #4: Cond jump to the first step in the dynamic part/Point2 if true/false
            ]

    dynamic = []
    for i in range(hc_size, 0, -1):
            ## TRUE: Check k and jump to respective step
            dynamic += [
                Instr(3, 8, 8,  0, hc_size-i, 6, 8, 4, 8, 0),                   #3: Compare idx6 (idx-k) == 0 ~ hc_size and assign result to idx4 (reg3)
                Instr(4, 8, 4, hc_size*2-1,  1, 8, 8, 8, 8, 2)                  #4: Cond jump to respective step/next in dynamic
            ]

    for i in range(hc_size):
            dynamic += [
                Instr(1, 8, 8, 8, 8, 8,hcs[i], 2, 8, 0),                        #1: set i of hard code nouns to idx2 (reg2)
                Instr(4, 8, 8,  (hc_size-i)*2-1, 8, 8, 8, 8, 8, 0)              #4: jump to "Point1" (The steps of jump changes depending on the size of the list of hard coded nouns)
            ]

    footer = [
            ## (Common) Increment k by 1 and jump to Step30
                Instr(2, 8, 8, 1, 8, 8, 8, 6, 8, 0),                 ## Point1  #2: add 1 to idx6 (idx-k)
                Instr(4, 8, 8, 4, 8, 8, 8, 8, 8, 0),                            #4: jump to Point3
            
            ## ELSE (Append from madlibs list)
                Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),                 ## Point2  #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                Instr(2, 8, 8, s_ml, 8, 8, 8, 4, 8, 0),                         #2: Add s_ml to idx4 (temp-idx/reg3) and shift the pointer (idx-i) to an appropriate position of the madlibs list
                Instr(6, 4, 8, 8, 8, 8, 8, 2, 8, 0),                            #6: Set idx4 (temp-idx/reg3) of the madlibs list to idx2 (reg2)

            ## APPEND and INCREMENT
                Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),                 ## Point3  #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                Instr(2, 8, 8, s_rs, 8, 8, 8, 4, 8, 0),                         #2: Add s_rs to idx4 (temp-idx/reg3) and shift the pointer (idx-i) to an appropriate position of the res list
                Instr(7, 8, 8, 2, 8, 8, 8, 8, 4, 1),                            #6: Set idx2 (reg2) to idx4 (temp-idx/reg3) of the res list
                Instr(2, 8, 8, 1, 8, 8, 8, 0, 8, 0),                            #2: Add 1 to idx0 (idx-i/reg1)
                
            ## Determine whether or not to iterate over again depending idx-i< len(madlibs_words)
                Instr(3, 8, 8, 2, ml_len, 0, 8, 4, 8, 0),                       #3: Compare idx0 (idx-i) < p5 (ml_len) and assign the result to idx4 (reg3)
                Instr(4, 8, 4,  hc_size*4+21,  1, 8, 8, 8, 8, 1),               #4: Cond jump to the very beginning/end if true/false

        # END
                Instr(0, 8, 8, 8, 8, 8, 8, 8, 8, 0),                            #0: Terminal
            ]

    program = header + dynamic + footer
    pro_prog = make_program(program)

    pc = 0
    weight = 0
    for i in range(n_iter):
        pc, weight = step(pro_prog, pc, mem, weight)

    prod_Y = reveal(mem, s_rs, s_rs + ml_len)
    print('\nprod_Y:', prod_Y)

    res = mux(exp_Y == prod_Y,
                mux(weight <= threshold, SecretInt(0), SecretInt(1))
                , SecretInt(1))
    assert0(res)
    assert(val_of(res)==0)

    prod_weight = val_of(weight)
    prod_size = len(program)
    
    return prod_weight, prod_size