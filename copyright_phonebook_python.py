from dataclasses import dataclass
from picozk import *

# Class to hold a single instruction
@dataclass
class Instr:
    def __init__(self, opcode: int, src1: int, src2: int, src3: int, src4: int, src5: int, src6: int,
                 dest: int, s_dest: int,
                 imm: int):
        self.opcode = opcode
        self.src1 = src1
        self.src2 = src2
        self.src3 = src3
        self.src4 = src4
        self.src5 = src5
        self.src6 = src6
        self.dest = dest
        self.s_dest = s_dest
        self.imm = imm


# Class to hold a program as multiple lists of instructions
@dataclass
class Program:
    def __init__(self, opcode: ZKList, src1: ZKList, src2: ZKList, src3: ZKList, src4: ZKList, src5: ZKList, src6: ZKList,
             dest: ZKList, s_dest: ZKList, imm: ZKList):
        
        self.opcode: ZKList = opcode
        self.src1: ZKList = src1
        self.src2: ZKList = src2
        self.src3: ZKList = src3
        self.src4: ZKList = src4
        self.src5: ZKList = src5
        self.src6: ZKList = src6
        self.dest: ZKList = dest
        self.s_dest: ZKList = s_dest
        self.imm: ZKList = imm




def make_program(prog):
    length = len(prog)
    opcode = ZKList([0 for _ in range(length)])
    src1 = ZKList([0 for _ in range(length)])
    src2 = ZKList([0 for _ in range(length)])
    src3 = ZKList([0 for _ in range(length)])
    src4 = ZKList([0 for _ in range(length)])
    src5 = ZKList([0 for _ in range(length)])
    src6 = ZKList([0 for _ in range(length)])
    dest = ZKList([0 for _ in range(length)])
    s_dest = ZKList([0 for _ in range(length)])
    imm = ZKList([0 for _ in range(length)])

    for i, instr in enumerate(prog):
        opcode[i] = instr.opcode
        src1[i] = instr.src1
        src2[i] = instr.src2
        src3[i] = instr.src3
        src4[i] = instr.src4
        src5[i] = instr.src5
        src6[i] = instr.src6
        dest[i] = instr.dest
        s_dest[i] = instr.s_dest
        imm[i] = instr.imm

    return Program(opcode, src1, src2, src3, src4, src5, src6,
                   dest, s_dest,
                   imm)


# Fetch an instruction from a program
def fetch(prog: Program, pc: SecretInt):
    return Instr(prog.opcode[pc],
                 prog.src1[pc],
                 prog.src2[pc],
                 prog.src3[pc],
                 prog.src4[pc],
                 prog.src5[pc],
                 prog.src6[pc],
                 prog.dest[pc],
                 prog.s_dest[pc],
                 prog.imm[pc])


def make_X(bg, honey_entries):
    res = bg.copy()
    res.update(honey_entries)
    return res


def string_to_int(s):
    return int(''.join(format(ord(char), '08b') for char in s), 2)


def int_to_string(n):
    binary_str = format(n, 'b')
    binary_str = '0' * ((8 - len(binary_str) % 8) % 8) + binary_str
    return ''.join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8))


def list_to_string(res_list):
    # Convert the List to a String
    result_str = ""
    idx = 0
    res_list_size = len(res_list)
    while idx < res_list_size:
        # Convert each tuple to a string and add to result_str
        item_str = "(" + "'" + int_to_string(val_of(res_list[idx][0])) + "'" + ", " + "'" + int_to_string(val_of(res_list[idx][1])) + "'" + ")"
        if result_str:
            result_str += ", " + item_str
        else:
            result_str = item_str
        idx += 1
    return result_str


def sort_by(input_list, sort_key):
    # Sort the List of Tuples
    n = len(input_list)
    i = 0
    while i < n:
        j = 0
        while j < n-i-1:
            # Compare the first element of each tuple
            if input_list[j][sort_key] > input_list[j+1][sort_key]:
                temp = input_list[j]
                input_list[j] = input_list[j+1]
                input_list[j+1] = temp
            j += 1
        i += 1
    return input_list


def producer_func(X):
    temp_list = [(k,v) for k,v in X.items()]
    return sort_by(temp_list, 0)


def reproducer_func(bg, honey_entries):
    temp_list = [(k,v) for k,v in bg.items()]
    temp_list += honey_entries
    return sort_by(temp_list, 1)


def main():

    bg = {
        string_to_int('1'): string_to_int('111-111-1111'),
        string_to_int('2'): string_to_int('222-222-2222'),
        string_to_int('3'): string_to_int('333-333-3333'),
        string_to_int('4'): string_to_int('444-444-4444'),
        string_to_int('5'): string_to_int('555-555-5555')
        }

    honey_entries = {
        string_to_int('6'): string_to_int('111-666-6666'),
        string_to_int('7'): string_to_int('222-777-7777')
        }

    X = make_X(bg, honey_entries)
    print('X', X)
    print('')

    exp_pro_Y = "('1', '111-111-1111'), ('2', '222-222-2222'), ('3', '333-333-3333'), ('4', '444-444-4444'), ('5', '555-555-5555'), ('6', '111-666-6666'), ('7', '222-777-7777')"
    print('exp_pro_Y', exp_pro_Y)
    print('')

    pro_Y = list_to_string(producer_func(X))
    print("pro_Y", pro_Y)
    print('')
    assert(exp_pro_Y == pro_Y)
    
    exp_repro_Y = "('1', '111-111-1111'), ('6', '111-666-6666'), ('2', '222-222-2222'), ('7', '222-777-7777'), ('3', '333-333-3333'), ('4', '444-444-4444'), ('5', '555-555-5555')"
    print('exp_repro_Y', exp_repro_Y)
    print('')
    honey_entries = [(string_to_int('6'), string_to_int('111-666-6666')), 
                     (string_to_int('7'), string_to_int('222-777-7777'))]
    repro_Y = list_to_string(reproducer_func(bg, honey_entries))
    print("repro_y", repro_Y)
    print('')
    assert(exp_repro_Y == repro_Y)

if __name__ == "__main__":
    main()