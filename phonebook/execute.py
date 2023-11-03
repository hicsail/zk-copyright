from picozk import *
from utils.steps import step
from utils.functions import make_program
from .helpers import reveal

def execute(program, mem, n_iter, threshold, exp_Y):
    
    prog = make_program(program)

    pc = 0
    weight = 0
    for i in range(n_iter):
        pc, weight = step(prog, pc, mem, weight)

    Y = reveal(mem, 14, len(mem))
    print('\n     Output:', Y)

    res = mux(exp_Y == Y,
                mux(weight <= threshold, SecretInt(0), SecretInt(1))
                , SecretInt(1))
    
    assert0(res)
    assert(exp_Y == Y)
    assert(val_of(weight) <= threshold)

    return val_of(weight), len(program)