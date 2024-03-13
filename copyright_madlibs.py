from picozk import *
from madlibs import madlibs

if __name__ == "__main__":
    DEBUG = False
    scale = 5
    num_blanks = scale // 2
    p = pow(2, 256) - 1
    with PicoZKCompiler("irs/picozk_test", field=[p], options=["ram"]):
        madlibs.run(DEBUG=DEBUG, scale=scale, num_blanks=num_blanks, p=p)
