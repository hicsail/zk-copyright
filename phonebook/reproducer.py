from picozk import *
from utils.steps import step
from utils.functions import make_program
from .helpers import reveal


def reproducer(program, repro_mem, n_iter, threshold, exp_Y):
    repro_prog = make_program(program)

    pc = 0
    weight = 0
    for i in range(n_iter):
        pc, weight = step(repro_prog, pc, repro_mem, weight)

    repro_Y = reveal(repro_mem, 14, len(repro_mem))
    print("\nreprod_Y:", repro_Y)

    res = mux(
        exp_Y == repro_Y, mux(weight <= threshold, SecretInt(0), SecretInt(1)), SecretInt(1)
    )
    assert0(res)
    assert exp_Y == repro_Y
    assert val_of(weight) <= threshold

    return val_of(weight), len(program)
