import argparse

import constants


class InstructionError(Exception):
    """Exception raised for invalid assembly instructions."""
    pass


class Assembler:
    def __init__(self, file_path: str, debug_output: bool):
        self.file_path = file_path
        self.debug_output = debug_output
        self.machine_code = bytes()
        self.lines: list[str] = []
        self.labels: dict[str, int] = dict()
    
    def assemble(self) -> bytes:
        with open(self.file_path, 'r') as f:
            self.lines = f.readlines()
        
        self.run_first_pass()
        if self.debug_output:
            print(f"Collected labels: {self.labels}")

        self.run_second_pass()

        return self.machine_code
    
    def run_first_pass(self):
        """Collect labels and clean comments from self.lines."""

        position = 0
        transformed_lines: list[str] = []
        for line in self.lines:
            line = line.split(';', 1)[0]  # Remove ';' comments
            line = line.strip()
            if line == '':
                continue

            line_parts = line.split(' ', 1)
            instruction = line_parts[0].strip().lower()
            if instruction in constants.OPCODES:
                info = constants.OPCODES[instruction]
                position += info.steps * 2  # 2 bytes per instruction
                transformed_lines.append(line)
            elif (pos := line.find(':')) != 1:
                label = line[:pos]
                self.labels[label] = position
            else:
                raise InstructionError(f"No such instruction '{instruction}'") 

        self.lines = transformed_lines
    
    def run_second_pass(self):
        """Assemble instructions in self.lines."""

        for line in self.lines:
            line_parts = line.split(' ', 1)
            instruction = line_parts[0]
            args_str = line_parts[1] if len(line_parts) == 2 else ''
            args = args_str.split(',')

            # Clean up arguments
            instruction = instruction.strip().lower()
            args = [arg for arg in args if arg != '']  # Remove empty args
            args = [arg.strip().lower() for arg in args]

            if self.debug_output:
                print(f'Assembling instruction {instruction} with args {args}')
            self.assemble_instruction(instruction, args)            

    def assemble_instruction(self, instruction: str, args: list[str]):
        # TODO validate args for each instruction
        # TODO check for invalid instruction name
        # TODO ensure 0 <= arguments <= 255
        
        if instruction not in constants.OPCODES:
            raise InstructionError(f"No such instruction '{instruction}'")

        # Validate no. of arguments
        info = constants.OPCODES[instruction]
        if len(args) != info.arity:
            raise InstructionError(f'Instruction {instruction} takes {info.arity} arguments, but recieved {len(args)}')        
        
        if info.steps == 1 and info.arity == 0:
            # Instruction with no arguments.
            instruction_code = [info.opcode, 0x0]
        elif info.steps == 1 and info.arity == 1:
            # Single argument in the second byte.
            arg_1_raw = args[0]
            if arg_1_raw in constants.REGISTERS:
                arg_1 = constants.REGISTERS[arg_1_raw]
            elif arg_1_raw in self.labels:
                arg_1 = self.labels[arg_1_raw]
            else:
                arg_1 = int(arg_1_raw, 0)
            instruction_code = [info.opcode, arg_1]
        elif info.steps == 1 and info.arity == 2:
            # Two register arguments in the second byte.
            # TODO ensure arguments are registers
            # TODO ensure 0 <= register code <= 15
            arg_1 = constants.REGISTERS[args[0]]
            arg_2 = constants.REGISTERS[args[1]]
            args_combined = arg_1 << 4 | arg_2
            instruction_code = [info.opcode, args_combined]
        elif info.steps == 2 and info.arity == 2:
            # Two calls to the opcode, one for each byte argument.
            arg_1_raw, arg_2_raw = args[0], args[1]
            if arg_1_raw in constants.REGISTERS:
                arg_1 = constants.REGISTERS[arg_1_raw]
            elif arg_1_raw in self.labels:
                arg_1 = self.labels[arg_1_raw]
            else:
                arg_1 = int(arg_1_raw, 0)
        
            if arg_2_raw in constants.REGISTERS:
                arg_2 = constants.REGISTERS[arg_2_raw]
            elif arg_2_raw in self.labels:
                arg_2 = self.labels[arg_2_raw]
            else:
                arg_2 = int(arg_2_raw, 0)
            
            instruction_code = [info.opcode, arg_1, info.opcode, arg_2]
        else:
            assert False, f"Unhandled opcode configuration for '{instruction}': {info.steps=}, {info.arity=}"
        
        self.machine_code += bytes(instruction_code)


def write_binary_file(filename: str, code: bytes):
    with open(filename, 'wb') as f:
        f.write(code)


def write_text_file(filename: str, code: bytes):
    text = ''
    for i, byte in enumerate(code):
        translated = hex(byte)[2:]
        if len(translated) == 1:
            translated = '0' + translated  # Add the leading nibble
        text += translated
        if i % 2 == 1:
            text += '\n'  # Add newline every 2 bytes

    with open(filename, 'w') as f:
        f.write(text)


def main():
    parser = argparse.ArgumentParser(
        prog='Custom CPU Assembler',
        description='Assemble the custom CPU machine code from assembly source'
    )
    parser.add_argument('filename', help='Path to the assembly source file')
    parser.add_argument('-o', '--output-file', help='Path at which to write the output file')
    parser.add_argument('-t', '--output-text', action='store_true', help='Output a text file instead of a binary file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print debugging information for each instruction')
    args = parser.parse_args()
    if args.output_file is None:
        if args.output_text:
            args.output_file = 'out.txt'
        else:
            args.output_file = 'out.bin'
    
    assembler = Assembler(args.filename, args.verbose)
    code = assembler.assemble()

    if args.output_text:
        write_text_file(args.output_file, code)
    else:
        write_binary_file(args.output_file, code)


if __name__ == '__main__':
    main()
