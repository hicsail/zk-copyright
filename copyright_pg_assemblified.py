from typing import List

# Class to hold a single instruction TODO: @dataclass
class Instr:
    def __init__(self, opcode: int, src1: int, src2: int, src3: int, dest: int, imm: int):
        self.opcode = opcode
        self.src1 = src1
        self.src2 = src2
        self.src3 = src3
        self.dest = dest
        self.imm = imm


# Class to hold a program as multiple lists of instructions TODO: @dataclass
class Program:
    def __init__(self, opcode: List[int], src1: List[int], src2: List[int], src3: List[int], dest: List[int], imm: List[int]):
        self.opcode: List[int] = opcode
        self.src1: List[int] = src1
        self.src2: List[int] = src2
        self.src3: List[int] = src3
        self.dest: List[int] = dest
        self.imm: List[int] = imm


def make_X(madlibs, nouns):
    X = madlibs.split()
    i = 0

    for k in range(len(X)):
        if X[k] == '_':
            X[k] = nouns[i]
            i+=1

    X = ' '.join(X) # This is the madlibs text with all blanks are filled

    return X


def step(prog: Program, pc: int, mem):
    
    instr = fetch(prog, pc)
    p1 = instr.src1
    p2 = instr.src2
    p3 = instr.src3
    des = instr.dest
    imm =  instr.imm
    new_pc = pc


    # 1. Set a const/mem[val] to dest
    if instr.opcode == 1:

        '''
            des:depends
            p1:const(imm==0) or by mem[val](imm==1)
        '''
        if imm == 0:
            mem[des] = p1
        elif imm ==1:
            mem[des] = mem[p1]

        return new_pc + 1


    # 2. add const/mem[val] to des
    elif instr.opcode == 2:

        '''
            des: target
            p1: increment by const(imm==0) or by mem[val](imm==1)
        '''
        if imm == 0:
            mem[des] += p1
        elif imm ==1:
            mem[des] += mem[p1]
        
        return new_pc + 1


    # 3. compare value in one index with const
    elif instr.opcode == 3:

        '''
            des: target
            p1: element 1 to compare
            p2: const(imm==0) or mem[val](imm==1) to compare
            p3: operation (0: equal, 1:not equal, 2: p1 is smaller than p2, 3: p1 is greater than p2)
        '''
        
        if imm == 0:
            p2 = p2
        elif imm == 1:
            p2 = mem[p2]

        if p3 ==0:
            mem[des] = (mem[p1] == p2)
        elif p3 ==1:
            mem[des] = (mem[p1] != p2)
        elif p3 ==2:
            mem[des] = (mem[p1] < p2)
        elif p3 ==3:
            mem[des] = (mem[p1] > p2)
        return new_pc + 1

            
    # 4. jump or cond-jump
    elif instr.opcode == 4:

        '''
            p1: pc shift always (imm==0)/if True(imm==1)
            p2: pc shift if False
            p3: condition(im==1)
        '''

        if imm == 0:
            return new_pc + p1
        elif mem[p3]==True:
            return new_pc + p1
        else:
            return new_pc + p2


    # 5. length of 
    elif instr.opcode == 5:
        '''
            des: target index
            p1: list/string to measure length
        '''
        mem[des] = len(mem[p1])
        
        return new_pc +1
    

    # 6. access more than one index in list
    elif instr.opcode == 6:

        '''
            des:target
            p1: index of origin
            p2: beginning index of nested list of origin
            p3: end index of nested list of origin (imm==0)/otherwise automatically till end (imm==1)
        '''
        if imm == 0:
            mem[des] = mem[p1][mem[p2]:mem[p3]]
        elif imm == 1:
            mem[des] = mem[p1][mem[p2]:]

        return new_pc + 1
        

    # 7. Access nested list by constant/pointer
    elif instr.opcode == 7:

        '''
            des:target
            p1: index of list
            p2: constant/pointer (imm==0/1)
        '''
        if imm == 0:
            mem[des] = mem[p1][p2]
        elif imm == 1:
            mem[des] = mem[p1][mem[p2]]

        return new_pc + 1


    # 8. Append Value
    if instr.opcode == 8:

        '''
            des:target memory address
            p1: any index
        '''
        mem[des].append(mem[p1])
        return new_pc + 1
   

    # -1. terminal
    elif instr.opcode == -1:

        return new_pc        


def make_program(prog): #TODO: ZKListify
    length = len(prog)
    opcode = [0 for _ in range(length)]
    src1 = [0 for _ in range(length)]
    src2 = [0 for _ in range(length)]
    src3 = [0 for _ in range(length)]
    dest = [0 for _ in range(length)]
    imm = [0 for _ in range(length)]

    for i, instr in enumerate(prog):
        opcode[i] = instr.opcode
        src1[i] = instr.src1
        src2[i] = instr.src2
        src3[i] = instr.src3
        dest[i] = instr.dest
        imm[i] = instr.imm

    return Program(opcode, src1, src2, src3, dest, imm)


# Fetch an instruction from a program
def fetch(prog: Program, pc: int): #TODO: change int to SecretInt
    return Instr(prog.opcode[pc],
                 prog.src1[pc],
                 prog.src2[pc],
                 prog.src3[pc],
                 prog.dest[pc],
                 prog.imm[pc])

def main():
    # The Mad Libs template
    madlibs = "I have a _ and _ , and every _ I walk _ to the _"

    # The list of potential fill-ins
    nouns = ['dog', 'cat', 'day', 'her', 'park', 'ball', 'cat', 'school', 'like', 'hour', 'tree', 'car', 'house', 'week', 'shoe', 'beach']

    X = make_X(madlibs, nouns)
    print('X: ', X)
    print('')

    n_iter = 1500
    fillup = 10
    X_len=len(X)
    mad_len=len(madlibs)

    #TODO: uncomment with PicoZKCompiler('picozk_test', options=['ram']):

    # Producer
    madlibs = madlibs #0
    nouns = nouns #1
    X = X #2
    
    madlibs_words = [] #3
    X_words = [] #4
    assembled_list = [] #5
    result = "" #6
    fill = [] #7
    
    reg1 = 0 #8
    reg2 = 0 #9
    reg3 = 0 #10
    reg4 = 0 #11

    mem = [madlibs, nouns, X, 
           madlibs_words, X_words, assembled_list, result, fill,
           reg1, reg2, reg3, reg4]
        
    program = [ 
        #  Making madlibs_words (a list of strings) by spliting madlibs into words

            ## Only IF madlibs[curr] (char) == " ": Append madlibs[idx-k : idx-i] (from last blank to current blank = word) to madlibs_words
               Instr(7, 0, 9, 0, 8, 1),       ## Step0  #7: Assign idx9 (idx-i) of idx 0(madlibs) to idx 8(reg1)
               Instr(3, 8, " ", 0, 8, 0),     ## Step1  #3: Compare idx 8(reg1) == " " and assign result to idx 8(reg1)
               Instr(4, 1, 5, 8, 0, 1),       ## Step2  #4: Cond jump to +1/+5 if true/false

               Instr(6, 0, 10, 9, 8, 0),      ## Step3  #6: Assign idx 10 to 9 of idx 0 (madlibs) to idx 8 (reg1)
               Instr(8, 8, 0, 0, 3, 0),       ## Step4  #14: append idx8 to idx 3 (madlibs_words)
               Instr(1, 9, 0, 0, 10, 1),      ## Step5  #1: Assign idx 9 (index i) to idx 10 (idx-k)
               Instr(2, 1, 0, 0, 10, 0),      ## Step6  #2: add 1 to idx 10 (idx-k)

               Instr(2, 1, 0, 0, 9, 0),       ## Step7  #2: add 1 to idx 9 (idx-i)
               
            ## Determine whether or not to iterate over again depending idx-i< len(madlibs_len)
               Instr(3, 9, mad_len, 2, 8, 0), ## Step8  #3: Check if idx 9 (idx-i) < madlibs_len, and assign result to idx 8(reg1)
               Instr(4, -9, 1, 8, 0, 1),      ## Step9  #4: jump to next or back to beginning
               
            ## Only IF last elem of madlibs != " " (if string not ending with blank): Append madlibs[k:] (the last word) to madlibs_words
               Instr(7, 0, -1, 0, 8, 0),      ## Step10  #7: take last elem of idx 0(madlibs) into idx 8(reg1)
               Instr(3, 8, " ", 1, 8, 0),     ## Step11  #3: Compare idx8(reg1) != " ", assign it to idx 8(reg1)
               Instr(4, 1, 3, 8, 0, 1),       ## Step12  #4: Cond jump to +1/+3 if true/false

               Instr(6, 0, 10, 0, 8, 1),      ## Step13  #6: Assign idx 10 till end of idx 0(madlibs) to idx 8 (reg1)
               Instr(8, 8, 0, 0, 3, 0),       ## Step14  #8: append idx8 (reg1) to idx 3(madlibs)

               Instr(1, 0, 0, 0, 9, 0),       ## Step15  #1: Set idx9(index-i) to 0
               Instr(1, 0, 0, 0, 10, 0),      ## Step16  #1: Set idx10(index-k) to 0


        # Make a fill list from hard-coded nouns 1 and 2

               Instr(7, 1, 3, 0, 8, 0),       ## Step17  #7: Set index 3 of idx1 (nouns) to idx 8 (reg1)
               Instr(8, 8, 0, 0, 7, 0),       ## Step18  #8: Append hard-coded noun1/2, idx 8(reg1), to idx 7(fill)
               Instr(7, 1, 4, 0, 8, 0),       ## Step19  #7: Set index 4 of idx1 (nouns) to idx 8 (reg1)
               Instr(8, 8, 0, 0, 7, 0),       ## Step20  #8: Append hard-coded noun2/2, idx 8(reg1), to idx 7(fill)


        # Making X_words (a list of strings) from X (a string)

            ## Only IF X[curr] == " ": Append X[idx-k : idx-i] (from last blank to current blank = word) to X_words
               Instr(7, 2, 9, 0, 8, 1),       ## Step21  #7: Assign idx9 (idx-i) of idx 2 (X) to idx 8(reg1)
               Instr(3, 8, " ", 0, 8, 0),     ## Step22  #3: Compare idx 8(reg1) and " " and assign result to idx 8(reg1)
               Instr(4, 1, 5, 8, 0, 1),       ## Step23  #4: Cond jump to +1/+5 if true/false

               Instr(6, 2, 10, 9, 8, 0),      ## Step24  #6: Assign idx10 (idx-k) to idx9 (idx-i) of idx 2 (X) to idx 8 (reg1)
               Instr(8, 8, 0, 0, 4, 0),       ## Step25  #8: Append idx8 (reg1) to idx 4 (X_words)
               Instr(1, 9, 0, 0, 10, 1),      ## Step26  #1: Assign idx 9 (idx-i) to idx 10 (idx-k)
               Instr(2, 1, 0, 0, 10, 0),      ## Step27  #2: add 1 to idx 10

               Instr(2, 1, 0, 0, 9, 0),       ## Step28  #2: add 1 to idx 11

            ## Determine whether or not to iterate over again depending idx-i< len(X)
               Instr(3, 9, X_len, 2, 8, 0),   ## Step29  #3: Compare idx 9 (idx-i) < len(X) and assign result to idx 8(reg1)
               Instr(4, -9, 1, 8, 0, 1),      ## Step30  #4: cond jump to next or start from the beginning of this block (-9)

            ## Only IF  X[-1] != " " (if string not ending with blank): Append X[k:] (the last word) to X_words
               Instr(7, 2, -1, 0, 8, 0),      ## Step31  #7 take last elem of idx2 (X) into idx 8(reg1)
               Instr(3, 8, " ", 1, 8, 0),     ## Step32  #3: Compare idx8(reg1) != " ", assign it to idx 8(reg1)
               Instr(4, 1, 3, 8, 0, 1),       ## Step33  #4: Cond jump to +1/+3 if true/false

               Instr(6, 2, 10, 0, 8, 1),      ## Step34  #6: Assign idx 10(idx-k) till end of idx 2(X) to idx 8 (reg1)
               Instr(8, 8, 0, 0, 4, 0),       ## Step35  #14: append idx8 to idx 4 (X_words)

               Instr(1, 0, 0, 0, 9, 0),       ## Step36  #1: Set idx-9 (idx-i) to 0
               Instr(1, 0, 0, 0, 10, 0),      ## Step37  #1: Set idx-10 (idx-k) to 0
  

        # Take the first three nouns from X and hard-code the rest from the fill list
        
            ## FIRST IF curr madlibs_words is equal to "_"
               Instr(7, 3, 9, 0, 8, 1),       ## Step38  #7: Assign idx9 (idx-i) of idx 3 (madlibs_words) to idx 8(reg1)
               Instr(3, 8, "_", 0, 8, 0),     ## Step39  #3: Compare idx 8(reg1) and "_" and assign result to idx 8(reg1)
               Instr(4, 1, 8, 8, 0, 1),       ## Step40  #4: Cond jump to +1/+8 if true/false

            ## SECOND IF index of madlibs_words is less than fill_upto (upto idx of third fill)
               Instr(3, 9, fillup, 2, 8, 0),  ## Step41  #3: Compare idx 9(idx-i) < fill_upto (10 for now) and assign result to idx 8(reg1)
               Instr(4, 1, 3, 8, 0, 1),       ## Step42  #4: Cond jump to +1/+3 if true/false

            ## IF Both TRUE (Append from X_Words)
               Instr(7, 4, 9, 0, 8, 1),       ## Step43  #7: Assign idx 9 (idx-i) of idx 4 (X_words) to idx 8(reg1)
               Instr(4, 5, 0, 0, 0, 0),       ## Step44  #4: jump to +5

            ## IF only the former TRUE (Append from fill/consts)
               Instr(7, 7, 10, 0, 8, 1),      ## Step45  #7: Assign idx10 (idx-k) of idx 7 (fill) to idx 8(reg1)
               Instr(2, 1, 0, 0, 10, 0),      ## Step46  #2: add 1 to idx 10 (idx-k)
               Instr(4, 2, 0, 0, 0, 0),       ## Step47  #4: jump to +2

            ## ELSE (Append from madlibs_words)
               Instr(7, 3, 9, 0, 8, 1),       ## Step48  #7: Assign idx9 (idx-i) of idx 3 (madlibs_words) to idx 8(reg1)

            ## APPEND and INCREMENT
               Instr(8, 8, 0, 0, 5, 0),       ## Step49  #8: append idx8 (reg1) to idx5 (assembled_list)
               Instr(2, 1, 0, 0, 9, 0),       ## Step50  #2: add 1 to idx 9 (idx-i)
                
            ## CHECK IF ITERATE OR NEXT
               Instr(5, 4, 0, 0, 8, 0),       ## Step51  #9: Measure a length of index4(X_words) and assign it to idx 8(reg1)
               Instr(3, 9, 8, 2, 8, 1),       ## Step52  #3: Compare idx 9(idx-i) < idx 8(reg1) and assign result to idx 8(reg1)
               Instr(4, -15, 1, 8, 0, 1),     ## Step53  #4: Cond jump to -15/+1 if true/false

               Instr(1, 0, 0, 0, 9, 0),       ## Step54  #1: Set index9 (idx-i) to 0


        # Stringify the assembled_list into result
               
            ## Only IF idx-i == 0: Append assembled_list[0] to result
               Instr(3, 9, 0, 0, 8, 0),       ## Step55  #3: Compare current index-i (idx 9) == 0 and assign result to idx 8(reg1)
               Instr(4, 1, 3, 8, 0, 1),       ## Step56  #4: Cond jump to +1/+4 if true/false
               Instr(7, 5, 0, 0, 6, 0),       ## Step57  #7: Take idx 8(reg1) of idx5(assembled_list) and assign it to des(6:result)
               Instr(1, 1, 0, 0, 9, 0),       ## Step58  #1: Assign 1 to idx 9(idx-i)
               
            ## Append " " +  assembled_list[idx-i] to result
               Instr(7, 5, 9, 0, 8, 1),       ## Step59  #7: Take idx 9(idx-i) of idx5 (assembled_list) and assign it to idx8(reg1)
               Instr(2, " ", 0, 0, 6, 0),     ## Step60  #2: add " " to des(6:res)
               Instr(2, 8, 0, 0, 6, 1),       ## Step61  #2: add idx8(reg1) to des(6:res)
               Instr(2, 1, 0, 0, 9, 0),       ## Step62  #2: add +1 to idx9 (index-i)
            
            ## Determine whether or not to iterate over again depending idx-i< len(assembled_list)
               Instr(5, 5, 0, 0, 8, 0),       ## Step63  #9: Measure a length of index5 (assembled_list) and assign it to idx 8(reg1)
               Instr(3, 9, 8, 2, 8, 1),       ## Step64  #3: Compare idx 9(idx-i) < idx 8(reg1) and assign result to idx 8(reg1)
               Instr(4, -10, 1, 8, 0, 1),     ## Step65  #4: Cond jump to -10/+1 if true/false


        # END
               Instr(-1, 0, 0, 0, 0, 0),      ## Step66  #-1: Terminal
              ]

    pro_prog = make_program(program)
    
    pc = 0

    for i in range(n_iter):
        pc = step(pro_prog, pc, mem)

    prod_Y = mem[6]
    print('prod_Y: ', prod_Y)
    print('')
    assert("I have a dog and cat , and every day I walk her to the park" == prod_Y)


    # Reproducer
    madlibs = madlibs #0
    nouns = nouns #1
    X = None #2 Not available for reproducer
    
    madlibs_words = [] #3
    X_words = None #4 Not available for reproducer
    assembled_list = [] #5
    result = "" #6
    fill = [] #7
    
    reg1 = 0 #8
    reg2 = 0 #9
    reg3 = 0 #10
    reg4 = 0 #11

    repro_mem = [madlibs, nouns, X, 
           madlibs_words, X_words, assembled_list, result, fill,
           reg1, reg2, reg3, reg4]
    
    program = [
        #  Making madlibs_words (a list of strings) by spliting madlibs into words

            ## Only IF madlibs[curr] (char) == " ": Append madlibs[idx-k : idx-i] (from last blank to current blank = word) to madlibs_words
               Instr(7, 0, 9, 0, 8, 1),       ## Step0  #7: Assign idx9 (idx-i) of idx 0(madlibs) to idx 8(reg1)
               Instr(3, 8, " ", 0, 8, 0),     ## Step1  #3: Compare idx 8(reg1) == " " and assign result to idx 8(reg1)
               Instr(4, 1, 5, 8, 0, 1),       ## Step2  #4: Cond jump to +1/+5 if true/false

               Instr(6, 0, 10, 9, 8, 0),      ## Step3  #6: Assign idx 10 to 9 of idx 0 (madlibs) to idx 8 (reg1)
               Instr(8, 8, 0, 0, 3, 0),       ## Step4  #14: append idx8 to idx 3 (madlibs_words)
               Instr(1, 9, 0, 0, 10, 1),      ## Step5  #1: Assign idx 9 (index i) to idx 10 (idx-k)
               Instr(2, 1, 0, 0, 10, 0),      ## Step6  #2: add 1 to idx 10 (idx-k)

               Instr(2, 1, 0, 0, 9, 0),       ## Step7  #2: add 1 to idx 9 (idx-i)
               
            ## Determine whether or not to iterate over again depending idx-i< len(madlibs_len)
               Instr(3, 9, mad_len, 2, 8, 0), ## Step8  #3: Check if idx 9 (idx-i) < madlibs_len, and assign result to idx 8(reg1)
               Instr(4, -9, 1, 8, 0, 1),      ## Step9  #4: jump to next or back to beginning
               
            ## Only IF last elem of madlibs != " " (if string not ending with blank): Append madlibs[k:] (the last word) to madlibs_words
               Instr(7, 0, -1, 0, 8, 0),      ## Step10  #7: take last elem of idx 0(madlibs) into idx 8(reg1)
               Instr(3, 8, " ", 1, 8, 0),     ## Step11  #3: Compare idx8(reg1) != " ", assign it to idx 8(reg1)
               Instr(4, 1, 3, 8, 0, 1),       ## Step12  #4: Cond jump to +1/+3 if true/false

               Instr(6, 0, 10, 0, 8, 1),      ## Step13  #6: Assign idx 10 till end of idx 0(madlibs) to idx 8 (reg1)
               Instr(8, 8, 0, 0, 3, 0),       ## Step14  #8: append idx8 (reg1) to idx 3(madlibs)

               Instr(1, 0, 0, 0, 9, 0),       ## Step15  #1: Set idx9(index-i) to 0
               Instr(1, 0, 0, 0, 10, 0),      ## Step16  #1: Set idx10(index-k) to 0


        # Make a fill list by appending hard-coded nouns 1 - 5

               Instr(7, 1, 0, 0, 8, 0),       ## Step17  #7: Set index 0 of idx1 (nouns) to 8 (reg1)
               Instr(8, 8, 0, 0, 7, 0),       ## Step18  #14: Append hard-coded noun1/5 to idx6 (fill)
               Instr(7, 1, 1, 0, 8, 0),       ## Step19  #7: Set index 0 of idx1 (nouns) to 8 (reg1)
               Instr(8, 8, 0, 0, 7, 0),       ## Step20  #14: Append hard-coded noun2/5 to idx6 (fil
               Instr(7, 1, 2, 0, 8, 0),       ## Step21  #7: Set index 0 of idx1 (nouns) to 8 (reg1)
               Instr(8, 8, 0, 0, 7, 0),       ## Step22  #14: Append hard-coded noun3/5 to idx6 (fil
               Instr(7, 1, 3, 0, 8, 0),       ## Step23  #7: Set index 0 of idx1 (nouns) to 8 (reg1)
               Instr(8, 8, 0, 0, 7, 0),       ## Step24  #14: Append hard-coded noun4/5 to idx6 (fil
               Instr(7, 1, 4, 0, 8, 0),       ## Step25  #7: Set index 0 of idx1 (nouns) to 8 (reg1)
               Instr(8, 8, 0, 0, 7, 0),       ## Step26  #14: Append hard-coded noun5/5 to idx6 (fil
               

        # Hard-Code all blanks from the nouns list
            
            ## IF madlibs_words[curr] == "_"
               Instr(7, 3, 9, 0, 8, 1),       ## Step27  #7: Assign idx9 (idx-i) of idx 3 (madlibs_words) to idx 8(reg1)
               Instr(3, 8, "_", 0, 8, 0),     ## Step28  #3: Compare idx 10(reg1) and "_" and assign result to idx 10(reg1)
               Instr(4, 1, 4, 8, 0, 1),       ## Step29  #4: Cond jump to +1/+4 if true/false

               ## TRUE: Append from fill[idx-k] to assembled_list
               Instr(7, 7, 10, 0, 8, 1),      ## Step30  #7: Assign idx10 (idx-k) of idx 7 (fill) to idx 8(reg1)
               Instr(2, 1, 0, 0, 10, 0),      ## Step31  #2: add 1 to idx 10 (idx-k)
               Instr(4, 2, 0, 0, 0, 0),       ## Step32  #4: jump to +2

               ## ELSE: Append from madlibs_words[idx-k] to assembled_list
               Instr(7, 3, 9, 0, 8, 1),       ## Step33  #7: Assign idx9 (idx-i) of idx 3 (madlibs_words) to idx 8(reg1)
                
            ## Append ops based on above
               Instr(8, 8, 0, 0, 5, 0),       ## Step34  #14: append idx 8(reg1) to idx 5 (assembled_list)
               Instr(2, 1, 0, 0, 9, 0),       ## Step35  #2: add 1 to idx 9 (idx-i)

            ## Determine whether or not to iterate over again depending idx-i< len(madlibs_words)
               Instr(5, 3, 0, 0, 8, 0),       ## Step36  #9: Measure a length of index0 (madlibs_words) and assign it to idx 8(reg1)
               Instr(3, 9, 8, 2, 8, 1),       ## Step37  #3: Compare idx 9(idx-i) < idx 8(reg1) and assign result to idx 8(reg1)
               Instr(4, -11, 1, 8, 0, 1),     ## Step38  #4: Cond jump to -11/+1 if true/false

               Instr(1, 0, 0, 0, 9, 0),       ## Step39  #1: Set index i to 0
               Instr(1, 0, 0, 0, 10, 0),      ## Step40  #1: Set index k to 0


        # Stringify the assembled_list into result
               
            ## Only IF idx-i == 0: Append assembled_list[0] to result
               Instr(3, 9, 0, 0, 8, 0),       ## Step41  #3: Compare current index-i (idx 9) == 0 and assign result to idx 8(reg1)
               Instr(4, 1, 3, 8, 0, 1),       ## Step42  #4: Cond jump to +1/+4 if true/false
               Instr(7, 5, 0, 0, 6, 0),       ## Step43  #7: Take idx 8(reg1) of idx5(assembled_list) and assign it to des(6:result)
               Instr(1, 1, 0, 0, 9, 0),       ## Step44  #1: Assign 1 to idx 9(idx-i)
               
            ## Append " " +  assembled_list[idx-i] to result
               Instr(7, 5, 9, 0, 8, 1),       ## Step45  #7: Take idx 9(idx-i) of idx5 (assembled_list) and assign it to idx8(reg1)
               Instr(2, " ", 0, 0, 6, 0),     ## Step46  #2: add " " to des(6:res)
               Instr(2, 8, 0, 0, 6, 1),       ## Step47  #2: add idx8(reg1) to des(6:res)
               Instr(2, 1, 0, 0, 9, 0),       ## Step48  #2: add +1 to idx9 (index-i)
            
            ## Determine whether or not to iterate over again depending idx-i< len(assembled_list)
               Instr(5, 5, 0, 0, 8, 0),       ## Step49  #9: Measure a length of index5 (assembled_list) and assign it to idx 8(reg1)
               Instr(3, 9, 8, 2, 8, 1),       ## Step50  #3: Compare idx 9(idx-i) < idx 8(reg1) and assign result to idx 8(reg1)
               Instr(4, -10, 1, 8, 0, 1),     ## Step51  #4: Cond jump to -10/+1 if true/false


        # END
               Instr(-1, 0, 0, 0, 0, 0),      ## Step52  #-1: Terminal
              ]
    repro_prog = make_program(program)

    pc = 0

    for i in range(n_iter):
        pc = step(repro_prog, pc, repro_mem)
        
    reprod_Y = repro_mem[6]
    print('reprod_Y: ', reprod_Y)
    print('')
    assert("I have a dog and cat , and every day I walk her to the park" == reprod_Y)


if __name__ == "__main__":
    main()