start:
    ; normal jcc call to check "if greater than"
    movi rjmp, label
    jcc 0b0010

    ; macro version
    ; emits the same machine code
    jg label

label:
    hlt
