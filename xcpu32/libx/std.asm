jmp LIBXSTD_END

define malloc(dest, size) mov dest, size \
                          ffp dest

define .BYTE  1
define .WORD  2
define .DWORD 4

define .BYTE_MAX  0xff
define .WORD_MAX  0xffff
define .DWORD_MAX 0xffffffff

puts:
    pop r10
    pusha
.puts_0000:
    movb r31, *r10
    int 0x10
    inc r10
    cmp r31, 0
    jne .puts_0000
    popa
    ret

reads:
    pusha
    int 0x05
    mov r7, r3
    mov r10, r11
.reads_0000:
    int 0x11
    int 0x10
    movb *r10, r31
    cmp r31, 0x08
    je .reads_0001
    jne .reads_0002
.reads_0001:
    int 0x05
    cmp r3, r7
    jl .reads_0002
    mov r31, 0x09
    int 0x10
    mov r31, 0x20
    int 0x10
    mov r31, 0x09
    int 0x10
    mov *r10, 0x00
    sub r10, 2
.reads_0002:
    inc r10
    cmp r31, 0x0d 
    jne .reads_0000
    mov r31, 0x0a
    int 0x10
    movb *r10, 0
    popa
    ret

itos:
    pop r0
    mov r16, 32
    ffp r16
    int 0x20
    push r16
    ret

stoi:
    pop r10
    int 0x21
    push r0
    ret

freestr:
    pop r0
    pusha
    mov r1, r0
.freestr_0001:
    movb r31, *r1
    inc r1
    cmp r31, 0
    jne .freestr_0001
.freestr_0002:
    mov *r0, 0
    inc r0
    cmp r0, r1
    jne .freestr_0002
    popa
    ret

LIBXSTD_END:
