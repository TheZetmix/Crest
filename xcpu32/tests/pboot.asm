jmp boot

puts:
    pop r10
    lea r10, r10
    pusha
.puts_0000:
    mov r31, *r10
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
.reads_0000:
    int 0x11
    int 0x10
    mov *r10, r31
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
    mov *r10, 0
    popa
    ret

boot:
    int 0x15
    push boot_msg_welcome
    call puts
boot_0000:
    push boot_greet
    call puts
    mov r10, boot_input
    call reads
    
    lea r11, boot_cmd_exit
    int 0x22
    je boot_exec_exit
    
    lea r11, boot_cmd_help
    int 0x22
    je boot_exec_help

    lea r11, boot_cmd_load
    int 0x22
    je boot_exec_load
    
    push boot_msg_unk
    call puts
    
    jmp boot_0000

boot_exec_exit:
    mov r31, 0
    int 0x00

boot_exec_help:
    push boot_msg_help
    call puts
    jmp boot_0000

boot_exec_load:
    int 0x15
    push boot_msg_loading
    call puts
    jmp PBOOT_END

boot_input:
boot_exit_msg:    w0xff, w0x1f, w0x1f, w0x1f, w0x1f, w0x1f, w0x1f w0x0a, 
                  w0xf2, w0x1f, w0x1f, w0x1f, w0x1f, w0x1f, w0x1f w0x0a, 
                  w0xf0, w0x1f, w0x1f, w0x1f, w0x1f, w0x1f, w0x1f w0x0a, w0xff, w0x00
boot_msg_unk:     w0xf0, "Unknown command.", w0xff, w0x0a, w0x00
boot_greet:       w0xf1, "#> ", w0xff, w0x00
boot_msg_welcome: "PizdOS Bootloader", w0x0a, w0x0a, w0x00
boot_msg_loading: "Booting into kernel.asm...", w0x0a, w0x00
boot_cmd_exit:    "exit", w0x0d, w0x00
boot_cmd_help:    "help", w0x0d, w0x00
boot_cmd_load:    "load", w0x0d, w0x00
boot_msg_help:    "Commands:", w0x0a
                  "    exit - Exit PizdOS Bootloader", w0x0a
                  "    help - Show this message", w0x0a
                  "    load - Load PizdOS", w0x0a, w0x00
PBOOT_END:
