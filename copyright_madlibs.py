from picozk import *
from utils.datatypes import Instr
from utils.steps import step
from utils.functions import make_program, int_to_string, string_to_int
import random
from faker import Faker


def make_exp_y(scale):
  
    fake = Faker() # Create an instance of Faker

    exp_Y = fake.sentence(nb_words=scale)
    exp_Y = exp_Y[:-1]

    _exp_Y = exp_Y.split()  # Splitting the sentence into words
        
    ''' Faker does not necessarily produce a fix number of words, but outputs the fixed number of words 'on average'
        Below if-else adjust the number of words by concatenating or removing to/from the tail of the sentence.
    '''
    if len(_exp_Y) < scale:
        increment = scale - len(_exp_Y)
        _exp_Y += _exp_Y[0:increment]
        exp_Y = " ".join(_exp_Y)

    elif len(_exp_Y) > scale:
        _exp_Y = _exp_Y[0:scale]
        exp_Y = " ".join(_exp_Y)
    return exp_Y, _exp_Y


def get_blanks(exp_Y, num_blanks):
    # Using integer division to ensure the second argument is an integer
    blank_idx = random.sample(range(0, len(exp_Y)), num_blanks)
    blank_idx.sort()
    return blank_idx


def make_madlibs(exp_Y, blank_idx):

    # Making madlibs
    madlibs = ['_' if i in blank_idx else exp_Y[i] for i in range(len(exp_Y))]
    
    return madlibs


def make_nouns(exp_Y, blank_idx):

    # Using list comprehension to get words at specific indices
    nouns = [exp_Y[i] for i in blank_idx]

    # Generate random words
    fake_add = Faker()

    addition = fake_add.words(nb=3, unique=False)
    nouns += addition
    return nouns


def make_X(madlibs, nouns, blank_idx, from_x, aft_idx):

    X = madlibs.copy()
    i = 0
    idx = range(len(blank_idx))

    for k in range(len(X)):
        if X[k] == '_':
            ''' from_x represents a threshold index as to whether nouns be same as Y or not
                Meaning, every noun in X matches Y till from_x and differs for noun in a blank(_)'''
            
            if k < from_x:
                X[k] = nouns[idx[i]]
                i+=1
            else:
                ''' aft_idx indicates a beginning index in 'nouns' for nouns not being used in Y
                    Therefore, the below deliberately samples nouns from unused list so that X is different from Y'''
                X[k] = random.sample(nouns[aft_idx:], 1)[0] 

    X = ' '.join(X)

    return X



def reveal(mem, st, end):

    if not (0 <= st <= len(mem)) or not (end <= len(mem)):
        raise ValueError("Start and end indices must be within the bounds of the list.")
    
    res = ""
    for i in range(st, end):
        res += int_to_string(val_of(mem[i])) + " "
    
    return res[:-1]
        
def debug():
   
    exp_Y = "I have a dog and cat , and every day I walk them to the park"
    print("\nexp_y:", exp_Y)

    blank_idx = [3, 5, 9, 12, 15]
    
    madlibs = "I have a _ and _ , and every _ I walk _ to the _".split()
    print("\nmadlibs:", madlibs)

    nouns = ['dog', 'cat', 'day', 'them', 'park', 'beach', 'her', 'school', 'like', 'hour', 'tree', 'car', 'house', 'week', 'shoe', 'beach']
    print("\nnouns:", nouns)

    from_x = 10

    X = make_X(madlibs, nouns, blank_idx, from_x)
    print('\nX: ', X)

    return exp_Y, X, madlibs, nouns, blank_idx, from_x

def main():
    
    DEBUG=False
    scale = 10
    n_iter = (11+4*(int(scale/2)+1)+11)*scale
    threshold = n_iter*2 # The program has to be performed within this (weight < )

    if DEBUG==True:
       exp_Y, X, madlibs, nouns, blank_idx, from_x = debug()

    else:
        exp_Y, _exp_Y = make_exp_y(scale)
        print("\nexp_y:", exp_Y)
        
        num_blanks = max(1, len(_exp_Y) // 3)
        blank_idx = get_blanks(_exp_Y, num_blanks)

        from_x = blank_idx[int(len(blank_idx)/2)]

        madlibs = make_madlibs(_exp_Y, blank_idx)
        print("\nmadlibs:", madlibs)

        nouns = make_nouns(_exp_Y, blank_idx)
        print("\nnouns:", nouns)

        X = make_X(madlibs, nouns, blank_idx, from_x, int(len(blank_idx)/2))
        print('\nX: ', X)

    X_list = [string_to_int(_str) for _str in X.split()]
    nouns_list = [string_to_int(_str) for _str in nouns]
    madlibs_list = [string_to_int(_str) for _str in madlibs]
    
    hc_size = len([x for x in blank_idx if x >= from_x])
    non_hc_size = len(blank_idx) - hc_size
    hcs = [string_to_int(_str) for _str in nouns[non_hc_size: non_hc_size + hc_size]]

    us = string_to_int("_")

    p = pow(2,256) - pow(2,32) - pow(2,9) - pow(2,8) - pow(2,7) - pow(2,6) - pow(2,4) - 1
    
    
    X_len = len(X_list)
    ml_len = len(madlibs_list)
    
    s_nl = 10
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

if __name__ == "__main__":
        main()