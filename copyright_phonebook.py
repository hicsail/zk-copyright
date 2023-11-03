from picozk import *
from phonebook import phonebook

if __name__ == "__main__":
    
    DEBUG=True
    scale = 5
    num_honeys = int(max(1, scale/10))
    p = pow(2,256) - pow(2,32) - pow(2,9) - pow(2,8) - pow(2,7) - pow(2,6) - pow(2,4) - 1
    with PicoZKCompiler('irs/picozk_test', field=[p], options=['ram']):
        phonebook.run(DEBUG, scale, num_honeys)