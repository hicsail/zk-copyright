
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
        k =0
        i = 0
        madlibs_len = len(madlibs)

        while i < madlibs_len:
            if madlibs[i] == " ":
                mem[0].append(madlibs[k:i])
                k = i + 1
            i += 1

        if madlibs[-1] != " ":
            mem[0].append(madlibs[k:])


    # 4. Split X into a list of strings, X_words
    elif instr == 4:
        # X_words = []: replaced with mem[1]
        k = 0
        i = 0
        X_len = len(X)

        while i < X_len:
            if X[i] == " ":
                mem[1].append(X[k:i])
                k = i + 1
            i += 1

        if X[-1] != " ":
            mem[1].append(X[k:])

    # 5. Take the first three nouns from X and hard-code the rest from the nouns list
    elif instr == 5:
        first = nouns[3]
        second = nouns[4]
        fill = [first, second]

        # assembled_list = []: replaced with mem[2]
        fill_index = 0
        madlibs_words_len = len(mem[0])

        i = 0
        while i < madlibs_words_len:
            if mem[0][i] == "_" and i < 10:
                mem[2].append(mem[1][i])
            elif mem[0][i] == "_":
                mem[2].append(fill[fill_index])
                fill_index += 1
            else:
                mem[2].append(mem[0][i])
            i += 1

    # 6. Stringify the list - No need to be secret anymore?
    elif instr == 6:
        if not mem[2]:
            return ""

        mem[3] = mem[2][0]
        result_len = len(mem[2])
        i = 1
        while i < result_len:
            mem[3] += " " + mem[2][i]
            i += 1
    
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
    '''

    madlibs_words = []
    X_words = []
    assembled_list = []
    result = ""
    mem = [madlibs_words, X_words, assembled_list, result]

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
    mem = [madlibs_words, X_words, assembled_list, result]

    step(3, nouns, madlibs, X, mem)
    step(7, nouns, madlibs, X, mem)
    step(6, nouns, madlibs, X, mem)
    reprod_Y = mem[3]
    print('reprod_Y: ', reprod_Y)
    print('')
    assert("I have a dog and cat , and every day I walk her to the park" == reprod_Y)

if __name__ == "__main__":
    main()