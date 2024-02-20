import random
from picozk import *

"""
    The following functions support the execution of the program for the madlibs case:

    - make_phone_entry: Produce random phone entry, name as key and phone# as value
    - make_phone_dict: Constructs a phonebook with a specified # of phone number.
    - make_exp_y: Make a completed phonebook with the aforementioned phonebook and honeywords
    - make_X: Constructs 'X', exclusively used by the producer.
    - reveal: Transforms a picozk-listified sentence into a stringified dictionary.
"""


def make_phone_entry(bg, key_list):
    elem = ""
    for i in range(10):
        if i == 0:
            # 0 Cannot be present at the beginning as it will be transformed into integer later
            ent = random.randint(1, 9)

        else:
            ent = random.randint(0, 9)
        elem += str(ent)

    key = key_list.pop()

    bg.update({key: int(elem)})
    return bg


def make_phone_dict(scale):
    key_list = [s for s in range(scale)]
    random.shuffle(key_list)
    bg = {}
    for i in range(scale):
        make_phone_entry(bg, key_list)
    return bg


def make_honey(scale, num_honeys):
    key_list = [s for s in range(scale, scale + num_honeys)]
    random.shuffle(key_list)
    bg = {}
    for i in range(num_honeys):
        make_phone_entry(bg, key_list)
    return bg


def make_exp_y(bg, honey_entries):
    res = bg.copy()
    res.update(honey_entries)
    res = dict(sorted(res.items(), key=lambda x: x[1]))
    res = [f"('{k}', '{v}')" for k, v in res.items()]
    return ", ".join(res)


def make_X(bg, honey_entries):
    res = bg.copy()
    res.update(honey_entries)
    res = dict(sorted(res.items()))
    res = {k: v for k, v in res.items()}
    return res


def reveal(res_list, start, end):
    # Convert the List to a String
    result_str = ""
    idx = start
    res_list_size = end
    while idx < res_list_size:
        key = str(val_of(res_list[idx]))
        phone = str(val_of(res_list[idx + 1]))

        item_str = "(" + "'" + key + "'" + ", " + "'" + phone + "'" + ")"
        if result_str:
            result_str += ", " + item_str
        else:
            result_str = item_str
        idx += 2
    return result_str
