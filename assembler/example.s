; example assembly source
start:
    nop                 ; no-op
    movi r4, smaller    ; test using label as immediate

    movi r4, 6
    movi r5, 4
    cmp r4, r5
    movi r6, greater
    mov rjmp, r6
    jcc 0b0000

smaller:
    add r4, r5
    movalu r4
    hlt

greater:
    sub r4, r5
    movalu r4
    hlt

