from dataclasses import dataclass
from typing import List
from picozk import *

# Class to hold a single instruction
@dataclass
class Instr:
    def __init__(self, opcode: int, src1: int, src2: int, src3: int, src4: int, src5: int, 
                 src9: int, src10: int, 
                 dest: int, s_dest: int,
                 imm: int):
        self.opcode = opcode
        self.src1 = src1
        self.src2 = src2
        self.src3 = src3
        self.src4 = src4
        self.src5 = src5
        self.src9 = src9
        self.src10 = src10
        self.dest = dest
        self.s_dest = s_dest
        self.imm = imm


# Class to hold a program as multiple lists of instructions
@dataclass
class Program:
    def __init__(self, opcode: List[int], src1: List[int], src2: List[int], src3: List[int], src4: List[int], src5: List[int], 
                 src9: List[int], src10: List[int], 
                 dest: List[int], s_dest: List[int], imm: List[int]):
        self.opcode: List[int] = opcode
        self.src1: List[int] = src1
        self.src2: List[int] = src2
        self.src3: List[int] = src3
        self.src4: List[int] = src4
        self.src5: List[int] = src5
        self.src9: List[int] = src9
        self.src10: List[int] = src10
        self.dest: List[int] = dest
        self.s_dest: List[int] = s_dest
        self.imm: List[int] = imm




def make_program(prog): #TODO: ZKListify
    length = len(prog)
    opcode = [0 for _ in range(length)]
    src1 = [0 for _ in range(length)]
    src2 = [0 for _ in range(length)]
    src3 = [0 for _ in range(length)]
    src4 = [0 for _ in range(length)]
    src5 = [0 for _ in range(length)]
    src9 = [0 for _ in range(length)]
    src10 = [0 for _ in range(length)]
    dest = [0 for _ in range(length)]
    s_dest = [0 for _ in range(length)]
    imm = [0 for _ in range(length)]

    for i, instr in enumerate(prog):
        opcode[i] = instr.opcode
        src1[i] = instr.src1
        src2[i] = instr.src2
        src3[i] = instr.src3
        src4[i] = instr.src4
        src5[i] = instr.src5
        src9[i] = instr.src9
        src10[i] = instr.src10
        dest[i] = instr.dest
        s_dest[i] = instr.s_dest
        imm[i] = instr.imm

    return Program(opcode, src1, src2, src3, src4, src5, 
                   src9, src10, 
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
                 prog.src9[pc],
                 prog.src10[pc],
                 prog.dest[pc],
                 prog.s_dest[pc],
                 prog.imm[pc])


def string_to_int(s):
    return int(''.join([f'{ord(char):03}' for char in s]))


def int_to_string(n):
    s = str(n)
    # Pad the string with leading zeros to ensure groups of 3 digits
    s = '0' * (3 - len(s) % 3) + s
    return ''.join([chr(int(s[i:i+3])) for i in range(0, len(s), 3)])


def reveal(list):
            res = ""
            for l in list:
                res += int_to_string(val_of(l)) + " "
            return res[:-1]
        

def make_X(madlibs, nouns):
    X = madlibs.split()
    i = 0

    for k in range(len(X)):
        if X[k] == '_':
            X[k] = nouns[i]
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
    p9 = instr.src9
    p10 = instr.src10
    des = instr.dest
    s_des = instr.s_dest
    imm =  instr.imm
    new_pc = pc


    # 1. Set a const/mem[val] to dest
    '''
        #This does not support list to list assignment or string/char to string/char
        des: depends
        p1: mem[val](imm==1)
        p4: const(imm==0)
    
        mem[des] = p4
    '''

    mem[des] = mux(instr.opcode == 1, p4, mem[des])
        

    # 2. add const/mem[val] to des
    '''
        des: target
        p1: increment by const(imm==0) or concat sec_string(imm==2)
        p1: concat sec_string(imm==4) indexed by ArithWire
        p4: increment by mem[val](imm==1)
        p5: char/strng(imm==3)
    
        mem[des] += p4
            
    '''

    mem[des] =  mux(instr.opcode == 2, mem[des] + p4, mem[des])

    # 3. compare value in one index with const
    '''
        des: target
        p10: element 1 to compare
        p3 mem[val](imm==1) to compare
        p4: operation (0: equal, 1:not equal, 2: p1 is smaller than p2, 3: p1 is greater than p2)
        p5: const(imm==0) 

        Below is for int
        if imm == 0:
            comp = p5
        elif imm == 1:
            comp = mem[p3]

        Below is for str
        if p4 ==0:
            mem[des] = (mem[p10] == comp)
        elif p4 ==2:
            mem[des] = (mem[p10] < comp)

    '''
        
    comp = mux(instr.opcode == 3, mux(imm == 0, p5, mux(imm == 1, mem[p3], 500000)), 500000)
    
    mem[des] = mux(instr.opcode == 3,
                   mux(p4 == 0, (mem[p10] == comp), 
                            mux(p4 == 2, (mem[p10] < comp),
                                    mem[des])), mem[des])
                                    


    # 4/-1. jump or cond-jump/terminal
    '''
        p3: condition(im==1)
        p4: pc shift always (imm==0)/if True(imm==1)
        p5: pc shift if False

        if imm == 0:
            return new_pc + p4, weight +1
        elif mem[p3]==True:
            return new_pc + p4, weight +1
        elif imm == 1:
            return new_pc + p5, weight +1
    '''
    step = mux(instr.opcode == -1, 0,
                mux(instr.opcode == 4,
                    mux(imm == 0 or mem[p3]==True, p4, p5), 
                1))


    # 5. length of 
    

    '''
        des: target index
        p1: list/string to measure length

        mem[des] = len(mem[p2])
    '''

    mem[des] = mux(instr.opcode == 5, len(mem[p2]), mem[des])
    

    # 7. Access nested list by constant/pointer
    '''
        des:target
        p1: index of list(imm==1)
        p2: constant/pointer (imm==0/1)
        p4: const index of list(imm==0/2)

        mem[des] = mem[p2][mem[p1]]
    '''

    mem[des] = mux(instr.opcode == 7, mem[p2][mem[p1]], mem[des])


    # 8. Set Value to list

    '''
        des:target memory address
        p9: index of target memory
        p3: any index
        
        if imm == 0:
            mem[s_des][p4] = mem[p3]
        elif imm == 1:
            mem[s_des][mem[p9]] = mem[p3]
        
    '''

    mem[s_des][mem[p9]] = mux(instr.opcode == 8, mem[p3], mem[s_des][mem[p9]])

    return new_pc + step, weight +1


def main():
    # The Mad Libs template
    madlibs = "I have a _ and _ , and every _ I walk _ to the _"

    # The list of potential fill-ins
    nouns = ['dog', 'cat', 'day', 'her', 'park', 'ball', 'cat', 'school', 'like', 'hour', 'tree', 'car', 'house', 'week', 'shoe', 'beach']
    
    X = make_X(madlibs, nouns)
    print('X: ', X)
    print('')

    X_words = [string_to_int(_str) for _str in X.split()]
    nouns_list = [string_to_int(_str) for _str in nouns]
    madlibs_words = [string_to_int(_str) for _str in madlibs.split()]

    n_iter = 1500
    fillup = 10

    under = string_to_int("_")
    
    with PicoZKCompiler('irs/picozk_test', options=['ram']):

        # Producer
        madlibs = madlibs #0 #TODO: Delete
        nouns_list = nouns_list #1
        X = X #2  #TODO: Delete
        madlibs_words = madlibs_words #3

        X_words = ZKList(X_words) #4
        assembled_list = ZKList([0] * 16) #5
        result = "" #6  #TODO: Delete
        X_nouns = ZKList([nouns_list[3], nouns_list[4]]) #7

        reg1 = 0 #8
        reg2 = 0 #9
        reg3 = 0 #10
        reg4 = 0 #11

        dummy_int = 0 #12
        dummy_list = ZKList([0] * 100) #13

        X_words_len = len(X_words)

        mem = [madlibs, nouns_list, X, 
                madlibs_words, X_words, assembled_list, result, X_nouns,
                reg1, reg2, reg3, reg4, dummy_int, dummy_list]
        
        program = [ 

            # Take the first three nouns from X and hard-code the rest from the fill list
            
                ## FIRST IF curr madlibs_words is equal to "_"
                    Instr(7, 9, 3, 12, 0, 0, 12, 12, 8, 13, 1),       ## Step1  #7: Assign idx9 (idx-i) of idx 3 (madlibs_words) to idx 8(reg1)
                    Instr(3, 12, 13, 12, 0, under, 12, 8, 8, 13, 0),     ## Step2  #3: Compare idx 8(reg1) and "_" and assign result to idx 8(reg1)
                    Instr(4, 12, 13, 8, 1, 8, 12, 12, 12, 13, 1),       ## Step3  #4: Cond jump to +1/+8 if true/false

                ## SECOND IF index of madlibs_words is less than fill_upto (upto idx of third fill)
                    Instr(3, 12, 13, 12, 2, fillup, 12, 9, 8, 13, 0),  ## Step4  #3: Compare idx 9(idx-i) < fill_upto (10 for now) and assign result to idx 8(reg1)
                    Instr(4, 12, 13, 8, 1, 3, 12, 12, 12, 13, 1),       ## Step5  #4: Cond jump to +1/+3 if true/false

                ## IF Both TRUE (Append from X_Words)
                    Instr(7, 9, 4, 12, 0, 0, 12, 12, 8, 13, 1),       ## Step6  #7: Assign idx 9 (idx-i) of idx 4 (X_words) to idx 8(reg1)
                    Instr(4, 12, 13, 12, 5, 0, 12, 12, 12, 13, 0),       ## Step7  #4: jump to +5

                ## IF only the former TRUE (Append from fill/consts)
                    Instr(7, 10, 7, 12, 0, 0, 12, 12, 8, 13, 1),      ## Step8  #7: Assign idx10 (idx-k) of idx 7 (fill) to idx 8(reg1)
                    Instr(2, 12, 13, 12, 1, 0, 12, 12, 10, 13, 0),      ## Step9  #2: add 1 to idx 10 (idx-k)
                    Instr(4, 12, 13, 12, 2, 0, 12, 12, 12, 13, 0),       ## Step10  #4: jump to +2

                ## ELSE (Append from madlibs_words)
                    Instr(7, 9, 3, 12, 0, 0, 12, 12, 8, 13, 1),       ## Step11  #7: Assign idx9 (idx-i) of idx 3 (madlibs_words) to idx 8(reg1)

                ## APPEND and INCREMENT
                    Instr(8, 12, 13, 8, 0, 0, 9, 12, 12, 5, 1),       ## Step12  #8: append idx8 (reg1) to idx5 (assembled_list)
                    Instr(2, 12, 13, 12, 1, 0, 12, 12, 9, 13, 0),       ## Step13  #2: add 1 to idx 9 (idx-i)
                    
                ## CHECK IF ITERATE OR NEXT
                    Instr(3, 12, 13, 12, 2, X_words_len, 12, 9, 8, 13, 0),       ## Step15  #3: Compare idx 9(idx-i) < idx 8(reg1) and assign result to idx 8(reg1)
                    Instr(4, 12, 13, 8, -14, 1, 12, 12, 12, 13, 1),     ## Step16  #4: Cond jump to -14/+1 if true/false

                    Instr(1, 12, 13, 12, 0, 0, 12, 12, 9, 13, 0),       ## Step17  #1: Set index9 (idx-i) to 0

            # END
                    Instr(-1, 12, 13, 12, 0, 0, 12, 12, 12, 13, 0),      ## Step18  #-1: Terminal
                    ]

        pro_prog = make_program(program)

        pc = 0
        weight = 0
        for i in range(n_iter):
            pc, weight = step(pro_prog, pc, mem, weight)
        
        prod_Y = reveal(mem[5]).replace('\x00', '') #TODO: FIXME

        print('prod_Y:', prod_Y)
        print('')

        res = mux("I have a dog and cat , and every day I walk her to the park" == prod_Y, 
                  mux(weight <= n_iter, SecretInt(0), SecretInt(1))
                  , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)


        # Reproducer
        madlibs = madlibs #0 #TODO: Delete
        nouns_list = nouns_list #1
        X = X #2  #TODO: Delete
        madlibs_words = madlibs_words #3
        
        X_words = None #4 Not available for reproducer
        assembled_list = ZKList([0] * 16) #5
        result = "" #6  #TODO: Delete
        X_nouns = ZKList([nouns_list[0], nouns_list[1], nouns_list[2], nouns_list[3], nouns_list[4]]) #7

        reg1 = 0 #8
        reg2 = 0 #9
        reg3 = 0 #10
        reg4 = 0 #11

        dummy_int = 0 #12
        dummy_list = ZKList([0] * 100) #13

        madlibs_len = len(madlibs_words)
        
        repro_mem = [madlibs, nouns_list, X, 
                madlibs_words, X_words, assembled_list, result, X_nouns,
                reg1, reg2, reg3, reg4, dummy_int, dummy_list]

        program = [

            # Hard-Code all blanks from the nouns list
                
                ## IF madlibs_words[curr] == "_"
                    Instr(7, 9, 3, 12, 0, 0, 12, 12, 8, 13, 1),       ## Step1  #7: Assign idx9 (idx-i) of idx 3 (madlibs_words) to idx 8(reg1)
                    Instr(3, 12, 13, 12, 0, under, 12, 8, 8, 13, 0),     ## Step2  #3: Compare idx 10(reg1) and "_" and assign result to idx 10(reg1)
                    Instr(4, 12, 13, 8, 1, 4, 12, 12, 12, 13, 1),       ## Step3  #4: Cond jump to +1/+4 if true/false

                    ## TRUE: Append from fill[idx-k] to assembled_list
                    Instr(7, 10, 7, 12, 0, 0, 12, 12, 8, 13, 1),      ## Step4  #7: Assign idx10 (idx-k) of idx 7 (fill) to idx 8(reg1)
                    Instr(2, 12, 13, 12, 1, 0, 12, 12, 10, 13, 0),      ## Step5  #2: add 1 to idx 10 (idx-k)
                    Instr(4, 12, 13, 12, 2, 0, 12, 12, 12, 13, 0),       ## Step6  #4: jump to +2

                    ## ELSE: Append from madlibs_words[idx-k] to assembled_list
                    Instr(7, 9, 3, 12, 0, 0, 12, 12, 8, 13, 1),       ## Step7  #7: Assign idx9 (idx-i) of idx 3 (madlibs_words) to idx 8(reg1)
                    
                ## Append ops based on above
                    Instr(8, 12, 13, 8, 0, 0, 9, 12, 12, 5, 1),       ## Step8  #14: append idx 8(reg1) to idx 5 (assembled_list)
                    Instr(2, 12, 13, 12, 1, 0, 12, 12, 9, 13, 0),       ## Step9  #2: add 1 to idx 9 (idx-i)

                ## Determine whether or not to iterate over again depending idx-i< len(madlibs_words)
                    Instr(3, 12, 13, 12, 2, madlibs_len, 12, 9, 8, 13, 0),  ## Step10  #3: Compare idx 9(idx-i) < idx 8(reg1) and assign result to idx 8(reg1)
                    Instr(4, 12, 13, 8, -10, 1, 12, 12, 12, 13, 1),     ## Step11  #4: Cond jump to -10/+1 if true/false

                    Instr(1, 12, 13, 12, 0, 0, 12, 12, 9, 13, 0),       ## Step12  #1: Set index i to 0
                    Instr(1, 12, 13, 12, 0, 0, 12, 12, 10, 13, 0),      ## Step13  #1: Set index k to 0

            # END
                    Instr(-1, 12, 13, 12, 0, 0, 12, 12, 12, 13, 0),      ## Step14  #-1: Terminal
                    ]
        repro_prog = make_program(program)

        pc = 0
        weight = 0

        for i in range(n_iter):
            pc, weight = step(repro_prog, pc, repro_mem, weight)

        reprod_Y = reveal(repro_mem[5]).replace('\x00', '') #TODO: FIXME
        print('reprod_Y: ', reprod_Y)
        print('')
        res = mux("I have a dog and cat , and every day I walk her to the park" == reprod_Y, 
                  mux(weight <= n_iter, SecretInt(0), SecretInt(1))
                  , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)

if __name__ == "__main__":
    main()