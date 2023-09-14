
def make_X(bg, honey_entries):
    res = bg.copy()
    res.update(honey_entries)
    return res


def string_to_int(s):
    return int(''.join(format(ord(char), '08b') for char in s), 2)


def int_to_string(n):
    binary_str = format(n, 'b')
    binary_str = '0' * ((8 - len(binary_str) % 8) % 8) + binary_str
    return ''.join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8))


def list_to_string(res_list):
    # Convert the List to a String
    result_str = ""
    idx = 0
    res_list_size = len(res_list)
    while idx < res_list_size:
        # Convert each tuple to a string and add to result_str
        item_str = "(" + "'" + res_list[idx][0] + "'" + ", " + "'" + res_list[idx][1] + "'" + ")"
        if result_str:
            result_str += ", " + item_str
        else:
            result_str = item_str
        idx += 1
    return result_str


def sort_by(input_list, sort_key):
    # Sort the List of Tuples
    n = len(input_list)
    i = 0
    while i < n:
        j = 0
        while j < n-i-1:
            # Compare the first element of each tuple
            if input_list[j][sort_key] > input_list[j+1][sort_key]:
                temp = input_list[j]
                input_list[j] = input_list[j+1]
                input_list[j+1] = temp
            j += 1
        i += 1
    return input_list


def producer_func(X):
    temp_list = [(k,v) for k,v in X.items()]
    return sort_by(temp_list, 0)


def reproducer_func(bg):
    temp_list = [(k,v) for k,v in bg.items()]
    temp_list += [('Honey Person1', '111-666-6666'), ('Honey Person2', '222-777-7777')]
    return sort_by(temp_list, 1)


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
    print('X', X)
    print('')

    exp_pro_Y = "('Alice Smith', '333-333-3333'), ('Bob Brown', '444-444-4444'), ('Charlie Clark', '555-555-5555'), ('Honey Person1', '111-666-6666'), ('Honey Person2', '222-777-7777'), ('Jane Doe', '222-222-2222'), ('John Keller', '111-111-1111')"
    print('exp_pro_Y', exp_pro_Y)
    print('')

    pro_Y = list_to_string(producer_func(X))
    print("pro_Y", pro_Y)
    print('')
    assert(exp_pro_Y == pro_Y)
    
    exp_repro_Y = "('John Keller', '111-111-1111'), ('Honey Person1', '111-666-6666'), ('Jane Doe', '222-222-2222'), ('Honey Person2', '222-777-7777'), ('Alice Smith', '333-333-3333'), ('Bob Brown', '444-444-4444'), ('Charlie Clark', '555-555-5555')"
    print('repro_Y', exp_repro_Y)
    print('')

    repro_Y = list_to_string(reproducer_func(bg))
    print("repro_y", repro_Y)
    print('')
    assert(exp_repro_Y == repro_Y)

if __name__ == "__main__":
    main()