# from picozk import *

def make_X(bg, honey_entries):
    res = bg.copy()
    res.update(honey_entries)
    return res


def producer_func(X):
    temp_list = [(k,v) for k,v in X.items()]
    return sorted(temp_list, key=lambda x:x[0], reverse=False)


def reproducer_func(bg, honey_entries):
    temp_list = [(k,v) for k,v in bg.items()]
    sorted_by_phone = sorted(temp_list, key=lambda x:x[1], reverse=False)
    
    for h_elm in honey_entries.items():
        inserted = False
        for i, (_, phone) in enumerate(sorted_by_phone):
            if h_elm[1] < phone:
                sorted_by_phone.insert(i, h_elm)
                inserted = True
                break
        if not inserted:  # If the entry wasn't inserted in the loop above
            sorted_by_phone.append(h_elm)

    return sorted_by_phone


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
    
    repro_y = reproducer_func(bg, honey_entries)
    print("repro_y", repro_y)

    
    # p = 11
    # n = 2
    # with PicoZKCompiler('irs/picozk_test', field=[p,n]):
    return 

if __name__ == "__main__":
    main()