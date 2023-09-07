from dataclasses import dataclass
from typing import List
from picozk import *

# Class to hold a single instruction
@dataclass
class Instr:
    def __init__(self, opcode: int, src1: int, src2: int, src3: int, src4: int, src5: int, src6: int, src7: int, src8: int, 
                 dest: int, s_dest: int, t_dest: int, 
                 imm: int):
        self.opcode = opcode
        self.src1 = src1
        self.src2 = src2
        self.src3 = src3
        self.src4 = src4
        self.src5 = src5
        self.src6 = src6
        self.src7 = src7
        self.src8 = src8
        self.dest = dest
        self.s_dest = s_dest
        self.t_dest = t_dest
        self.imm = imm


# Class to hold a program as multiple lists of instructions
@dataclass
class Program:
    def __init__(self, opcode: List[int], src1: List[int], src2: List[int], src3: List[int], src4: List[int], src5: List[int], src6: List[int],  src7: List[int],  src8: List[int], 
                 dest: List[int], s_dest: List[int], t_dest: List[int], imm: List[int]):
        self.opcode: List[int] = opcode
        self.src1: List[int] = src1
        self.src2: List[int] = src2
        self.src3: List[int] = src3
        self.src4: List[int] = src4
        self.src5: List[int] = src5
        self.src6: List[int] = src6
        self.src7: List[int] = src7
        self.src8: List[int] = src8
        self.dest: List[int] = dest
        self.s_dest: List[int] = s_dest
        self.t_dest: List[int] = t_dest
        self.imm: List[int] = imm


def string_to_int(s):
    return int(''.join([f'{ord(char):03}' for char in s]))


def int_to_string(n):
    s = str(n)
    # Pad the string with leading zeros to ensure groups of 3 digits
    s = '0' * (3 - len(s) % 3) + s
    return ''.join([chr(int(s[i:i+3])) for i in range(0, len(s), 3)])



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
    p6 = instr.src6
    p7 = instr.src7
    p8 = instr.src8
    des = instr.dest
    s_des = instr.s_dest
    t_des = instr.t_dest
    imm =  instr.imm
    new_pc = pc

    print("step", pc+1, "ops:", instr.opcode, "-", imm, "mem[des]", mem[p1], type(mem[p1]))

    assert(type(mem[p1])==bool or type(mem[p1])==int or type(mem[p1])==ArithmeticWire)
    assert(type(mem[p2])==list or type(mem[p2])==ZKList or type(mem[p2])==str)
    assert(type(mem[p3])!=list or type(mem[p3])!=ZKList)
    assert(type(p4)==bool or type(p4)==int)
    assert(type(p5)!=list or type(p5)!=ZKList, type(p5)==int)
    
    assert(type(mem[p6][mem[p7]:mem[p8]])==str)
    

    assert(type(mem[des])==bool or type(mem[des])==int or type(mem[des])==ArithmeticWire)
    assert(type(mem[t_des])==str)
    assert(type(mem[s_des])==ZKList or type(mem[s_des])==List)

    # 1. Set a const/mem[val] to dest
    if instr.opcode == 1:

        '''
            #This does not support list to list assignment or string/char to string/char
            des: depends
            p1: mem[val](imm==1)
            p4: const(imm==0)
        '''
        if imm == 0:
            mem[des] = p4
        elif imm ==1:
            mem[des] = mem[p1]
        
        return new_pc + 1, weight +1


    # 2. add const/mem[val] to des
    elif instr.opcode == 2:

        '''
            des: target
            p1: increment by const(imm==0) or concat sec_string(imm==2)
            p4: increment by mem[val](imm==1)
            p5: char/strng(imm==3)
        '''
        if imm == 0: # This is for arithmetic addition
            mem[des] += p4
        elif imm ==1:
            mem[des] += mem[p1]
        elif imm == 2:
            mem[t_des] += int_to_string(val_of(mem[p1]))
        elif imm == 3: # This is for char/string append
            mem[t_des] += " "

        return new_pc + 1, weight +1


    # 3. compare value in one index with const
    elif instr.opcode == 3:

        '''
            des: target
            p1: element 1 to compare
            p5: const(imm==0) 
            p3 mem[val](imm==1) to compare
            p4: operation (0: equal, 1:not equal, 2: p1 is smaller than p2, 3: p1 is greater than p2)
        '''
        
        if imm == 0:
            comp = p5
        elif imm == 1:
            comp = mem[p3]
        elif imm == 2:
            comp = " "

        if p4 ==0:
            mem[des] = (mem[p1] == comp)
        elif p4 ==1:
            mem[des] = (mem[p1] != comp)
        elif p4 ==2:
            mem[des] = (mem[p1] < comp)
        elif p4 ==3:
            mem[des] = (mem[p1] > comp)
        elif p4 ==4:
            mem[des] = (mem[p6] == comp)
        elif p4 ==5:
            mem[des] = (mem[p6] != comp)
        return new_pc + 1, weight +1

            
    # 4. jump or cond-jump
    elif instr.opcode == 4:

        '''
            p3: condition(im==1)
            p4: pc shift always (imm==0)/if True(imm==1)
            p5: pc shift if False
        '''

        if imm == 0:
            return new_pc + p4, weight +1
        elif mem[p3]==True:
            return new_pc + p4, weight +1
        else:
            return new_pc + p5, weight +1


    # 5. length of 
    elif instr.opcode == 5:

        '''
            des: target index
            p1: list/string to measure length
        '''
        mem[des] = len(mem[p2])
        
        return new_pc + 1, weight +1
    

    # 6. access more than one index in list
    elif instr.opcode == 6:

        '''
            des:target
            p7: beginning index of nested list of origin
            p6: index of string type in mem
            p8: end index of nested list of origin (imm==0)/otherwise automatically till end (imm==1)
        '''
        if imm == 0:
            mem[des] = string_to_int(mem[p6][mem[p7]:mem[p8]])
        elif imm == 1:
            mem[des] = string_to_int(mem[p6][mem[p7]:])

        return new_pc + 1, weight +1
        

    # 7. Access nested list by constant/pointer
    elif instr.opcode == 7:

        '''
            des:target
            p1: index of list(imm==1)
            p2: constant/pointer (imm==0/1)
            p4: const index of list(imm==0/2)
        '''
        if imm == 0:
            mem[des] = mem[p2][p4]
        elif imm == 1:
            mem[des] = mem[p2][mem[p1]]
        elif imm == 2:
            mem[t_des] = int_to_string(val_of(mem[p2][p4]))
        elif imm == 3:
            mem[t_des] = mem[p2][mem[p1]] #This is for stringa , used during X_words creation

        return new_pc + 1, weight +1


    # 8. Set Value to list
    if instr.opcode == 8:

        '''
            des:target memory address
            p1: index of target memory
            p3: any index
            
        '''
                
        if imm == 0:
            mem[s_des][p4] = mem[p3]
        elif imm == 1:
            mem[s_des][mem[p1]] = mem[p3]
   
        return new_pc + 1, weight +1
    
    # -1. terminal
    elif instr.opcode == -1:

        return new_pc, weight


def make_program(prog): #TODO: ZKListify
    length = len(prog)
    opcode = [0 for _ in range(length)]
    src1 = [0 for _ in range(length)]
    src2 = [0 for _ in range(length)]
    src3 = [0 for _ in range(length)]
    src4 = [0 for _ in range(length)]
    src5 = [0 for _ in range(length)]
    src6 = [0 for _ in range(length)]
    src7 = [0 for _ in range(length)]
    src8 = [0 for _ in range(length)]
    dest = [0 for _ in range(length)]
    s_dest = [0 for _ in range(length)]
    t_dest = [0 for _ in range(length)]
    imm = [0 for _ in range(length)]

    for i, instr in enumerate(prog):
        opcode[i] = instr.opcode
        src1[i] = instr.src1
        src2[i] = instr.src2
        src3[i] = instr.src3
        src4[i] = instr.src4
        src5[i] = instr.src5
        src6[i] = instr.src6
        src7[i] = instr.src7
        src8[i] = instr.src8
        dest[i] = instr.dest
        s_dest[i] = instr.s_dest
        t_dest[i] = instr.t_dest
        imm[i] = instr.imm

    return Program(opcode, src1, src2, src3, src4, src5, src6, src7, src8, 
                   dest, s_dest, t_dest, 
                   imm)


# Fetch an instruction from a program
def fetch(prog: Program, pc: int):
    return Instr(prog.opcode[pc],
                 prog.src1[pc],
                 prog.src2[pc],
                 prog.src3[pc],
                 prog.src4[pc],
                 prog.src5[pc],
                 prog.src6[pc],
                 prog.src7[pc],
                 prog.src8[pc],
                 prog.dest[pc],
                 prog.s_dest[pc],
                 prog.t_dest[pc],
                 prog.imm[pc])

def main():
    # The Mad Libs template
    madlibs = "I have a _ and _ , and every _ I walk _ to the _"
    madlibs_words = [string_to_int(_str) for _str in madlibs.split()]

    # The list of potential fill-ins
    nouns = ['dog', 'cat', 'day', 'her', 'park', 'ball', 'cat', 'school', 'like', 'hour', 'tree', 'car', 'house', 'week', 'shoe', 'beach']
    
    X = make_X(madlibs, nouns)
    print('X: ', X)
    print('')

    n_iter = 1500
    fillup = 10
    X_len=len(X)

    under = string_to_int("_")
    blank = 0
    
    with PicoZKCompiler('irs/picozk_test', options=['ram']):

        # Producer
        madlibs = madlibs #0
        nouns_list = [string_to_int(_str) for _str in nouns] #1
        X = X #2 TODO: Secrefy

        madlibs_words = madlibs_words #3
        X_words = ZKList([0] * 16) #4
        assembled_list = ZKList([0] * 16) #5
        result = "" #6
        fill = ZKList([0] * 2) #7

        reg1 = 0 #8
        reg2 = 0 #9
        reg3 = 0 #10
        reg4 = 0 #11

        dummy_int = 0 #12
        dummy_list = ZKList([0] * 16) #13
        reg5 = '' #14 This is used for only str
        dummy_str = "abcdefghijklmnopqrstuvwxyz" #15

        mem = [madlibs, nouns_list, X, 
                madlibs_words, X_words, assembled_list, result, fill,
                reg1, reg2, reg3, reg4, dummy_int, dummy_list, reg5, dummy_str]
        
        program = [ 

            # Make a fill list from hard-coded nouns 1 and 2

                    Instr(7, 12, 1, 12, 3, blank, 15, 12, 12, 8, 13, 6, 0),       ## Step1  #7: Set index 3 of idx1 (nouns) to idx 8 (reg1)
                    Instr(8, 12, 13, 8, 0, blank, 15, 12, 12, 12, 7, 6, 0),       ## Step2  #8: Set hard-coded noun1/2, idx 8(reg1), to idx 7(fill)
                    Instr(7, 12, 1, 12, 4, blank, 15, 12, 12, 8, 13, 6, 0),       ## Step3  #7: Set index 4 of idx1 (nouns) to idx 8 (reg1)
                    Instr(8, 12, 13, 8, 1, blank, 15, 12, 12, 12, 7, 6, 0),       ## Step4  #8: Set hard-coded noun2/2, idx 8(reg1), to idx 7(fill)


            # Making X_words (a list of strings) from X (a string)

                ## Only IF X[curr] == " ": Append X[idx-k : idx-i] (from last blank to current blank = word) to X_words
                    Instr(7, 9, 2, 12, 0, blank, 15, 12, 12, 8, 13, 14, 3),       ## Step5  #7: Assign idx9 (idx-i/reg2) of idx 2 (X) to idx 14(reg5)
                    Instr(3, 12, 13, 12, 4, blank, 14, 12, 12, 8, 13, 6, 2),     ## Step6  #3: Compare idx 8(reg1) and " " and assign result to idx 8(reg1)
                    Instr(4, 12, 13, 8, 1, 6, 0, 12, 12, 12, 13, 6, 1),       ## Step7  #4: Cond jump to +1/+6 if true/false

                    Instr(6, 12, 13, 12, 0, blank, 2, 10, 9, 8, 13, 6, 0),      ## Step8  #6: Assign idx10 (idx-k) : idx9 (idx-i) of idx 2 (X) to idx 8 (reg1)
                    Instr(8, 11, 13, 8, 0, blank, 15, 12, 12, 12, 4, 6, 1),      ## Step9  #8: Set idx8 (reg1) to idx 11 (reg4:idx to set the val) of idx 4 (X_words)
                    Instr(1, 9, 13, 12, 0, blank, 15, 12, 12, 10, 13, 6, 1),      ## Step10  #1: Assign idx 9 (idx-i/reg2) to idx 10 (idx-k/reg3)
                    Instr(2, 12, 13, 12, 1, blank, 15, 12, 12, 10, 13, 6, 0),      ## Step11  #2: add 1 to idx 10 (idx-k/reg3)
                    Instr(2, 12, 13, 12, 1, blank, 15, 12, 12, 11, 13, 6, 0),      ## Step12  #2: add 1 to idx 11 (X_words counter/reg4)

                    Instr(2, 12, 13, 12, 1, blank, 15, 12, 12, 9, 13, 6, 0),       ## Step13  #2: add 1 to idx 9 (idx-i/reg2)

                ## Determine whether or not to iterate over again depending idx-i< len(X)
                    Instr(3, 9, 13, 12, 2, X_len, 15, 12, 12, 8, 13, 6, 0),   ## Step14  #3: Compare idx 9 (idx-i) < len(X) and assign result to idx 8(reg1)
                    Instr(4, 12, 13, 8, -10, 1, 15, 12, 12, 12, 13, 6, 1),     ## Step15  #4: cond jump to next or start from the beginning of this block (-10)

                ## Only IF  X[-1] != " " (if string not ending with blank): Append X[k:] (the last word) to X_words
                    Instr(7, 12, 2, 12, -1, blank, 15, 12, 12, 8, 13, 14, 3),      ## Step16  #7 take last elem of idx2 (X) into idx 8(reg1)
                    Instr(3, 12, 13, 12, 5, blank, 14, 12, 12, 8, 13, 6, 2),     ## Step17  #3: Compare idx8(reg1) != " ", assign it to idx 8(reg1)
                    Instr(4, 12, 13, 8, 1,   3, 15, 12, 12, 12, 13, 6, 1),       ## Step18  #4: Cond jump to +1/+3 if true/false

                    Instr(6, 12, 13, 12, 0, blank, 2, 10, 12, 8, 13, 6, 1),      ## Step19  #6: Assign idx 10(idx-k) till end of idx 2(X) to idx 8 (reg1)
                    Instr(8, 11, 13, 8, 0, blank, 15, 12, 12, 12, 4, 6, 1),      ## Step20  #8: Set idx8 to idx 11 (X_words counter/reg4:idx to set the val) of idx 4 (X_words)

                    Instr(1, 12, 13, 12, 0, blank, 15, 12, 12, 9, 13, 6, 0),       ## Step21  #1: Set idx-9 (idx-i) to 0
                    Instr(1, 12, 13, 12, 0, blank, 15, 12, 12, 10, 13, 6, 0),      ## Step22  #1: Set idx-10 (idx-k) to 0
                    Instr(1, 12, 13, 12, 0, blank, 15, 12, 12, 11, 13, 6, 0),      ## Step23  #1: Set idx-11 (X_words counter/reg4) to 0


            # Take the first three nouns from X and hard-code the rest from the fill list
            
                ## FIRST IF curr madlibs_words is equal to "_"
                    Instr(7, 9, 3, 12, 0, blank, 15, 12, 12, 8, 13, 6, 1),       ## Step24  #7: Assign idx9 (idx-i) of idx 3 (madlibs_words) to idx 8(reg1)
                    Instr(3, 8, 13, 12, 0, under, 15, 12, 12, 8, 13, 6, 0),     ## Step25  #3: Compare idx 8(reg1) and "_" and assign result to idx 8(reg1)
                    Instr(4, 12, 13, 8, 1, 8, 15, 12, 12, 12, 13, 6, 1),       ## Step26  #4: Cond jump to +1/+8 if true/false

                ## SECOND IF index of madlibs_words is less than fill_upto (upto idx of third fill)
                    Instr(3, 9, 13, 12, 2, fillup, 15, 12, 12, 8, 13, 6, 0),  ## Step27  #3: Compare idx 9(idx-i) < fill_upto (10 for now) and assign result to idx 8(reg1)
                    Instr(4, 12, 13, 8, 1, 3, 15, 12, 12, 12, 13, 6, 1),       ## Step28  #4: Cond jump to +1/+3 if true/false

                ## IF Both TRUE (Append from X_Words)
                    Instr(7, 9, 4, 12, 0, blank, 15, 12, 12, 8, 13, 6, 1),       ## Step29  #7: Assign idx 9 (idx-i) of idx 4 (X_words) to idx 8(reg1)
                    Instr(4, 12, 13, 12, 5, 0, 15, 12, 12, 12, 13, 6, 0),       ## Step30  #4: jump to +5

                ## IF only the former TRUE (Append from fill/consts)
                    Instr(7, 10, 7, 12, 0, blank, 15, 12, 12, 8, 13, 6, 1),      ## Step31  #7: Assign idx10 (idx-k) of idx 7 (fill) to idx 8(reg1)
                    Instr(2, 12, 13, 12, 1, blank, 15, 12, 12, 10, 13, 6, 0),      ## Step32  #2: add 1 to idx 10 (idx-k)
                    Instr(4, 12, 13, 12, 2, 0, 15, 12, 12, 12, 13, 6, 0),       ## Step33  #4: jump to +2

                ## ELSE (Append from madlibs_words)
                    Instr(7, 9, 3, 12, 0, blank, 15, 12, 12, 8, 13, 6, 1),       ## Step34  #7: Assign idx9 (idx-i) of idx 3 (madlibs_words) to idx 8(reg1)

                ## APPEND and INCREMENT
                    Instr(8, 9, 13, 8, 0, blank, 15, 12, 12, 12, 5, 6, 1),       ## Step35  #8: append idx8 (reg1) to idx5 (assembled_list)
                    Instr(2, 12, 13, 12, 1, blank, 15, 12, 12, 9, 13, 6, 0),       ## Step36  #2: add 1 to idx 9 (idx-i)
                    
                ## CHECK IF ITERATE OR NEXT
                    Instr(5, 12, 4, 12, 0, blank, 15, 12, 12, 8, 13, 6, 0),       ## Step37  #9: Measure a length of index4(X_words) and assign it to idx 8(reg1)
                    Instr(3, 9, 13, 8, 2, blank, 15, 12, 12, 8, 13, 6, 1),       ## Step38  #3: Compare idx 9(idx-i) < idx 8(reg1) and assign result to idx 8(reg1)
                    Instr(4, 12, 13, 8, -15, 1, 15, 12, 12, 12, 13, 6, 1),     ## Step39  #4: Cond jump to -15/+1 if true/false

                    Instr(1, 12, 13, 12, 0, blank, 15, 12, 12, 9, 13, 6, 0),       ## Step40  #1: Set index9 (idx-i) to 0


            # Stringify the assembled_list into result
                    
                ## Only IF idx-i == 0: Append assembled_list[0] to result
                    Instr(3, 9, 13, 12, 0, 0, 15, 12, 12, 8, 13, 6, 0),       ## Step41  #3: Compare current index-i (idx 9) == 0 and set result to idx 8(reg1)
                    Instr(4, 12, 13, 8, 1, 3, 15, 12, 12, 12, 13, 6, 1),       ## Step42  #4: Cond jump to +1/+4 if true/false
                    Instr(7, 12, 5, 12, 0, blank, 15, 12, 12, 12, 13, 6, 2),       ## Step43  #7: Take the first element (idx 0) of idx5(assembled_list) and set it to des(6:result)
                    Instr(1, 12, 13, 12, 1, blank, 15, 12, 12, 9, 13, 6, 0),       ## Step44  #1: Set 1 to idx 9(idx-i)
                    
                ## Append " " +  assembled_list[idx-i] to result
                    Instr(7, 9, 5, 12, 0, blank, 15, 12, 12, 8, 13, 6, 1),       ## Step45  #7: Take idx 9(idx-i) of idx5 (assembled_list) and set it to idx8(reg1)
                    Instr(2, 12, 13, 12, 0, blank, 15, 12, 12, 12, 13, 6, 3),     ## Step46  #2: add " " to des(6:res)
                    Instr(2, 8, 13, 12, 0, blank, 15, 12, 12, 12, 13, 6, 2),       ## Step47  #2: add idx8(reg1) to des(6:res)
                    Instr(2, 12, 13, 12, 1, blank, 15, 12, 12, 9, 13, 6, 0),       ## Step48  #2: add +1 to idx9 (index-i)
                
                ## Determine whether or not to iterate over again depending idx-i< len(assembled_list)
                    Instr(5, 12, 5, 12, 0, blank, 15, 12, 12, 8, 13, 6, 0),       ## Step49  #9: Measure a length of index5 (assembled_list) and set it to idx 8(reg1)
                    Instr(3, 9, 13, 8, 2, blank, 15, 12, 12, 8, 13, 6, 1),       ## Step50  #3: Compare idx 9(idx-i) < idx 8(reg1) and assign result to idx 8(reg1)
                    Instr(4, 12, 13, 8, -10, 1, 0, 12, 12, 12, 13, 6, 1),     ## Step51  #4: Cond jump to -10/+1 if true/false


            # END
                    Instr(-1, 12, 13, 12, 0, blank, 15, 12, 12, 12, 13, 6, 0),      ## Step52  #-1: Terminal
                    ]

        pro_prog = make_program(program)

        pc = 0
        weight = 0

        for i in range(n_iter):
            pc, weight = step(pro_prog, pc, mem, weight)
        
        prod_Y = mem[6].replace('\x00', '') #TODO: FIXME
        print('prod_Y:', prod_Y)
        print('')
        res = mux("I have a dog and cat , and every day I walk her to the park" == prod_Y, 
                  mux(weight < n_iter, SecretInt(0), SecretInt(1))
                  , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)


        # Reproducer
        madlibs = madlibs #0
        nouns_list = [string_to_int(_str) for _str in nouns] #1
        X = None #2 Not available for reproducer

        madlibs_words = madlibs_words #3
        X_words = None #4 Not available for reproducer
        assembled_list = ZKList([0] * 16) #5
        result = "" #6
        fill = ZKList([0] * 5) #7

        reg1 = 0 #8
        reg2 = 0 #9
        reg3 = 0 #10
        reg4 = 0 #11

        dummy_int = 0 #12
        dummy_list = ZKList([0] * 16) #13
        reg5 = '' #14 This is used for only str
        dummy_str = "abcdefghijklmnopqrstuvwxyz" #15

        repro_mem = [madlibs, nouns_list, X, 
                madlibs_words, X_words, assembled_list, result, fill,
                reg1, reg2, reg3, reg4, dummy_int, dummy_list, reg5, dummy_str]

        program = [

            # Make a fill list by appending hard-coded nouns 1 - 5

                    Instr(7, 12, 1, 12, 0, blank, 15, 12, 12, 8, 13, 6, 0),       ## Step1  #7: Set index 0 of idx1 (nouns) to 8 (reg1)
                    Instr(8, 12, 13, 8, 0, blank, 15, 12, 12, 12, 7, 6, 0),       ## Step2  #14: Set hard-coded noun1/5 to idx7 (fill)
                    Instr(7, 12, 1, 12, 1, blank, 15, 12, 12, 8, 13, 6, 0),       ## Step3  #7: Set index 1 of idx1 (nouns) to 8 (reg1)
                    Instr(8, 12, 13, 8, 1, blank, 15, 12, 12, 12, 7, 6, 0),       ## Step4  #14: Set hard-coded noun2/5 to idx7 (fill)
                    Instr(7, 12, 1, 12, 2, blank, 15, 12, 12, 8, 13, 6, 0),       ## Step5  #7: Set index 2 of idx1 (nouns) to 8 (reg1)
                    Instr(8, 12, 13, 8, 2, blank, 15, 12, 12, 12, 7, 6, 0),       ## Step6  #14: Set hard-coded noun3/5 to idx7 (fill)
                    Instr(7, 12, 1, 12, 3, blank, 15, 12, 12, 8, 13, 6, 0),       ## Step7  #7: Set index 3 of idx1 (nouns) to 8 (reg1)
                    Instr(8, 12, 13, 8, 3, blank, 15, 12, 12, 12, 7, 6, 0),       ## Step8  #14: Set hard-coded noun4/5 to idx7 (fill)
                    Instr(7, 12, 1, 12, 4, blank, 15, 12, 12, 8, 13, 6, 0),       ## Step9  #7: Set index 4 of idx1 (nouns) to 8 (reg1)
                    Instr(8, 12, 13, 8, 4, blank, 15, 12, 12, 12, 7, 6, 0),       ## Step10 #14: Set hard-coded noun5/5 to idx7 (fill)
                    

            # Hard-Code all blanks from the nouns list
                
                ## IF madlibs_words[curr] == "_"
                    Instr(7, 9, 3, 12, 0, blank, 15, 12, 12, 8, 13, 6, 1),       ## Step11  #7: Assign idx9 (idx-i) of idx 3 (madlibs_words) to idx 8(reg1)
                    Instr(3, 8, 13, 12, 0, under, 15, 12, 12, 8, 13, 6, 0),     ## Step12  #3: Compare idx 10(reg1) and "_" and assign result to idx 10(reg1)
                    Instr(4, 12, 13, 8, 1, 4, 15, 12, 12, 12, 13, 6, 1),       ## Step13  #4: Cond jump to +1/+4 if true/false

                    ## TRUE: Append from fill[idx-k] to assembled_list
                    Instr(7, 10, 7, 12, 0, blank, 15, 12, 12, 8, 13, 6, 1),      ## Step14  #7: Assign idx10 (idx-k) of idx 7 (fill) to idx 8(reg1)
                    Instr(2, 12, 13, 12, 1, blank, 15, 12, 12, 10, 13, 6, 0),      ## Step15  #2: add 1 to idx 10 (idx-k)
                    Instr(4, 12, 13, 12, 2, 0, 15, 12, 12, 12, 13, 6, 0),       ## Step16  #4: jump to +2

                    ## ELSE: Append from madlibs_words[idx-k] to assembled_list
                    Instr(7, 9, 3, 12, 0, blank, 15, 12, 12, 8, 13, 6, 1),       ## Step17  #7: Assign idx9 (idx-i) of idx 3 (madlibs_words) to idx 8(reg1)
                    
                ## Append ops based on above
                    Instr(8, 9, 13, 8, 0, blank, 15, 12, 12, 12, 5, 6, 1),       ## Step18  #14: append idx 8(reg1) to idx 5 (assembled_list)
                    Instr(2, 12, 13, 12, 1, blank, 15, 12, 12, 9, 13, 6, 0),       ## Step19  #2: add 1 to idx 9 (idx-i)

                ## Determine whether or not to iterate over again depending idx-i< len(madlibs_words)
                    Instr(5, 12, 3, 12, 0, blank, 15, 12, 12, 8, 13, 6, 0),       ## Step20  #9: Measure a length of index0 (madlibs_words) and assign it to idx 8(reg1)
                    Instr(3, 9, 13, 8, 2, 0, 15, 12, 12, 8, 13, 6, 1),       ## Step21  #3: Compare idx 9(idx-i) < idx 8(reg1) and assign result to idx 8(reg1)
                    Instr(4, 12, 13, 8, -11, 1, 15, 12, 12, 12, 13, 6, 1),     ## Step22  #4: Cond jump to -11/+1 if true/false

                    Instr(1, 12, 13, 12, 0, blank, 15, 12, 12, 9, 13, 6, 0),       ## Step23  #1: Set index i to 0
                    Instr(1, 12, 13, 12, 0, blank, 15, 12, 12, 10, 13, 6, 0),      ## Step24  #1: Set index k to 0


            # Stringify the assembled_list into result
                    
                ## Only IF idx-i == 0: Append assembled_list[0] to result
                    Instr(3, 9, 13, 12, 0, 0, 15, 12, 12, 8, 13, 6, 0),       ## Step25  #3: Compare current index-i (idx 9) == 0 and set result to idx 8(reg1)
                    Instr(4, 12, 13, 8, 1, 3, 15, 12, 12, 12, 13, 6, 1),       ## Step26  #4: Cond jump to +1/+4 if true/false
                    Instr(7, 12, 5, 12, 0, blank, 15, 12, 12, 12, 13, 6, 2),       ## Step27  #7: Take the first element (idx 0) of idx5(assembled_list) and set it to des(6:result)
                    Instr(1, 12, 13, 12, 1, blank, 15, 12, 12, 9, 13, 6, 0),       ## Step28  #1: Set 1 to idx 9(idx-i)
                    
                ## Append " " +  assembled_list[idx-i] to result
                    Instr(7, 9, 5, 12, 0, blank, 15, 12, 12, 8, 13, 6, 1),       ## Step29  #7: Take idx 9(idx-i) of idx5 (assembled_list) and set it to idx8(reg1)
                    Instr(2, 12, 13, 12, 0, blank, 15, 12, 12, 12, 13, 6, 3),     ## Step30  #2: add " " to des(6:res)
                    Instr(2, 8, 13, 12, 0, blank, 15, 12, 12, 12, 13, 6, 2),       ## Step31  #2: add idx8(reg1) to des(6:res)
                    Instr(2, 12, 13, 12, 1, blank, 15, 12, 12, 9, 13, 6, 0),       ## Step32  #2: add +1 to idx9 (index-i)
                
                ## Determine whether or not to iterate over again depending idx-i< len(assembled_list)
                    Instr(5, 12, 5, 12, 0, blank, 15, 12, 12, 8, 13, 6, 0),       ## Step33  #9: Measure a length of index5 (assembled_list) and set it to idx 8(reg1)
                    Instr(3, 9, 13, 8, 2, 0, 15, 12, 12, 8, 13, 6, 1),       ## Step34  #3: Compare idx 9(idx-i) < idx 8(reg1) and assign result to idx 8(reg1)
                    Instr(4, 12, 13, 8, -10, 1, 15, 12, 12, 12, 13, 6, 1),     ## Step35  #4: Cond jump to -10/+1 if true/false


            # END
                    Instr(-1, 12, 13, 12, 0, blank, 15, 12, 12, 12, 13, 6, 0),      ## Step36  #-1: Terminal
                    ]
        repro_prog = make_program(program)

        pc = 0
        weight = 0

        for i in range(n_iter):
            pc, weight = step(repro_prog, pc, repro_mem, weight)

        reprod_Y = repro_mem[6].replace('\x00', '') #TODO: FIXME
        print('reprod_Y: ', reprod_Y)
        print('')
        res = mux("I have a dog and cat , and every day I walk her to the park" == reprod_Y, 
                  mux(weight < n_iter, SecretInt(0), SecretInt(1))
                  , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)

if __name__ == "__main__":
    main()