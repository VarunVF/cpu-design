# Custom CPU Design

Specifications:
- 8-bit registers
- 8-bit memory

## Registers

The flags register can be used like other registers, but is read-only.

| Register Code | Register Name(s) | Description     |
| ------------- | ---------------- | --------------- |
| 0             | `r0` / `rsp`     | Stack Pointer   |
| 1             | `r1` / `rpc`     | Program Counter |
| 2             | `r2` / `rjmp`    | Jump Register   |
| 3             | `r3` / `rflags`  | Flags Register  |
| 4-15          | `r4` - `r15`     | General Purpose |

## Instruction Format

Each instruction is 2 bytes wide.
The first 5 bits of the first byte represent the opcode.
The second byte is the argument.

## Quirks

For opcodes with 2 steps, the opcode must be called twice to provide 2 arguments.
For opcodes with 1 step but 2 (register) arguments, the first 4 bits are for the destination register and the next 4 bits are for the source register.

Register code 2 is the "jump register". When JUMP is called, the instruction pointer is set to the jump register.
The programmer must set the jump register to a valid address before calling JUMP.


## Opcode Table

| Opcode | Mnemonic      | Instruction          | No. of Steps | Argument 1 | Argument 2 |
| ------ | ------------- | -------------------- | ------------ | ---------- | ---------- |
| `0x00` | nop           | SPACE                | 1            | -          | -          |
| `0x01` | hlt           | HALT                 | 1            | -          | -          |
| `0x02` | stri          | -> RAM               | 2            | ADDRESS    | DATA       |
| `0x03` | movi          | -> REGISTER          | 2            | LOCATION   | DATA       |
| `0x04` | ldr           | RAM -> REGISTER      | 2            | ADDRESS    | REGISTER   |
| `0x05` | str           | REGISTER -> RAM      | 2            | REGISTER   | ADDRESS    |
| `0x06` | mov           | REGISTER -> REGISTER | 1            | REGISTER A | REGISTER B |
| `0x07` | -             | (UNUSED)             | -            | -          | -          |
| `0x08` | -             | (UNUSED)             | -            | -          | -          |
| `0x09` | jmp           | JUMP                 | 1            | -          | -          |
| `0x0a` | cmp           | COMPARE              | 1            | REGISTER A | REGISTER B |
| `0x0b` | jcc           | JUMP ON CONDITION    | 1            | FLAGS      | -          |
| `0x0c` | -             | (UNUSED)             | -            | -          |            |
| `0x0d` | call          | CALL                 | 1            | ADDRESS    | -          |
| `0x0e` | ret           | RETURN               | 1            | -          | -          |
| `0x0f` | -             | (UNUSED)             | -            | -          |            |
| `0x10` | add           | ADD                  | 1            | REGISTER A | REGISTER B |
| `0x11` | sub           | SUB                  | 1            | REGISTER A | REGISTER B |
| `0x12` | shr           | >>                   | 1            | REGISTER   | -          | 
| `0x13` | shl           | <<                   | 1            | REGISTER   | -          | 
| `0x14` | and           | AND                  | 1            | REGISTER A | REGISTER B |
| `0x15` | or            | OR                   | 1            | REGISTER A | REGISTER B |
| `0x16` | not           | NOT                  | 1            | REGISTER   | -          |
| `0x17` | mul           | MUL                  | 1            | REGISTER A | REGISTER B |
| `0x18` | div           | DIV                  | 1            | REGISTER A | REGISTER B |
| `0x19` | mod           | MOD                  | 1            | REGISTER A | REGISTER B |
| `0x1a` | movalu        | STORE FROM ALU       | 1            | REGISTER A | -          |
| `0x1b` | -             | (UNUSED)             | -            | -          | -          |
| `0x1c` | -             | (UNUSED)             | -            | -          | -          |
| `0x1d` | -             | (UNUSED)             | -            | -          | -          |
| `0x1e` | -             | (UNUSED)             | -            | -          | -          |
| `0x1f` | -             | (UNUSED)             | -            | -          | -          |

Example:

```asm
shr r2
; 12 02
movi r0, 5
; 03 00
; 03 05
movi r1, 5
; 03 01
; 03 05
cmp r0, r1
; 0a 01
```
