from picozk import *
from madlibs import run

if __name__ == "__main__":

    DEBUG=False
    scale = 5
    num_blanks = scale//2

    p = pow(2,256) - pow(2,32) - pow(2,9) - pow(2,8) - pow(2,7) - pow(2,6) - pow(2,4) - 1

    with PicoZKCompiler('irs/picozk_test', field=[p], options=['ram']):
        run.execute(DEBUG=DEBUG, scale=scale, num_blanks=num_blanks)