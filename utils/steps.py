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


    # 1. set p4 at mem[des]
    '''
        p4: const to set

        ops: mem[des] = p4
            #This does not support list to list assignment or string/char to string/char
    '''

    mem[des] = mux(instr.opcode == 1, p4, mem[des])
        

    # 2. add/subract const/mem[val] to des
    '''
        p4: value to increment by

        ops: mem[des] += p4
    '''

    mem[des] =  mux(instr.opcode == 2, mux(imm==0, mem[des] + p4,  
                                           mux(imm==1, mem[des] - p4, 
                                               mux(imm==2, mem[des] - mem[p4], mem[des]))), 
                                       mem[des])

    # 3. compare value in one index with const
    '''
        p3 mem address to compare (imm==1)
        p4: comparison type
        p5: const to compare (imm==0) 
        p6: element to compare

        ops: 
            # Below is for int
            if imm == 0:
                comp = p5
            elif imm == 1:
                comp = mem[p3]

            # Below is for str
            if p4 ==0:
                mem[des] = (mem[p6] == comp)
            elif p4 ==2:
                mem[des] = (mem[p6] < comp)
    '''
        
    comp = mux(instr.opcode == 3, mux(imm == 0, p5, mux(imm == 1, mem[p3], 500000)), 500000)
    
    mem[des] = mux(instr.opcode == 3,
                   mux(p4 == 0, mux(mem[p6] == comp, 1, 0),
                            mux(p4 == 2, mux(mem[p6] < comp, 1, 0),
                                    mem[des])), mem[des])
                                    


    # 4/100. jump or cond-jump/terminal
    '''
        p3: where condition is saved (im==1)
        p4: pc shift always (imm==0)/if True(imm==1)
        p5: pc shift if False

        ops: 
            if imm == 0:
                return new_pc + p4, weight +1
            elif mem[p3]==True:
                return new_pc + p4, weight +1
            elif imm == 1:
                return new_pc + p5, weight +1
    '''
    new_pc = mux(instr.opcode == 100, new_pc,
                mux(instr.opcode == 4,
                    mux(imm == 0, p4,
                        mux(mem[p3]==True, p4, p5)),
                new_pc+1))


    # 5. Copy val to register
    '''
        p1: address of index of memory

        ops: mem[des] = mem[mem[p2]]
    '''

    mem[des] = mux(instr.opcode == 5, mem[p2], mem[des])


    # 6. Access list by pointer saved in register
    '''
        p1: address of index of memory

        ops: mem[des] = mem[mem[p2]]
    '''

    mem[des] = mux(instr.opcode == 6, mem[mem[p2]], mem[des])


    # 7. Set Value by const pointer

    '''
        p4: any memory address
                
    '''

    mem[mem[s_des]] = mux(instr.opcode == 7, mem[p4], mem[mem[s_des]])


    # 100. Terminal
    w = mux(instr.opcode == 100, 0, 1)

    return new_pc, weight + w