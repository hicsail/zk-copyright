from picozk import *
from utils.datatypes import Instr
from utils.steps import step
from utils.functions import make_program, int_to_string, string_to_int
import random

def make_X(bg, honey_entries):
    res = bg.copy()
    res.update(honey_entries)
    res = dict(sorted(res.items()))
    print("\nX", res)
    res = {string_to_int(k): string_to_int(v) for k, v in res.items()}
    return res


def reveal(res_list, start, end):
    # Convert the List to a String
    result_str = ""
    idx = start
    res_list_size = end
    while idx < res_list_size:
        # Convert each tuple to a string and add to result_str
        item_str = "(" + "'" + int_to_string(val_of(res_list[idx])) + "'" + ", " + "'" + int_to_string(val_of(res_list[idx+1])) + "'" + ")"
        if result_str:
            result_str += ", " + item_str
        else:
            result_str = item_str
        idx += 2
    return result_str


def make_phone_entry(bg):

  elem = ''
  for i in range(10):
    ent = str(random.randint(0, 9))
    if i == 3 or i==6:
      elem+='-'
    elem += ent

  key = str(random.randint(0, 2**63 - 1))

  bg.update({key:elem})
  return bg


def make_phone_dict(scale):
  bg = {}
  for i in range(scale):
    make_phone_entry(bg)
  return bg



def make_Y(bg, honey_entries):
    res = bg.copy()
    res.update(honey_entries)
    res = dict(sorted(res.items(), key=lambda x: x[1]))
    res = [f"('{k}', '{v}')" for k, v in res.items()]
    return ", ".join(res)



def debug():
    bg = {
        '2': '222-222-2222',
        '1': '111-111-1111',
        '3': '333-333-3333',
        '4': '444-444-4444',
        '5': '555-555-5555'
        }

    honey_entries = {
        '6': '111-666-6666',
        '7': '222-777-7777'
        }

    exp_Y = "('1', '111-111-1111'), ('6', '111-666-6666'), ('2', '222-222-2222'), ('7', '222-777-7777'), ('3', '333-333-3333'), ('4', '444-444-4444'), ('5', '555-555-5555')"
       
    return bg, honey_entries, exp_Y


def main():
    DEBUG=False
    scale = 5

    n_iter = 2000
    threshold = 500 # The program has to be performed within this (weight < )

    if DEBUG==True:
       bg, honey_entries, exp_Y = debug()
    else:
       bg = make_phone_dict(scale)
       honey_entries = make_phone_dict(int(max(1, scale/10)))
       exp_Y = make_Y(bg, honey_entries)
    
    X = make_X(bg, honey_entries)

    print("\nbg", bg)
    print("\nhoney_entries", honey_entries)
    print("\nexp_Y", exp_Y)

    p = pow(2,256) - pow(2,32) - pow(2,9) - pow(2,8) - pow(2,7) - pow(2,6) - pow(2,4) - 1

    with PicoZKCompiler('irs/picozk_test', field=[p], options=['ram']):

        # Producer
        reg1 = 1 #0 i
        reg2 = 0 #2 j
        reg3 = 0 #4 temp index
        reg4 = 0 #6 res etc..
        reg5 = 0 #8 temp
        reg6 = 0 #10 temp
        dummy_int = 0 #12
        X_list = [i for k, v in X.items() for i in (k, v)] #14-27

        bot = 0
        n = len(X_list) * 2
        
        mem = ZKList([reg1] + [bot] + [reg2] + [bot] + [reg3] 
                     + [bot] + [reg4] + [bot] + [reg5] + [bot] 
                     + [reg6] + [bot] + [dummy_int] + [bot] + X_list)
        
        program = [


            ## Set j = 1
            Instr(1, 12, 12, 12, 12, 12,  15, 2, 12, 0),    ## Step0   #6: Set 15 to idx2 (idx-j/reg2)

            ## Check if  mem[j+2] < mem[j] 
            Instr(5,  2, 12, 12, 12, 12, 12,  4, 12, 0),    ## Step1   #5: Copy idx2 (idx-j/reg2) to idx4 (temp-idx/reg3)
            Instr(2, 12, 12,  2, 12, 12, 12,  4, 12, 0),    ## Step2   #2: Add 2 to idx4 (temp-idx/reg3) = j+2
            Instr(6,  4, 12, 12, 12, 12, 12,  8, 12, 0),    ## Step3   #6: Set mem[mem[4]] (mem[j+2]) to idx8 (reg5)
            Instr(6,  2, 12, 12, 12, 12, 12, 10, 12, 0),    ## Step4   #6: Set mem[mem[2]] (mem[j]) to idx10 (temp1/reg6)
            Instr(3, 12, 10,  2, 12,  8, 12,  6, 12, 1),    ## Step5   #3: Compare mem[8] (reg5/mem[j+2]) < mem[10] (reg6/mem[j]) and assign result to idx6 (reg4)
            Instr(4, 12,  6,  1, 11, 12, 12, 12, 12, 2),    ## Step6   #4: Cond jump to Step7/17 if true/false

            ## Set mem[j] = mem[j+2] *Set temp1/reg6 = mem[j] is done at Step3
            Instr(7, 12, 12,  8, 12, 12, 12, 12,  2, 0),    ## Step7   #6: Set mem[idx8/reg5] (mem[j+2]) to mem[mem[idx2](=j)]
            
            ## Set mem[j+2] = temp1
            Instr(7, 12, 12, 10, 12, 12, 12, 12,  4, 0),    ## Step8   #6: Set mem[idx10](temp1/reg6) to mem[mem[idx4]] (mem[j+2])
            

            ## Set temp2 = mem[j-1]
            Instr(5,  2, 12, 12, 12, 12, 12,  4, 12, 0),    ## Step9   #5: Copy idx2 (idx-j/reg2) to idx4 (temp-idx/reg3)
            Instr(2, 12, 12,  1, 12, 12, 12,  4, 12, 1),    ## Step10  #2: Subtract 1 from idx4 (temp-idx/reg3) = j-1
            Instr(6,  4, 12, 12, 12, 12, 12,  8, 12, 0),    ## Step11  #6: Set mem[mem[4]] (mem[j-1]) to idx8 (temp2/reg5)

            ## Set mem[j-1] = mem[j+1]
            Instr(5,  2, 12, 12, 12, 12, 12, 10, 12, 0),    ## Step12  #5: Copy idx2 (idx-j/reg2) to idx10 (temp-idx2/reg6)
            Instr(2, 12, 12,  1, 12, 12, 12, 10, 12, 0),    ## Step13  #2: Add 1 to idx10 (temp-idx2/reg6) = j+1
            Instr(6, 10, 12, 12, 12, 12, 12,  6, 12, 0),    ## Step14  #6: Set mem[mem[10]] (mem[j+1]) to idx6
            Instr(7, 12, 12,  6, 12, 12, 12, 12,  4, 0),    ## Step15  #7: Set mem[idx6] (mem[j+1]) to mem[mem[idx4](=j-1)]
            
            ## Set mem[j+1] = temp2
            Instr(7, 12, 12,  8, 12, 12, 12, 12, 10, 0),    ## Step16  #7: Set mem[idx8/reg5] to mem[mem[idx10](=j+1)]

            ## Check if j < n-i-1 and determine to loop or end
            Instr(2, 12, 12,  2, 12, 12, 12,  2, 12, 0),    ## Step17  #2: Add 2 to idx2 (idx-j/reg2)
            Instr(1, 12, 12, 12, 12, 12,  n,  6, 12, 0),    ## Step18  #1: Set 28/n to idx 6 (reg4)
            Instr(2, 12, 12,  1, 12, 12, 12,  6, 12, 1),    ## Step19  #2: Subtract 1 from idx6 (reg4)
            Instr(2, 12, 12,  0, 12, 12, 12,  6, 12, 2),    ## Step20  #2: Subtract idx-i(idx0/reg1) from idx6 (reg4)
            Instr(3, 12,  6,  2, 12,  2, 12,  4, 12, 1),    ## Step21  #3: Compare idx6 (idx-j/reg2) < mem[p3] (n-i-1) and assign result to idx4 (reg3)
            Instr(4, 12,  4, 21,  1, 12, 12, 12, 12, 1),    ## Step22  #4: Cond jump to Step1/23 if true/false

            ## Check if i < n
            Instr(2, 12, 12,  2, 12, 12, 12,  0, 12, 0),     ## Step23  #2: Add 2 to idx0 (idx-i/reg1)
            Instr(3, 12, 12,  2,  n,  0, 12,  4, 12, 0),     ## Step24  #3: Compare idx0 (idx-i/reg1) < n (=28) and assign result to idx4 (reg3)
            Instr(4, 12,  4, 25,  1, 12, 12, 12, 12, 1),     ## Step25  #4: Cond jump to Step0/26 if true/false
                    

            # END
            Instr(100, 12, 12, 12, 12, 12, 12, 12, 12, 0),   ## Step26  #100: Terminal
        ]
        pro_prog = make_program(program)

        pc = 0
        weight = 0
        for i in range(n_iter):
            pc, weight = step(pro_prog, pc, mem, weight)

        prod_Y = reveal(mem, 14, len(mem))
        print('\nprod_Y:', prod_Y)

        res = mux(exp_Y == prod_Y,
                    mux(weight <= threshold, SecretInt(0), SecretInt(1))
                    , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)


        # Reproducer
        reg1 = 1 #0 i
        reg2 = 0 #2 j
        reg3 = 0 #4 temp index
        reg4 = 0 #6 res etc..
        reg5 = 0 #8 temp
        reg6 = 0 #10 temp
        dummy_int = 0 #12
        bg_list = [string_to_int(i) for k, v in bg.items() for i in (k, v)] #14-23
        honey_entries = [0] * 4 #24-27
        
        bot = 0
        n = 28

        repro_mem = ZKList([reg1] + [bot] + [reg2] + [bot] + [reg3] 
                           + [bot] + [reg4] + [bot] + [reg5] + [bot] 
                           + [reg6] + [bot] + [dummy_int] + [bot] + bg_list + honey_entries)

        hc0 = string_to_int('6')
        hc1 = string_to_int('111-666-6666')
        hc2 = string_to_int('7')
        hc3 = string_to_int('222-777-7777')

        program = [

            ## Hard-code Honey Entries
            Instr(1, 12, 12, 12, 12, 12,hc0, 24, 12, 0),    ## Step0   #6: Set hc1 to mem[24]
            Instr(1, 12, 12, 12, 12, 12,hc1, 25, 12, 0),    ## Step1   #6: Set hc2 to mem[25]
            Instr(1, 12, 12, 12, 12, 12,hc2, 26, 12, 0),    ## Step2   #6: Set hc3 to mem[26]
            Instr(1, 12, 12, 12, 12, 12,hc3, 27, 12, 0),    ## Step3   #6: Set hc4 to mem[27]


            ## Set j = 1
            Instr(1, 12, 12, 12, 12, 12,  15, 2, 12, 0),    ## Step4   #6: Set 15 to idx2 (idx-j/reg2)

            ## Check if  mem[j+2] < mem[j] 
            Instr(5,  2, 12, 12, 12, 12, 12,  4, 12, 0),    ## Step5   #5: Copy idx2 (idx-j/reg2) to idx4 (temp-idx/reg3)
            Instr(2, 12, 12,  2, 12, 12, 12,  4, 12, 0),    ## Step6   #2: Add 2 to idx4 (temp-idx/reg3) = j+2
            Instr(6,  4, 12, 12, 12, 12, 12,  8, 12, 0),    ## Step7   #6: Set mem[mem[4]] (mem[j+2]) to idx8 (reg5)
            Instr(6,  2, 12, 12, 12, 12, 12, 10, 12, 0),    ## Step8   #6: Set mem[mem[2]] (mem[j]) to idx10 (temp1/reg6)
            Instr(3, 12, 10,  2, 12,  8, 12,  6, 12, 1),    ## Step9   #3: Compare mem[8] (reg5/mem[j+2]) < mem[10] (reg6/mem[j]) and assign result to idx6 (reg4)
            Instr(4, 12,  6,  1, 11, 12, 12, 12, 12, 2),    ## Step10  #4: Cond jump to Step11/21 if true/false

            ## Set mem[j] = mem[j+2] *Set temp1/reg6 = mem[j] is done at Step3
            Instr(7, 12, 12,  8, 12, 12, 12, 12,  2, 0),    ## Step11   #6: Set mem[idx8/reg5] (mem[j+2]) to mem[mem[idx2](=j)]
            
            ## Set mem[j+2] = temp1
            Instr(7, 12, 12, 10, 12, 12, 12, 12,  4, 0),    ## Step12   #6: Set mem[idx10](temp1/reg6) to mem[mem[idx4]] (mem[j+2])
            

            ## Set temp2 = mem[j-1]
            Instr(5,  2, 12, 12, 12, 12, 12,  4, 12, 0),    ## Step13  #5: Copy idx2 (idx-j/reg2) to idx4 (temp-idx/reg3)
            Instr(2, 12, 12,  1, 12, 12, 12,  4, 12, 1),    ## Step14  #2: Subtract 1 from idx4 (temp-idx/reg3) = j-1
            Instr(6,  4, 12, 12, 12, 12, 12,  8, 12, 0),    ## Step15  #6: Set mem[mem[4]] (mem[j-1]) to idx8 (temp2/reg5)

            ## Set mem[j-1] = mem[j+1]
            Instr(5,  2, 12, 12, 12, 12, 12, 10, 12, 0),    ## Step16  #5: Copy idx2 (idx-j/reg2) to idx10 (temp-idx2/reg6)
            Instr(2, 12, 12,  1, 12, 12, 12, 10, 12, 0),    ## Step17  #2: Add 1 to idx10 (temp-idx2/reg6) = j+1
            Instr(6, 10, 12, 12, 12, 12, 12,  6, 12, 0),    ## Step18  #6: Set mem[mem[10]] (mem[j+1]) to idx6
            Instr(7, 12, 12,  6, 12, 12, 12, 12,  4, 0),    ## Step19  #7: Set mem[idx6] (mem[j+1]) to mem[mem[idx4](=j-1)]
            
            ## Set mem[j+1] = temp2
            Instr(7, 12, 12,  8, 12, 12, 12, 12, 10, 0),    ## Step20  #7: Set mem[idx8/reg5] to mem[mem[idx10](=j+1)]

            ## Check if j < n-i-1 and determine to loop or end
            Instr(2, 12, 12,  2, 12, 12, 12,  2, 12, 0),    ## Step21  #2: Add 2 to idx2 (idx-j/reg2)
            Instr(1, 12, 12, 12, 12, 12,  n,  6, 12, 0),    ## Step22  #1: Set 28/n to idx 6 (reg4)
            Instr(2, 12, 12,  1, 12, 12, 12,  6, 12, 1),    ## Step23  #2: Subtract 1 from idx6 (reg4)
            Instr(2, 12, 12,  0, 12, 12, 12,  6, 12, 2),    ## Step24  #2: Subtract idx-i(idx0/reg1) from idx6 (reg4)
            Instr(3, 12,  6,  2, 12,  2, 12,  4, 12, 1),    ## Step25  #3: Compare idx6 (idx-j/reg2) < mem[p3] (n-i-1) and assign result to idx4 (reg3)
            Instr(4, 12,  4, 21,  1, 12, 12, 12, 12, 1),    ## Step26  #4: Cond jump to Step5/27 if true/false

            ## Check if i < n
            Instr(2, 12, 12,  2, 12, 12, 12,  0, 12, 0),     ## Step27  #2: Add 2 to idx0 (idx-i/reg1)
            Instr(3, 12, 12,  2,  n,  0, 12,  4, 12, 0),     ## Step28  #3: Compare idx0 (idx-i/reg1) < n (=28) and assign result to idx4 (reg3)
            Instr(4, 12,  4, 25,  1, 12, 12, 12, 12, 1),     ## Step29  #4: Cond jump to Step4/30 if true/false
                    

            # END
            Instr(100, 12, 12, 12, 12, 12, 12, 12, 12, 0),   ## Step30  #100: Terminal
        ]

        repro_prog = make_program(program)

        pc = 0
        weight = 0
        for i in range(n_iter):
            pc, weight = step(repro_prog, pc, repro_mem, weight)

        repro_Y = reveal(repro_mem, 14, 27)
        print('\nreprod_Y:', repro_Y)

        res = mux(exp_Y == repro_Y,
                    mux(weight <= threshold, SecretInt(0), SecretInt(1))
                    , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)


if __name__ == "__main__":
    main()