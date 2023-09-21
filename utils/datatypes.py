from dataclasses import dataclass
from picozk import *

@dataclass
class Instr:
    opcode: int
    src1: int
    src2: int
    src3: int
    src4: int
    src5: int
    dest: int
    s_dest: int
    imm: int

@dataclass
class Program:
    opcode: ZKList
    src1: ZKList
    src2: ZKList
    src3: ZKList
    src4: ZKList
    src5: ZKList
    dest: ZKList
    s_dest: ZKList
    imm: ZKList