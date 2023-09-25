from picozk import *
from utils.datatypes import Instr
from utils.steps import step
from utils.functions import make_program, int_to_string, string_to_int


def make_X(bg, honey_entries):
    res = bg.copy()
    res.update(honey_entries)
    res = dict(sorted(res.items()))
    print("X", res, "\n")
    res = {string_to_int(k): string_to_int(v) for k, v in res.items()}
    return res


def reveal(res_list):
    # Convert the List to a String
    result_str = ""
    idx = 0
    res_list_size = 14
    while idx < res_list_size:
        # Convert each tuple to a string and add to result_str
        item_str = "(" + "'" + int_to_string(val_of(res_list[idx])) + "'" + ", " + "'" + int_to_string(val_of(res_list[idx+1])) + "'" + ")"
        if result_str:
            result_str += ", " + item_str
        else:
            result_str = item_str
        idx += 2
    return result_str



def main():

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

    X = make_X(bg, honey_entries)

    exp_Y = "('1', '111-111-1111'), ('6', '111-666-6666'), ('2', '222-222-2222'), ('7', '222-777-7777'), ('3', '333-333-3333'), ('4', '444-444-4444'), ('5', '555-555-5555')"
    print('exp_Y', exp_Y, '\n')

    p = pow(2,256) - pow(2,32) - pow(2,9) - pow(2,8) - pow(2,7) - pow(2,6) - pow(2,4) - 1
    n_iter = 1500
    n = 14
    threshold = 400 # The program has to be performed within this (weight < )

    with PicoZKCompiler('irs/picozk_test', field=[p], options=['ram']):

        # Producer
        X_list = [i for k, v in X.items() for i in (k, v)] #0-13
        reg1 = 1 #15 i
        reg2 = 0 #17 j
        reg3 = 0 #19 temp index
        reg4 = 0 #21 res etc..
        reg5 = 0 #23 temp
        reg6 = 0 #25 temp
        dummy_int = 0 #27

        bot = 0
        
        mem = ZKList(X_list + [bot] + [reg1] + [bot] + [reg2] + [bot] + [reg3] + [bot] + [reg4] + [bot] + [reg5] + [bot] + [reg6] + [bot] + [dummy_int])
        
        program = [


            ## Set j = 1
            Instr(1, 27, 27, 27, 27, 27,  1, 17, 27, 0),    ## Step0   #6: Set 1 idx17 (idx-j/reg2)

            ## Check if  mem[j+2] < mem[j] 
            Instr(5, 17, 27, 27, 27, 27, 27, 19, 27, 0),    ## Step1   #5: Copy idx17 (idx-j/reg2) to idx19 (temp-idx/reg3)
            Instr(2, 27, 27,  2, 27, 27, 27, 19, 27, 0),    ## Step2   #2: Add 2 to idx19 (temp-idx/reg3) = j+2
            Instr(6, 19, 27, 27, 27, 27, 27, 23, 27, 0),    ## Step3   #6: Set mem[mem[19]] (mem[j+2]) to idx23 (reg5)
            Instr(6, 17, 27, 27, 27, 27, 27, 25, 27, 0),    ## Step4   #6: Set mem[mem[17]] (mem[j]) to idx25 (temp1/reg6)
            Instr(3, 27, 25,  2, 27, 23, 27, 21, 27, 1),    ## Step5   #3: Compare mem[23] (reg5/mem[j+2]) < mem[25] (reg6/mem[j]) and assign result to idx21 (reg4)
            Instr(4, 27, 21,  1, 11, 27, 27, 27, 27, 2),    ## Step6   #4: Cond jump to Step7/17 if true/false

            ## Set mem[j] = mem[j+2] *Set temp1/reg6 = mem[j] is done at Step3
            Instr(7, 27, 27, 23, 27, 27, 27, 27, 17, 0),    ## Step7   #6: Set mem[idx23/reg5] (mem[j+2]) to mem[mem[idx17](=j)]
            
            ## Set mem[j+2] = temp1
            Instr(7, 27, 27, 25, 27, 27, 27, 27, 19, 0),    ## Step8   #6: Set mem[idx25](temp1/reg6) to mem[mem[idx19]] (mem[j+2])
            

            ## Set temp2 = mem[j-1]
            Instr(5, 17, 27, 27, 27, 27, 27, 19, 27, 0),    ## Step9  #5: Copy idx17 (idx-j/reg2) to idx19 (temp-idx/reg3)
            Instr(2, 27, 27,  1, 27, 27, 27, 19, 27, 1),    ## Step10  #2: Subtract 1 from idx19 (temp-idx/reg3) = j-1
            Instr(6, 19, 27, 27, 27, 27, 27, 23, 27, 0),    ## Step11  #6: Set mem[mem[19]] (mem[j-1]) to idx23 (temp2/reg5)

            ## Set mem[j-1] = mem[j+1]
            Instr(5, 17, 27, 27, 27, 27, 27, 25, 27, 0),    ## Step12  #5: Copy idx17 (idx-j/reg2) to idx25 (temp-idx2/reg6)
            Instr(2, 27, 27,  1, 27, 27, 27, 25, 27, 0),    ## Step13  #2: Add 1 to idx25 (temp-idx2/reg6) = j+1
            Instr(6, 25, 27, 27, 27, 27, 27, 21, 27, 0),    ## Step14  #6: Set mem[mem[25]] (mem[j+1]) to idx21
            Instr(7, 27, 27, 21, 27, 27, 27, 27, 19, 0),    ## Step15  #7: Set mem[idx21] (mem[j+1]) to mem[mem[idx19](=j-1)]
            
            ## Set mem[j+1] = temp2
            Instr(7, 27, 27, 23, 27, 27, 27, 27, 25, 0),    ## Step16  #7: Set mem[idx23/reg5] to mem[mem[idx25](=j+1)]

            ## Check if j < n-i-2 and determine to loop or end
            Instr(2, 27, 27,  2, 27, 27, 27, 17, 27, 0),    ## Step17  #2: Add 2 to idx17 (idx-j/reg2)
            Instr(1, 27, 27, 27, 27, 27,  n, 21, 27, 0),    ## Step18  #1: Set 14 to idx 21 (reg4)
            Instr(2, 27, 27,  1, 27, 27, 27, 21, 27, 1),    ## Step19  #2: Subtract 1 from idx21 (reg4)
            Instr(2, 27, 27, 15, 27, 27, 27, 21, 27, 2),    ## Step20  #2: Subtract idx-i(idx15/reg1) from idx21 (reg4)
            Instr(3, 27, 21,  2, 27, 17, 27, 19, 27, 1),    ## Step21  #3: Compare idx17 (idx-j/reg2) < mem[p3] (n-i-1) and assign result to idx19 (reg3)
            Instr(4, 27, 19, 21,  1, 27, 27, 27, 27, 1),    ## Step22  #4: Cond jump to Step1/23 if true/false

            ## Check if i < n
            Instr(2, 27, 27,  2, 27, 27, 27, 15, 27, 0),    ## Step23  #2: Add 2 to idx15 (idx-i/reg1)
            Instr(3, 27, 27,  2,  n, 15, 27, 19, 27, 0),    ## Step24  #3: Compare idx15 (idx-i/reg1) < n)(=14) and assign result to idx19 (reg3)
            Instr(4, 27, 19, 25,  1, 27, 27, 27, 27, 1),    ## Step25  #4: Cond jump to Step0/26 if true/false
                    

            # END
            Instr(100, 27, 27, 27, 27, 27, 27, 27, 27, 0),   ## Step26  #100: Terminal
        ]
        pro_prog = make_program(program)

        pc = 0
        weight = 0
        for i in range(n_iter):
            pc, weight = step(pro_prog, pc, mem, weight)

        prod_Y = reveal(mem)
        print('prod_Y:', prod_Y, '\n')

        res = mux(exp_Y == prod_Y,
                    mux(weight <= threshold, SecretInt(0), SecretInt(1))
                    , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)


        # Reproducer
        bg_list = [string_to_int(i) for k, v in bg.items() for i in (k, v)] #0-9
        honey_entries = [0] * 4 #10-13
        
        reg1 = 1 #15 i
        reg2 = 0 #17 j
        reg3 = 0 #19 temp index
        reg4 = 0 #21 res etc..
        reg5 = 0 #23 temp
        reg6 = 0 #25 temp
        dummy_int = 0 #27
        
        bot = 0

        repro_mem = ZKList(bg_list + honey_entries + [bot] + [reg1] + [bot] + [reg2] + [bot] + [reg3] + [bot] + [reg4] + [bot] + [reg5] + [bot] + [reg6] + [bot] + [dummy_int])

        hc1 = string_to_int('6')
        hc2 = string_to_int('111-666-6666')
        hc3 = string_to_int('7')
        hc4 = string_to_int('222-777-7777')

        program = [

            ## Hard-code Honey Entries
            Instr(1, 27, 27, 27, 27, 27,hc1, 10, 27, 0),    ## Step0   #6: Set hc1 to mem[10]
            Instr(1, 27, 27, 27, 27, 27,hc2, 11, 27, 0),    ## Step1   #6: Set hc2 to mem[11]
            Instr(1, 27, 27, 27, 27, 27,hc3, 12, 27, 0),    ## Step2   #6: Set hc3 to mem[12]
            Instr(1, 27, 27, 27, 27, 27,hc4, 13, 27, 0),    ## Step3   #6: Set hc4 to mem[13]


            ## Set j = 1
            Instr(1, 27, 27, 27, 27, 27,  1, 17, 27, 0),    ## Step4   #6: Set 1 idx17 (idx-j/reg2)

            ## Check if  mem[j+2] < mem[j] 
            Instr(5, 17, 27, 27, 27, 27, 27, 19, 27, 0),    ## Step5   #5: Copy idx17 (idx-j/reg2) to idx19 (temp-idx/reg3)
            Instr(2, 27, 27,  2, 27, 27, 27, 19, 27, 0),    ## Step6   #2: Add 2 to idx19 (temp-idx/reg3) = j+2
            Instr(6, 19, 27, 27, 27, 27, 27, 23, 27, 0),    ## Step7   #6: Set mem[mem[19]] (mem[j+2]) to idx23 (reg5)
            Instr(6, 17, 27, 27, 27, 27, 27, 25, 27, 0),    ## Step8   #6: Set mem[mem[17]] (mem[j]) to idx25 (temp1/reg6)
            Instr(3, 27, 25,  2, 27, 23, 27, 21, 27, 1),    ## Step9   #3: Compare mem[23] (reg5/mem[j+2]) < mem[25] (reg6/mem[j]) and assign result to idx21 (reg4)
            Instr(4, 27, 21,  1, 11, 27, 27, 27, 27, 2),    ## Step10  #4: Cond jump to Step11/21 if true/false

            ## Set mem[j] = mem[j+2] *Set temp1/reg6 = mem[j] is done at Step3
            Instr(7, 27, 27, 23, 27, 27, 27, 27, 17, 0),    ## Step11   #6: Set mem[idx23/reg5] (mem[j+2]) to mem[mem[idx17](=j)]
            
            ## Set mem[j+2] = temp1
            Instr(7, 27, 27, 25, 27, 27, 27, 27, 19, 0),    ## Step12   #6: Set mem[idx25](temp1/reg6) to mem[mem[idx19]] (mem[j+2])
            

            ## Set temp2 = mem[j-1]
            Instr(5, 17, 27, 27, 27, 27, 27, 19, 27, 0),    ## Step13  #5: Copy idx17 (idx-j/reg2) to idx19 (temp-idx/reg3)
            Instr(2, 27, 27,  1, 27, 27, 27, 19, 27, 1),    ## Step14  #2: Subtract 1 from idx19 (temp-idx/reg3) = j-1
            Instr(6, 19, 27, 27, 27, 27, 27, 23, 27, 0),    ## Step15  #6: Set mem[mem[19]] (mem[j-1]) to idx23 (temp2/reg5)

            ## Set mem[j-1] = mem[j+1]
            Instr(5, 17, 27, 27, 27, 27, 27, 25, 27, 0),    ## Step16  #5: Copy idx17 (idx-j/reg2) to idx25 (temp-idx2/reg6)
            Instr(2, 27, 27,  1, 27, 27, 27, 25, 27, 0),    ## Step17  #2: Add 1 to idx25 (temp-idx2/reg6) = j+1
            Instr(6, 25, 27, 27, 27, 27, 27, 21, 27, 0),    ## Step18  #6: Set mem[mem[25]] (mem[j+1]) to idx21
            Instr(7, 27, 27, 21, 27, 27, 27, 27, 19, 0),    ## Step19  #7: Set mem[idx21] (mem[j+1]) to mem[mem[idx19](=j-1)]
            
            ## Set mem[j+1] = temp2
            Instr(7, 27, 27, 23, 27, 27, 27, 27, 25, 0),    ## Step20  #7: Set mem[idx23/reg5] to mem[mem[idx25](=j+1)]

            ## Check if j < n-i-2 and determine to loop or end
            Instr(2, 27, 27,  2, 27, 27, 27, 17, 27, 0),    ## Step21  #2: Add 2 to idx17 (idx-j/reg2)
            Instr(1, 27, 27, 27, 27, 27,  n, 21, 27, 0),    ## Step22  #1: Set 14 to idx 21 (reg4)
            Instr(2, 27, 27,  1, 27, 27, 27, 21, 27, 1),    ## Step23  #2: Subtract 1 from idx21 (reg4)
            Instr(2, 27, 27, 15, 27, 27, 27, 21, 27, 2),    ## Step24  #2: Subtract idx-i(idx15/reg1) from idx21 (reg4)
            Instr(3, 27, 21,  2, 27, 17, 27, 19, 27, 1),    ## Step25  #3: Compare idx17 (idx-j/reg2) < mem[p3] (n-i-1) and assign result to idx19 (reg3)
            Instr(4, 27, 19, 21,  1, 27, 27, 27, 27, 1),    ## Step26  #4: Cond jump to Step5/27 if true/false

            ## Check if i < n
            Instr(2, 27, 27,  2, 27, 27, 27, 15, 27, 0),     ## Step27  #2: Add 2 to idx15 (idx-i/reg1)
            Instr(3, 27, 27,  2,  n, 15, 27, 19, 27, 0),     ## Step28  #3: Compare idx15 (idx-i/reg1) < n)(=14) and assign result to idx19 (reg3)
            Instr(4, 27, 19, 25,  1, 27, 27, 27, 27, 1),     ## Step29  #4: Cond jump to Step4/30 if true/false
                    

            # END
            Instr(100, 27, 27, 27, 27, 27, 27, 27, 27, 0),   ## Step30  #100: Terminal
        ]

        repro_prog = make_program(program)

        pc = 0
        weight = 0
        for i in range(n_iter):
            pc, weight = step(repro_prog, pc, repro_mem, weight)

        repro_Y = reveal(repro_mem)
        print('reprod_Y:', repro_Y, '\n')

        res = mux(exp_Y == repro_Y,
                    mux(weight <= threshold, SecretInt(0), SecretInt(1))
                    , SecretInt(1))
        assert0(res)
        assert(val_of(res)==0)


if __name__ == "__main__":
    main()