
def make_X(bg, honey_entries):
    res = bg.copy()
    res.update(honey_entries)
    return res


def producer_func(X):
    temp_list = [(k,v) for k,v in X.items()]
    return str(sorted(temp_list, key=lambda x:x[0], reverse=False))[1:-1]


def reproducer_func(bg):
    temp_list = [(k,v) for k,v in bg.items()] + [('Honey Person1', '111-666-6666'), ('Honey Person2', '222-777-7777')]
    return str(sorted(temp_list, key=lambda x:x[1], reverse=False))[1:-1]


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
    
    prod_y = producer_func(X)
    print("prod_y", prod_y)
    
    repro_y = reproducer_func(bg)
    print("repro_y", repro_y)

if __name__ == "__main__":
    main()