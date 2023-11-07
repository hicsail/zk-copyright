from picozk import *
from .debug import debug
from .helpers import make_X, make_phone_dict, make_exp_y
from .execute import execute
from .assembly import assembly

def run(DEBUG, scale, num_honeys):

    print("\n--- Running phonebook case ", "(scale", scale, " honeys", num_honeys, ")  ---")
    
    if DEBUG==True:
       scale = 5
       bg, honey_entries, exp_Y = debug()

    else:
       bg = make_phone_dict(scale)
       honey_entries = make_phone_dict(num_honeys)
       exp_Y = make_exp_y(bg, honey_entries)


    # Configure # of iteration and threshold to validate proof
    n_iter = int(num_honeys + 22*(scale+num_honeys)*(scale+num_honeys+1)/2 + 4*(scale+num_honeys+1))
    threshold = n_iter*2 # The program has to be performed within this (weight < )


    # Sort bg and Create X for producer function (Sorting bg is important, otherwise producer func typicaly takes longer)
    bg = dict(sorted(bg.items()))
    X = make_X(bg, honey_entries)

    # Print out components    
    print("\n  bg", bg)
    print("\n  honey_entries", honey_entries)
    print("\n  X", X)
    print("\n  exp_Y", exp_Y)

    

    '''
        ----- Producer execution -----
    '''
    
    print("\n  Running Producer function")

    # Build Producer memory
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

    # Build producer Program
    n = len(mem)
    is_producer = True
    program = assembly(is_producer, n)
    prod_weight, prod_size =  execute(program, mem, n_iter, threshold, exp_Y)



    '''
        ----- Re-producer execution -----
    '''
    
    print("\n  Running Reproducer function")

    # Build Reproducer memory
    reg1 = 1 #0 i
    reg2 = 0 #2 j
    reg3 = 0 #4 temp index
    reg4 = 0 #6 res etc..
    reg5 = 0 #8 temp
    reg6 = 0 #10 temp
    dummy_int = 0 #12
    bg_list = [i for k, v in bg.items() for i in (k, v)] #14-23
    honey_entries = [i for k, v in honey_entries.items() for i in (k, v)]
    _honey_entries = [0] * len(honey_entries) #24-27
    
    bot = 0
    
    repro_mem = ZKList([reg1] + [bot] + [reg2] + [bot] + [reg3] 
                        + [bot] + [reg4] + [bot] + [reg5] + [bot] 
                        + [reg6] + [bot] + [dummy_int] + [bot] + bg_list + _honey_entries)


    # Build reproducer Program
    n = len(repro_mem)
    is_producer = False
    idxHE = 14 + len(bg_list)
    
    reprogram = assembly(is_producer, n, honey_entries, idxHE)
    reprod_weight, reprod_size =  execute(reprogram, repro_mem, n_iter, threshold, exp_Y)

    return prod_weight, prod_size, reprod_weight, reprod_size