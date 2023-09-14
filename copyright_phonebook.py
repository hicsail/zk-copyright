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
    res_list_size = 14
    while idx < res_list_size:
        # Convert each tuple to a string and add to result_str
        item_str = "(" + "'" + int_to_string(val_of(res_list[idx])) + "'" + ", " + "'" + int_to_string(val_of(res_list[idx+1])) + "'" + ")"
        if result_str:
            result_str += ", " + item_str
        else:
            result_str = item_str
        idx += 2
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


def producer_func(mem):
    n = 14
    i = 0
    while i < n:
        j = 0
        while j < n-i-2:
            # Compare the first element of each tuple
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


def reproducer_func(repro_mem):
    mem = repro_mem[0:10] + repro_mem[11:]
        # Sort the List of Tuples
    n = 14
    i = 1
    while i < n:
        j = 1
        while j < n-i-1:
            if mem[j] > mem[j+2]:
                temp1 = mem[j]
                temp2 = mem[j-1]
                mem[j] = mem[j+2]
                mem[j-1] = mem[j+1]
                mem[j+2] = temp1
                mem[j+1] = temp2
            j += 2
        i += 2
    return mem


def main():

    bg = {
        string_to_int('2'): string_to_int('222-222-2222'),
        string_to_int('1'): string_to_int('111-111-1111'),
        string_to_int('3'): string_to_int('333-333-3333'),
        string_to_int('4'): string_to_int('444-444-4444'),
        string_to_int('5'): string_to_int('555-555-5555')
        }

    honey_entries = {
        string_to_int('6'): string_to_int('111-666-6666'),
        string_to_int('7'): string_to_int('222-777-7777')
        }

    X = make_X(bg, honey_entries)

    exp_pro_Y = "('1', '111-111-1111'), ('2', '222-222-2222'), ('3', '333-333-3333'), ('4', '444-444-4444'), ('5', '555-555-5555'), ('6', '111-666-6666'), ('7', '222-777-7777')"
    exp_repro_Y = "('1', '111-111-1111'), ('6', '111-666-6666'), ('2', '222-222-2222'), ('7', '222-777-7777'), ('3', '333-333-3333'), ('4', '444-444-4444'), ('5', '555-555-5555')"
    print('exp_pro_Y', exp_pro_Y, '\n')
    print('exp_repro_Y', exp_repro_Y, '\n')

    p = pow(2,256) - pow(2,32) - pow(2,9) - pow(2,8) - pow(2,7) - pow(2,6) - pow(2,4) - 1
    n_iter = 1500
    lim = 10
    threshold = 300 # The program has to be performed within this (weight < )

    with PicoZKCompiler('irs/picozk_test', field=[p], options=['ram']):

        # Producer
        X_list = [i for k, v in X.items() for i in (k, v)] #0-13
        bots_list = [0] *4 #15-18
        reg1 = 0 #20
        reg2 = 0 #22
        reg3 = 0 #24
        reg4 = 0 #26
        dummy_int = 0 #28

        bot = 0
        
        mem = ZKList(X_list + [bot] + bots_list + [bot] + [reg1] + [bot] + [reg2] + [bot] + [reg3] + [bot] + [reg4] + [bot] + [dummy_int])
        
        program = [

                # Take the first three nouns from X and hard-code the rest from the fill list
                
                    # ## FIRST IF curr madlibs_words is equal to "_"
                    #     Instr(5, 76, 68, 76, 76, 76, 76, 72, 76, 0),    ## Step0   #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    #     Instr(2, 76, 76, 76, 17, 76, 76, 72, 76, 0),    ## Step1   #2: Add 17 to idx72 (temp-idx/reg3) = Shifting pointer idx-i to madlibs list by 17
                    #     Instr(6, 76, 72, 76, 76, 76, 76, 70, 76, 0),    ## Step2   #6: Set idx72 (temp-idx/reg3) of madlibs list to idx70 (reg2)
                    #     Instr(3, 76, 76, 76,  0, us, 70, 70, 76, 0),    ## Step3   #3: Compare idx70 (reg2) and "_" and assign result to idx70 (reg2)
                    #     Instr(4, 76, 76, 70,  5, 16, 76, 76, 76, 1),    ## Step4   #4: Cond jump to Step5/Step16 if true/false

                    # ## SECOND IF index of madlibs_words is less than lim (upto idx of third)
                    #     Instr(3, 76, 76, 76,  2,lim, 68, 70, 76, 0),    ## Step5   #3: Compare idx 68(idx-i/reg1) < fill_upto (10 for now) and set the result to idx70 (reg2)
                    #     Instr(4, 76, 76, 70,  7, 11, 76, 76, 76, 1),    ## Step6   #4: Cond jump to Step7/Step11 if true/false

                    # ## IF Both TRUE (Append from X list)
                    #     Instr(5, 76, 68, 76, 76, 76, 76, 72, 76, 0),    ## Step7   #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    #     Instr(2, 76, 76, 76, 34, 76, 76, 72, 76, 0),    ## Step8   #2: Add 34 to idx72 (temp-idx/reg3) = Shifting pointer to X_list idx-i by 34
                    #     Instr(6, 76, 72, 76, 76, 76, 76, 70, 76, 0),    ## Step9   #6: Set idx72 (temp-idx/reg3) of X_words to idx70 (reg2)
                    #     Instr(4, 76, 76, 76, 19, 76, 76, 76, 76, 0),    ## Step10  #4: jump to Step19

                    # ## IF only the former TRUE (Append from nouns list)
                    #     Instr(5, 76, 74, 76, 76, 76, 76, 72, 76, 0),    ## Step11  #5: Copy idx74 (idx-k/reg2) to idx72 (temp-idx/reg3)
                    #     Instr(2, 76, 76, 76,  3, 76, 76, 72, 76, 0),    ## Step12  #2: Add 3 to idx72 (temp-idx/reg3) = Shifting pointer idx-k to nouns list by 3
                    #     Instr(6, 76, 72, 76, 76, 76, 76, 70, 76, 1),    ## Step13  #6: Set idx72 (temp-idx/reg3) of nouns list to idx70 (reg2)
                    #     Instr(2, 76, 76, 76,  1, 76, 76, 74, 76, 0),    ## Step14  #2: Add 1 to idx74 (idx-k/reg3)
                    #     Instr(4, 76, 76, 76, 19, 76, 76, 76, 76, 0),    ## Step15  #4: jump to Step19

                    # ## ELSE (Append from madlibs list)
                    #     Instr(5, 76, 68, 76, 76, 76, 76, 72, 76, 0),    ## Step16  #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    #     Instr(2, 76, 76, 76, 17, 76, 76, 72, 76, 0),    ## Step17  #2: Add 17 to idx72 (temp-idx/reg3) = Shifting pointer idx-i to madlibs list by 17
                    #     Instr(6, 76, 72, 76, 76, 76, 76, 70, 76, 0),    ## Step18  #6: Set idx72 (temp-idx/reg3) of madlibs list to idx70 (reg2)

                    # ## APPEND and INCREMENT
                    #     Instr(5, 76, 68, 76, 76, 76, 76, 72, 76, 0),    ## Step19  #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    #     Instr(2, 76, 76, 76, 51, 76, 76, 72, 76, 0),    ## Step20  #2: Add 51 to idx72 (temp-idx/reg3) = Shifting pointer idx-i to res list by 51
                    #     Instr(7, 76, 76, 76, 70, 76, 76, 76, 72, 1),    ## Step21  #6: Set idx70 (reg2) to idx72 (temp-idx/reg3) of res list
                    #     Instr(2, 76, 76, 76,  1, 76, 76, 68, 76, 0),    ## Step22  #2: Add 1 to idx 68 (idx-i)
                        
                    # ## CHECK IF ITERATE OR NEXT
                    #     Instr(3, 76, 76, 76, 2, X_len, 68, 72, 76, 0),  ## Step23  #3: Compare idx68 (idx-i) < p5 (X_len) and assign result to idx72 (reg3)
                    #     Instr(4, 76, 76, 72, 0, 25, 76, 76, 76, 1),     ## Step24  #4: Cond jump to Step0/25 if true/false

                # END
                        Instr(100, 28, 28, 28, 28, 28, 28, 28, 28, 0),   ## Step25  #-1: Terminal
        ]
        pro_prog = make_program(program)

        pc = 0
        weight = 0
        for i in range(n_iter):
            pc, weight = step(pro_prog, pc, mem, weight)

        prod_Y = list_to_string(mem)
        print('prod_Y:', prod_Y, '\n')

        res = mux(exp_pro_Y == prod_Y,
                    mux(weight <= threshold, SecretInt(0), SecretInt(1))
                    , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)


        # Reproducer
        bg_list = [i for k, v in bg.items() for i in (k, v)]
        honey_entries = [string_to_int('6'), string_to_int('111-666-6666'), 
                        string_to_int('7'), string_to_int('222-777-7777')]
        
        bot = 0
        repro_mem = bg_list + [bot] + honey_entries


        repro_Y = list_to_string(reproducer_func(repro_mem)[0:14])
        print("repro_y", repro_Y, '\n')
        assert(exp_repro_Y == repro_Y)

if __name__ == "__main__":
    main()