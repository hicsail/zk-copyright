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
    print(res_list)
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


def step(prog: Program, pc: int, mem: list, weight: int):
    
    instr = fetch(prog, pc)
    p1 = instr.src1
    p2 = instr.src2
    p3 = instr.src3
    p4 = instr.src4
    p5 = instr.src5
    p6 = instr.src6
    des = instr.dest
    s_des = instr.s_dest
    imm =  instr.imm
    new_pc = pc


    # 1. set p4 at mem[des]
    '''
        p4: const to set

        ops: mem[des] = p4
            #This does not support list to list assignment or string/char to string/char
    '''

    mem[des] = mux(instr.opcode == 1, p4, mem[des])
        

    # 2. add const/mem[val] to des
    '''
        p4: value to increment by

        ops: mem[des] += p4
    '''

    mem[des] =  mux(instr.opcode == 2, mem[des] + p4, mem[des])

    # 3. compare value in one index with const
    '''
        p3 mem address to compare (imm==1)
        p4: comparison type
        p5: const to compare (imm==0) 
        p6: element to compare

        ops: 
            # Below is for int
            if imm == 0:
                comp = p5
            elif imm == 1:
                comp = mem[p3]

            # Below is for str
            if p4 ==0:
                mem[des] = (mem[p6] == comp)
            elif p4 ==2:
                mem[des] = (mem[p6] < comp)
    '''
        
    comp = mux(instr.opcode == 3, mux(imm == 0, p5, mux(imm == 1, mem[p3], 500000)), 500000)
    
    mem[des] = mux(instr.opcode == 3,
                   mux(p4 == 0, mux(mem[p6] == comp, 1, 0),
                            mux(p4 == 2, mux(mem[p6] < comp, 1, 0),
                                    mem[des])), mem[des])
                                    


    # 4/100. jump or cond-jump/terminal
    '''
        p3: where condition is saved (im==1)
        p4: pc shift always (imm==0)/if True(imm==1)
        p5: pc shift if False

        ops: 
            if imm == 0:
                return new_pc + p4, weight +1
            elif mem[p3]==True:
                return new_pc + p4, weight +1
            elif imm == 1:
                return new_pc + p5, weight +1
    '''
    new_pc = mux(instr.opcode == 100, new_pc,
                mux(instr.opcode == 4,
                    mux(imm == 0, p4,
                        mux(mem[p3]==True, p4, p5)),
                new_pc+1))


    # 5. Copy val to register
    '''
        p1: address of index of memory

        ops: mem[des] = mem[mem[p2]]
    '''

    mem[des] = mux(instr.opcode == 5, mem[p2], mem[des])


    # 6. Access list by pointer saved in register
    '''
        p1: address of index of memory

        ops: mem[des] = mem[mem[p2]]
    '''

    mem[des] = mux(instr.opcode == 6, mem[mem[p2]], mem[des])


    # 7. Set Value by const pointer

    '''
        p4: any memory address
                
    '''

    mem[mem[s_des]] = mux(instr.opcode == 7, mem[p4], mem[mem[s_des]])


    # 100. Terminal
    w = mux(instr.opcode == 100, 0, 1)

    return new_pc, weight + w


def sort_by(mem, sort_by):
    # Sort the List of Tuples
    n = len(mem)
    i = 0
    while i < n:
        j = sort_by
        while j < n-i-2:
            # Compare the first element of each tuple
            if sort_by==0:
                if mem[j] > mem[j+2]:
                    temp1 = mem[j]
                    temp2 = mem[j+1]
                    mem[j] = mem[j+2]
                    mem[j+1] = mem[j+3]
                    mem[j+2] = temp1
                    mem[j+2] = temp2
            j += 2
        i += 2
    return mem


def producer_func(X_list):
    return sort_by(X_list[0:14], 0)


def reproducer_func(bg_list, honey_entries):
    bg_list += honey_entries
    return sort_by(bg_list, 1)


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
    exp_repro_Y = "('1', '111-111-1111'), ('6', '111-666-6666'), ('2', '222-222-2222'), ('7', '222-777-7777'), ('3', '333-333-3333'), ('4', '444-444-4444'), ('5', '555-555-5555')"
    print('exp_repro_Y', exp_repro_Y)
    print('')

    # with PicoZKCompiler('irs/picozk_test', options=['ram']):

    bot = [0]
    # Producer
    X_list = [i for k, v in X.items() for i in (k, v)]
    bots_list = [0] *4
    mem = X_list + bot + bots_list
    pro_Y = list_to_string(producer_func(mem))
    print("pro_Y", pro_Y)
    print('')
    assert(exp_pro_Y == pro_Y)

    
    # Reproducer
    bg_list = [i for k, v in bg.items() for i in (k, v)]
    print(bg_list)
    honey_entries = [string_to_int('6'), string_to_int('111-666-6666'), 
                    string_to_int('7'), string_to_int('222-777-7777')]

    repro_Y = list_to_string(reproducer_func(bg_list, honey_entries))
    print("repro_y", repro_Y)
    print('')
    assert(exp_repro_Y == repro_Y)

if __name__ == "__main__":
    main()