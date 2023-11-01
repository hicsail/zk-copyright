from picozk import *
from .datatypes import Program, Instr


# Fetch an instruction from a program
def fetch(prog: Program, pc: SecretInt):
    return Instr(prog.opcode[pc],
                 prog.src1[pc],
                 prog.src2[pc],
                 prog.src3[pc],
                 prog.src4[pc],
                 prog.src5[pc],
                 prog.src6[pc],
                 prog.dest[pc],
                 prog.s_dest[pc],
                 prog.imm[pc])


def step(prog: Program, pc: int, mem: list, weight: int):

    instr = fetch(prog, pc)
    p1 = instr.src1
    p2 = instr.src2
    p3 = instr.src3
    p4 = instr.src4
    p5 = instr.src5
    p6 = instr.src6
    des = instr.dest
    s_des = instr.s_dest
    imm =  instr.imm
    new_pc = pc


    # 1. set p3 at mem[des]
    '''
        p6: const to set

        ops: mem[des] = p6
            #This does not support list to list assignment or string/char to string/char
    '''

    mem[des] = mux(instr.opcode == 1, p6, mem[des])
        

    # 2. add/subract const/mem[val] to des
    '''
        p3: value to increment by

        ops: mem[des] += p3
    '''

    mem[des] =  mux(instr.opcode == 2, mux(imm==0, mem[des] + p3,  
                                           mux(imm==1, mem[des] - p3, 
                                               mux(imm==2, mem[des] - mem[p3], mem[des]))), 
                                       mem[des])

    # 3. compare value in one index with const
    '''
        p2 mem address to compare (imm==1)
        p3: comparison type
        p4: const to compare (imm==0) 
        p5: element to compare

        ops: 
            if imm == 0:
                comp = p4
            elif imm == 1:
                comp = mem[p2]

            if p3 ==0:
                mem[des] = (mem[p5] == comp)
            elif p3 ==2:
                mem[des] = (mem[p5] < comp)
    '''
        
    comp = mux(instr.opcode == 3, mux(imm == 0, p4, mux(imm == 1, mem[p2], 500000)), 500000)
    
    mem[des] = mux(instr.opcode == 3,
                   mux(p3 == 0, mux(mem[p5] == comp, 1, 0),
                            mux(p3 == 2, mux(mem[p5] < comp, 1, 0),
                                    mem[des])), mem[des])
                                    


    # 4/100. jump or cond-jump/terminal
    '''
        p2: where condition is saved (im==1)
        p3: pc shift always (imm==0)/if True(imm==1)
        p4: pc shift if False

        ops: 
            if imm == 0:
                return new_pc + p3, weight +1
            elif imm == 1:
                mem[p2]==True:
                    return new_pc - p3, weight +1
                else:
                    return new_pc + p4, weight +1
            elif imm == 2:
                mem[p2]==True:
                    return new_pc + p3, weight +1
                else:
                    return new_pc + p4, weight +1
    '''
    new_pc = mux(instr.opcode == 0, new_pc,
                mux(instr.opcode == 4,
                    mux(imm == 0, new_pc + p3,
                        mux(imm == 1,
                            mux(mem[p2]==True, new_pc - p3, new_pc + p4), 
                            mux(mem[p2]==True, new_pc + p3, new_pc + p4) #if imm == 2
                            )
                        ),
                new_pc+1))


    # 5. Copy val to register
    '''
        p1: address of index of memory

        ops: mem[des] = mem[p1]
    '''

    mem[des] = mux(instr.opcode == 5, mem[p1], mem[des])


    # 6. Access list by pointer saved in register
    '''
        p1: address of index of memory

        ops: mem[des] = mem[mem[p1]]
    '''

    mem[des] = mux(instr.opcode == 6, mem[mem[p1]], mem[des])


    # 7. Copy value to a dest at const pointer

    '''
        p3: any memory address
        ops: mem[mem[s_des]] = mem[mem[p3]]
                
    '''

    mem[mem[s_des]] = mux(instr.opcode == 7, mem[p3], mem[mem[s_des]])


    '''
    Weights
        0   Terminal (weight => 0)
        1	Set const (weight => 1)
        2	Add/Sub (weight => 2)
        3	compare vals (weight => 2)
        4	Jump (weight => 2)
        5	Copy val by const (weight => 1)
        6	Copy val by pointer in memory (weight => 2)
        7	Copy value to a dest pointed by a pointer in memory (weight => 2)
    '''
                    # 0  1  2  3  4  5  6  7
    weights = ZKList([0, 1, 2, 2, 2, 1, 2, 2])
    # weights = ZKList([0, 1, 1, 1, 1, 1, 1, 1])
    w = weights[instr.opcode]

    return new_pc, weight + w