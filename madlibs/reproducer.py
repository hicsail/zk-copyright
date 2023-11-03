from picozk import *
from utils.datatypes import Instr
from utils.steps import step
from utils.functions import make_program
from .helpers import reveal

def reproducer(nouns_list, madlibs_list, X_len, ml_len, blank_idx, s_ml, us, s_rs, n_iter, exp_Y, threshold):
   
    reg1 = 0 #0
    reg2 = 0 #2
    reg3 = 0 #4
    reg4 = 0 #6
    dummy_int = 0 #8

    nouns_list = nouns_list #10-25
    madlibs_list = madlibs_list #27 - 42
    bots_list = [0] * X_len #44 - 59
    res_list = [0] * ml_len #61 - 76

    hc_size = len(blank_idx)
    hcs = [nouns_list[i] for i in range(hc_size)]
    bot = 0

    repro_mem = ZKList([reg1] + [bot] + [reg2] + [bot] + [reg3] + [bot] + [reg4]
                    + [bot] + [dummy_int] + [bot] + nouns_list + [bot] 
                    + madlibs_list + [bot] + bots_list + [bot] + res_list)

    # Hard-Code all blanks from the nouns list
    header = [

            ## IF madlibs_words[curr] == "_"
                Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),                       #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                Instr(2, 8, 8, s_ml, 8, 8, 8, 4, 8, 0),                    #2: Add s_ml to idx4 (temp-idx/reg3) and shift the pointer (temp-idx) to the madlibs list
                Instr(6, 4, 8, 8, 8, 8, 8, 2, 8, 0),                       #6: Set idx4 (temp-idx/reg3) of madlibs list to idx2 (reg2)
                Instr(3, 8, 8, 0, us, 2, 8, 2, 8, 0),                      #3: Compare idx2 (reg2) and "_" and assign result to idx2 (reg2)
                Instr(4, 8, 2, 1, hc_size*4+3, 8, 8, 8, 8, 2),             #4: Cond jump to the first step in the dynamic part/Point2 if true/false
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
                Instr(4, 8, 8, (hc_size-i)*2-1, 8, 8, 8, 8, 8, 0)          #4: jump to "Point1" (The steps of jump changes depending on the size of the list of hard coded nouns)
            ]


    footer = [
                ## (Common) Increment k by 1 and jump to Step30
                Instr(2, 8, 8, 1, 8, 8, 8, 6, 8, 0),             ## Point1  #2: add 1 to idx6 (idx-k)
                Instr(4, 8, 8, 4, 8, 8, 8, 8, 8, 0),                        #4: jump to Point3

                ## ELSE: Append from madlibs_list[idx] to res_list
                Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),             ## Point2  #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                Instr(2, 8, 8, s_ml, 8, 8, 8, 4, 8, 0),                     #2: Add s_ml to idx4 (temp-idx/reg3) and shift the pointer (temp-idx) to an appropriate position of the madlibs list
                Instr(6, 4, 8, 8, 8, 8, 8, 2, 8, 0),                        #6: Set idx4 (temp-idx/reg3) of the madlibs list to idx2 (reg2)
                
            ## APPEND and INCREMENT
                Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),             ## Point3  #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                Instr(2, 8, 8, s_rs, 8, 8, 8, 4, 8, 0),                     #2: Add s_rs to idx4 (temp-idx/reg3) and shift the pointer (temp-idx) to an approproate position of the res list
                Instr(7, 8, 8, 2, 8, 8, 8, 8, 4, 1),                        #6: Set idx2 (reg2) to idx4 (temp-idx/reg3) of the res list
                Instr(2, 8, 8, 1, 8, 8, 8, 0, 8, 0),                        #2: Add 1 to idx 0 (idx-i)

            ## Determine whether or not to iterate over again depending idx-i< len(madlibs_words)
                Instr(3, 8, 8, 2, ml_len, 0, 8, 4, 8, 0),                   #3: Compare idx0 (idx-i) < p5 (ml_len) and assign the result to idx4 (reg3)
                Instr(4, 8, 4, hc_size*4+15, 1, 8, 8, 8, 8, 1),             #4: Cond jump to the very beginning/end if true/false

        # END
                Instr(0, 8, 8, 8, 8, 8, 8, 8, 8, 0),                        #0: Terminal
            ]
    
    program = header + dynamic + footer
    repro_prog = make_program(program)

    pc = 0
    weight = 0

    for i in range(n_iter):
        pc, weight = step(repro_prog, pc, repro_mem, weight)
    
    reprod_Y = reveal(repro_mem, s_rs, s_rs + ml_len)
    print('\nreprod_Y: ', reprod_Y)
    
    res = mux(exp_Y == reprod_Y, 
                mux(weight <= threshold, SecretInt(0), SecretInt(1))
                , SecretInt(1))
    assert0(res)
    assert(val_of(res)==0)

    reprod_weight = val_of(weight)
    reprod_size = len(program)
    return reprod_weight, reprod_size