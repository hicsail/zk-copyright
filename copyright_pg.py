
def make_X(madlibs, nouns):
    X = madlibs.split()
    i = 0

    for k in range(len(X)):
        if X[k] == '_':
            X[k] = nouns[i]
            i+=1

    X = ' '.join(X) # This is the madlibs text with all blanks are filled

    return X


def fill_blank(text, fill):
    return ' '.join([word if word != '_' else fill.pop(0) for word in text.split()])


def producer_func(nouns, madlibs, X):
    madlibs_words = madlibs.split()
    X_words = X.split()

    partial_X = ' '.join([X_words[i] if madlibs_words[i] == "_" and i< 10 else madlibs_words[i] for i in range(len(madlibs_words))])

    first = nouns[3]
    second = nouns[4]

    fill = [first, second]

    return fill_blank(partial_X, fill)


def reproducer_func(madlibs, nouns):
    first = nouns[0]
    second = nouns[1]
    third = nouns[2]
    fourth = nouns[3]
    fifth = nouns[4]

    fill = [first, second, third, fourth, fifth]

    return fill_blank(madlibs, fill)


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

    reprod_Y = reproducer_func(madlibs, nouns)
    print('reprod_Y: ', reprod_Y)
    print('')

if __name__ == "__main__":
    main()