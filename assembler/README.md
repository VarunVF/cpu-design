# Assembler

Aim to provide 2 output formats:
- Binary
- Text form of the hex bytes

We could start with raw binary, then add the text option later.

## Notes

Instead of a strict one to one mapping between assembly lines and instructions...
```asm
; Loading 5 into r0
movi r0    ; 03 00
movi 5     ; 03 05
```

...we allow the assembler to internally generate 2 instructions when it sees 2 arguments if required, and the programmer only needs to write 1.
```asm
movi r0, 5
```

Also, for conditional jumps, instead of passing the flags to check directly...
```asm
jcc 4, label
```

...we define "macros" like `jz`, `je`, `jg`, `jl`, etc. which expand to the appropriate `jcc` call.
```asm
jz label
```

We decided on this approach to make it easier to write programs.
