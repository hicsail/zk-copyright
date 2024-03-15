from picozk import *
from madlibs import madlibs

if __name__ == "__main__":
    DEBUG = True
    scale = 5
    num_blanks = scale // 2
    p = 115792089237316195423570985008687907853269984665640564039457584007913129640233
    with PicoZKCompiler("irs/picozk_test", field=[p], options=["ram"]):
        madlibs.run(DEBUG=DEBUG, scale=scale, num_blanks=num_blanks, p=p)
