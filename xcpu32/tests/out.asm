main:
    mov *0x00, 0x05
    mov *0x04, 0x05
    mov *0x08, 0x02
    push *0
    push *4
    pop r1
    pop r0
    add r0, r1
    push r0
    push *8
    pop r1
    pop r0
    sub r0, r1
    push r0
    pop r0
    mov *0x0c, r0
    int 0x00
