from picozk import *
from utils.datatypes import Instr
from utils.steps import step
from utils.functions import make_program
from .helpers import reveal

def producer(X, n_iter, threshold, exp_Y):
    # Producer
    reg1 = 1 #0 i
    reg2 = 0 #2 j
    reg3 = 0 #4 temp index
    reg4 = 0 #6 res etc..
    reg5 = 0 #8 temp
    reg6 = 0 #10 temp
    dummy_int = 0 #12
    X_list = [i for k, v in X.items() for i in (k, v)] #14-27

    bot = 0
    
    mem = ZKList([reg1] + [bot] + [reg2] + [bot] + [reg3] 
                    + [bot] + [reg4] + [bot] + [reg5] + [bot] 
                    + [reg6] + [bot] + [dummy_int] + [bot] + X_list)
    n = len(mem)
    program = [

        ## Set j = 15
        Instr(1, 12, 12, 12, 12, 12,  15, 2, 12, 0),    #Point1    #6: Set 15 to idx2 (idx-j/reg2)

        ## Check if  mem[j+2] < mem[j] 
        Instr(5,  2, 12, 12, 12, 12, 12,  4, 12, 0),    #Point2    #5: Copy idx2 (idx-j/reg2) to idx4 (temp-idx/reg3)
        Instr(2, 12, 12,  2, 12, 12, 12,  4, 12, 0),               #2: Add 2 to idx4 (temp-idx/reg3) = j+2
        Instr(6,  4, 12, 12, 12, 12, 12,  8, 12, 0),               #6: Set mem[mem[4]] (mem[j+2]) to idx8 (reg5)
        Instr(6,  2, 12, 12, 12, 12, 12, 10, 12, 0),               #6: Set mem[mem[2]] (mem[j]) to idx10 (temp1/reg6)
        Instr(3, 12, 10,  2, 12,  8, 12,  6, 12, 1),               #3: Compare mem[8] (reg5/mem[j+2]) < mem[10] (reg6/mem[j]) and assign result to idx6 (reg4)
        Instr(4, 12,  6,  1, 11, 12, 12, 12, 12, 2),               #4: Cond jump to Next/Point3 if true/false

        ## Set mem[j] = mem[j+2] *Set temp1/reg6 = mem[j] is done at Step3
        Instr(7, 12, 12,  8, 12, 12, 12, 12,  2, 0),               #6: Set mem[idx8/reg5] (mem[j+2]) to mem[mem[idx2](=j)]
        
        ## Set mem[j+2] = temp1
        Instr(7, 12, 12, 10, 12, 12, 12, 12,  4, 0),               #6: Set mem[idx10](temp1/reg6) to mem[mem[idx4]] (mem[j+2])
        

        ## Set temp2 = mem[j-1]
        Instr(5,  2, 12, 12, 12, 12, 12,  4, 12, 0),               #5: Copy idx2 (idx-j/reg2) to idx4 (temp-idx/reg3)
        Instr(2, 12, 12,  1, 12, 12, 12,  4, 12, 1),               #2: Subtract 1 from idx4 (temp-idx/reg3) = j-1
        Instr(6,  4, 12, 12, 12, 12, 12,  8, 12, 0),               #6: Set mem[mem[4]] (mem[j-1]) to idx8 (temp2/reg5)

        ## Set mem[j-1] = mem[j+1]
        Instr(5,  2, 12, 12, 12, 12, 12, 10, 12, 0),               #5: Copy idx2 (idx-j/reg2) to idx10 (temp-idx2/reg6)
        Instr(2, 12, 12,  1, 12, 12, 12, 10, 12, 0),               #2: Add 1 to idx10 (temp-idx2/reg6) = j+1
        Instr(6, 10, 12, 12, 12, 12, 12,  6, 12, 0),               #6: Set mem[mem[10]] (mem[j+1]) to idx6
        Instr(7, 12, 12,  6, 12, 12, 12, 12,  4, 0),               #7: Set mem[idx6] (mem[j+1]) to mem[mem[idx4](=j-1)]
        
        ## Set mem[j+1] = temp2
        Instr(7, 12, 12,  8, 12, 12, 12, 12, 10, 0),               #7: Set mem[idx8/reg5] to mem[mem[idx10](=j+1)]

        ## Check if j < n-i-1 and determine to loop or end
        Instr(2, 12, 12,  2, 12, 12, 12,  2, 12, 0),    #Point3    #2: Add 2 to idx2 (idx-j/reg2)
        Instr(1, 12, 12, 12, 12, 12,  n,  6, 12, 0),               #1: Set n (size of mem) to idx 6 (reg4)
        Instr(2, 12, 12,  1, 12, 12, 12,  6, 12, 1),               #2: Subtract 1 from idx6 (reg4)
        Instr(2, 12, 12,  0, 12, 12, 12,  6, 12, 2),               #2: Subtract idx-i(idx0/reg1) from idx6 (reg4)
        Instr(3, 12,  6,  2, 12,  2, 12,  4, 12, 1),               #3: Compare idx6 (idx-j/reg2) < mem[p3] (n-i-1) and assign the result to idx4 (reg3)
        Instr(4, 12,  4, 21,  1, 12, 12, 12, 12, 1),               #4: Cond jump to Point2/Next if true/false

        ## Check if i < n
        Instr(2, 12, 12,  2, 12, 12, 12,  0, 12, 0),               #2: Add 2 to idx0 (idx-i/reg1)
        Instr(3, 12, 12,  2,  n,  0, 12,  4, 12, 0),               #3: Compare idx0 (idx-i/reg1) < n (size of mem) and assign the result to idx4 (reg3)
        Instr(4, 12,  4, 25,  1, 12, 12, 12, 12, 1),               #4: Cond jump to Point1/Next if true/false
                

        # END
        Instr(0, 12, 12, 12, 12, 12, 12, 12, 12, 0),             #100: Terminal
    ]
    pro_prog = make_program(program)

    pc = 0
    weight = 0
    for i in range(n_iter):
        pc, weight = step(pro_prog, pc, mem, weight)

    prod_Y = reveal(mem, 14, len(mem))
    print('\nprod_Y:', prod_Y)

    res = mux(exp_Y == prod_Y,
                mux(weight <= threshold, SecretInt(0), SecretInt(1))
                , SecretInt(1))
    assert0(res)
    assert(exp_Y == prod_Y)
    assert(val_of(weight) <= threshold)

    prod_weight = val_of(weight)
    prod_size = len(program)

    return prod_weight, prod_size, program