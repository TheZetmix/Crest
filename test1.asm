jmp main

main:
    mov f7, hsp
    
    push 10
    push 100
    
    pop r0
    pop r1
    add r0, r1
    push r0
    
    int 0x00
