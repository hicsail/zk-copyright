import random
from picozk import *
from utils.functions import int_to_string, string_to_int

def make_X(bg, honey_entries):
    res = bg.copy()
    res.update(honey_entries)
    res = dict(sorted(res.items()))
    res = {string_to_int(k): string_to_int(v) for k, v in res.items()}
    return res


def reveal(res_list, start, end):
    # Convert the List to a String
    result_str = ""
    idx = start
    res_list_size = end
    while idx < res_list_size:
        # Convert each tuple to a string and add to result_str
        item_str = "(" + "'" + int_to_string(val_of(res_list[idx])) + "'" + ", " + "'" + int_to_string(val_of(res_list[idx+1])) + "'" + ")"
        if result_str:
            result_str += ", " + item_str
        else:
            result_str = item_str
        idx += 2
    return result_str


def make_phone_entry(bg):

    elem = ''
    for i in range(10):
        ent = str(random.randint(0, 9))
        if i == 3 or i==6:
            elem+='-'
        elem += ent

    key = str(random.randint(0, 2**63 - 1))

    bg.update({key:elem})
    return bg


def make_phone_dict(scale):
    bg = {}
    for i in range(scale):
        make_phone_entry(bg)
    return bg



def make_Y(bg, honey_entries):
    res = bg.copy()
    res.update(honey_entries)
    res = dict(sorted(res.items(), key=lambda x: x[1]))
    res = [f"('{k}', '{v}')" for k, v in res.items()]
    return ", ".join(res)