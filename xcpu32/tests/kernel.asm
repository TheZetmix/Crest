include "./pboot.asm"
jmp main

get_system_info:
    mov r2, 0
    int 0x05
    push .status_msg_1
    call puts
    int 0x14
    mov r31, 0x0a
    int 0x10
    push .status_msg_2
    call puts
    mov r0, r1
    int 0x14
    mov r31, 0x0a
    int 0x10
    push .status_msg_3
    call puts
    mov r0, r2
    int 0x14
    mov r31, 0x0a
    int 0x10
    ret
.status_msg_1:  "Version: ", w0x00
.status_msg_2:  "Memory total: ", w0x00
.status_msg_3:  "Memory free: ", w0x00

panic:
    mov r0, 0
    mov r1, 60
    mov r2, 130
    int 0x09
    pop r16
    pop r15
    int 0x15
    push .panic1 ; pc ;
    call puts
    mov r0, r16
    int 0x14
    mov r31, 0x0a
    int 0x10
    push .panic2 ; error code ;
    call puts
    mov r0, r15
    int 0x14
    mov r31, 0x0a
    int 0x10
    push .panic3 ; msg ;
    call puts
    int 0x11
    mov r31, r15
    int 0x00
.panic1:       "      / ", w0x0a,
               " .   |  ", w0x0a,
               "     |  ", w0x0a,
               " .   |  ", w0x0a,
               "      \ ", w0x0a,
               w0x0a, "something wrong going here: ", w0x00
.panic2:       w0x0a, "error code: ", w0x00
.panic3:       "press any key to exit", w0x00


draw_pixel:
    int 0x05
    mov r7, r3
    mov r8, r4
    pop r3
    pop r4
    int 0x06
    mov r31, 0x1f
    int 0x10
    mov r3, r7
    mov r4, r8
    int 0x06
    ret

init_mouse:
    int 0x07
    push r4
    push r3
    call draw_pixel
    ret

main:
    int 0x15
    push msg_welcome
    call puts
execloop:
    push greet
    call puts

    mov r10, input
    call reads
    
    lea r11, cmd_exit
    int 0x22
    je exec_exit
    
    lea r11, cmd_fetch
    int 0x22
    je exec_fetch
    
    lea r11, cmd_videotest
    int 0x22
    je exec_videotest
    
    lea r11, cmd_cls
    int 0x22
    je exec_cls
    
    lea r11, cmd_help
    int 0x22
    je exec_help

    jmp execloop

exec_exit:
    mov r5, 200
    int 0x04
    jmp boot

exec_fetch:
    push boot_exit_msg
    call puts
    call get_system_info
    jmp execloop

exec_videotest:
    push .msg_videotest
    call puts
.exec_videotest_0000:
    push 0xdead
    int 0x02
    push r0
    call panic
    call init_mouse
    jmp .exec_videotest_0000
.msg_videotest: "Cursor Test (focus (  here  ) to exit)", w0x0a, w0x00

exec_cls:
    int 0x15
    jmp execloop

exec_help:
    push msg_help
    call puts
    jmp execloop

input: w0x00
greet:         w0xf3, ">> ", w0xff, w0x00
msg_welcome:   "Welcome to PizdOS!", w0x0a, w0x0a
               "Type help to see help message.", w0x0a, w0x0a, w0x00
cmd_exit:      "exit", w0x0d, w0x00
cmd_fetch:     "fetch", w0x0d, w0x00
cmd_videotest: "videotest", w0x0d, w0x00
cmd_cls:       "cls", w0x0d, w0x00
cmd_help:      "help", w0x0d, w0x00
msg_help:      "PizdOS Command list:", w0x0a
               "    exit", w0x0a
               "    fetch", w0x0a
               "    videotest (not working!!!!)" w0x0a
               "    cls", w0x0a, w0x00
               
