from picozk import *
from .datatypes import Program


def make_program(prog):
    length = len(prog)
    opcode = ZKList([0 for _ in range(length)])
    src1 = ZKList([0 for _ in range(length)])
    src2 = ZKList([0 for _ in range(length)])
    src3 = ZKList([0 for _ in range(length)])
    src4 = ZKList([0 for _ in range(length)])
    src5 = ZKList([0 for _ in range(length)])
    src6 = ZKList([0 for _ in range(length)])
    dest = ZKList([0 for _ in range(length)])
    s_dest = ZKList([0 for _ in range(length)])
    imm = ZKList([0 for _ in range(length)])

    for i, instr in enumerate(prog):
        opcode[i] = instr.opcode
        src1[i] = instr.src1
        src2[i] = instr.src2
        src3[i] = instr.src3
        src4[i] = instr.src4
        src5[i] = instr.src5
        src6[i] = instr.src6
        dest[i] = instr.dest
        s_dest[i] = instr.s_dest
        imm[i] = instr.imm

    return Program(opcode, src1, src2, src3, src4, src5, src6, dest, s_dest, imm)


def string_to_int(s):
    return int("".join(format(ord(char), "08b") for char in s), 2)


def int_to_string(n):
    binary_str = format(n, "b")
    binary_str = "0" * ((8 - len(binary_str) % 8) % 8) + binary_str
    return "".join(chr(int(binary_str[i : i + 8], 2)) for i in range(0, len(binary_str), 8))
