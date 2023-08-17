
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
def step(instr, nouns, madlibs, X, mem):

    # 3. Split madlibs into a list of strings, madlibs_words
    if instr == 3:
        # madlibs_words = []: replaced with mem[0]
        # k = 0: replaced with mem[5]
        # i = 0: replaced with mem[4]
        madlibs_len = len(madlibs)
        while mem[4] < madlibs_len:
            if madlibs[mem[4]] == " ":
                mem[0].append(madlibs[mem[5]:mem[4]])
                mem[5] = mem[4] + 1
            mem[4] += 1

        if madlibs[-1] != " ":
            mem[0].append(madlibs[mem[5]:])
        
        mem[4] = 0
        mem[5] = 0


    # 4. Split X into a list of strings, X_words
    elif instr == 4:
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
    elif instr == 5:
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
    elif instr == 6:
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
    elif instr == 7:
        first = nouns[0]
        second = nouns[1]
        third = nouns[2]
        fourth = nouns[3]
        fifth = nouns[4]

        fill = [first, second, third, fourth, fifth]

        # assembled_list = [] 
        fill_index = 0
        for word in mem[0]:
            if word == "_":
                mem[2].append(fill[fill_index])
                fill_index += 1
            else:
                mem[2].append(word)


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
    '''

    madlibs_words = []
    X_words = []
    assembled_list = []
    result = ""
    i = 0
    k = 0
    mem = [madlibs_words, X_words, assembled_list, result, i, k]

    step(3, nouns, madlibs, X, mem)
    step(4, nouns, madlibs, X, mem)
    step(5, nouns, madlibs, X, mem)
    step(6, nouns, madlibs, X, mem)
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
    mem = [madlibs_words, X_words, assembled_list, result, i, k]

    step(3, nouns, madlibs, X, mem)
    step(7, nouns, madlibs, X, mem)
    step(6, nouns, madlibs, X, mem)
    reprod_Y = mem[3]
    print('reprod_Y: ', reprod_Y)
    print('')
    assert("I have a dog and cat , and every day I walk her to the park" == reprod_Y)

if __name__ == "__main__":
    main()