from dataclasses import dataclass
from typing import List
from picozk import *

# Class to hold a single instruction
@dataclass
class Instr:
    def __init__(self, opcode: int, src1: int, src2: int, src3: int, src4: int, src5: int, 
                 src6: int, src7: int, 
                 dest: int, s_dest: int,
                 imm: int):
        self.opcode = opcode
        self.src1 = src1
        self.src2 = src2
        self.src3 = src3
        self.src4 = src4
        self.src5 = src5
        self.src6 = src6
        self.src7 = src7
        self.dest = dest
        self.s_dest = s_dest
        self.imm = imm


# Class to hold a program as multiple lists of instructions
@dataclass
class Program:
    def __init__(self, opcode: ZKList, src1: ZKList, src2: ZKList, src3: ZKList, src4: ZKList, src5: ZKList, 
             src6: ZKList, src7: ZKList,
             dest: ZKList, s_dest: ZKList, imm: ZKList):
        
        self.opcode: ZKList = opcode
        self.src1: ZKList = src1
        self.src2: ZKList = src2
        self.src3: ZKList = src3
        self.src4: ZKList = src4
        self.src5: ZKList = src5
        self.src6: ZKList = src6
        self.src7: ZKList = src7
        self.dest: ZKList = dest
        self.s_dest: ZKList = s_dest
        self.imm: ZKList = imm




def make_program(prog): #TODO: ZKListify
    length = len(prog)
    opcode = ZKList([0 for _ in range(length)])
    src1 = ZKList([0 for _ in range(length)])
    src2 = ZKList([0 for _ in range(length)])
    src3 = ZKList([0 for _ in range(length)])
    src4 = ZKList([0 for _ in range(length)])
    src5 = ZKList([0 for _ in range(length)])
    src6 = ZKList([0 for _ in range(length)])
    src7 = ZKList([0 for _ in range(length)])
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
        src7[i] = instr.src7
        dest[i] = instr.dest
        s_dest[i] = instr.s_dest
        imm[i] = instr.imm

    return Program(opcode, src1, src2, src3, src4, src5, 
                   src6, src7, 
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
                 prog.src7[pc],
                 prog.dest[pc],
                 prog.s_dest[pc],
                 prog.imm[pc])


def string_to_int(s):
    return int(''.join(format(ord(char), '08b') for char in s), 2)


def int_to_string(n):
    binary_str = format(n, 'b')
    # Pad the binary string with leading zeros to ensure groups of 8 bits
    binary_str = '0' * ((8 - len(binary_str) % 8) % 8) + binary_str
    return ''.join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8))


def reveal(list, st, end):
            res = ""
            for i in range(st, end):
                res += int_to_string(val_of(list[i])) + " "
            return res[:-1].replace('\x00', '') #TODO: FIXME
        

def make_X(madlibs, nouns):
    X = madlibs.split()
    i = 0
    idx = [0,1,2,5,6]

    for k in range(len(X)):
        if X[k] == '_':
            X[k] = nouns[idx[i]]
            i+=1

    X = ' '.join(X) # This is the madlibs text with all blanks are filled

    return X


def reveal_string(input):
    res = ""
    for elm in input:
        elm = int_to_string(val_of(elm)).rstrip('\x00')
        res += elm + " "
    return res[:-1]
        

def step(prog: Program, pc: int, mem: list, weight: int):
    
    instr = fetch(prog, pc)
    p1 = instr.src1
    p2 = instr.src2
    p3 = instr.src3
    p4 = instr.src4
    p5 = instr.src5
    p6 = instr.src6
    p7 = instr.src7
    des = instr.dest
    s_des = instr.s_dest
    imm =  instr.imm
    new_pc = pc

        
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
        p7: element to compare

        ops: 
            # Below is for int
            if imm == 0:
                comp = p5
            elif imm == 1:
                comp = mem[p3]

            # Below is for str
            if p4 ==0:
                mem[des] = (mem[p7] == comp)
            elif p4 ==2:
                mem[des] = (mem[p7] < comp)
    '''
        
    comp = mux(instr.opcode == 3, mux(imm == 0, p5, mux(imm == 1, mem[p3], 500000)), 500000)
    
    mem[des] = mux(instr.opcode == 3,
                   mux(p4 == 0, mux(mem[p7] == comp, 1, 0),
                            mux(p4 == 2, mux(mem[p7] < comp, 1, 0),
                                    mem[des])), mem[des])
                                    


    # 4/-1. jump or cond-jump/terminal
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
    step = mux(instr.opcode == -1, 0,
                mux(instr.opcode == 4,
                    mux(imm == 0, p4, 
                        mux(mem[p3]==True, p4, p5)), 
                1))


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
        p1: any memory address
                
    '''

    mem[mem[s_des]] = mux(instr.opcode == 7, mem[p1], mem[mem[s_des]])

    return new_pc + step, weight +1


def main():

    madlibs = "I have a _ and _ , and every _ I walk _ to the _"
    nouns = ['dog', 'cat', 'day', 'her', 'park', 'them', 'beach', 'school', 'like', 'hour', 'tree', 'car', 'house', 'week', 'shoe', 'beach']
    exp_Y = "I have a dog and cat , and every day I walk her to the park"
    print('Y: ', exp_Y) #TODO: Change to differ from X
    print('')
    X = make_X(madlibs, nouns)
    print('X: ', X)
    print('')

    X_list = [string_to_int(_str) for _str in X.split()]
    nouns_list = [string_to_int(_str) for _str in nouns]
    madlibs_list = [string_to_int(_str) for _str in madlibs.split()]

    n_iter = 1500
    lim = 10

    us = string_to_int("_")
    
    with PicoZKCompiler('irs/picozk_test', options=['ram']):

        # Producer
        nouns_list = nouns_list #0-15
        madlibs_list = madlibs_list #17 - 32
        X_list = X_list #34 - 49
        res_list = [0] * 16 #51 - 66

        reg1 = 0 #68
        reg2 = 0 #70
        reg3 = 0 #72
        reg4 = 0 #74
        dummy_int = 0 #76
        
        bot = 0

        mem = ZKList(nouns_list + [bot] + madlibs_list + [bot] + X_list + [bot] + res_list + [bot] + [reg1] + [bot] + [reg2] + [bot] + [reg3] + [bot] + [reg4] + [bot] + [dummy_int])

        X_len = len(X_list)

        program = [

            # Take the first three nouns from X and hard-code the rest from the fill list
            
                ## FIRST IF curr madlibs_words is equal to "_"
                    Instr(5, 76, 68, 76, 76, 76, 76, 76, 72, 76, 0),    ## Step0   #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76, 17, 76, 76, 76, 72, 76, 0),    ## Step1   #2: Add 17 to idx72 (temp-idx/reg3) = Shifting pointer idx-i to madlibs list by 17
                    Instr(6, 76, 72, 76, 76, 76, 76, 76, 70, 76, 0),    ## Step2   #6: Set idx72 (temp-idx/reg3) of madlibs list to idx70 (reg2)
                    Instr(3, 76, 76, 76,  0, us, 76, 70, 70, 76, 0),    ## Step3   #3: Compare idx70 (reg2) and "_" and assign result to idx70 (reg2)
                    Instr(4, 76, 76, 70,  1, 12, 76, 76, 76, 76, 1),    ## Step4   #4: Cond jump to +1/+12 if true/false

                ## SECOND IF index of madlibs_words is less than lim (upto idx of third)
                    Instr(3, 76, 76, 76,  2,lim, 76, 68, 70, 76, 0),    ## Step5   #3: Compare idx 68(idx-i/reg1) < fill_upto (10 for now) and set the result to idx70 (reg2)
                    Instr(4, 76, 76, 70,  1,  5, 76, 76, 76, 76, 1),    ## Step6   #4: Cond jump to +1/+5 if true/false

                ## IF Both TRUE (Append from X list)
                    Instr(5, 76, 68, 76, 76, 76, 76, 76, 72, 76, 0),    ## Step7   #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76, 34, 76, 76, 76, 72, 76, 0),    ## Step8   #2: Add 34 to idx72 (temp-idx/reg3) = Shifting pointer to X_list idx-i by 34
                    Instr(6, 76, 72, 76, 76, 76, 76, 76, 70, 76, 0),    ## Step9   #6: Set idx72 (temp-idx/reg3) of X_words to idx70 (reg2)
                    Instr(4, 76, 76, 76,  9, 76, 76, 76, 76, 76, 0),    ## Step10  #4: jump to +9

                ## IF only the former TRUE (Append from nouns list)
                    Instr(5, 76, 74, 76, 76, 76, 76, 76, 72, 76, 0),    ## Step11  #5: Copy idx74 (idx-k/reg2) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76,  3, 76, 76, 76, 72, 76, 0),    ## Step12  #2: Add 3 to idx72 (temp-idx/reg3) = Shifting pointer idx-k to nouns list by 3  #TODO: Change to match Y
                    Instr(6, 76, 72, 76, 76, 76, 76, 76, 70, 76, 1),    ## Step13  #6: Set idx72 (temp-idx/reg3) of nouns list to idx70 (reg2)
                    Instr(2, 76, 76, 76,  1, 76, 76, 76, 74, 76, 0),    ## Step14  #2: Add 1 to idx74 (idx-k/reg3)
                    Instr(4, 76, 76, 76,  4, 76, 76, 76, 76, 76, 0),    ## Step15  #4: jump to +4

                ## ELSE (Append from madlibs list)
                    Instr(5, 76, 68, 76, 76, 76, 76, 76, 72, 76, 0),    ## Step16  #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76, 17, 76, 76, 76, 72, 76, 0),    ## Step17  #2: Add 17 to idx72 (temp-idx/reg3) = Shifting pointer idx-i to madlibs list by 17
                    Instr(6, 76, 72, 76, 76, 76, 76, 76, 70, 76, 0),    ## Step18  #6: Set idx72 (temp-idx/reg3) of madlibs list to idx70 (reg2)

                ## APPEND and INCREMENT
                    Instr(5, 76, 68, 76, 76, 76, 76, 76, 72, 76, 0),    ## Step19  #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76, 51, 76, 76, 76, 72, 76, 0),    ## Step20  #2: Add 51 to idx72 (temp-idx/reg3) = Shifting pointer idx-i to res list by 51
                    Instr(7, 70, 76, 76, 76, 76, 76, 76, 76, 72, 1),    ## Step21  #6: Set idx70 (reg2) to idx72 (temp-idx/reg3) of res list
                    Instr(2, 76, 76, 76,  1, 76, 76, 76, 68, 76, 0),    ## Step22  #2: Add 1 to idx 68 (idx-i)
                    
                ## CHECK IF ITERATE OR NEXT
                    Instr(3, 76, 76, 76, 2, X_len, 76, 68, 72, 76, 0),  ## Step23  #3: Compare idx68 (idx-i) < p5 (X_len) and assign result to idx72 (reg3)
                    Instr(4, 76, 76, 72, -24, 1, 76, 76, 76, 76, 1),    ## Step24  #4: Cond jump to -24/+1 if true/false

            # END
                    Instr(-1, 76, 76, 76, 76, 76, 76, 76, 76, 76, 0),   ## Step25  #-1: Terminal
                    ]
        pro_prog = make_program(program)

        pc = 0
        weight = 0
        for i in range(n_iter):
            pc, weight = step(pro_prog, pc, mem, weight)
        
        prod_Y = reveal(mem, 51, 67)

        print('prod_Y:', prod_Y)
        print('')

        res = mux(exp_Y == prod_Y,
                  mux(weight <= n_iter, SecretInt(0), SecretInt(1))
                  , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)


        # Reproducer
        nouns_list = nouns_list #0-15
        madlibs_list = madlibs_list #17 - 32
        bots_list = [0] * 16 #34 - 49
        res_list = [0] * 16 #51 - 66

        reg1 = 0 #68
        reg2 = 0 #70
        reg3 = 0 #72
        reg4 = 0 #74
        dummy_int = 0 #76
        
        bot = 0

        repro_mem = ZKList(nouns_list + [bot] + madlibs_list + [bot] + bots_list + [bot] + res_list + [bot] + [reg1] + [bot] + [reg2] + [bot] + [reg3] + [bot] + [reg4] + [bot] + [dummy_int])


        lim = len(madlibs_list)

        program = [

            # Hard-Code all blanks from the nouns list
                
                ## IF madlibs_words[curr] == "_"
                    Instr(5, 76, 68, 76, 76, 76, 76, 76, 72, 76, 0),    ## Step0   #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76, 17, 76, 76, 76, 72, 76, 0),    ## Step1   #2: Add 17 to idx72 (temp-idx/reg3) = Shifting pointer idx-i to madlibs list by 17
                    Instr(6, 76, 72, 76, 76, 76, 76, 76, 70, 76, 0),    ## Step2   #6: Set idx72 (temp-idx/reg3) of madlibs list to idx70 (reg2)
                    Instr(3, 76, 76, 76,  0, us, 76, 70, 70, 76, 0),    ## Step3   #3: Compare idx70 (reg2) and "_" and assign result to idx70 (reg2)
                    Instr(4, 76, 76, 70,  1, 4, 76, 76, 76, 76, 1),     ## Step4   #4: Cond jump to +1/+4 if true/false

                    ## TRUE: Append from nouns_list[idx-k] to res_list
                    Instr(6, 76, 74, 76, 76, 76, 76, 76, 70, 76, 0),    ## Step5   #6: Set idx74 (idx-k/reg4) of nouns list to idx70 (reg2)
                    Instr(2, 76, 76, 76,  1, 76, 76, 76, 74, 76, 0),    ## Step6   #2: add 1 to idx74 (idx-k)
                    Instr(4, 76, 76, 76,  4, 76, 76, 76, 76, 76, 0),    ## Step7   #4: jump to +2

                    ## ELSE: Append from madlibs_list[idx-k] to res_list
                    Instr(5, 76, 68, 76, 76, 76, 76, 76, 72, 76, 0),    ## Step8   #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76, 17, 76, 76, 76, 72, 76, 0),    ## Step9   #2: Add 17 to idx72 (temp-idx/reg3) = Shifting pointer idx-i to madlibs list by 17
                    Instr(6, 76, 72, 76, 76, 76, 76, 76, 70, 76, 0),    ## Step10  #6: Set idx72 (temp-idx/reg3) of madlibs list to idx70 (reg2)
                    
                ## APPEND and INCREMENT
                    Instr(5, 76, 68, 76, 76, 76, 76, 76, 72, 76, 0),    ## Step11  #5: Copy idx68 (idx-i/reg1) to idx72 (temp-idx/reg3)
                    Instr(2, 76, 76, 76, 51, 76, 76, 76, 72, 76, 0),    ## Step12  #2: Add 51 to idx72 (temp-idx/reg3) = Shifting pointer idx-i to res list by 51
                    Instr(7, 70, 76, 76, 76, 76, 76, 76, 76, 72, 1),    ## Step13  #6: Set idx70 (reg2) to idx72 (temp-idx/reg3) of res list
                    Instr(2, 76, 76, 76,  1, 76, 76, 76, 68, 76, 0),    ## Step14  #2: Add 1 to idx 68 (idx-i)

                ## Determine whether or not to iterate over again depending idx-i< len(madlibs_words)
                    Instr(3, 76, 76, 76, 2, lim, 76, 68, 72, 76, 0),    ## Step15  #3: Compare idx68 (idx-i) < p5 (X_len) and assign result to idx72 (reg3)
                    Instr(4, 76, 76, 72, -16, 1, 76, 76, 76, 76, 1),    ## Step16  #4: Cond jump to -16/+1 if true/false

            # END
                    Instr(-1, 76, 76, 76, 76, 76, 76, 76, 76, 76, 0),   ## Step17  #-1: Terminal
                    ]
        repro_prog = make_program(program)

        pc = 0
        weight = 0

        for i in range(n_iter):
            pc, weight = step(repro_prog, pc, repro_mem, weight)

        reprod_Y = reveal(repro_mem, 51, 67)
        print('reprod_Y: ', reprod_Y)
        print('')
        res = mux("I have a dog and cat , and every day I walk her to the park" == reprod_Y, 
                  mux(weight <= n_iter, SecretInt(0), SecretInt(1))
                  , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)

if __name__ == "__main__":
    main()