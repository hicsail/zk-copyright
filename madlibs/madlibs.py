from picozk import *
from utils.functions import word_to_integer
from .debug import debug
from .helpers import make_exp_y, make_madlibs, get_blanks, make_nouns, make_X
from .execute import execute
from .assembly import assembly


def run(DEBUG, scale, num_blanks):
    print("\n--- Running madlibs case ", "(scale", scale, " num_blanks", num_blanks, ")  ---")

    if DEBUG == True:
        scale = 16
        exp_Y, madlibs, nouns, blank_idx = debug()

    else:
        exp_Y, _exp_Y = make_exp_y(scale)

        blank_idx = get_blanks(_exp_Y, num_blanks)

        from_x = blank_idx[int(len(blank_idx) / 2)]

        madlibs = make_madlibs(_exp_Y, blank_idx)

        nouns = make_nouns(_exp_Y, blank_idx)

    # Configure # of iteration and threshold to validate proof
    n_iter = (11 + 4 * (int(scale / 2) + 1) + 11) * scale
    threshold = n_iter * 2  # The program has to be performed within this (weight < )

    # Create X for producer function
    from_x = blank_idx[int(len(blank_idx) / 2)]
    X = make_X(madlibs, nouns, blank_idx, from_x, int(len(blank_idx) / 2))

    # Listify all components
    X_list = [str(word_to_integer(_str)) for _str in X.split()]
    nouns_list = [str(word_to_integer(_str)) for _str in nouns]
    madlibs_list = [str(word_to_integer(_str)) for _str in madlibs]
    exp_Y = " ".join([str(word_to_integer(_str)) for _str in exp_Y.split()])

    # Print out components
    print("\n  madlibs:", madlibs)
    print("\n  nouns:", nouns_list)
    print("\n  X: ", " ".join(X_list))
    print("\n  exp_y:", exp_Y)

    # Organize indexes
    X_len = len(X_list)
    ml_len = len(madlibs_list)

    s_nl = 10
    s_ml = s_nl + len(nouns_list) + 1
    s_xl = s_ml + ml_len + 1
    s_rs = s_xl + X_len + 1

    """
        ----- Producer execution -----
    """

    print("\n  Running Producer function")

    # Build Producer memory
    reg1 = 0  # 0
    reg2 = 0  # 2
    reg3 = 0  # 4
    reg4 = 0  # 6
    dummy_int = 0  # 8
    bot = 0

    nouns_list = nouns_list  # 10-25
    madlibs_list = madlibs_list  # 27 - 42
    X_list = X_list  # 44 - 59
    res_list = [0] * max(
        7, ml_len
    )  # 61 - 76 Need min 7 space so that a program pointer at the final step does not exceed memory length

    mem = ZKList(
        [reg1]
        + [bot]
        + [reg2]
        + [bot]
        + [reg3]
        + [bot]
        + [reg4]
        + [bot]
        + [dummy_int]
        + [bot]
        + nouns_list
        + [bot]
        + madlibs_list
        + [bot]
        + X_list
        + [bot]
        + res_list
    )

    # Build producer Program
    is_producer = True
    fwd = 9
    bwd = 21

    # Organize hard code related components
    hc_size = len([x for x in blank_idx if x >= from_x])
    non_hc_size = len(blank_idx) - hc_size
    hcs = [word_to_integer(_str) for _str in nouns[non_hc_size : non_hc_size + hc_size]]

    program = assembly(is_producer, fwd, bwd, s_ml, hc_size, hcs, s_rs, ml_len, from_x, s_xl)
    prod_weight, prod_size = execute(program, mem, ml_len, s_rs, n_iter, exp_Y, threshold)

    """
        ----- Re-producer execution -----
    """

    print("\n  Running Reproducer function")

    # Build Reproducer memory
    reg1 = 0  # 0
    reg2 = 0  # 2
    reg3 = 0  # 4
    reg4 = 0  # 6
    dummy_int = 0  # 8
    bot = 0

    nouns_list = nouns_list  # 10-25
    madlibs_list = madlibs_list  # 27 - 42
    bots_list = [0] * X_len  # 44 - 59
    res_list = [0] * max(
        7, ml_len
    )  # 61 - 76 Need min 7 space so that a program pointer at the final step does not exceed memory length

    repro_mem = ZKList(
        [reg1]
        + [bot]
        + [reg2]
        + [bot]
        + [reg3]
        + [bot]
        + [reg4]
        + [bot]
        + [dummy_int]
        + [bot]
        + nouns_list
        + [bot]
        + madlibs_list
        + [bot]
        + bots_list
        + [bot]
        + res_list
    )

    # Build reproducer Program
    is_producer = False
    fwd = 3
    bwd = 15

    # Organize hard code related components
    hc_size = len(blank_idx)
    hcs = [word_to_integer(nouns[i]) for i in range(hc_size)]

    reprogram = assembly(is_producer, fwd, bwd, s_ml, hc_size, hcs, s_rs, ml_len)
    reprod_weight, reprod_size = execute(
        reprogram, repro_mem, ml_len, s_rs, n_iter, exp_Y, threshold
    )

    return prod_weight, prod_size, reprod_weight, reprod_size
