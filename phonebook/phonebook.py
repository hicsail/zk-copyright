from picozk import *
from utils.datatypes import Instr
from utils.steps import step
from .debug import debug
from .helpers import make_X, reveal, make_phone_dict, make_Y
from .producer import producer
from .reproducer import reproducer

def run(DEBUG, scale, num_honeys):

    print("\n--- Running phonebook case ", "(scale", scale, " honeys", num_honeys, ")  ---")
    
    if DEBUG==True:
       scale = 5
       bg, honey_entries, exp_Y = debug()
    else:
       bg = make_phone_dict(scale)
       honey_entries = make_phone_dict(num_honeys)
       exp_Y = make_Y(bg, honey_entries)

    n_iter = int(num_honeys + 22*(scale+num_honeys)*(scale+num_honeys+1)/2 + 4*(scale+num_honeys+1))
    threshold = n_iter*2 # The program has to be performed within this (weight < )

    bg = dict(sorted(bg.items()))
    print("\nbg", bg)
    print("\nhoney_entries", honey_entries)
    X = make_X(bg, honey_entries)
    print("\nexp_Y", exp_Y)

    prod_weight, prod_size, program =  producer(X, n_iter, threshold, exp_Y)
    reprod_weight, reprod_size =  reproducer(bg, honey_entries, program, n_iter, threshold, exp_Y)

    return prod_weight, prod_size, reprod_weight, reprod_size