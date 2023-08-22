from typing import List

# Class to hold a single instruction TODO: @dataclass
class Instr:
    def __init__(self, opcode: int, src1: int, src2: int, src3: int, src4: int, src5: int, src6: int, dest: int):
        self.opcode = opcode
        self.src1 = src1
        self.src2 = src2
        self.src3 = src3
        self.src4 = src4
        self.src5 = src5
        self.src6 = src6
        self.dest = dest


# Class to hold a program as multiple lists of instructions TODO: @dataclass
class Program:
    def __init__(self, opcode: List[int], src1: List[int], src2: List[int], src3: List[int], src4: List[int], src5: List[int], src6: List[int], dest: List[int]):
        self.opcode: List[int] = opcode
        self.src1: List[int] = src1
        self.src2: List[int] = src2
        self.src3: List[int] = src3
        self.src4: List[int] = src4
        self.src5: List[int] = src5
        self.src6: List[int] = src6
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
    p4 = instr.src4
    p5 = instr.src5
    p6 = instr.src6
    des = instr.dest
    new_pc = pc

    # 3. Split madlibs into a list of strings, madlibs_words
    if instr.opcode == 3:

        '''
            des:0
            p2:4 index-i
            p3:5 index-k
            p4:6 madlibs_len
            p5:13 (= " ")
            p6:17 madlibs
        '''

        # Instr(17, 17, 4, 0, 0, 0, 0, 20),    ## Step0  #17: Assign idx4 of idx 17 (madlibs) to idx 20(bot1)
        # Instr(14, 20, " ", 0, 0, 0, 0, 21),   ## Step1  #14: Compare idx 20(bot1) and " " and assign result to idx 21(bot2)
        # Instr(20, 21, 1, 5, 0, 0, 0, 0),     ## Step2  #20: Cond jump to +1/+5 if true/false
        
        # Instr(11, 17, 5, 4, 0, 0, 0, 22),    ## Step3  #11: Assign idx 5 to 4 of idx 17 to idx 22 (bot 3)
        # Instr(8, 22, 0, 0, 0, 0, 0, 0),      ## Step4  #8: append idx22 to idx 0 (madlibs_words)
        # Instr(9, 4, 0, 0, 0, 0, 0, 5),       ## Step5  #9: Assign idx 4 (index i) to idx 5 (idx-k)
        # Instr(15, 1, 0, 0, 0, 0, 0, 5),      ## Step6  #15: add 1 to idx 5 (idx-k)
        
        # Instr(15, 1, 0, 0, 0, 0, 0, 4),      ## Step7  #15: add 1 to idx 4 (idx-i)

        if mem[p6][mem[p2]] == mem[p5]:
            mem[des].append(mem[p6][mem[p3]:mem[p2]])
            mem[p3] = mem[p2] + 1
        mem[p2] += 1

        # Instr(13, 4, 6, 2, 0, 0, 0, 20),     ## Step8  #13: Check if idx 4 (idx-i) < idx 6 (madlibs_len), and assign result to idx 20(bot1)
        # Instr(20, 20, -9, 1, 0, 0, 0, 0),    ## Step9 #20: jump to next or back to beginning

        if mem[p2] < mem[p4]:
            return new_pc
        else: 

            # Instr(18, 17, -1, 0, 0, 0, 0, 21),   ## Step10 #18 take last elem of idx 17(madlibs) into idx 21(bot2)
            # Instr(14, 21, " ", 1, 0, 0, 0, 22),  ## Step11 #14 Compare idx13 (" ") and idx21(bot2) to check inequality, assign it to idx 22(bot3)
            # Instr(20, 22, 1, 3, 0, 0, 0, 0),     ## Step12 #19: Cond jump to +1/+3 if true/false
            # Instr(12, 17, 5, 0, 0, 0, 0, 22),    ## Step13 #12: Assign idx 5 till end of idx 17(madlibs) to idx 22 (bot 4)
            # Instr(8, 22, 0, 0, 0, 0, 0, 0),      ## Step14 #8: append idx22 to idx 0(madlibs_words)

            if mem[p6][-1] != mem[p5]:
                mem[des].append(mem[p6][mem[p3]:])
            return new_pc + 1 

    
    # 4. Split X into a list of strings, X_words
    if instr.opcode == 4:

        '''
            des:1
            p2: 4 index-i
            p3: 5 index-k
            p4: 14 X_len
            p5: 13 (= " ")
            p6: 19 X
        '''
        # Instr(17, 19, 4, 0, 0, 0, 0, 20), #Step0  #17: Assign idx4 of idx 19 (X) to idx 20(bot1)
        # Instr(14, 20, " ", 0, 0, 0, 0, 21), #Step1  #13: Compare idx 21(bot2) and idx 13 and assign result to idx 21(bot2)
        # Instr(20, 21, 1, 5, 0, 0, 0, 0), #Step2  #20: Cond jump to +1/+5 if true/false

        # Instr(11, 19, 5, 4, 0, 0, 0, 22), #Step3  #11: Assign idx k/5 to i/4 of idx 17 (X) to idx 22 (bot 3)
        # Instr(8, 22, 0, 0, 0, 0, 0, 1), #Step4  #8: append idx22 to idx 1 (X_words)
        # Instr(9, 4, 0, 0, 0, 0, 0, 5), #Step5  #9: Assign idx 4 (index i) to idx 5
        # Instr(15, 1, 0, 0, 0, 0, 0, 5), #Step6  #15: add 1 to idx 5

        # Instr(15, 1, 0, 0, 0, 0, 0, 4), #Step7  #15: add 1 to idx 4

        if mem[p6][mem[p2]] == mem[p5]:
            mem[des].append(mem[p6][mem[p3]:mem[p2]])
            mem[p3] = mem[p2] + 1
        mem[p2] += 1

        # Instr(13, 4, 14, 2, 0, 0, 0, 20), #Step8  #13: Compare idx 4 and idx 6 and assign result to idx 20(bot1)
        # Instr(20, 20, -9, 1, 0, 0, 0, 0), #Step9 #20: cond jump to next or start from the beginning of this block (-9)

        if mem[p2] < mem[p4]:
            return new_pc

        # Instr(18, 19, -1, 0, 0, 0, 0, 21),  #Step10 #18 take last elem of idx 19 into idx 21(bot2)
        # Instr(14, 21, " ", 1, 0, 0, 0, 22), #Step11 #14 Compare idx13 (" ") and idx21(bot2) to check inequality, assign it to idx 22(bot3)
        # Instr(20, 22, 1, 3, 0, 0, 0, 0),    #Step12 #20: Cond jump to +1/+3 if true/false

        # Instr(12, 19, 5, 0, 0, 0, 0, 22),   #Step13 #12: Assign idx 5 till end of idx 19(X) to idx 22 (bot 4)
        # Instr(8, 22, 0, 0, 0, 0, 0, 1),     #Step14 #8: append idx22 to idx 1 (X_words)

        else: 
            if mem[p6][-1] != mem[p5]:
                mem[des].append(mem[p6][mem[p3]:])
            return new_pc + 1 

    # 5. Take the first three nouns from X and hard-code the rest from the nouns list
    elif instr.opcode == 5:

        '''
            des:2
            p1:0 (madlibs_words)
            p2:1 X_words
            p3:4 index-i
            p4:5 index-k
            p5:12 fill
            p6:16 underscore
        '''

        madlibs_words_len = len(mem[p1])
        
        if mem[p1][mem[p3]] == mem[p6] and mem[p3] < 10:
            mem[des].append(mem[p2][mem[p3]])
        elif mem[p1][mem[p3]] == mem[p6]:
            mem[des].append(mem[p5][mem[p4]])
            mem[p4] += 1
        else:
            mem[des].append(mem[p1][mem[p3]])
        mem[p3] += 1

        if mem[p3] < madlibs_words_len:
            return new_pc
        else:
            return new_pc + 1


    # 6. Stringify the list
    elif instr.opcode == 6:

        '''
            des:3
            p1: 2 assembled_list
            p2:4 index-i
        '''

        if not mem[p1]:
            return ""
        result_len = len(mem[p1]) #TODO: make a command for measuring size
        
        if mem[p2] == 0:
            mem[des] = mem[p1][0]
            mem[p2] = 1
        mem[des] += " " + mem[p1][mem[p2]]
        mem[p2] += 1
    
        if mem[p2] < result_len:
            return new_pc
        else:
            return new_pc + 1


    # 7. Hard-Code all blanks from the nouns list
    elif instr.opcode == 7:

        '''
            des:2
            p1:4 index-i
            p2: 5 index-k
            p3: 0 madlibs_words
            p4:mem[12]
            p5: mem[16]
        '''

        assembled_size = len(mem[0])

        if mem[p3][mem[p1]] == mem[p5]:
            mem[des].append(mem[p4][mem[p2]])
            mem[p2] += 1
        else:
            mem[des].append(mem[p3][mem[p1]])
        mem[p1] += 1
        
        if mem[p1] < assembled_size:
            return new_pc
        else:
            return new_pc + 1
        

    # 8. Append Value
    elif instr.opcode == 8:

        '''
            des:target memory address
            p1: any index
        '''

        mem[des].append(mem[p1])
        return new_pc + 1


    # 9. Set a value to dest
    elif instr.opcode == 9:

        '''
            des:depends
            p1:any index
        '''

        mem[des] = mem[p1]

        return new_pc + 1


    # 10. Assign a const to dest
    elif instr.opcode == 10:

        '''
            des:depends
            p1:any const
        '''

        mem[des] = p1

        return new_pc + 1


    # 11. access more than one index in list
    elif instr.opcode == 11:

        '''
            des:target
            p1: index of origin
            p2: beginning index of nested list of origin
            p3: end index of nested list of origin
        '''
        mem[des] = mem[p1][mem[p2]:mem[p3]]

        return new_pc + 1


    # 12. access more than one index till end of list
    elif instr.opcode == 12:

        '''
            des:target
            p1: index of origin
            p2: beginning index of nested list of origin
        '''

        mem[des] = mem[p1][mem[p2]:]

        return new_pc + 1


    # 13. compare values in two indexes
    elif instr.opcode == 13:

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


    # 14. compare value in one index with const
    elif instr.opcode == 14:

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
    

    # 15. add const
    elif instr.opcode == 15:

        '''
            des: target
            p1: increment by
        '''
        mem[des] += p1
        
        return new_pc + 1


    # 16. Set a const to dest
    elif instr.opcode == 16:

        '''
            des:depends
            p1:any const value
        '''

        mem[des] = p1

        return new_pc + 1
    

    # 17. Access nested list by pointer
    elif instr.opcode == 17:

        '''
            des:target
            p1: index of list
            p2: pointer in memory
        '''

        mem[des] = mem[p1][mem[p2]]

        return new_pc + 1
    

    # 18. Access nested list by constant
    elif instr.opcode == 18:

        '''
            des:target
            p1: index of list
            p2: constant/pointer
        '''

        mem[des] = mem[p1][p2]

        return new_pc + 1
    

    # 19. jump
    elif instr.opcode == 19:

        '''
            p1: next pc
        '''

        return new_pc + p1

            
    # 20. cond jump
    elif instr.opcode == 20:

        '''
            p1: condition
            p2: pc shift if True
            p3: pc shift if False
        '''
        
        if mem[p1]==True:
            return new_pc + p2
        else:
            return new_pc + p3
            
    
    # 21. terminal
    elif instr.opcode == 21:

        return new_pc        


def make_program(prog): #TODO: ZKListify
    length = len(prog)
    opcode = [0 for _ in range(length)]
    src1 = [0 for _ in range(length)]
    src2 = [0 for _ in range(length)]
    src3 = [0 for _ in range(length)]
    src4 = [0 for _ in range(length)]
    src5 = [0 for _ in range(length)]
    src6 = [0 for _ in range(length)]
    dest = [0 for _ in range(length)]

    for i, instr in enumerate(prog):
        opcode[i] = instr.opcode
        src1[i] = instr.src1
        src2[i] = instr.src2
        src3[i] = instr.src3
        src4[i] = instr.src4
        src5[i] = instr.src5
        src6[i] = instr.src6
        dest[i] = instr.dest

    return Program(opcode, src1, src2, src3, src4, src5, src6,dest)


# Fetch an instruction from a program
def fetch(prog: Program, pc: int): #TODO: change int to SecretInt
    return Instr(prog.opcode[pc],
                 prog.src1[pc],
                 prog.src2[pc],
                 prog.src3[pc],
                 prog.src4[pc],
                 prog.src5[pc],
                 prog.src6[pc],
                 prog.dest[pc])

def main():
    # The Mad Libs template
    madlibs = "I have a _ and _ , and every _ I walk _ to the _"

    # The list of potential fill-ins
    nouns = ['dog', 'cat', 'day', 'her', 'park', 'ball', 'cat', 'school', 'like', 'hour', 'tree', 'car', 'house', 'week', 'shoe', 'beach']

    X = make_X(madlibs, nouns)
    print('X: ', X)
    print('')
    n_iter = 1000 #361

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
    blank = " " #13 TODO: Delete after ops4 modified
    X_len = len(X) #14
    zero = 0 #15 TODO: Delete
    underscore ="_" #16
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
               Instr(17, 17, 4, 0, 0, 0, 0, 20),    ## Step0  #17: Assign idx4 of idx 17 (madlibs) to idx 20(bot1)
               Instr(14, 20, " ", 0, 0, 0, 0, 21),  ## Step1  #13: Compare idx 20(bot1) and idx 13 and assign result to idx 21(bot2)
               Instr(20, 21, 1, 5, 0, 0, 0, 0),     ## Step2  #20: Cond jump to +1/+5 if true/false
               
               Instr(11, 17, 5, 4, 0, 0, 0, 22),    ## Step3  #11: Assign idx 5 to 4 of idx 17 to idx 22 (bot 3)
               Instr(8, 22, 0, 0, 0, 0, 0, 0),      ## Step4  #8: append idx22 to idx 0
               Instr(9, 4, 0, 0, 0, 0, 0, 5),       ## Step5  #9: Assign idx 4 (index i) to idx 5 (idx-k)
               Instr(15, 1, 0, 0, 0, 0, 0, 5),      ## Step6  #15: add 1 to idx 5 (idx-k)
               
               Instr(15, 1, 0, 0, 0, 0, 0, 4),      ## Step7  #15: add 1 to idx 4 (idx-i)
               
               Instr(13, 4, 6, 2, 0, 0, 0, 20),     ## Step8  #13: Check if idx 4 (idx-i) < idx 6 (madlibs_len), and assign result to idx 20(bot1)
               Instr(20, 20, -9, 1, 0, 0, 0, 0),    ## Step9 #20: jump to next or back to beginning
               
               Instr(18, 17, -1, 0, 0, 0, 0, 21),   ## Step10 #18 take last elem of idx 17(madlibs) into idx 21(bot2)
               Instr(14, 21, " ", 1, 0, 0, 0, 22),  ## Step11 #13 Compare idx13 (" ") and idx21(bot2) to check non-equality, assign it to idx 22(bot3)

               Instr(12, 17, 5, 0, 0, 0, 0, 22),    ## Step13 #12: Assign idx 5 till end of idx 17(madlibs) to idx 22 (bot 4)
               Instr(8, 22, 0, 0, 0, 0, 0, 0),      ## Step14 #8: append idx22 to idx 0

               Instr(16, 0, 0, 0, 0, 0, 0, 4),      ## Step15 #9: Set index i to 0
               Instr(16, 0, 0, 0, 0, 0, 0, 5),      ## Step16 #9: Set index k to 0

               # Assigning hard-coded nouns 1 and 2
               Instr(18, 18, 3, 0, 0, 0, 0, 20),    ## Step20 #9: Set index 3 of nouns to idx 20 (bot1)
               Instr(8, 20, 0, 0, 0, 0, 0, 12),     ## Step21 #8: Append hard-coded noun1/2, idx 20(bot1)
               Instr(18, 18, 4, 0, 0, 0, 0, 20),    ## Step22 #9: Set index 4 of nouns to idx 20 (bot1)
               Instr(8, 20, 0, 0, 0, 0, 0, 12),     ## Step23 #8: Append hard-coded noun2/2, idx 20(bot1)

               # Split X into a list of strings, X_words
               Instr(17, 19, 4, 0, 0, 0, 0, 20), #Step0  #17: Assign idx4 of idx 19 (X) to idx 20(bot1)
               Instr(14, 20, " ", 0, 0, 0, 0, 21), #Step1  #13: Compare idx 21(bot2) and idx 13 and assign result to idx 21(bot2)
               Instr(20, 21, 1, 5, 0, 0, 0, 0), #Step2  #20: Cond jump to +1/+5 if true/false

               Instr(11, 19, 5, 4, 0, 0, 0, 22), #Step3  #11: Assign idx k/5 to i/4 of idx 19 (X) to idx 22 (bot 3)
               Instr(8, 22, 0, 0, 0, 0, 0, 1), #Step4  #8: append idx22 to idx 1 (X_words)
               Instr(9, 4, 0, 0, 0, 0, 0, 5), #Step5  #9: Assign idx 4 (index i) to idx 5
               Instr(15, 1, 0, 0, 0, 0, 0, 5), #Step6  #15: add 1 to idx 5

               Instr(15, 1, 0, 0, 0, 0, 0, 4), #Step7  #15: add 1 to idx 4

               Instr(13, 4, 14, 2, 0, 0, 0, 20), #Step8  #13: Compare idx 4 and idx 6 and assign result to idx 20(bot1)
               Instr(20, 20, -9, 1, 0, 0, 0, 0), #Step9 #20: cond jump to next or start from the beginning of this block (-9)
               Instr(18, 19, -1, 0, 0, 0, 0, 21),  #Step10 #18 take last elem of idx 19 into idx 21(bot2)
               Instr(14, 21, " ", 1, 0, 0, 0, 22), #Step11 #14 Compare idx13 (" ") and idx21(bot2) to check inequality, assign it to idx 22(bot3)
               Instr(20, 22, 1, 3, 0, 0, 0, 0),    #Step12 #20: Cond jump to +1/+3 if true/false

               Instr(12, 19, 5, 0, 0, 0, 0, 22),   #Step13 #12: Assign idx 5 till end of idx 19(X) to idx 22 (bot 4)
               Instr(8, 22, 0, 0, 0, 0, 0, 1),     #Step14 #8: append idx22 to idx 1 (X_words)

               Instr(16, 0, 0, 0, 0, 0, 0, 4),      ## Step18 #9: Set index i to 0
               Instr(16, 0, 0, 0, 0, 0, 0, 5),      ## Step19 #9: Set index k to 0

               # TODO: Work on following steps
               Instr(5, 0, 1, 4, 5, 12, 16, 2),   ## Step22 #5: Take the first three nouns from X and hard-code the rest from the nouns list
               
               Instr(16, 0, 0, 0, 0, 0, 0, 4),    ## Step23 #9: Set index i to 0
               
               Instr(6, 2, 4, 0, 0, 0, 0, 3),     ## Step23 #6: Stringify the list
               
               Instr(21, 0, 0, 0, 0, 0, 0, 0),    ## Step24 #21: Terminal
              ]

    pro_prog = make_program(program)
    
    pc = 0

    for i in range(n_iter):
        pc = step(pro_prog, pc, mem)
        print(pc,": ", mem[1] )

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
    madlibs_len = len(madlibs) #6
    first = 0 #7
    second = 1 #8
    third = 2 #9
    fourth = 3 #10
    fifth = 4 #11
    fill = [] #12
    blank = " " #13 TODO: Delete after ops4 modified
    X_len = None #14
    zero = 0 #15
    underscore ="_" #16
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
               Instr(17, 17, 4, 0, 0, 0, 0, 20),    ## Step0  #17: Assign idx4 of idx 17 (madlibs) to idx 20(bot1)
               Instr(14, 20, " ", 0, 0, 0, 0, 21),   ## Step1  #13: Compare idx 20(bot1) and idx 13 (=" ") and assign result to idx 21(bot2)
               Instr(20, 21, 1, 5, 0, 0, 0, 0),     ## Step2  #20: Cond jump to +1/+5 if true/false
               
               Instr(11, 17, 5, 4, 0, 0, 0, 22),    ## Step3  #11: Assign idx 5 to 4 of idx 17 to idx 22 (bot 3)
               Instr(8, 22, 0, 0, 0, 0, 0, 0),      ## Step4  #8: append idx22 to idx 0
               Instr(9, 4, 0, 0, 0, 0, 0, 5),       ## Step5  #9: Assign idx 4 (index i) to idx 5 (idx-k)
               Instr(15, 1, 0, 0, 0, 0, 0, 5),      ## Step6  #15: add 1 to idx 5 (idx-k)
               
               Instr(15, 1, 0, 0, 0, 0, 0, 4),      ## Step7  #15: add 1 to idx 4 (idx-i)
               
               Instr(13, 4, 6, 2, 0, 0, 0, 20),     ## Step8  #13: Check if idx 4 (idx-i) < idx 6 (madlibs_len), and assign result to idx 20(bot1)
               Instr(20, 20, -9, 1, 0, 0, 0, 0),    ## Step9 #20: jump to next or back to beginning
               
               Instr(18, 17, -1, 0, 0, 0, 0, 21),   ## Step10 #18 take last elem of idx 17(madlibs) into idx 21(bot2)
               Instr(14, 21, " ", 1, 0, 0, 0, 22),   ## Step11 #13 Compare idx13 (" ") and idx21(bot2) to check non-equality, assign it to idx 22(bot3)

               Instr(12, 17, 5, 0, 0, 0, 0, 22),    ## Step13 #12: Assign idx 5 till end of idx 17(madlibs) to idx 22 (bot 4)
               Instr(8, 22, 0, 0, 0, 0, 0, 0),      ## Step14 #8: append idx22 to idx 0

               Instr(9, 15, 0, 0, 0, 0, 0, 4),      ## Step15 #9: Setting index i to 0
               Instr(9, 15, 0, 0, 0, 0, 0, 5),      ## Step16 #9: Setting index k to 0

               # Assigning hard-coded nouns 1 - 5
               Instr(18, 18, 0, 0, 0, 0, 0, 20),  ## Step17 #9: Setting index i to 20 (bot1)
               Instr(8, 20, 0, 0, 0, 0, 0, 12),   ## Step18 #8: Assigning hard-coded noun1/2
               Instr(18, 18, 1, 0, 0, 0, 0, 20),  ## Step19 #9: Setting index i to 20 (bot1)
               Instr(8, 20, 0, 0, 0, 0, 0, 12),   ## Step20 #8: Assigning hard-coded noun2/2
               Instr(18, 18, 2, 0, 0, 0, 0, 20),  ## Step21 #9: Setting index i to 20 (bot1)
               Instr(8, 20, 0, 0, 0, 0, 0, 12),   ## Step22 #8: Assigning hard-coded noun1/2
               Instr(18, 18, 3, 0, 0, 0, 0, 20),  ## Step23 #9: Setting index i to 20 (bot1)
               Instr(8, 20, 0, 0, 0, 0, 0, 12),   ## Step24 #8: Assigning hard-coded noun2/2
               Instr(18, 18, 4, 0, 0, 0, 0, 20),  ## Step25 #9: Setting index i to 20 (bot1)
               Instr(8, 20, 0, 0, 0, 0, 0, 12),   ## Step26 #8: Assigning hard-coded noun2/2

               #TODO: Work on following steps
               Instr(7, 4, 5, 0, 12, 16, 0, 2),   ## Step27 #7: Hard-Code all blanks from the nouns list
               Instr(9, 15, 0, 0, 0, 0, 0, 4),    ## Step28 #9: Setting index i to 0
               Instr(9, 15, 0, 0, 0, 0, 0, 5),    ## Step29 #9: Setting index k to 0
               Instr(6, 2, 4, 5, 0, 0, 0, 3),     ## Step30 #6: Stringify the list
               Instr(21, 0, 0, 0, 0, 0, 0, 0),    ## Step31 #21: Terminal
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