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
        # madlibs_words = []: replaced with mem[0]
        # k = 0: replaced with mem[5]
        # i = 0: replaced with mem[4]
        # madlibs_len = len(madlibs): replaced with mem[6]
        while a2 < a4:
            if madlibs[a2] == a5:
                mem[des].append(madlibs[a3:a2])
                a3 = a2 + 1
            a2 += 1

        if madlibs[-1] != a5:
            mem[des].append(madlibs[a3:])
        '''
            des:0
            a2:mem[4]
            a3:mem[5]
            a4:mem[6]
            a5:mem[13] (= " ")
        '''        

    # 4. Split X into a list of strings, X_words
    elif instr.opcode == 4:
        # X_words = []: replaced with mem[1]
        # k = 0: replaced with m[5]
        # i = 0: replaced with m[4]

        # X_len = len(X): replaced with a4
        while a2 < a4:
            if X[a2] == a5:
                mem[des].append(X[a3:a2])
                a3 = a2 + 1
            a2 += 1

        if X[-1] != a5:
            mem[des].append(X[a3:])

        '''
            des:1
            a2:mem[4]
            a3:mem[5]
            a4:mem[14]
            a5:mem[13] (= " ")
        '''        

    # 5. Take the first three nouns from X and hard-code the rest from the nouns list
    elif instr.opcode == 5:
        #fill: replaced with mem[12]
        
        # These are done in opcode=8
            # mem[12].append(nouns[mem[7]])
            # mem[12].append(nouns[mem[8]])

        # assembled_list = []: replaced with mem[2]
        # fill_index = 0: replaced with mem[5]
        madlibs_words_len = len(a1)

        # i = 0: replaced with m[4]
        while a3 < madlibs_words_len:
            if a1[a3] == a6 and a3 < 10:
                mem[des].append(a2[a3])
            elif a1[a3] == a6:
                mem[des].append(a5[a4])
                a4 += 1
            else:
                mem[des].append(a1[a3])
            a3 += 1

        a3 = 0
        '''
            des:2
            a1:mem[0]
            a2:mem[1]
            a3:mem[4]
            a4:mem[5]
            a5:mem[12]
            a6:mem[16]
        '''

    # 6. Stringify the list - No need to be secret anymore?
    elif instr.opcode == 6:
        if not a1:
            return ""

        mem[des] = a1[0]
        result_len = len(a1)
        a2 = 1
        while a2 < result_len:
            mem[des] += " " + a1[a2]
            a2 += 1
    
        a2 = 0
        
        '''
            des:3
            a1:mem[2]
            a2:mem[4]
        '''

    # 7. Hard-Code all blanks from the nouns list
    elif instr.opcode == 7:

        #fill: replaced with mem[12]
        # These are done in opcode=8
            # mem[12].append(nouns[mem[7]])
            # mem[12].append(nouns[mem[8]])
            # mem[12].append(nouns[mem[9]])
            # mem[12].append(nouns[mem[10]])
            # mem[12].append(nouns[mem[11]])

        # assembled_list = []: replaced with mem[2]
        # fill_index = 0: replaced with mem[5]
        assembled_size = len(mem[0])
        while mem[4] < assembled_size:
            if mem[0][mem[4]] == "_":
                mem[2].append(mem[12][mem[5]])
                mem[5] += 1
            else:
                mem[2].append(mem[0][mem[4]])
            mem[4] += 1
        
        mem[4] = 0
        mem[5] = 0

    # 8. Append Value, nouns[a1] to dest
    elif instr.opcode == 8:
        mem[des].append(nouns[a1])
        '''
            des:12
            a1:depends
        '''

    # 9. Assign a value (a1) to dest
    elif instr.opcode == 9:
        mem[des] = a1
        '''
            des:depends
            a1:depends
        '''

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

    madlibs_words = []
    X_words = []
    assembled_list = []
    result = ""
    i = 0
    k = 0
    madlibs_len = len(madlibs)
    first = 3
    second = 4
    third = None
    fourth = None
    fifth = None
    fill = []
    blank = " "
    X_len = len(X)
    zero = 0
    underscore ="_"
    mem = [madlibs_words, X_words, assembled_list, result, i, k, madlibs_len,
           first, second, third, fourth, fifth, fill, blank, X_len, zero, underscore]
        
    program = [Instr(3, 0, 4, 5, 6, 13, 0, 0),
               Instr(9, 15, 0, 0, 0, 0, 0, 4),
               Instr(9, 15, 0, 0, 0, 0, 0, 5),
                Instr(4, 0, 4, 5, 14, 13, 0, 1),
                Instr(9, 15, 0, 0, 0, 0, 0, 4),
               Instr(9, 15, 0, 0, 0, 0, 0, 5),
                Instr(8, 7, 0, 0, 0, 0, 0, 12),
                Instr(8, 8, 0, 0, 0, 0, 0, 12),
                Instr(5, 0, 1, 4, 5, 12, 16, 2),
                Instr(6, 2, 4, 5, 0, 0, 0, 3),
              ]

    pro_prog = make_program(program)

    for i in range(len(program)):
        step(pro_prog, i, nouns, madlibs, X, mem)

    prod_Y = mem[3]
    print('prod_Y: ', prod_Y)
    print('')
    assert("I have a dog and cat , and every day I walk her to the park" == prod_Y)

    madlibs_words = []
    X_words = []
    assembled_list = []
    result = ""
    i = 0
    k = 0
    madlibs_len = len(madlibs)
    first = 0
    second = 1
    third = 2
    fourth = 3
    fifth = 4
    fill = []
    blank = " "
    X_len = None
    zero = 0
    repro_mem = [madlibs_words, X_words, assembled_list, result, i, k, madlibs_len,
           first, second, third, fourth, fifth, fill, blank, X_len, zero, underscore]
    program = [Instr(3, 0, 4, 5, 6, 13, 0, 0),
               Instr(9, 15, 0, 0, 0, 0, 0, 4),
               Instr(9, 15, 0, 0, 0, 0, 0, 5),
               Instr(8, 7, 0, 0, 0, 0, 0, 12),
               Instr(8, 8, 0, 0, 0, 0, 0, 12),
               Instr(8, 9, 0, 0, 0, 0, 0, 12),
               Instr(8, 10, 0, 0, 0, 0, 0, 12),
               Instr(8, 11, 0, 0, 0, 0, 0, 12),
               Instr(7, 0, 0, 0, 0, 0, 0, 0),
               Instr(6, 2, 4, 5, 0, 0, 0, 3),
              ]
    repro_prog = make_program(program)

    for i in range(len(program)):
        step(repro_prog, i, nouns, madlibs, X, repro_mem)

    reprod_Y = repro_mem[3]
    print('reprod_Y: ', reprod_Y)
    print('')
    assert("I have a dog and cat , and every day I walk her to the park" == reprod_Y)

if __name__ == "__main__":
    main()