from picozk import *
from utils.datatypes import Instr
from utils.steps import step
from utils.functions import make_program, string_to_int
from .helpers import reveal

def reproducer(bg, honey_entries, program, n_iter, threshold, exp_Y):
    reg1 = 1 #0 i
    reg2 = 0 #2 j
    reg3 = 0 #4 temp index
    reg4 = 0 #6 res etc..
    reg5 = 0 #8 temp
    reg6 = 0 #10 temp
    dummy_int = 0 #12
    bg_list = [string_to_int(i) for k, v in bg.items() for i in (k, v)] #14-23
    honey_entries = [string_to_int(i) for k, v in honey_entries.items() for i in (k, v)]
    _honey_entries = [0] * len(honey_entries) #24-27
    
    bot = 0
    
    repro_mem = ZKList([reg1] + [bot] + [reg2] + [bot] + [reg3] 
                        + [bot] + [reg4] + [bot] + [reg5] + [bot] 
                        + [reg6] + [bot] + [dummy_int] + [bot] + bg_list + _honey_entries)

    idxHE = 14 + len(bg_list)

    header = []
    # Hard code honey entries
    for i in range(len(honey_entries)):
        header += [
            Instr(1, 12, 12, 12, 12, 12, honey_entries[i], idxHE + i, 12, 0),            #6: Set hc1 to mem[24]
        ]
        
    program = header + program #The of the code is same as the producer's

    repro_prog = make_program(program)

    pc = 0
    weight = 0
    for i in range(n_iter):
        pc, weight = step(repro_prog, pc, repro_mem, weight)

    repro_Y = reveal(repro_mem, 14, len(repro_mem))
    print('\nreprod_Y:', repro_Y)

    res = mux(exp_Y == repro_Y,
                mux(weight <= threshold, SecretInt(0), SecretInt(1))
                , SecretInt(1))
    assert0(res)
    assert(exp_Y == repro_Y)
    assert(val_of(weight) <= threshold)

    reprod_weight = val_of(weight)
    reprod_size = len(program)

    return reprod_weight, reprod_size