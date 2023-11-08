from picozk import *
from madlibs import madlibs

if __name__ == "__main__":
    DEBUG = True
    scale = 5
    num_blanks = scale // 2
    # fmt: off
    p = pow(2,61) - 1
    
    with PicoZKCompiler("picozk_test", field=[p], options=["ram"]):
        madlibs.run(DEBUG=DEBUG, scale=scale, num_blanks=num_blanks)
    # fmt: on
