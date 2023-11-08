from picozk import *
from madlibs import madlibs

if __name__ == "__main__":
    DEBUG = True
    scale = 10
    num_blanks = scale // 2

    p = 2305843009213693951

    with PicoZKCompiler("picozk_test", field=[p], options=["ram"]):
        madlibs.run(DEBUG=DEBUG, scale=scale, num_blanks=num_blanks)
