# from picozk import *
import random

def make_X(madlibs, nouns, S):
    X = madlibs.split()
    i = 0

    for j, s in enumerate(X):
        if s =='_':
            X[j] = S[i]
            i+=1
            if i == len(S):
                break
    _X = ' '.join(X) # This is the madlibs text with only words in S are filled
    
    for k in range(j, len(X)):
        if X[k] == '_':
            X[k] = nouns[i]
            i+=1

    X = ' '.join(X) # This is the madlibs text with all blanks are filled

    return _X, X


def fill_blank(text, fill):
    return ' '.join([word if word != '_' else fill.pop(0) for word in text.split()])


def producer_func(nouns, _X):
    first = nouns[3]
    second = nouns[4]

    fill = [first, second]

    return fill_blank(_X, fill)


def reproducer_func(madlibs, nouns):
    first = nouns[3]
    second = nouns[4]
    third = nouns[5]
    fourth = nouns[6]
    fifth = nouns[7]

    fill = [first, second, third, fourth, fifth]

    return fill_blank(madlibs, fill)


def main():
    # The Mad Libs template
    madlibs = "I have a _ which I really _ and every _ I walk _ to the _"

    # The list of potential fill-ins
    nouns = ['dog', 'love', 'day', 'her', 'park', 'ball', 'cat', 'school', 'like', 'hour', 'tree', 'car', 'house', 'week', 'shoe', 'beach']

    S = nouns[0:3]
    print('S', S)
    print('')

    _X, X = make_X(madlibs, nouns, S)
    print('X: ', X)
    print('')
    print("_X: ", _X)
    print('')

    prod_Y = producer_func(nouns, _X)
    print('prod_Y: ', prod_Y)
    print('')

    reprod_Y = reproducer_func(madlibs, nouns)
    print('reprod_Y: ', reprod_Y)
    print('')
    # p = 11
    # n = 2
    # with PicoZKCompiler('irs/picozk_test', field=[p,n]):

if __name__ == "__main__":
    main()