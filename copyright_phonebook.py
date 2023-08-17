
def make_X(bg, honey_entries):
    res = bg.copy()
    res.update(honey_entries)
    return res


def producer_func(X):
    temp_list = [(k,v) for k,v in X.items()]

    # Sort the List of Tuples
    sort_key = 0
    n = len(temp_list)
    i = 0
    while i < n:
        j = 0
        while j < n-i-1:
            # Compare the first element of each tuple
            if temp_list[j][sort_key] > temp_list[j+1][sort_key]:
                temp = temp_list[j]
                temp_list[j] = temp_list[j+1]
                temp_list[j+1] = temp
            j += 1
        i += 1


    # Convert the List to a String
    result_str = ""
    idx = 0
    temp_list_size = len(temp_list)
    while idx < temp_list_size:
        # Convert each tuple to a string and add to result_str
        item_str = "(" + "'" + temp_list[idx][0] + "'" + ", " + "'" + temp_list[idx][1] + "'" + ")"
        if result_str:
            result_str += ", " + item_str
        else:
            result_str = item_str
        idx += 1

    return result_str



def reproducer_func(bg):
    temp_list = [(k,v) for k,v in bg.items()]
    temp_list += [('Honey Person1', '111-666-6666'), ('Honey Person2', '222-777-7777')]
    
    # Sort the List of Tuples
    sort_key = 1
    n = len(temp_list)
    i = 0
    while i < n:
        j = 0
        while j < n-i-1:
            # Compare the first element of each tuple
            if temp_list[j][sort_key] > temp_list[j+1][sort_key]:
                temp = temp_list[j]
                temp_list[j] = temp_list[j+1]
                temp_list[j+1] = temp
            j += 1
        i += 1


    # Convert the List to a String
    result_str = ""
    idx = 0
    temp_list_size = len(temp_list)
    while idx < temp_list_size:
        # Convert each tuple to a string and add to result_str
        item_str = "(" + "'" + temp_list[idx][0] + "'" + ", " + "'" + temp_list[idx][1] + "'" + ")"
        if result_str:
            result_str += ", " + item_str
        else:
            result_str = item_str
        idx += 1

    return result_str



def main():

    bg = {
        'John Keller': '111-111-1111',
        'Jane Doe': '222-222-2222',
        'Alice Smith': '333-333-3333',
        'Bob Brown': '444-444-4444',
        'Charlie Clark': '555-555-5555'
    }

    honey_entries = {
        'Honey Person1': '111-666-6666',
        'Honey Person2': '222-777-7777'
    }

    X = make_X(bg, honey_entries)
    print('Original X', X)
    
    prod_Y = producer_func(X)
    print("prod_y", prod_Y)
    assert("('Alice Smith', '333-333-3333'), ('Bob Brown', '444-444-4444'), ('Charlie Clark', '555-555-5555'), ('Honey Person1', '111-666-6666'), ('Honey Person2', '222-777-7777'), ('Jane Doe', '222-222-2222'), ('John Keller', '111-111-1111')" == prod_Y)
    
    reprod_Y = reproducer_func(bg)
    print("repro_y", reprod_Y)
    assert("('John Keller', '111-111-1111'), ('Honey Person1', '111-666-6666'), ('Jane Doe', '222-222-2222'), ('Honey Person2', '222-777-7777'), ('Alice Smith', '333-333-3333'), ('Bob Brown', '444-444-4444'), ('Charlie Clark', '555-555-5555')" == reprod_Y)

if __name__ == "__main__":
    main()