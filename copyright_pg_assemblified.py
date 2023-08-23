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

    ''' mem: 
            0: madlibs_words
            1: X_words
            2: assembled_list
            3: result
            4: i (index for for-loop)
            5: k (index for inner for-loop)
            6: madlibs_len (length of string by char)
            7: first
            8: second
            9: third
            10: fourth
            11: fifth
            12: fill
            13: " "
            14: X_len
            15: zero (= 0)
            16: underscore = "_"
            17: madlibs
            18: nouns
            19: X
            20: bot1
            21: bot2
            22: bot3
            23: bot4
    '''
    #TODO: uncomment with PicoZKCompiler('picozk_test', options=['ram']):

    # Producer
    madlibs_words = [] #0
    X_words = [] #1
    assembled_list = [] #2
    result = "" #3
    i = 0 #4
    k = 0 #5
    madlibs_len = len(madlibs) #6
    first = 3 #7
    second = 4 #8
    third = None #9
    fourth = None #10
    fifth = None #11
    fill = [] #12
    blank = None #13 TODO: Delete 
    X_len = len(X) #14
    zero = 0 #15 TODO: Delete
    underscore ="_" #16 TODO: Delete after ops5 modified
    madlibs = madlibs #17
    nouns = nouns #18 
    X = X #19
    bot1 = None #20
    bot2 = None #21
    bot3 = None #22
    bot4 = None #23

    mem = [madlibs_words, X_words, assembled_list, result, i, k, madlibs_len,
           first, second, third, fourth, fifth, fill, blank, X_len, zero, underscore, 
           madlibs, nouns, X, bot1, bot2, bot3, bot4]
        
    program = [ 
               #  Split madlibs into a list of strings, madlibs_words
               Instr(13, 17, 4, 0, 20),    ## Step0  #13: Assign idx4 of idx 17 (madlibs) to idx 20(bot1)
               Instr(5, 20, " ", 0, 21),  ## Step1  #5: Compare idx 20(bot1) and idx 13 and assign result to idx 21(bot2)
               Instr(8, 21, 1, 5, 0),     ## Step2  #8: Cond jump to +1/+5 if true/false
               
               Instr(10, 17, 5, 4, 22),    ## Step3  #10: Assign idx 5 to 4 of idx 17 to idx 22 (bot 3)
               Instr(14, 22, 0, 0, 0),      ## Step4  #14: append idx22 to idx 0
               Instr(2, 4, 0, 0, 5),       ## Step5  #2: Assign idx 4 (index i) to idx 5 (idx-k)
               Instr(3, 1, 0, 0, 5),      ## Step6  #3: add 1 to idx 5 (idx-k)
               
               Instr(3, 1, 0, 0, 4),      ## Step7  #3: add 1 to idx 4 (idx-i)
               
               Instr(5, 4, madlibs_len, 2, 20), ## Step8  #5: Check if idx 4 (idx-i) < madlibs_len, and assign result to idx 20(bot1)
               Instr(8, 20, -9, 1, 0),    ## Step9 #8: jump to next or back to beginning
               
               Instr(12, 17, -1, 0, 21),   ## Step10 #12 take last elem of idx 17(madlibs) into idx 21(bot2)
               Instr(5, 21, " ", 1, 22),  ## Step11 #5 Compare idx13 (" ") and idx21(bot2) to check non-equality, assign it to idx 22(bot3)

               Instr(11, 17, 5, 0, 22),    ## Step12 #11: Assign idx 5 till end of idx 17(madlibs) to idx 22 (bot 4)
               Instr(14, 22, 0, 0, 0),      ## Step13 #14: append idx22 to idx 0

               Instr(1, 0, 0, 0, 4),      ## Step14 #1: Set index i to 0
               Instr(1, 0, 0, 0, 5),      ## Step15 #1: Set index k to 0


               # Assigning hard-coded nouns 1 and 2
               Instr(12, 18, 3, 0, 20),    ## Step16 #12: Set index 3 of nouns to idx 20 (bot1)
               Instr(14, 20, 0, 0, 12),     ## Step17 #14: Append hard-coded noun1/2, idx 20(bot1)
               Instr(12, 18, 4, 0, 20),    ## Step18 #12: Set index 4 of nouns to idx 20 (bot1)
               Instr(14, 20, 0, 0, 12),     ## Step19 #14: Append hard-coded noun2/2, idx 20(bot1)

               # Split X into a list of strings, X_words
               Instr(13, 19, 4, 0, 20), #Step20  #13: Assign idx4 of idx 19 (X) to idx 20(bot1)
               Instr(5, 20, " ", 0, 21), #Step21  #5: Compare idx 21(bot2) and ()" ") and assign result to idx 21(bot2)
               Instr(8, 21, 1, 5, 0), #Step22  #8: Cond jump to +1/+5 if true/false

               Instr(10, 19, 5, 4, 22), #Step23  #10: Assign idx k/5 to i/4 of idx 19 (X) to idx 22 (bot 3)
               Instr(14, 22, 0, 0, 1), #Step24  #14: append idx22 to idx 1 (X_words)
               Instr(2, 4, 0, 0, 5), #Step25  #2: Assign idx 4 (index i) to idx 5
               Instr(3, 1, 0, 0, 5), #Step26  #3: add 1 to idx 5

               Instr(3, 1, 0, 0, 4), #Step27  #3: add 1 to idx 4

               Instr(6, 4, 14, 2, 20), #Step28  #6: Compare idx 4 and idx 6 and assign result to idx 20(bot1)
               Instr(8, 20, -9, 1, 0), #Step29 #8: cond jump to next or start from the beginning of this block (-9)
               Instr(12, 19, -1, 0, 21),  #Step30 #12 take last elem of idx 19 into idx 21(bot2)
               Instr(5, 21, " ", 1, 22), #Step31 #5 Compare idx21(bot2) and (" ") to check inequality, assign it to idx 22(bot3)
               Instr(8, 22, 1, 3, 0),    #Step32 #8: Cond jump to +1/+3 if true/false

               Instr(11, 19, 5, 0, 22),   #Step33 #11: Assign idx 5 till end of idx 19(X) to idx 22 (bot 4)
               Instr(14, 22, 0, 0, 1),     #Step34 #14: append idx22 to idx 1 (X_words)

               Instr(1, 0, 0, 0, 4),      ## Step35 #1: Set index i to 0
               Instr(1, 0, 0, 0, 5),      ## Step36 #1: Set index k to 0
  

               # Take the first three nouns from X and hard-code the rest from the nouns list
               ## FIRST IF curr madlibs_words is equal to "_"
               Instr(13, 0, 4, 0, 20), #Step37  #13: Assign idx4 (idx-i) of idx 0 (madlibs_words) to idx 20(bot1)
               Instr(5, 20, "_", 0, 21), #Step38  #5: Compare idx 20(bot1) and "_" and assign result to idx 21(bot2)
               Instr(8, 21, 1, 8, 0), #Step39  #8: Cond jump to +1/+8 if true/false

               ## SECOND IF index of madlibs_words is less than 10 (idx of third fill)
               Instr(5, 4, 10, 2, 22), #Step40  #5: Compare idx 4(idx-i) < 10 and assign result to idx 22(bot3)
               Instr(8, 22, 1, 3, 0), #Step41  #8: Cond jump to +1/+3 if true/false

               ## IF Both TRUE (Append from X_Words)
               Instr(13, 1, 4, 0, 23), #Step42  #13: Assign idx4 (idx-i) of idx 1 (X_words) to idx 23(bot4)
               Instr(7, 5, 0, 0, 0), #Step43  #7: jump to +5

               ## IF only the former TRUE (Append from fill/consts)
               Instr(13, 12, 5, 0, 23), #Step44  #13: Assign idx5 (idx-k) of idx 12 (fill) to idx 23(bot4)
               Instr(3, 1, 0, 0, 5), #Step45  #3: add 1 to idx 5 (idx-k)
               Instr(7, 2, 0, 0, 0), #Step46  #7: jump to +2

               ## ELSE (Append from madlibs_words)
               Instr(13, 0, 4, 0, 23), #Step47  #13: Assign idx4 (idx-i) of idx 0 (madlibs_words) to idx 23(bot4)

               ## APPEND and INCREMENT
               Instr(14, 23, 0, 0, 2), #Step48  #14: append idx23(bot4) to idx 2 (X_words)
               Instr(3, 1, 0, 0, 4), #Step49  #3: add 1 to idx 4
                
               ## CHECK IF ITERATE OR NEXT
               Instr(9, 1, 0, 0, 20), #Step50  #9: Measure a length of index1(X_words) and assign it to idx 20(bot1)
               Instr(6, 4, 20, 2, 21), #Step51  #6: Compare idx 4(idx-i) < idx 20(bot1) and assign result to idx 21(bot2)
               Instr(8, 21, -15, 1, 0), #Step52  #8: Cond jump to -15/+1 if true/false

               Instr(1, 0, 0, 0, 4),    ## Step53 #1: Set index i to 0


               # Stringify the list
               Instr(5, 4, 0, 0,  20), #Step54  #5: Compare current index (idx 4) == 0 and assign result to idx 20(bot1)
               Instr(8, 20, 1, 4, 0), #Step55  #8: Cond jump to +1/+4 if true/false

               ## IF TRUE
               Instr(1, 0, 0, 0, 21), #Step56  #1: Assign 0 to idx 21(bot2)
               Instr(13, 2, 21, 0, 3), #Step57  #13: Take idx21(bot2) of idx2(assembled_list) and assign it to des(3:res)
               Instr(1, 1, 0, 0, 4), #Step58  #1: Assign 1 to idx 4(idx-i)
                
               Instr(13, 2, 4, 0, 22), #Step59  #13: Take idx 4(idx-i) of idx2(assembled_list) and assign it to idx22(bot2)
               Instr(3, " ", 0, 0, 3), #Step60  #3: add " " to des(3:res)
               Instr(4, 22, 0, 0, 3), #Step61  #4: add idx22(bot2) to des(3:res)
               Instr(3, 1, 0, 0, 4), #Step62  #3: add +1 to idx4 (index-i)
            
               Instr(9, 2, 0, 0, 20), #Step63  #9: Measure a length of index2 (assembled_list) and assign it to idx 20(bot1)
               Instr(6, 4, 20, 2, 21), #Step64  #6: Compare idx 4(idx-i) < idx 20(bot1) and assign result to idx 21(bot2)
               Instr(8, 21, -11, 1, 0), #Step65  #8: Cond jump to -11/+1 if true/false
               
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
    madlibs_len = len(madlibs) #6 TODO: Delete
    first = 0 #7
    second = 1 #8
    third = 2 #9
    fourth = 3 #10
    fifth = 4 #11
    fill = [] #12
    blank = None #13 TODO: Delete
    X_len = None #14 TODO: Consider replacing with bot
    zero = 0 #15 TODO: Delete
    underscore ="_" #16 TODO: Delete
    madlibs = madlibs #17 
    nouns = nouns #18
    X = None #19 Not available for reproducer
    bot1 = None #20
    bot2 = None #21
    bot3 = None #22
    bot4 = None #23

    repro_mem = [madlibs_words, X_words, assembled_list, result, i, k, madlibs_len,
           first, second, third, fourth, fifth, fill, blank, X_len, zero, underscore, 
           madlibs, nouns, X, bot1, bot2, bot3, bot4]
    
    program = [
               #  Split madlibs into a list of strings, madlibs_words
               Instr(13, 17, 4, 0, 20),    ## Step0  #13: Assign idx4 of idx 17 (madlibs) to idx 20(bot1)
               Instr(5, 20, " ", 0, 21),  ## Step1  #5: Compare idx 20(bot1) and idx 13 and assign result to idx 21(bot2)
               Instr(8, 21, 1, 5, 0),     ## Step2  #8: Cond jump to +1/+5 if true/false
               
               Instr(10, 17, 5, 4, 22),    ## Step3  #10: Assign idx 5 to 4 of idx 17 to idx 22 (bot 3)
               Instr(14, 22, 0, 0, 0),      ## Step4  #14: append idx22 to idx 0
               Instr(2, 4, 0, 0, 5),       ## Step5  #2: Assign idx 4 (index i) to idx 5 (idx-k)
               Instr(3, 1, 0, 0, 5),      ## Step6  #3: add 1 to idx 5 (idx-k)
               
               Instr(3, 1, 0, 0, 4),      ## Step7  #3: add 1 to idx 4 (idx-i)
               
               Instr(5, 4, madlibs_len, 2, 20), ## Step8  #5: Check if idx 4 (idx-i) < madlibs_len, and assign result to idx 20(bot1)
               Instr(8, 20, -9, 1, 0),    ## Step9 #8: jump to next or back to beginning
               
               Instr(12, 17, -1, 0, 21),   ## Step10 #12: take last elem of idx 17(madlibs) into idx 21(bot2)
               Instr(5, 21, " ", 1, 22),  ## Step11 #5: Compare idx13 (" ") and idx21(bot2) to check non-equality, assign it to idx 22(bot3)

               Instr(11, 17, 5, 0, 22),    ## Step12 #11: Assign idx 5 till end of idx 17(madlibs) to idx 22 (bot 4)
               Instr(14, 22, 0, 0, 0),      ## Step13 #14: append idx22 to idx 0

               Instr(1, 0, 0, 0, 4),      ## Step14 #1: Set index i to 0
               Instr(1, 0, 0, 0, 5),      ## Step15 #1: Set index k to 0


               # Assigning hard-coded nouns 1 - 5
               Instr(12, 18, 0, 0, 20),  ## Step17 #12: Setting index i to 20 (bot1)
               Instr(14, 20, 0, 0, 12),   ## Step18 #14: Assigning hard-coded noun1/2
               Instr(12, 18, 1, 0, 20),  ## Step19 #12: Setting index i to 20 (bot1)
               Instr(14, 20, 0, 0, 12),   ## Step20 #14: Assigning hard-coded noun2/2
               Instr(12, 18, 2, 0, 20),  ## Step21 #12: Setting index i to 20 (bot1)
               Instr(14, 20, 0, 0, 12),   ## Step22 #14: Assigning hard-coded noun1/2
               Instr(12, 18, 3, 0, 20),  ## Step23 #12: Setting index i to 20 (bot1)
               Instr(14, 20, 0, 0, 12),   ## Step24 #14: Assigning hard-coded noun2/2
               Instr(12, 18, 4, 0, 20),  ## Step25 #12: Setting index i to 20 (bot1)
               Instr(14, 20, 0, 0, 12),   ## Step26 #14: Assigning hard-coded noun2/2


               # Hard-Code all blanks from the nouns list
               ## IF curr madlibs_words is equal to "_"
               Instr(13, 0, 4, 0, 20), #Step27  #13: Assign idx4 (idx-i) of idx 0 (madlibs_words) to idx 20(bot1)
               Instr(5, 20, "_", 0, 21), #Step28  #5: Compare idx 20(bot1) and "_" and assign result to idx 21(bot2)
               Instr(8, 21, 1, 4, 0), #Step29  #8: Cond jump to +1/+4 if true/false

               ## IF TRUE append fill[idx-k] to assembled_list
               Instr(13, 12, 5, 0, 22), #Step30  #13: Assign idx5 (idx-k) of idx 12 (fill) to idx 22(bot3)
               Instr(3, 1, 0, 0, 5), #Step31  #3: add 1 to idx 5 (idx-k)
               Instr(7, 2, 0, 0, 0), #Step32  #7: jump to +2

               ## ELSE append fill[idx-k] to assembled_list
               Instr(13, 0, 4, 0, 22), #Step33  #13: Assign idx4 (idx-i) of idx 0 (madlibs_words) to idx 22(bot3)
                
               ## Append ops & Increment
               Instr(14, 22, 0, 0, 2), #Step34  #14: append idx22(bot3) to idx 2 (assembled_list)
               Instr(3, 1, 0, 0, 4), #Step35  #3: add 1 to idx 4 (idx-i)
                
               Instr(9, 0, 0, 0, 20), #Step36  #9: Measure a length of index0 (madlibs_words) and assign it to idx 20(bot1)
               Instr(6, 4, 20, 2, 21), #Step37  #6: Compare idx 4(idx-i) < idx 20(bot1) and assign result to idx 21(bot2)
               Instr(8, 21, -11, 1, 0), #Step38  #8: Cond jump to -11/+1 if true/false   

               Instr(2, 15, 0, 0, 4),    # Step39 #2: Setting index i to 0
               Instr(2, 15, 0, 0, 5),    # Step40 #2: Setting index k to 0


               # Stringify the list
               Instr(5, 4, 0, 0, 20), #Step41  #5: Compare current index (idx 4) == 0 and assign result to idx 20(bot1)
               Instr(8, 20, 1, 4, 0), #Step42  #8: Cond jump to +1/+4 if true/false

               ##IF TRUE
               Instr(1, 0, 0, 0, 21), #Step43  #1: Assign 0 to idx 21(bot2)
               Instr(13, 2, 21, 0, 3), #Step44  #13: Take idx21(bot2) of idx2(assembled_list) and assign it to des(3:res)
               Instr(1, 1, 0, 0, 4), #Step45  #1: Assign 1 to idx 4(idx-i)
                
               Instr(13, 2, 4, 0, 22), #Step46  #13: Take idx 4(idx-i) of idx2(assembled_list) and assign it to idx22(bot2)
               Instr(3, " ", 0, 0, 3), #Step47  #3: add " " to des(3:res)
               Instr(4, 22, 0, 0, 3), #Step48  #4: add idx22(bot2) to des(3:res)
               Instr(3, 1, 0, 0, 4), #Step49  #3: add +1 to idx4 (index-i)
            
               Instr(9, 2, 0, 0, 20), #Step50  #9: Measure a length of index2 (assembled_list) and assign it to idx 20(bot1)
               Instr(6, 4, 20, 2, 21), #Step51  #6: Compare idx 4(idx-i) < idx 20(bot1) and assign result to idx 21(bot2)
               Instr(8, 21, -11, 1, 0), #Step52  #8: Cond jump to -11/+1 if true/false
               
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