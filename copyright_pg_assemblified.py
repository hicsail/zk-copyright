from typing import List

# Class to hold a single instruction TODO: @dataclass
class Instr:
    def __init__(self, opcode: int, src1: int, src2: int, dest: int):
        self.opcode = opcode
        self.src1 = src1
        self.src2 = src2
        self.dest = dest


# Class to hold a program as multiple lists of instructions TODO: @dataclass
class Program:
    def __init__(self, opcode: List[int], src1: List[int], src2: List[int], dest: List[int]):
        self.opcode: List[int] = opcode
        self.src1: List[int] = src1
        self.src2: List[int] = src2
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
    # 3. Split madlibs into a list of strings, madlibs_words
    if instr.opcode == 3:
        # madlibs_words = []: replaced with mem[0]
        # k = 0: replaced with mem[5]
        # i = 0: replaced with mem[4]
        # madlibs_len = len(madlibs): replaced with mem[6]
        while mem[4] < mem[6]:
            if madlibs[mem[4]] == " ":
                mem[0].append(madlibs[mem[5]:mem[4]])
                mem[5] = mem[4] + 1
            mem[4] += 1

        if madlibs[-1] != " ":
            mem[0].append(madlibs[mem[5]:])
        
        mem[4] = 0
        mem[5] = 0


    # 4. Split X into a list of strings, X_words
    elif instr.opcode == 4:
        # X_words = []: replaced with mem[1]
        # k = 0: replaced with m[5]
        # i = 0: replaced with m[4]
        X_len = len(X)

        while mem[4] < X_len:
            if X[mem[4]] == " ":
                mem[1].append(X[mem[5]:mem[4]])
                mem[5] = mem[4] + 1
            mem[4] += 1

        if X[-1] != " ":
            mem[1].append(X[mem[5]:])

        mem[4] = 0
        mem[5] = 0

    # 5. Take the first three nouns from X and hard-code the rest from the nouns list
    elif instr.opcode == 5:
        first = nouns[3]
        second = nouns[4]
        fill = [first, second]

        # assembled_list = []: replaced with mem[2]
        fill_index = 0
        madlibs_words_len = len(mem[0])

        # i = 0: replaced with m[4]
        while mem[4] < madlibs_words_len:
            if mem[0][mem[4]] == "_" and mem[4] < 10:
                mem[2].append(mem[1][mem[4]])
            elif mem[0][mem[4]] == "_":
                mem[2].append(fill[fill_index])
                fill_index += 1
            else:
                mem[2].append(mem[0][mem[4]])
            mem[4] += 1

        mem[4] = 0

    # 6. Stringify the list - No need to be secret anymore?
    elif instr.opcode == 6:
        if not mem[2]:
            return ""

        mem[3] = mem[2][0]
        result_len = len(mem[2])
        mem[4] = 1
        while mem[4] < result_len:
            mem[3] += " " + mem[2][mem[4]]
            mem[4] += 1
    
        mem[4] = 0
        mem[5] = 0

    # 7. Hard-Code all blanks from the nouns list
    elif instr.opcode == 7:
        first = nouns[0]
        second = nouns[1]
        third = nouns[2]
        fourth = nouns[3]
        fifth = nouns[4]

        fill = [first, second, third, fourth, fifth]

        # assembled_list = []: replaced with mem[2]
        # fill_index = 0: replaced with mem[5]
        assembled_size = len(mem[0])
        while mem[4] < assembled_size:
            if mem[0][mem[4]] == "_":
                mem[2].append(fill[mem[5]])
                mem[5] += 1
            else:
                mem[2].append(mem[0][mem[4]])
            mem[4] += 1
        
        mem[4] = 0
        mem[5] = 0

def make_program(prog): #TODO: ZKListify
    length = len(prog)
    opcode = [0 for _ in range(length)]
    src1 = [0 for _ in range(length)]
    src2 = [0 for _ in range(length)]
    dest = [0 for _ in range(length)]

    for i, instr in enumerate(prog):
        opcode[i] = instr.opcode
        src1[i] = instr.src1
        src2[i] = instr.src2
        dest[i] = instr.dest

    return Program(opcode, src1, src2, dest)


# Fetch an instruction from a program
def fetch(prog: Program, pc: int): #TODO: change int to SecretInt
    return Instr(prog.opcode[pc],
                 prog.src1[pc],
                 prog.src2[pc],
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
    '''
    #TODO: uncomment with PicoZKCompiler('picozk_test', options=['ram']):

    madlibs_words = []
    X_words = []
    assembled_list = []
    result = ""
    i = 0
    k = 0
    madlibs_len = len(madlibs)
    mem = [madlibs_words, X_words, assembled_list, result, i, k, madlibs_len]
    program = [Instr(3, 0, 0, 0),
                Instr(4, 0, 0, 0),
                Instr(5, 0, 0, 0),
                Instr(6, 0, 0, 0),
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
    repro_mem = [madlibs_words, X_words, assembled_list, result, i, k, madlibs_len]
    program = [Instr(3, 0, 0, 0),
                Instr(7, 0, 0, 0),
                Instr(6, 0, 0, 0),
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