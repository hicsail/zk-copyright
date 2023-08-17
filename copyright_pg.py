
def make_X(madlibs, nouns):
    X = madlibs.split()
    i = 0

    for k in range(len(X)):
        if X[k] == '_':
            X[k] = nouns[i]
            i+=1

    X = ' '.join(X) # This is the madlibs text with all blanks are filled

    return X


def producer_func(nouns, madlibs, X):
    
    ''' Split madlibs into a list of strings, madlibs_words
        Requirements:
            - memory 
            - mov(copy/value assignment)
            - increment/decrement
            - comparison
            - jmp
    '''
    madlibs_words = []
    k =0
    i = 0
    madlibs_len = len(madlibs)

    while i < madlibs_len:
        if madlibs[i] == " ":
            madlibs_words.append(madlibs[k:i])
            k = i + 1
        i += 1

    if madlibs[-1] != " ":
        madlibs_words.append(madlibs[k:])


    ''' Split X into a list of strings, X_words
        Requirements:
            - memory
            - mov(copy/value assignment)
            - increment/decrement
            - comparison
            - jmp
    '''
    X_words = []
    k = 0
    i = 0
    X_len = len(X)

    while i < X_len:
        if X[i] == " ":
            X_words.append(X[k:i])
            k = i + 1
        i += 1

    if X[-1] != " ":
        X_words.append(X[k:])
    

    ''' Take the first three nouns from X and hard-code the rest from the nouns list
        Requirements:
            - memory 
            - mov(copy/value assignment)
            - increment/decrement
            - comparison
            - jmp
    '''
    first = nouns[3]
    second = nouns[4]
    fill = [first, second]

    assembled_list = []
    fill_index = 0
    madlibs_words_len = len(madlibs_words)

    i = 0
    while i < madlibs_words_len:
        if madlibs_words[i] == "_" and i < 10:
            assembled_list.append(X_words[i])
        elif madlibs_words[i] == "_":
            assembled_list.append(fill[fill_index])
            fill_index += 1
        else:
            assembled_list.append(madlibs_words[i])
        i += 1

    # Stringify the list
    if not assembled_list:
        return ""
    
    result = assembled_list[0]
    result_len = len(assembled_list)
    i = 1
    while i < result_len:
        result += " " + assembled_list[i]
        i += 1
    
    return result


def reproducer_func(madlibs, nouns):
        
    # Split madlibs into a list of strings, madlibs_words
    madlibs_words = []
    k =0
    i = 0
    madlibs_len = len(madlibs)

    while i < madlibs_len:
        if madlibs[i] == " ":
            madlibs_words.append(madlibs[k:i])
            k = i + 1
        i += 1

    if madlibs[-1] != " ":
        madlibs_words.append(madlibs[k:])

    
    # Hard-Code all blanks from the nouns list
    first = nouns[0]
    second = nouns[1]
    third = nouns[2]
    fourth = nouns[3]
    fifth = nouns[4]

    fill = [first, second, third, fourth, fifth]

    assembled_list = []
    fill_index = 0
    for word in madlibs_words:
        if word == "_":
            assembled_list.append(fill[fill_index])
            fill_index += 1
        else:
            assembled_list.append(word)


    # Stringify the list
    if not assembled_list:
        return ""
    
    result = assembled_list[0]
    for item in assembled_list[1:]:
        result += " " + item
    
    return result


def main():
    # The Mad Libs template
    madlibs = "I have a _ and _ , and every _ I walk _ to the _"

    # The list of potential fill-ins
    nouns = ['dog', 'cat', 'day', 'her', 'park', 'ball', 'cat', 'school', 'like', 'hour', 'tree', 'car', 'house', 'week', 'shoe', 'beach']

    X = make_X(madlibs, nouns)
    print('X: ', X)
    print('')
    
    prod_Y = producer_func(nouns, madlibs, X)
    print('prod_Y: ', prod_Y)
    print('')
    assert("I have a dog and cat , and every day I walk her to the park" == prod_Y)

    reprod_Y = reproducer_func(madlibs, nouns)
    print('reprod_Y: ', reprod_Y)
    print('')
    assert("I have a dog and cat , and every day I walk her to the park" == reprod_Y)

if __name__ == "__main__":
    main()