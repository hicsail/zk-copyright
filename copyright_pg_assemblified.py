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

# Simulate naively -TODO to be modified with prog and mem etc.
def step(prog: Program, pc: int, nouns, madlibs, X, mem):
    
    instr = fetch(prog, pc)
    a1 = mem[instr.src1]
    a2 = mem[instr.src2]
    a3 = mem[instr.src3]
    a4 = mem[instr.src4]
    a5 = mem[instr.src5]
    a6 = mem[instr.src6]
    des = instr.dest
    new_pc = pc

    # 3. Split madlibs into a list of strings, madlibs_words
    if instr.opcode == 3:

        '''
            des:0
            mem[instr.src2]:mem[4]
            mem[instr.src3]:mem[5]
            a4:mem[6]
            a5:mem[13] (= " ")
        '''

        if madlibs[mem[instr.src2]] == a5:
            mem[des].append(madlibs[mem[instr.src3]:mem[instr.src2]])
            mem[instr.src3] = mem[instr.src2] + 1
        mem[instr.src2] += 1

        if mem[instr.src2] < a4:
            return new_pc
        else: 
            if madlibs[-1] != a5:
                mem[des].append(madlibs[mem[instr.src3]:])
            return new_pc + 1 

    # 4. Split X into a list of strings, X_words
    elif instr.opcode == 4:

        '''
            des:1
            mem[instr.src2]:mem[4]
            mem[instr.src3]:mem[5]
            a4:mem[14]
            a5:mem[13] (= " ")
        '''

        if X[mem[instr.src2]] == a5:
            mem[des].append(X[mem[instr.src3]:mem[instr.src2]])
            mem[instr.src3] = mem[instr.src2] + 1
        mem[instr.src2] += 1

        if mem[instr.src2] < a4:
            return new_pc
        else: 
            if X[-1] != a5:
                mem[des].append(X[a3:])
            return new_pc + 1 

    # 5. Take the first three nouns from X and hard-code the rest from the nouns list
    elif instr.opcode == 5:

        '''
            des:2
            a1:mem[0]
            a2:mem[1]
            mem[instr.src3]:mem[4]
            mem[instr.src4]:mem[5]
            a5:mem[12]
            a6:mem[16]
        '''

        madlibs_words_len = len(a1)
        
        if a1[a3] == a6 and a3 < 10:
            mem[des].append(a2[a3])
        elif a1[a3] == a6:
            mem[des].append(a5[a4])
            mem[instr.src4] += 1
        else:
            mem[des].append(a1[a3])
        mem[instr.src3] += 1

        if mem[instr.src3] < madlibs_words_len:
            return new_pc
        else:
            return new_pc + 1

    # 6. Stringify the list
    elif instr.opcode == 6:

        '''
            des:3
            a1:mem[2]
            a2:mem[4]
        '''

        if not a1:
            return ""
        result_len = len(a1)
        
        if a2 == 0:
            mem[des] = a1[0]
            mem[instr.src2] = 1
            a2 = 1
        
        mem[des] += " " + a1[a2]
        mem[instr.src2] += 1
    
        if mem[instr.src2] < result_len:
            return new_pc
        else:
            return new_pc + 1

    # 7. Hard-Code all blanks from the nouns list
    elif instr.opcode == 7:

        '''
            des:2
            mem[instr.src1]:mem[4]
            mem[instr.src2]:mem[5]
            a3:mem[0]
            a4:mem[12]
        '''

        assembled_size = len(mem[0])
        
        if a3[mem[instr.src1]] == "_":
            mem[des].append(a4[mem[instr.src2]])
            mem[instr.src2] += 1
        else:
            mem[des].append(a3[mem[instr.src1]])
        mem[instr.src1] += 1
        
        if mem[instr.src1] < assembled_size:
            return new_pc
        else:
            return new_pc + 1
        
    # 8. Append Value, nouns[a1] to dest
    elif instr.opcode == 8:
        mem[des].append(nouns[a1])

        '''
            des:12
            a1:depends
        '''

        return new_pc + 1

    # 9. Assign a value (a1) to dest
    elif instr.opcode == 9:
        mem[des] = a1

        '''
            des:depends
            a1:depends
        '''

        return new_pc + 1

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
    blank = " " #13
    X_len = len(X) #14
    zero = 0 #15
    underscore ="_" #16
    mem = [madlibs_words, X_words, assembled_list, result, i, k, madlibs_len,
           first, second, third, fourth, fifth, fill, blank, X_len, zero, underscore]
        
    program = [Instr(3, 0, 4, 5, 6, 13, 0, 0), #  Split madlibs into a list of strings, madlibs_words
               Instr(9, 15, 0, 0, 0, 0, 0, 4),      ## Setting index i to 0
               Instr(9, 15, 0, 0, 0, 0, 0, 5),      ## Setting index k to 0
               Instr(4, 0, 4, 5, 14, 13, 0, 1), # Split X into a list of strings, X_words
               Instr(9, 15, 0, 0, 0, 0, 0, 4),      ## Setting index i to 0
               Instr(9, 15, 0, 0, 0, 0, 0, 5),      ## Setting index k to 0
               Instr(8, 7, 0, 0, 0, 0, 0, 12),      ##Assigning hard-coded noun1/2
               Instr(8, 8, 0, 0, 0, 0, 0, 12),      ##Assigning hard-coded noun2/2
               Instr(5, 0, 1, 4, 5, 12, 16, 2), # Take the first three nouns from X and hard-code the rest from the nouns list
               Instr(9, 15, 0, 0, 0, 0, 0, 4),      ## Setting index i to 0
               Instr(6, 2, 4, 5, 0, 0, 0, 3),  #  Stringify the list
              ]

    pro_prog = make_program(program)
    
    pc = 0

    for i in range(len(program)+47+58+15+14): #TODO: FIXME un-hard-code (Step 3, 4, 5, 6)
        pc = step(pro_prog, pc, nouns, madlibs, X, mem)

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
    blank = " " #13
    X_len = None #14
    zero = 0 #15
    repro_mem = [madlibs_words, X_words, assembled_list, result, i, k, madlibs_len,
           first, second, third, fourth, fifth, fill, blank, X_len, zero, underscore]
    program = [Instr(3, 0, 4, 5, 6, 13, 0, 0), #  Split madlibs into a list of strings, madlibs_words
               Instr(9, 15, 0, 0, 0, 0, 0, 4),      ## Setting index i to 0
               Instr(9, 15, 0, 0, 0, 0, 0, 5),      ## Setting index k to 0
               Instr(8, 7, 0, 0, 0, 0, 0, 12),      ## Assigning hard-coded noun1/5
               Instr(8, 8, 0, 0, 0, 0, 0, 12),      ## Assigning hard-coded noun2/5
               Instr(8, 9, 0, 0, 0, 0, 0, 12),      ## Assigning hard-coded noun3/5
               Instr(8, 10, 0, 0, 0, 0, 0, 12),     ##Assigning hard-coded noun4/5
               Instr(8, 11, 0, 0, 0, 0, 0, 12),     ##Assigning hard-coded noun5/5
               Instr(7, 4, 5, 0, 12, 0, 0, 2),  #  Hard-Code all blanks from the nouns list
               Instr(9, 15, 0, 0, 0, 0, 0, 4),      ## Setting index i to 0
               Instr(9, 15, 0, 0, 0, 0, 0, 5),      ## Setting index k to 0
               Instr(6, 2, 4, 5, 0, 0, 0, 3),  #  Stringify the list
              ]
    repro_prog = make_program(program)

    pc = 0

    for i in range(len(program)+47 + 14 + 15): #TODO: FIXME un-hard-code (Step 3, 6, 7)
        pc = step(repro_prog, pc, nouns, madlibs, X, repro_mem)

    reprod_Y = repro_mem[3]
    print('reprod_Y: ', reprod_Y)
    print('')
    assert("I have a dog and cat , and every day I walk her to the park" == reprod_Y)


if __name__ == "__main__":
    main()