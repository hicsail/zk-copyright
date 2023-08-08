# from picozk import *
import random

def make_X(madlibs, nouns, S):
    return madlibs.format(S[0], S[1], S[2], nouns[3], nouns[4])


def producer_func(madlibs, nouns, S):
    return madlibs.format(S[0], S[1], S[2], nouns[3], nouns[4])


def reproducer_func(madlibs, nouns):
    words = random.choices(nouns, k = 5)
    return madlibs.format(words[0], words[1], words[2], words[3], words[4])


def main():
    # The Mad Libs template
    madlibs = "I have a {}, which I really {}. Every {}, I walk {} to the {}."

    # The list of potential fill-ins
    nouns = ['dog', 'love', 'day', 'her', 'park', 'ball', 'cat', 'school', 'like', 'hour', 'tree', 'car', 'house', 'week', 'shoe', 'beach']
    S = nouns[0:3]
    X = make_X(madlibs, nouns, S)
    print('Original X', X)

    prod_Y = producer_func(madlibs, nouns, S)
    print('prod_Y', prod_Y)
    reprod_Y = reproducer_func(madlibs, nouns)
    print('reprod_Y', reprod_Y)

    # p = 11
    # n = 2
    # with PicoZKCompiler('irs/picozk_test', field=[p,n]):
    return 

if __name__ == "__main__":
    main()