from picozk import *
from utils.functions import int_to_string
import random
from faker import Faker

"""
    The following functions support the execution of the program for the madlibs case:

    - make_exp_y: Constructs a sentence with a specified length.
    - get_blanks: Generates a list of indices corresponding to blank spaces in the sentence produced by make_exp_y.
    - make_madlibs: Produces a list of words and "_" based on the outputs from the aforementioned methods.
    - make_nouns: Creates a list of nouns using exp_y and indices of blanks, then appends random English words.
    - make_X: Constructs 'X', exclusively used by the producer.
    - reveal: Transforms a picozk-listified sentence into a string.
"""


def make_exp_y(scale):
    fake = Faker()  # Create an instance of Faker

    exp_Y = fake.sentence(nb_words=scale)
    exp_Y = exp_Y[:-1]

    _exp_Y = exp_Y.split()  # Splitting the sentence into words

    """ Faker does not necessarily produce a fix number of words, but outputs the fixed number of words 'on average'
        Below if-else adjust the number of words by concatenating or removing to/from the tail of the sentence.
    """
    if len(_exp_Y) < scale:
        increment = scale - len(_exp_Y)
        _exp_Y += _exp_Y[0:increment]
        exp_Y = " ".join(_exp_Y)

    elif len(_exp_Y) > scale:
        _exp_Y = _exp_Y[0:scale]
        exp_Y = " ".join(_exp_Y)
    return exp_Y, _exp_Y


def get_blanks(exp_Y, num_blanks):
    # Using integer division to ensure the second argument is an integer
    blank_idx = random.sample(range(0, len(exp_Y)), num_blanks)
    blank_idx.sort()
    return blank_idx


def make_madlibs(exp_Y, blank_idx):
    # Making madlibs
    madlibs = ["_" if i in blank_idx else exp_Y[i] for i in range(len(exp_Y))]

    return madlibs


def make_nouns(exp_Y, blank_idx):
    # Using list comprehension to get words at specific indices
    nouns = [exp_Y[i] for i in blank_idx]

    # Generate random words
    fake_add = Faker()

    addition = fake_add.words(nb=int(len(exp_Y) // 2), unique=False)
    nouns += addition
    return nouns


def make_X(madlibs, nouns, blank_idx, from_x, aft_idx):
    X = madlibs.copy()
    i = 0
    idx = range(len(blank_idx))

    for k in range(len(X)):
        if X[k] == "_":
            """from_x represents a threshold index as to whether nouns be same as Y or not
            Meaning, every noun in X matches Y till from_x and differs for noun in a blank(_)
            """

            if k < from_x:
                X[k] = nouns[idx[i]]
                i += 1
            else:
                """aft_idx indicates a beginning index in 'nouns' for nouns not being used in Y
                Therefore, the below deliberately samples nouns from unused list so that X is different from Y
                """
                X[k] = random.sample(nouns[aft_idx:], 1)[0]

    X = " ".join(X)

    return X


def reveal(mem, st, end):
    if not (0 <= st <= len(mem)) or not (end <= len(mem)):
        raise ValueError("Start and end indices must be within the bounds of the list.")

    res = ""
    for i in range(st, end):
        res += str(val_of(mem[i])) + " "
    
    return res[:-1]
