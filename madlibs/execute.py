from picozk import *
from utils.steps import step
from utils.functions import make_program
from .helpers import reveal

def execute(program, mem, ml_len, s_rs, n_iter, exp_Y, threshold):

    prog = make_program(program)

    pc = 0
    weight = 0
    for i in range(n_iter):
        pc, weight = step(prog, pc, mem, weight)

    Y = reveal(mem, s_rs, s_rs + ml_len)
    print('\n     Output:', Y)

    res = mux(exp_Y == Y,
                mux(weight <= threshold, SecretInt(0), SecretInt(1))
                , SecretInt(1))

    assert0(res)
    assert(val_of(res)==0)
    assert(val_of(weight) <= threshold)

    return val_of(weight), len(program)