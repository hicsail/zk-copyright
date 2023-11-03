from picozk import *
from utils.steps import step
from utils.functions import make_program
from .helpers import reveal

def execute(program, mem, ml_len, s_rs, n_iter, exp_Y, threshold):

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

    return val_of(weight), len(program)