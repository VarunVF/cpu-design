class OpcodeInfo:
    def __init__(self, opcode: int, steps: int, arity: int):
        self.opcode = opcode
        self.steps = steps
        self.arity = arity


OPCODES = {
    'nop': OpcodeInfo(0x00, 1, 0),
    'hlt': OpcodeInfo(0x01, 1, 0),
    'stri': OpcodeInfo(0x02, 2, 2),
    'movi': OpcodeInfo(0x03, 2, 2),
    'ldr': OpcodeInfo(0x04, 2, 2),
    'str': OpcodeInfo(0x05, 2, 2),
    'mov': OpcodeInfo(0x06, 1, 2),
    # 0x07 unused
    # 0x08 unused
    'jmp': OpcodeInfo(0x09, 1, 0),
    'cmp': OpcodeInfo(0x0a, 1, 2),
    'jcc': OpcodeInfo(0x0b, 1, 1),
    # 0x0c unused
    'call': OpcodeInfo(0x0d, 1, 1),
    'ret': OpcodeInfo(0x0e, 1, 0),
    # 0x0f unused
    'add': OpcodeInfo(0x10, 1, 2),
    'sub': OpcodeInfo(0x11, 1, 2),
    'shr': OpcodeInfo(0x12, 1, 1),
    'shl': OpcodeInfo(0x13, 1, 1),
    'and': OpcodeInfo(0x14, 1, 2),
    'or': OpcodeInfo(0x15, 1, 2),
    'not': OpcodeInfo(0x16, 1, 1),
    'mul': OpcodeInfo(0x17, 1, 2),
    'div': OpcodeInfo(0x18, 1, 2),
    'mod': OpcodeInfo(0x19, 1, 2),
    'movalu': OpcodeInfo(0x1a, 1, 1),
    # 0x1b to 0x1f unused

    # Macros for `jcc`
    'jg': OpcodeInfo(0x0b, 1, 1),
    'jl': OpcodeInfo(0x0b, 1, 1),
    'je': OpcodeInfo(0x0b, 1, 1),
}

JCC_MACROS = {
    #       NZCV flags
    'jg': 0b0010,
    'jl': 0b1000,
    'je': 0b0100,
}

REGISTERS = {
    'r0': 0, 'rsp': 0,
    'r1': 1, 'rpc': 1,
    'r2': 2, 'rjmp': 2,
    'r3': 3, 'rflags': 3,
    'r4': 4,
    'r5': 5,
    'r6': 6,
    'r7': 7,
    'r8': 8,
    'r9': 9,
    'r10': 10, 'ra': 10,
    'r11': 11, 'rb': 11,
    'r12': 12, 'rc': 12,
    'r13': 13, 'rd': 13,
    'r14': 14, 're': 14,
    'r15': 15, 'rf': 15,
}
