from picozk import *
from madlibs import madlibs

if __name__ == "__main__":
    DEBUG = False
    scale = 5
    num_blanks = scale // 2
    # fmt: off
    p = pow(2,256) - pow(2,32) - pow(2,9) - pow(2,8) - pow(2,7) - pow(2,6) - pow(2,4) - 1
    
    with PicoZKCompiler("irs/picozk_tst", field=[p], options=["ram"]):
        madlibs.run(DEBUG=DEBUG, scale=scale, num_blanks=num_blanks)
    # fmt: on
