from picozk import *
from phonebook import phonebook

if __name__ == "__main__":
    DEBUG = False
    scale = 5
    num_honeys = int(max(1, scale / 10))
    p = pow(2, 61) - 1

    with PicoZKCompiler("irs/picozk_test", field=[p], options=["ram"]):
        phonebook.run(DEBUG, scale, num_honeys)
