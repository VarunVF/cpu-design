import argparse

import constants


class InstructionError(Exception):
    """Exception raised for invalid assembly instructions."""
    pass


class ArgumentError(Exception):
    """Exception raised for invalid instruction arguments."""
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
            arg_1 = self.resolve_argument(args[0])
            if instruction in constants.JCC_MACROS:
                instruction_code = [
                    constants.OPCODES['movi'].opcode,
                    constants.REGISTERS['rjmp'],
                    constants.OPCODES['movi'].opcode,
                    arg_1,
                    constants.OPCODES['jcc'].opcode,
                    constants.JCC_MACROS[instruction]  # flags
                ]
            else:
                instruction_code = [info.opcode, arg_1]
        elif info.steps == 1 and info.arity == 2:
            # Two register arguments in the second byte.
            for arg in args:
                if arg not in constants.REGISTERS:
                    raise ArgumentError(f"Instruction '{instruction}' expected a register argument, not '{arg}'")

            arg_1 = constants.REGISTERS[args[0]]
            arg_2 = constants.REGISTERS[args[1]]
            args_combined = arg_1 << 4 | arg_2
            instruction_code = [info.opcode, args_combined]
        elif info.steps == 2 and info.arity == 2:
            # Two calls to the opcode, one for each byte argument.
            arg_1 = self.resolve_argument(args[0])
            arg_2 = self.resolve_argument(args[1])
            instruction_code = [info.opcode, arg_1, info.opcode, arg_2]
        else:
            assert False, f"Unhandled opcode configuration for '{instruction}': {info.steps=}, {info.arity=}"
        
        self.machine_code += bytes(instruction_code)
    
    def resolve_argument(self, argument: str) -> int:
        if argument in constants.REGISTERS:
            return constants.REGISTERS[argument]
        elif argument in self.labels:
            return self.labels[argument]
        else:
            try:
                number = int(argument, 0)
            except ValueError:
                raise ArgumentError(f"Invalid numeric literal '{argument}'")
            
            if not -128 <= number <= 255:
                raise ArgumentError(f"Numeric literal '{argument}' is out of range for 8-bit representation")

            # Convert to 2's complement
            return number & 0xFF


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
