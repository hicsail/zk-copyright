from picozk import *
from utils.datatypes import Instr
from utils.steps import step
from utils.functions import make_program, string_to_int
from .debug import debug
from .helpers import make_exp_y, make_madlibs, get_blanks, make_nouns, make_X, reveal
from .producer import producer
from .reproducer import reproducer

def run(DEBUG, scale, num_blanks):
    print("\n--- Running madlibs case ", "(scale", scale, ")  ---")
    
    if DEBUG==True:
        scale = 16
        exp_Y, madlibs, nouns, blank_idx = debug()

    else:
        exp_Y, _exp_Y = make_exp_y(scale)
        print("\nexp_y:", exp_Y)
        
        blank_idx = get_blanks(_exp_Y, num_blanks)

        from_x = blank_idx[int(len(blank_idx)/2)]

        madlibs = make_madlibs(_exp_Y, blank_idx)
        print("\nmadlibs:", madlibs)

        nouns = make_nouns(_exp_Y, blank_idx)
        print("\nnouns:", nouns)

    n_iter = (11+4*(int(scale/2)+1)+11)*scale
    threshold = n_iter*2 # The program has to be performed within this (weight < )
    
    from_x = blank_idx[int(len(blank_idx)/2)]
    X = make_X(madlibs, nouns, blank_idx, from_x, int(len(blank_idx)/2))
    print('\nX: ', X)

    X_list = [string_to_int(_str) for _str in X.split()]
    nouns_list = [string_to_int(_str) for _str in nouns]
    madlibs_list = [string_to_int(_str) for _str in madlibs]
    
    hc_size = len([x for x in blank_idx if x >= from_x])
    non_hc_size = len(blank_idx) - hc_size
    hcs = [string_to_int(_str) for _str in nouns[non_hc_size: non_hc_size + hc_size]]

    us = string_to_int("_")

    X_len = len(X_list)
    ml_len = len(madlibs_list)
    
    s_nl = 10
    s_ml = s_nl + len(nouns_list) + 1
    s_xl = s_ml + ml_len + 1
    s_rs = s_xl + X_len + 1
    prod_weight, prod_size = producer(nouns_list, madlibs_list, X_list,  ml_len, s_ml, us, hc_size, from_x, s_xl, hcs, s_rs, n_iter, exp_Y, threshold)
    reprod_weight, reprod_size = reproducer(nouns_list, madlibs_list, X_len, ml_len, blank_idx, s_ml, us, s_rs, n_iter, exp_Y, threshold)

    return prod_weight, prod_size, reprod_weight, reprod_size