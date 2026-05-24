class OpcodeInfo:
    def __init__(self, opcode: int, steps: int, arity: int):
        self.opcode = opcode
        self.steps = steps
        self.arity = arity


OPCODES = {
    # TODO add the rest of the instructions
    'nop': OpcodeInfo(0x00, 1, 0),
    'hlt': OpcodeInfo(0x01, 1, 0),
    'mov': OpcodeInfo(0x06, 1, 2),
    'add': OpcodeInfo(0x10, 1, 2),
    'movalu': OpcodeInfo(0x1a, 1, 1),

    # TODO add the pseudo jump instructions
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
