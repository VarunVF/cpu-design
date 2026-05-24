# Assembler

The assembler provides 2 output formats:
- Binary
- Text form of the hex bytes (using the `-t` option)

## Notes

Instead of a strict one to one mapping between assembly lines and instructions...
```asm
; Loading 5 into r0
movi r0    ; 03 00
movi 5     ; 03 05
```

...the assembler internally generates 2 instructions when it sees 2 arguments if required, and the programmer only needs to write 1.
```asm
movi r0, 5
```

Also, for conditional jumps, instead of passing the flags to check directly...
```asm
movi rjmp, label
jcc 0b0010
```

...we define "macros" like `je`, `jg`, and `jl` which expand to the appropriate `movi` and `jcc` calls.
```asm
jg label
```

We decided on this approach to make it easier to write programs.
