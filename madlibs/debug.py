def debug():
    exp_Y = "I have a dog and cat , and every day I walk them to the park"

    blank_idx = [3, 5, 9, 12, 15]

    madlibs = "I have a _ and _ , and every _ I walk _ to the _".split()

    nouns = [
        "dog",
        "cat",
        "day",
        "them",
        "park",
        "beach",
        "her",
        "school",
        "like",
        "hour",
        "tree",
        "car",
        "house",
        "week",
        "shoe",
        "beach",
    ]

    return exp_Y, madlibs, nouns, blank_idx
