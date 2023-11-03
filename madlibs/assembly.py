from utils.datatypes import Instr
from utils.functions import string_to_int

'''
    This method compiles the instructions for the madlibs copyright case. 
    While both the producer and reproducer share common instructions in the header and footer, 
    the specific set of instructions varies based on the 'is_producer' argument.

    A fundamental aspect of the madlibs case is that the reproducer needs to fill in more blanks, denoted by hc_size. 
    It's also noteworthy that the producer copies certain nouns from X, as seen in the 'header2' section. Due to this 'header2' section, 
    the jump steps in line 5 and the penultimate line differ by fwd/bwd when compared to the reproducer's instruction set.
'''


def assembly(is_producer, fwd, bwd, s_ml, hc_size, hcs, s_rs, ml_len, from_x=None, s_xl=None):

    us = string_to_int("_")

    # Hard-Code all blanks from the nouns list
    header = [

            ## IF madlibs_words[curr] == "_"
                Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),                       #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                Instr(2, 8, 8, s_ml, 8, 8, 8, 4, 8, 0),                    #2: Add s_ml to idx4 (temp-idx/reg3) and shift the pointer (temp-idx) to the madlibs list
                Instr(6, 4, 8, 8, 8, 8, 8, 2, 8, 0),                       #6: Set idx4 (temp-idx/reg3) of madlibs list to idx2 (reg2)
                Instr(3, 8, 8, 0, us, 2, 8, 2, 8, 0),                      #3: Compare idx2 (reg2) and "_" and assign result to idx2 (reg2)
                Instr(4, 8, 2, 1, hc_size*4+fwd, 8, 8, 8, 8, 2),           #4: Cond jump to the first step in the dynamic part/Point2 if true/false
            ]
    header2 = [
                ## SECOND IF index of madlibs_words is less than lim
                Instr(3, 8, 8,  2,from_x, 0, 8, 2, 8, 0),                  #3: Compare idx0 (idx-i/reg1) < from_x and set the result to idx2 (reg2)
                Instr(4, 8, 2,  1,  5, 8, 8, 8, 8, 2),                     #4: Cond jump to Next/Dynamic if true/false

            ## IF Both TRUE (Append from X list)
                Instr(5, 0, 8, 8, 8, 8, 8, 4, 8, 0),                       #5: Copy idx0 (idx-i/reg1) to idx4 (temp-idx/reg3)
                Instr(2, 8, 8, s_xl, 8, 8, 8, 4, 8, 0),                    #2: Add s_xl to idx4 (temp-idx/reg3) and shift the pointer (temp-idx) to an appropriate position of the X_list
                Instr(6, 4, 8, 8, 8, 8, 8, 2, 8, 0),                       #6: Set idx4 (temp-idx/reg3) of X_words to idx2 (reg2)
                Instr(4, 8, 2, 1, hc_size*4+6, 8, 8, 8, 8, 2),             #4: Cond jump to the first step in the dynamic part/Point2 if true/false
            
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
                Instr(4, 8, 4, hc_size*4+bwd,  1, 8, 8, 8, 8, 1),           #4: Cond jump to the very beginning/end if true/false

        # END
                Instr(0, 8, 8, 8, 8, 8, 8, 8, 8, 0),                        #0: Terminal
            ]
    
    if is_producer==True:
        return header + header2 + dynamic + footer
    else:
        return header + dynamic + footer