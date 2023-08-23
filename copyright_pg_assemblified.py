from typing import List

# Class to hold a single instruction TODO: @dataclass
class Instr:
    def __init__(self, opcode: int, src1: int, src2: int, src3: int, dest: int):
        self.opcode = opcode
        self.src1 = src1
        self.src2 = src2
        self.src3 = src3
        self.dest = dest


# Class to hold a program as multiple lists of instructions TODO: @dataclass
class Program:
    def __init__(self, opcode: List[int], src1: List[int], src2: List[int], src3: List[int], dest: List[int]):
        self.opcode: List[int] = opcode
        self.src1: List[int] = src1
        self.src2: List[int] = src2
        self.src3: List[int] = src3
        self.dest: List[int] = dest


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
    new_pc = pc


    # 1. Set a const to dest
    if instr.opcode == 1:

        '''
            des:depends
            p1:any const
        '''

        mem[des] = p1

        return new_pc + 1
    

    # 2. Set a value to dest
    elif instr.opcode == 2:

        '''
            des:depends
            p1:any index
        '''

        mem[des] = mem[p1]

        return new_pc + 1


    # 3. add const
    elif instr.opcode == 3:

        '''
            des: target
            p1: increment by
        '''
        mem[des] += p1
        
        return new_pc + 1



    # 4. add val from memory
    elif instr.opcode == 4:

        '''
            des: target
            p1: add of value to increment by
        '''
        mem[des] += mem[p1]
        
        return new_pc + 1


    # 5. compare value in one index with const
    elif instr.opcode == 5:

        '''
            des: target
            p1: element 1 to compare
            p2: const to compare
            p3: operation (0: equal, 1:not equal, 2: p1 is smaller than p2, 3: p1 is greater than p2)
        '''
        
        if p3 ==0:
            mem[des] = (mem[p1] == p2)
        elif p3 ==1:
            mem[des] = (mem[p1] != p2)
        elif p3 ==2:
            mem[des] = (mem[p1] < p2)
        elif p3 ==3:
            mem[des] = (mem[p1] > p2)
        return new_pc + 1
    

    # 6. compare values in two indexes
    elif instr.opcode == 6:

        '''
            des: target
            p1: element 1 to compare
            p2: element 2 to compare
            p3: operation (0: equal, 1:not equal, 2: p1 is smaller than p2, 3: p1 is greater than p2)
        '''
        if p3 ==0:
            mem[des] = (mem[p1] == mem[p2])
        elif p3 ==1:
            mem[des] = (mem[p1] != mem[p2])
        elif p3 ==2:
            mem[des] = (mem[p1] < mem[p2])
        elif p3 ==3:
            mem[des] = (mem[p1] > mem[p2])
        return new_pc + 1
    

    # 7. jump
    elif instr.opcode == 7:

        '''
            p1: next pc
        '''

        return new_pc + p1

            
    # 8. cond jump
    elif instr.opcode == 8:

        '''
            p1: condition
            p2: pc shift if True
            p3: pc shift if False
        '''

        if mem[p1]==True:
            return new_pc + p2
        else:
            return new_pc + p3

    # 9. length of 
    elif instr.opcode == 9:
        '''
            des: target index
            p1: list/string to measure length
        '''
        mem[des] = len(mem[p1])
        
        return new_pc +1
    

    # 10. access more than one index in list
    elif instr.opcode == 10:

        '''
            des:target
            p1: index of origin
            p2: beginning index of nested list of origin
            p3: end index of nested list of origin
        '''

        mem[des] = mem[p1][mem[p2]:mem[p3]]

        return new_pc + 1


    # 11. access more than one index till end of list
    elif instr.opcode == 11:

        '''
            des:target
            p1: index of origin
            p2: beginning index of nested list of origin
        '''

        mem[des] = mem[p1][mem[p2]:]

        return new_pc + 1
        

    # 12. Access nested list by constant
    elif instr.opcode == 12:

        '''
            des:target
            p1: index of list
            p2: constant/pointer
        '''
        mem[des] = mem[p1][p2]

        return new_pc + 1
    

    # 13. Access nested list by pointer
    elif instr.opcode == 13:

        '''
            des:target
            p1: index of list
            p2: pointer in memory
        '''
        mem[des] = mem[p1][mem[p2]]

        return new_pc + 1


    # 14. Append Value
    if instr.opcode == 14:

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

    for i, instr in enumerate(prog):
        opcode[i] = instr.opcode
        src1[i] = instr.src1
        src2[i] = instr.src2
        src3[i] = instr.src3
        dest[i] = instr.dest

    return Program(opcode, src1, src2, src3, dest)


# Fetch an instruction from a program
def fetch(prog: Program, pc: int): #TODO: change int to SecretInt
    return Instr(prog.opcode[pc],
                 prog.src1[pc],
                 prog.src2[pc],
                 prog.src3[pc],
                 prog.dest[pc])

def main():
    # The Mad Libs template
    madlibs = "I have a _ and _ , and every _ I walk _ to the _"

    # The list of potential fill-ins
    nouns = ['dog', 'cat', 'day', 'her', 'park', 'ball', 'cat', 'school', 'like', 'hour', 'tree', 'car', 'house', 'week', 'shoe', 'beach']

    X = make_X(madlibs, nouns)
    print('X: ', X)
    print('')

    n_iter = 1500
    X_len=len(X)
    mad_len=len(madlibs)

    #TODO: uncomment with PicoZKCompiler('picozk_test', options=['ram']):

    # Producer
    madlibs_words = [] #0
    X_words = [] #1
    assembled_list = [] #2
    result = "" #3
    i = 0 #4
    k = 0 #5
    fill = [] #6
    madlibs = madlibs #7
    nouns = nouns #8
    X = X #9
    bot1 = None #10
    bot2 = None #11
    bot3 = None #12
    bot4 = None #13

    mem = [madlibs_words, X_words, assembled_list, result, i, k, fill,
           madlibs, nouns, X, bot1, bot2, bot3, bot4]
        
    program = [ 
               # Split madlibs into a list of strings, madlibs_words
               Instr(13, 7, 4, 0, 10),    ## Step0  #13: Assign idx4 of idx 7(madlibs) to idx 10(bot1)
               Instr(5, 10, " ", 0, 11),  ## Step1  #5: Compare idx 10(bot1) == " " and assign result to idx 11(bot2)
               Instr(8, 11, 1, 5, 0),     ## Step2  #8: Cond jump to +1/+5 if true/false
               
               Instr(10, 7, 5, 4, 12),    ## Step3  #10: Assign idx 5 to 4 of idx 7 to idx 12 (bot3)
               Instr(14, 12, 0, 0, 0),     ## Step4  #14: Append idx12 to idx 0 (madlibs_words)
               Instr(2, 4, 0, 0, 5),       ## Step5  #2: Assign idx 4 (index i) to idx 5 (idx-k)
               Instr(3, 1, 0, 0, 5),      ## Step6  #3: add 1 to idx 5 (idx-k)
               
               Instr(3, 1, 0, 0, 4),      ## Step7  #3: add 1 to idx 4 (idx-i)
               
               Instr(5, 4, mad_len, 2, 10), ## Step8  #5: Check if idx 4 (idx-i) < madlibs_len, and assign result to idx 10(bot1)
               Instr(8, 10, -9, 1, 0),    ## Step9 #8: jump to next or back to beginning
               
               Instr(12, 7, -1, 0, 11),   ## Step10 #12 take last elem of idx 7(madlibs) into idx 11(bot2)
               Instr(5, 11, " ", 1, 12),  ## Step11 #5 Compare idx11(bot2) == " " and assign res to idx 12(bot3)

               Instr(11, 7, 5, 0, 12),    ## Step12 #11: Assign idx 5 till end of idx 7(madlibs) to idx 12 (bot4)
               Instr(14, 12, 0, 0, 0),    ## Step13 #14: Append idx22 to idx 0

               Instr(1, 0, 0, 0, 4),      ## Step14 #1: Set index i to 0
               Instr(1, 0, 0, 0, 5),      ## Step15 #1: Set index k to 0


               # Assigning hard-coded nouns 1 and 2 to idx6 (fill)
               Instr(12, 8, 3, 0, 10),    ## Step16 #12: Set index 3 of idx8 (nouns) to idx 10 (bot1)
               Instr(14, 10, 0, 0, 6),     ## Step17 #14: Append hard-coded noun1/2, idx 10(bot1), to idx 6(fill)
               Instr(12, 8, 4, 0, 10),    ## Step18 #12: Set index 4 of idx8 (nouns) to idx 10 (bot1)
               Instr(14, 10, 0, 0, 6),     ## Step19 #14: Append hard-coded noun2/2, idx 10(bot1), to idx 6(fill)

               # Split X into a list of strings, X_words
               Instr(13, 9, 4, 0, 10), #Step20  #13: Assign idx4 of idx 9 (X) to idx 10(bot1)
               Instr(5, 10, " ", 0, 11), #Step21  #5: Compare idx 10(bot1) and ()" ") and assign result to idx 11(bot2)
               Instr(8, 11, 1, 5, 0), #Step22  #8: Cond jump to +1/+5 if true/false

               Instr(10, 9, 5, 4, 12), #Step23  #10: Assign idx k/5 to i/4 of idx 9 (X) to idx 12 (bot3)
               Instr(14, 12, 0, 0, 1), #Step24  #14: append idx12 (bot3) to idx 1 (X_words)
               Instr(2, 4, 0, 0, 5), #Step25  #2: Assign idx 4 (index i) to idx 5
               Instr(3, 1, 0, 0, 5), #Step26  #3: add 1 to idx 5

               Instr(3, 1, 0, 0, 4), #Step27  #3: add 1 to idx 4

               Instr(5, 4, X_len, 2, 10), #Step28  #5: Compare idx 4 (idx-i) < len(X) and assign result to idx 10(bot1)
               Instr(8, 10, -9, 1, 0), #Step30 #29: cond jump to next or start from the beginning of this block (-9)
               Instr(12, 9, -1, 0, 11),  #Step30 #12 take last elem of idx9 (X) into idx 11(bot2)
               Instr(5, 11, " ", 1, 12), #Step31 #5 Compare idx11(bot2) and (" ") to check inequality, assign it to idx 12(bot3)
               Instr(8, 12, 1, 3, 0),    #Step32 #8: Cond jump to +1/+3 if true/false

               Instr(11, 9, 5, 0, 12),   #Step33 #11: Assign idx 5 till end of idx 9(X) to idx 12 (bot3)
               Instr(14, 12, 0, 0, 1),     #Step34 #14: append idx22 to idx 1 (X_words)

               Instr(1, 0, 0, 0, 4),      ## Step35 #1: Set index i to 0
               Instr(1, 0, 0, 0, 5),      ## Step36 #1: Set index k to 0
  

               # Take the first three nouns from X and hard-code the rest from the fill list
               ## FIRST IF curr madlibs_words is equal to "_"
               Instr(13, 0, 4, 0, 10), #Step37  #13: Assign idx4 (idx-i) of idx 0 (madlibs_words) to idx 10(bot1)
               Instr(5, 10, "_", 0, 11), #Step38  #5: Compare idx 10(bot1) and "_" and assign result to idx 11(bot2)
               Instr(8, 11, 1, 8, 0), #Step39  #8: Cond jump to +1/+8 if true/false

               ## SECOND IF index of madlibs_words is less than 10 (idx of third fill)
               Instr(5, 4, 10, 2, 12), #Step40  #5: Compare idx 4(idx-i) < 10 and assign result to idx 12(bot3)
               Instr(8, 12, 1, 3, 0), #Step41  #8: Cond jump to +1/+3 if true/false

               ## IF Both TRUE (Append from X_Words)
               Instr(13, 1, 4, 0, 13), #Step42  #13: Assign idx4 (idx-i) of idx 1 (X_words) to idx 13(bot4)
               Instr(7, 5, 0, 0, 0), #Step43  #7: jump to +5

               ## IF only the former TRUE (Append from fill/consts)
               Instr(13, 6, 5, 0, 13), #Step44  #13: Assign idx5 (idx-k) of idx 6 (fill) to idx 13(bot4)
               Instr(3, 1, 0, 0, 5), #Step45  #3: add 1 to idx 5 (idx-k)
               Instr(7, 2, 0, 0, 0), #Step46  #7: jump to +2

               ## ELSE (Append from madlibs_words)
               Instr(13, 0, 4, 0, 13), #Step47  #13: Assign idx4 (idx-i) of idx 0 (madlibs_words) to idx 13(bot4)

               ## APPEND and INCREMENT
               Instr(14, 13, 0, 0, 2), #Step48  #14: append idx13 (bot4) to idx2 (assembled_list)
               Instr(3, 1, 0, 0, 4), #Step49  #3: add 1 to idx 4
                
               ## CHECK IF ITERATE OR NEXT
               Instr(9, 1, 0, 0, 10), #Step50  #9: Measure a length of index1(X_words) and assign it to idx 10(bot1)
               Instr(6, 4, 10, 2, 11), #Step51  #6: Compare idx 4(idx-i) < idx 10(bot1) and assign result to idx 11(bot2)
               Instr(8, 11, -15, 1, 0), #Step52  #8: Cond jump to -15/+1 if true/false

               Instr(1, 0, 0, 0, 4),    ## Step53 #1: Set index i to 0


               # Stringify the list
               Instr(5, 4, 0, 0, 10), #Step54  #5: Compare current index (idx 4) == 0 and assign result to idx 10(bot1)
               Instr(8, 10, 1, 4, 0), #Step55  #8: Cond jump to +1/+4 if true/false

               ## IF TRUE
               Instr(1, 0, 0, 0, 11), #Step56  #1: Assign 0 to idx 11(bot2)
               Instr(13, 2, 11, 0, 3), #Step57  #13: Take idx11(bot2) of idx2(assembled_list) and assign it to des(3:res)
               Instr(1, 1, 0, 0, 4), #Step58  #1: Assign 1 to idx 4(idx-i)
               
               ## ELSE
               Instr(13, 2, 4, 0, 12), #Step59  #13: Take idx 4(idx-i) of idx2(assembled_list) and assign it to idx12(bot2)
               Instr(3, " ", 0, 0, 3), #Step60  #3: add " " to des(3:res)
               Instr(4, 12, 0, 0, 3), #Step61  #4: add idx12(bot2) to des(3:res)
               Instr(3, 1, 0, 0, 4), #Step62  #3: add +1 to idx4 (index-i)
            
               Instr(9, 2, 0, 0, 10), #Step63  #9: Measure a length of index2 (assembled_list) and assign it to idx 10(bot1)
               Instr(6, 4, 10, 2, 11), #Step64  #6: Compare idx 4(idx-i) < idx 10(bot1) and assign result to idx 11(bot2)
               Instr(8, 11, -11, 1, 0), #Step65  #8: Cond jump to -11/+1 if true/false
               
               Instr(-1, 0, 0, 0, 0),    ## Step66 #-1: Terminal
              ]

    pro_prog = make_program(program)
    
    pc = 0

    for i in range(n_iter): #TODO: FIXME un-hard-code (Step 3, 4, 5, 6) +47*8+58+15+14
        pc = step(pro_prog, pc, mem)

    prod_Y = mem[3]
    print('prod_Y: ', prod_Y)
    print('')
    assert("I have a dog and cat , and every day I walk her to the park" == prod_Y)


    # Reproducer
    madlibs_words = [] #0
    X_words = [] #1
    assembled_list = [] #2
    result = "" #3
    i = 0 #4
    k = 0 #5
    fill = [] #6
    madlibs = madlibs #7
    nouns = nouns #8
    X = None #9 Not available for reproducer
    bot1 = None #10
    bot2 = None #11
    bot3 = None #12
    bot4 = None #13

    repro_mem = [madlibs_words, X_words, assembled_list, result, i, k, fill,
           madlibs, nouns, X, bot1, bot2, bot3, bot4]
    
    program = [
               #  Split madlibs into a list of strings (madlibs_words)
               Instr(13, 7, 4, 0, 10),    ## Step0  #13: Assign idx4 of idx 7(madlibs) to idx 10(bot1)
               Instr(5, 10, " ", 0, 11),  ## Step1  #5: Compare idx 10(bot1) and idx 13 and assign result to idx 11(bot2)
               Instr(8, 11, 1, 5, 0),     ## Step2  #8: Cond jump to +1/+5 if true/false
               
               Instr(10, 7, 5, 4, 12),    ## Step3  #10: Assign idx 5 to 4 of idx 7 (madlibs) to idx 12 (bot3)
               Instr(14, 12, 0, 0, 0),      ## Step4  #14: append idx12 to idx 0 (madlibs_words)
               Instr(2, 4, 0, 0, 5),       ## Step5  #2: Assign idx 4 (index i) to idx 5 (idx-k)
               Instr(3, 1, 0, 0, 5),      ## Step6  #3: add 1 to idx 5 (idx-k)
               
               Instr(3, 1, 0, 0, 4),      ## Step7  #3: add 1 to idx 4 (idx-i)
               
               Instr(5, 4, mad_len, 2, 10), ## Step8  #5: Check if idx 4 (idx-i) < madlibs_len, and assign result to idx 10(bot1)
               Instr(8, 10, -9, 1, 0),    ## Step9 #8: jump to next or back to beginning
               
               Instr(12, 7, -1, 0, 11),   ## Step10 #12: take last elem of idx 7(madlibs) into idx 11(bot2)
               Instr(5, 11, " ", 1, 12),  ## Step11 #5: Compare idx13 (" ") and idx11(bot2) to check non-equality, assign it to idx 12(bot3)

               Instr(11, 7, 5, 0, 12),    ## Step12 #11: Assign idx 5 till end of idx 7(madlibs) to idx 12 (bot4)
               Instr(14, 12, 0, 0, 0),    ## Step13 #14: append idx12 to idx 0

               Instr(1, 0, 0, 0, 4),      ## Step14 #1: Set index i to 0
               Instr(1, 0, 0, 0, 5),      ## Step15 #1: Set index k to 0


               # Append hard-coded nouns 1 - 5
               Instr(12, 8, 0, 0, 10),  ## Step17 #12: Set index 0 of idx8 (nouns) to 10 (bot1)
               Instr(14, 10, 0, 0, 6),   ## Step18 #14: Append hard-coded noun1/5 to fill
               Instr(12, 8, 1, 0, 10),  ## Step19 #12: Set index 1 of idx8 (nouns) to 10 (bot1)
               Instr(14, 10, 0, 0, 6),   ## Step20 #14: Append hard-coded noun2/5 to fill
               Instr(12, 8, 2, 0, 10),  ## Step21 #12: Set index 2 of idx8 (nouns) to 10 (bot1)
               Instr(14, 10, 0, 0, 6),   ## Step22 #14: Append hard-coded noun3/5 to fill
               Instr(12, 8, 3, 0, 10),  ## Step23 #12: Set index 3 of idx8 (nouns) to 10 (bot1)
               Instr(14, 10, 0, 0, 6),   ## Step24 #14: Append hard-coded noun4/5 to fill
               Instr(12, 8, 4, 0, 10),  ## Step25 #12: Set index 4 of idx8 (nouns) to 10 (bot1)
               Instr(14, 10, 0, 0, 6),   ## Step26 #14: Append hard-coded noun5/5 to fill


               # Hard-Code all blanks from the nouns list
               ## IF curr madlibs_words is equal to "_"
               Instr(13, 0, 4, 0, 10), #Step27  #13: Assign idx4 (idx-i) of idx 0 (madlibs_words) to idx 10(bot1)
               Instr(5, 10, "_", 0, 11), #Step28  #5: Compare idx 20(bot1) and "_" and assign result to idx 11(bot2)
               Instr(8, 11, 1, 4, 0), #Step29  #8: Cond jump to +1/+4 if true/false

               ## IF TRUE append fill[idx-k] to assembled_list
               Instr(13, 6, 5, 0, 12), #Step30  #13: Assign idx5 (idx-k) of idx 6 (fill) to idx 12(bot3)
               Instr(3, 1, 0, 0, 5), #Step31  #3: add 1 to idx 5 (idx-k)
               Instr(7, 2, 0, 0, 0), #Step32  #7: jump to +2

               ## ELSE append fill[idx-k] to assembled_list
               Instr(13, 0, 4, 0, 12), #Step33  #13: Assign idx4 (idx-i) of idx 0 (madlibs_words) to idx 12(bot3)
                
               ## Append ops & Increment
               Instr(14, 12, 0, 0, 2), #Step34  #14: append idx 12(bot3) to idx 2 (assembled_list)
               Instr(3, 1, 0, 0, 4), #Step35  #3: add 1 to idx 4 (idx-i)
                
               Instr(9, 0, 0, 0, 10), #Step36  #9: Measure a length of index0 (madlibs_words) and assign it to idx 10(bot1)
               Instr(6, 4, 10, 2, 11), #Step37  #6: Compare idx 4(idx-i) < idx 10(bot1) and assign result to idx 11(bot2)
               Instr(8, 11, -11, 1, 0), #Step38  #8: Cond jump to -11/+1 if true/false

               Instr(1, 0, 0, 0, 4),    # Step39 #1: Set index i to 0
               Instr(1, 0, 0, 0, 5),    # Step40 #1: Set index k to 0


               # Stringify the list
               Instr(5, 4, 0, 0, 10), #Step41  #5: Compare current index (idx 4) == 0 and assign result to idx 10(bot1)
               Instr(8, 10, 1, 4, 0), #Step42  #8: Cond jump to +1/+4 if true/false

               ##IF TRUE
               Instr(1, 0, 0, 0, 11), #Step43  #1: Assign 0 to idx 11(bot2)
               Instr(13, 2, 11, 0, 3), #Step44  #13: Take idx11(bot2) of idx2(assembled_list) and assign it to des(3:res)
               Instr(1, 1, 0, 0, 4), #Step45  #1: Assign 1 to idx 4(idx-i)
                
               Instr(13, 2, 4, 0, 12), #Step46  #13: Take idx 4(idx-i) of idx2(assembled_list) and assign it to idx12(bot2)
               Instr(3, " ", 0, 0, 3), #Step47  #3: add " " to des(3:res)
               Instr(4, 12, 0, 0, 3), #Step48  #4: add idx12(bot2) to des(3:res)
               Instr(3, 1, 0, 0, 4), #Step49  #3: add +1 to idx4 (index-i)
            
               Instr(9, 2, 0, 0, 10), #Step50  #9: Measure a length of index2 (assembled_list) and assign it to idx 10(bot1)
               Instr(6, 4, 10, 2, 11), #Step51  #6: Compare idx 4(idx-i) < idx 10(bot1) and assign result to idx 11(bot2)
               Instr(8, 11, -11, 1, 0), #Step52  #8: Cond jump to -11/+1 if true/false
               
               Instr(-1, 0, 0, 0, 0),    ## Step53 #-1: Terminal
              ]
    repro_prog = make_program(program)

    pc = 0

    for i in range(n_iter):
        pc = step(repro_prog, pc, repro_mem)

    reprod_Y = repro_mem[3]
    print('reprod_Y: ', reprod_Y)
    print('')
    assert("I have a dog and cat , and every day I walk her to the park" == reprod_Y)


if __name__ == "__main__":
    main()