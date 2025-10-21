#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <math.h>
#include <termios.h>
#ifndef CPU_NO_CCFLAGS
#include <ccflags.h>
#endif

#include "./cpu.h"
#define VIDEOOUTPUT 0
#if VIDEOOUTPUT
#include "../../emu/libterm.h"
#endif

#define len(arr) sizeof(arr)/sizeof(arr[0])

#define U0  void
#define U8  uint8_t
#define U16 uint16_t
#define U32 uint32_t

#define I8  int8_t
#define I16 int16_t
#define I32 int32_t

U16 BYTECODE_START_ADDR = 0x8000;
U16 CPU_START_ADDR = 0x8000;

U8 DEBUG_MODE = 0;
U8 DISK_MODE = 0;

U16 TERM_COL = 0;
U16 TERM_ROW = 0;
char COLOR[] = {255, 255, 255};
char BG_COLOR[] = {0, 0, 0};

#if VIDEOOUTPUT
X11Context *ctx = NULL;
#endif

void term_draw_char(char ch) {
#if VIDEOOUTPUT
    switch (ch) {
    case 0x00: {
        break;
    }
    case 0xf0: {
        COLOR[0] = 255;
        COLOR[1] = 0;
        COLOR[2] = 0;
        break;
    }
    case 0xf1: {
        COLOR[0] = 0;
        COLOR[1] = 255;
        COLOR[2] = 0;
        break;
    }
    case 0xf2: {
        COLOR[0] = 0;
        COLOR[1] = 0;
        COLOR[2] = 255;
        break;
    }
    case 0xf3: {
        COLOR[0] = 0xa0;
        COLOR[1] = 0xa0;
        COLOR[2] = 0xa0;
        break;
    }
    case 0xff: {
        COLOR[0] = 255;
        COLOR[1] = 255;
        COLOR[2] = 255;
        break;
    }
    case 0x0a: {
        TERM_ROW += 8;
        TERM_COL = 0;
        break;
    }
    case 0x0d: {
        TERM_COL = 0;
        break;
    }
    case 0x09: {
        TERM_COL -= 8;
        break;
    }
    default: {
        if (TERM_COL > ((ctx->width / 3) - 8)) {
            TERM_ROW += 8;
            TERM_COL = 0;
        }
        x11_draw_char(ctx, TERM_COL, TERM_ROW, ch, COLOR[0], COLOR[1], COLOR[2]);
        TERM_COL += 8;
        x11_flush(ctx);
        break;
    }
    }
#else
    putchar(ch);
#endif
}

char term_get_char() {
#if VIDEOOUTPUT
    char key = 0;
    while (1) {
        if (x11_key_pressed(ctx, &key)) {
            return key;
        }
        usleep(1000); 
    }
#else
    return getchar();
#endif
}

void SystemDump(const CPU *cpu);
void error(CPU *cpu, char *msg) {
    printf("(%s) at %04x\n", msg, cpu->pc);
    cpu->running = 0;
}

void SystemDump(const CPU *cpu) {
    const char *GREEN = "\033[32m";
    const char *RED = "\033[31m";
    const char *RESET = "\033[0m";
    
    printf("\nGeneral Purpose Registers:\n");
    printf("%sr0%s:  0x%08X  %sr1%s:  0x%08X  %sr2%s:  0x%08X  %sr3%s:  0x%08X\n",
           cpu->reg.r0 ? GREEN : RED, RESET, cpu->reg.r0,
           cpu->reg.r1 ? GREEN : RED, RESET, cpu->reg.r1,
           cpu->reg.r2 ? GREEN : RED, RESET, cpu->reg.r2,
           cpu->reg.r3 ? GREEN : RED, RESET, cpu->reg.r3);
    printf("%sr4%s:  0x%08X  %sr5%s:  0x%08X  %sr6%s:  0x%08X  %sr7%s:  0x%08X\n",
           cpu->reg.r4 ? GREEN : RED, RESET, cpu->reg.r4,
           cpu->reg.r5 ? GREEN : RED, RESET, cpu->reg.r5,
           cpu->reg.r6 ? GREEN : RED, RESET, cpu->reg.r6,
           cpu->reg.r7 ? GREEN : RED, RESET, cpu->reg.r7);
    printf("%sr8%s:  0x%08X  %sr9%s:  0x%08X  %sr10%s: 0x%08X  %sr11%s: 0x%08X\n",
           cpu->reg.r8 ? GREEN : RED, RESET, cpu->reg.r8,
           cpu->reg.r9 ? GREEN : RED, RESET, cpu->reg.r9,
           cpu->reg.r10 ? GREEN : RED, RESET, cpu->reg.r10,
           cpu->reg.r11 ? GREEN : RED, RESET, cpu->reg.r11);
    printf("%sr12%s: 0x%08X  %sr13%s: 0x%08X  %sr14%s: 0x%08X  %sr15%s: 0x%08X\n",
           cpu->reg.r12 ? GREEN : RED, RESET, cpu->reg.r12,
           cpu->reg.r13 ? GREEN : RED, RESET, cpu->reg.r13,
           cpu->reg.r14 ? GREEN : RED, RESET, cpu->reg.r14,
           cpu->reg.r15 ? GREEN : RED, RESET, cpu->reg.r15);
    printf("%sr16%s: 0x%08X  %sr17%s: 0x%08X  %sr18%s: 0x%08X  %sr19%s: 0x%08X\n",
           cpu->reg.r16 ? GREEN : RED, RESET, cpu->reg.r16,
           cpu->reg.r17 ? GREEN : RED, RESET, cpu->reg.r17,
           cpu->reg.r18 ? GREEN : RED, RESET, cpu->reg.r18,
           cpu->reg.r19 ? GREEN : RED, RESET, cpu->reg.r19);
    printf("%sr20%s: 0x%08X  %sr21%s: 0x%08X  %sr22%s: 0x%08X  %sr23%s: 0x%08X\n",
           cpu->reg.r20 ? GREEN : RED, RESET, cpu->reg.r20,
           cpu->reg.r21 ? GREEN : RED, RESET, cpu->reg.r21,
           cpu->reg.r22 ? GREEN : RED, RESET, cpu->reg.r22,
           cpu->reg.r23 ? GREEN : RED, RESET, cpu->reg.r23);
    printf("%sr24%s: 0x%08X  %sr25%s: 0x%08X  %sr26%s: 0x%08X  %sr27%s: 0x%08X\n",
           cpu->reg.r24 ? GREEN : RED, RESET, cpu->reg.r24,
           cpu->reg.r25 ? GREEN : RED, RESET, cpu->reg.r25,
           cpu->reg.r26 ? GREEN : RED, RESET, cpu->reg.r26,
           cpu->reg.r27 ? GREEN : RED, RESET, cpu->reg.r27);
    printf("%sr28%s: 0x%08X  %sr29%s: 0x%08X  %sr30%s: 0x%08X  %sr31%s: 0x%08X\n",
           cpu->reg.r28 ? GREEN : RED, RESET, cpu->reg.r28,
           cpu->reg.r29 ? GREEN : RED, RESET, cpu->reg.r29,
           cpu->reg.r30 ? GREEN : RED, RESET, cpu->reg.r30,
           cpu->reg.r31 ? GREEN : RED, RESET, cpu->reg.r31);

    printf("\nFlag Registers:\n");
    printf("%sf0%s: %d  %sf1%s: %d  %sf2%s: %d  %sf3%s: %d\n",
           cpu->reg.f0 ? GREEN : RED, RESET, cpu->reg.f0,
           cpu->reg.f1 ? GREEN : RED, RESET, cpu->reg.f1,
           cpu->reg.f2 ? GREEN : RED, RESET, cpu->reg.f2,
           cpu->reg.f3 ? GREEN : RED, RESET, cpu->reg.f3);
    printf("%sf4%s: %d  %sf5%s: %d  %sf6%s: %d  %sf7%s: %d\n",
           cpu->reg.f4 ? GREEN : RED, RESET, cpu->reg.f4,
           cpu->reg.f5 ? GREEN : RED, RESET, cpu->reg.f5,
           cpu->reg.f6 ? GREEN : RED, RESET, cpu->reg.f6,
           cpu->reg.f7 ? GREEN : RED, RESET, cpu->reg.f7);
    
    printf("\nStack Pointers:\n");
    printf("%shsp%s: 0x%04X  %srsp%s: 0x%04X\n",
           cpu->reg.hsp ? GREEN : RED, RESET, cpu->reg.hsp,
           cpu->reg.rsp ? GREEN : RED, RESET, cpu->reg.rsp);
    
    printf("\nProgram Counter: 0x%08X\n", cpu->pc);
    
    printf("\nMemory Dump (non-zero only):\n");
    printf("Address  00 01 02 03 04 05 06 07  08 09 0A 0B 0C 0D 0E 0F  0123456789abcdef\n");
    printf("-------  -----------------------  -----------------------  ----------------\n");
    
    for (int i = 0; i < MAX_MEMORY_SIZE; i += 16) {
        // Check if this line has any non-zero values
        int has_data = 0;
        for (int j = 0; j < 16; j++) {
            if (i + j < MAX_MEMORY_SIZE && cpu->memory.Addressable[i + j].value != 0) {
                has_data = 1;
                break;
            }
        }
        if (!has_data) continue;
        
        // Print address
        printf("%04X     ", i);
        
        // Print hex values
        for (int j = 0; j < 16; j++) {
            if (j == 8) printf(" ");
            if (i + j < MAX_MEMORY_SIZE) {
                printf("%02X ", cpu->memory.Addressable[i + j].value & 0xFF);
            } else {
                printf("   ");
            }
        }
        printf(" ");
        for (int j = 0; j < 16; j++) {
            if (i + j < MAX_MEMORY_SIZE) {
                unsigned char c = cpu->memory.Addressable[i + j].value & 0xFF;
                printf("%c", (c >= 32 && c <= 126) ? c : '.');
            }
        }
        printf("\n");
    }
    
    printf("\nHardware Stack (Top %d):\n", cpu->reg.hsp);
    for (int i = 0; i < cpu->reg.hsp; ++i) { // Limit to top 16 entries
        printf("[%04X] 0x%08X  %d  '%c'\n", 
               i,
               cpu->memory.HardwareStack[i].value,
               cpu->memory.HardwareStack[i].value,
               (cpu->memory.HardwareStack[i].value >= 32 && 
                cpu->memory.HardwareStack[i].value <= 126) ? 
                cpu->memory.HardwareStack[i].value : '.');
    }
    
    printf("\nReturn Stack (Top %d):\n", cpu->reg.rsp);
    for (int i = 0; i < cpu->reg.rsp && i < 16; ++i) { // Limit to top 16 entries
        printf("[%04X] Return to 0x%04X\n", 
               i, 
               cpu->memory.ReturnStack[i].value);
    }
    
    printf("\nCPU Status: %s%s%s\n", 
           cpu->running ? GREEN : RED,
           cpu->running ? "RUNNING" : "HALTED",
           RESET);
}

I16 calculate_instruction_len(CPU *cpu, U16 start, I16 args_count) {
    U16 len = 1;
    for (int16_t i = 0; i < args_count; ++i) {
        U32 byte = cpu->memory.Addressable[start+len].value;
        if (byte == 0x50) {
            i--;
            len += 1;
        }
        if (byte == 0x51) {
            len += 2;
        }
        else if (byte == 0x52) {
            len += 2;
        }
        else if (byte == 0x53) {
            len += 5;
        }
    }
    return len;
}

I16 calculate_arg_len(CPU *cpu, U16 start) {
    U16 len = 0;
    for (;;) {
        U32 byte = cpu->memory.Addressable[start+len].value;
        if (byte == 0x50) {
            len += 1;
        }
        if (byte == 0x51) {
            len += 2;
            break;
        }
        else if (byte == 0x52) {
            len += 2;
            break;
        }
        else if (byte == 0x53) {
            len += 5;
            break;
        }
    }
    return len+1;
}

U32 get_number(CPU *cpu, U16 start) {
    return (cpu->memory.Addressable[start].value   << 24) | 
           (cpu->memory.Addressable[start+1].value << 16) | 
           (cpu->memory.Addressable[start+2].value << 8)  | 
           cpu->memory.Addressable [start+3].value;
}

void write_32(CPU *cpu, U32 value, U16 addr) {
    cpu->memory.Addressable[addr].value   = (value >> 24) & 0xFF;
    cpu->memory.Addressable[addr+1].value = (value >> 16) & 0xFF;
    cpu->memory.Addressable[addr+2].value = (value >> 8)  & 0xFF;
    cpu->memory.Addressable[addr+3].value = value         & 0xFF;
}

U32 read_32(CPU *cpu, U16 addr) {
    return (cpu->memory.Addressable[addr].value   << 24) | 
           (cpu->memory.Addressable[addr+1].value << 16) | 
           (cpu->memory.Addressable[addr+2].value << 8)  | 
           cpu->memory.Addressable [addr+3].value;

}

U32 get_value(CPU *cpu, U16 start) {
    U8 byte = cpu->memory.Addressable[start].value;
    
    if (byte == 0x50) { // pointer
        if (cpu->memory.Addressable[start+1].value == 0x52) { // register pointer
            U16 reg_index = cpu->memory.Addressable[start+2].value;
            return read_32(cpu, GetRegisterValue(cpu, REGISTERS_NAMES[reg_index]));
        }
        else if (cpu->memory.Addressable[start+1].value == 0x53) { // pointer to memory
            U32 addr = get_number(cpu, start+2);
            return read_32(cpu, addr);
        }
    }
    else if (byte == 0x52) { // register
        U16 reg_index = cpu->memory.Addressable[start+1].value;
        return GetRegisterValue(cpu, REGISTERS_NAMES[reg_index]);
    }
    else if (byte == 0x53) { // immediate value
        return get_number(cpu, start+1);
    }
    return 0xDEAD;
}

U0 set_value(CPU *cpu, U16 start, U32 set) {
    U8 byte = cpu->memory.Addressable[start].value;
    
    if (byte == 0x50) { // pointer
        if (cpu->memory.Addressable[start+1].value == 0x52) { // register pointer
            U16 reg_index = cpu->memory.Addressable[start+2].value;
            write_32(cpu, set, GetRegisterValue(cpu, REGISTERS_NAMES[reg_index]));
        }
        else if (cpu->memory.Addressable[start+1].value == 0x53) { // pointer to memory
            U32 addr = get_number(cpu, start+2);
            write_32(cpu, set, addr);
        }
    }
    else if (byte == 0x51) { // Immediate memory address
        U32 addr = get_number(cpu, start+1);
        write_32(cpu, set, addr);
    }
    else if (byte == 0x52) { // Register
        U16 reg_index = cpu->memory.Addressable[start+1].value;
        EditRegister(cpu, REGISTERS_NAMES[reg_index], set);
    }
    // for immediate value we dont write back as its a constant
}

U8 get_byte_value(CPU *cpu, U16 start) {
    U8 byte = cpu->memory.Addressable[start].value;
    
    if (byte == 0x50) { // pointer
        if (cpu->memory.Addressable[start+1].value == 0x52) { // register pointer
            U16 reg_index = cpu->memory.Addressable[start+2].value;
            return cpu->memory.Addressable[GetRegisterValue(cpu, REGISTERS_NAMES[reg_index])].value;
        }
        else if (cpu->memory.Addressable[start+1].value == 0x53) { // pointer to memory
            U32 addr = get_number(cpu, start+2);
            return cpu->memory.Addressable[addr].value;
        }
    }
    else if (byte == 0x52) { // register
        U16 reg_index = cpu->memory.Addressable[start+1].value;
        return (U8)(GetRegisterValue(cpu, REGISTERS_NAMES[reg_index]) & 0xFF);
    }
    else if (byte == 0x53) { // immediate value
        return (U8)(get_number(cpu, start+1) & 0xFF);
    }
    return 0;
}

void set_byte_value(CPU *cpu, U16 start, U8 value) {
    U8 byte = cpu->memory.Addressable[start].value;
    
    if (byte == 0x50) { // pointer
        if (cpu->memory.Addressable[start+1].value == 0x52) { // register pointer
            U16 reg_index = cpu->memory.Addressable[start+2].value;
            cpu->memory.Addressable[GetRegisterValue(cpu, REGISTERS_NAMES[reg_index])].value = value;
        }
        else if (cpu->memory.Addressable[start+1].value == 0x53) { // pointer to memory
            U32 addr = get_number(cpu, start+2);
            cpu->memory.Addressable[addr].value = value;
        }
    }
    else if (byte == 0x52) { // register
        U16 reg_index = cpu->memory.Addressable[start+1].value;
        // Сохраняем только младший байт, остальные биты обнуляем
        EditRegister(cpu, REGISTERS_NAMES[reg_index], (U32)value);
    }
}

U16 calc_offset(CPU *cpu, int n) {
    if (n == 1) return 1;
    return calculate_arg_len(cpu, cpu->pc + calc_offset(cpu, n - 1));
}

U32 get_arg(CPU *cpu, int n) {
    if (n == 1) return get_value(cpu, cpu->pc + 1);
    return get_value(cpu, cpu->pc + calc_offset(cpu, n));
}

/* Instructions implementation */

void MOV(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              get_arg(cpu, 2)
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void ADD(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              get_value(cpu, cpu->pc+1)+get_value(cpu, cpu->pc+calculate_arg_len(cpu, cpu->pc+1))
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void SUB(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              get_value(cpu, cpu->pc+1)-get_value(cpu, cpu->pc+calculate_arg_len(cpu, cpu->pc+1))
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void MUL(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              get_value(cpu, cpu->pc+1)*get_value(cpu, cpu->pc+calculate_arg_len(cpu, cpu->pc+1))
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void DIV(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              get_value(cpu, cpu->pc+1)/get_value(cpu, cpu->pc+calculate_arg_len(cpu, cpu->pc+1))
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void MOD(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              get_value(cpu, cpu->pc+1)%get_value(cpu, cpu->pc+calculate_arg_len(cpu, cpu->pc+1))
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void INC(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              get_value(cpu, cpu->pc+1)+1
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 1);
}

void DEC(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              get_value(cpu, cpu->pc+1)-1
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 1);
}

void AND(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              get_value(cpu, cpu->pc+1)&get_value(cpu, cpu->pc+calculate_arg_len(cpu, cpu->pc+1))
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void OR(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              get_value(cpu, cpu->pc+1)|get_value(cpu, cpu->pc+calculate_arg_len(cpu, cpu->pc+1))
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void XOR(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              get_value(cpu, cpu->pc+1)^get_value(cpu, cpu->pc+calculate_arg_len(cpu, cpu->pc+1))
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void NOT(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              ~get_value(cpu, cpu->pc+1)
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 1);
}

void SHL(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              get_value(cpu, cpu->pc+1)<<get_value(cpu, cpu->pc+calculate_arg_len(cpu, cpu->pc+1))
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void SHR(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              get_value(cpu, cpu->pc+1)>>get_value(cpu, cpu->pc+calculate_arg_len(cpu, cpu->pc+1))
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void PUSH(CPU *cpu) {
    HardwareStackPush(cpu, get_value(cpu, cpu->pc+1));
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 1);
}

void POP(CPU *cpu) {
    set_value(cpu, cpu->pc+1, HardwareStackPop(cpu));
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 1);
}

void LEA(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              get_value(cpu, cpu->pc+calculate_arg_len(cpu, cpu->pc+1))+BYTECODE_START_ADDR
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void JMP(CPU *cpu) {
    cpu->pc = BYTECODE_START_ADDR+get_value(cpu, cpu->pc+1);
}

void CALL(CPU *cpu) {
    RetStackPush(cpu, cpu->pc+calculate_instruction_len(cpu, cpu->pc, 1));
    cpu->pc = BYTECODE_START_ADDR+get_value(cpu, cpu->pc+1);
}

void RET(CPU *cpu) {
    cpu->pc = RetStackPop(cpu);
}

void JE(CPU *cpu) {
    if (cpu->reg.f0) cpu->pc = BYTECODE_START_ADDR+get_value(cpu, cpu->pc+1);
    else             cpu->pc += calculate_instruction_len(cpu, cpu->pc, 1);
}

void JNE(CPU *cpu) { // !=
    if (!cpu->reg.f0) cpu->pc = BYTECODE_START_ADDR+get_value(cpu, cpu->pc+1);
    else              cpu->pc += calculate_instruction_len(cpu, cpu->pc, 1);
}

void JG(CPU *cpu) { // >
    if (cpu->reg.f1) cpu->pc = BYTECODE_START_ADDR+get_value(cpu, cpu->pc+1);
    else              cpu->pc += calculate_instruction_len(cpu, cpu->pc, 1);
}

void JL(CPU *cpu) { // <
    if (cpu->reg.f2) cpu->pc = BYTECODE_START_ADDR+get_value(cpu, cpu->pc+1);
    else              cpu->pc += calculate_instruction_len(cpu, cpu->pc, 1);
}

void JGE(CPU *cpu) {
    if (cpu->reg.f0 || !cpu->reg.f1) cpu->pc = BYTECODE_START_ADDR+get_value(cpu, cpu->pc+1);
    else                             cpu->pc += calculate_instruction_len(cpu, cpu->pc, 1);
}

void JLE(CPU *cpu) {
    if (cpu->reg.f0 || !cpu->reg.f2) cpu->pc = BYTECODE_START_ADDR+get_value(cpu, cpu->pc+1);
    else                             cpu->pc += calculate_instruction_len(cpu, cpu->pc, 1);
}

void CMP(CPU *cpu) {
    U32 op1 = get_value(cpu, cpu->pc+1);
    U32 op2 = get_value(cpu, cpu->pc+calculate_arg_len(cpu, cpu->pc+1));
    cpu->reg.f0 = (op1 == op2);
    cpu->reg.f1 = (op1 >  op2);
    cpu->reg.f2 = (op1 <  op2);
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void NOP(CPU *cpu) {
    cpu->pc++;
}

void HLT(CPU *cpu) {}

void INT(CPU *cpu) {
    U32 interrupt = get_value(cpu, cpu->pc + 1);
    
    switch (interrupt) {
        // system interrupts
    case 0x00: // Exit program
        cpu->running = 0;
        break;
            
    case 0x01: // System Dump
        SystemDump(cpu);
        break;
            
    case 0x02: // Get current PC
        cpu->reg.r0 = cpu->pc;
        break;
        
    case 0x04: { // delay
        usleep(cpu->reg.r5*1000);
        break;
    }
        
    case 0x05: { // get system info
        cpu->reg.r0 = 1; // version
        cpu->reg.r1 = MAX_MEMORY_SIZE; // max memory
        for (int i = 0; i < MAX_MEMORY_SIZE; ++i) {
            if (cpu->memory.Addressable[i].value == 0) cpu->reg.r2++; // free memory
        }
        cpu->reg.r3 = TERM_COL / 8;
        cpu->reg.r4 = TERM_ROW / 8;
        break;
    }

    case 0x06: {
        TERM_COL = cpu->reg.r3 * 8;
        TERM_ROW = cpu->reg.r4 * 8;
        break;
    }
        
    case 0x07: {
#if VIDEOOUTPUT
        I32 x, y;
        x11_get_mouse_coords(ctx, &x, &y);
        cpu->reg.r3 = x / (8 * ctx->char_size);
        cpu->reg.r4 = y / (8 * ctx->char_size);
#endif
        break;
    }
        
    case 0x08: {
#if VIDEOOUTPUT
        x11_flush(ctx);
#endif
        break;
    }
        
    case 0x09: {
        BG_COLOR[0] = cpu->reg.r0;
        BG_COLOR[1] = cpu->reg.r1;
        BG_COLOR[2] = cpu->reg.r2;
#if VIDEOOUTPUT
        x11_fill(ctx, BG_COLOR[0], BG_COLOR[1], BG_COLOR[2]);
        ctx->bg_color = ((cpu->reg.r0 << 16) | (cpu->reg.r1 << 8) | cpu->reg.r2);
#endif
        break;
    }
        
        // io interrupts
    case 0x10: {
        term_draw_char(cpu->reg.r31);
        break;
    }
        
    case 0x11: {
        cpu->reg.r31 = term_get_char();
        break;
    }
        
    case 0x12: {
        for (int i = cpu->reg.r10; cpu->memory.Addressable[i].value != 0x00; ++i) {
            putchar(cpu->memory.Addressable[i].value);fflush(stdout);
        }
        break;
    }

    case 0x13: {
        for (int i = cpu->reg.r10; 1; ++i) {
            char ch = getchar();
            cpu->memory.Addressable[i].value = ch;
            if (ch == '\n') {
                break;
            }
        }
    }
        
    case 0x14: {
        U32 num = cpu->reg.r0;
        char f[8];
        sprintf(f, "%d", num);
        for (int i = 0; f[i]; ++i) {
#if VIDEOOUTPUT 
            term_draw_char(f[i]);
#else
            putchar(f[i]);
#endif
        }
        break;
    }

    case 0x15: {
        TERM_COL = 0;
        TERM_ROW = 0;
#if VIDEOOUTPUT
        x11_fill(ctx, BG_COLOR[0], BG_COLOR[1], BG_COLOR[2]);
#endif
        break;
    }

    case 0x20: { // number to string
        U16 addr = cpu->reg.r1;
        U32 num = cpu->reg.r0;
    
        if (num == 0) {
            cpu->memory.Addressable[addr++].value = '0';
            cpu->memory.Addressable[addr].value = 0x00;
            break;
        }
    
        U32 rnum = 0;
        int digit_count = 0;
    
        while (num != 0) {
            rnum = rnum * 10 + num % 10;
            num /= 10;
            digit_count++;
        }
    
        for (int i = 0; i < digit_count; i++) {
            cpu->memory.Addressable[addr++].value = (rnum % 10) + '0';
            rnum /= 10;
        }
    
        cpu->memory.Addressable[addr].value = 0x00;
        break;
    }

    case 0x21: { // string to number
        U32 num = 0;
        U16 i = cpu->reg.r10;
        while (cpu->memory.Addressable[i].value >= '0' && 
               cpu->memory.Addressable[i].value <= '9') {
            num = num * 10 + (cpu->memory.Addressable[i++].value - '0');
        }
        cpu->reg.r0 = num;
        break;
    }
        
    case 0x22: {
        U16 addr1 = cpu->reg.r10;
        U16 addr2 = cpu->reg.r11;
    
        while (cpu->memory.Addressable[addr1].value &&
               cpu->memory.Addressable[addr2].value &&
               (cpu->memory.Addressable[addr1].value == cpu->memory.Addressable[addr2].value)) {
            addr1++;
            addr2++;
        }
        
        if (cpu->memory.Addressable[addr1].value == cpu->memory.Addressable[addr2].value) {
            cpu->reg.f0 = 1;
        } else {
            cpu->reg.f0 = 0;
        }
        break;
    }
        
        // file interrupts
    case 0x30: {
        
        break;
    }
    case 0x40: {
        break;
    }
       
        // video interrupts
    case 0x50: {
        
        break;
    }
    }
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 1);
}

void TRAP(CPU *cpu) {
    while (1) {
        char buf[128];
        printf("?> ");
        scanf("%s", buf);
        fflush(stdout);
        if (!strcmp(buf, "q")) {
            cpu->running = 0;
            break;
        }
        if (!strcmp(buf, "r")) {
            break;
        }
        if (!strcmp(buf, "reg")) {
            SystemDump(cpu);
        }
    }
    cpu->pc += 1;
}

void STR(CPU *cpu) {
    write_32(cpu, get_arg(cpu, 2), get_arg(cpu, 1));
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void LDR(CPU *cpu) {
    set_value(cpu, cpu->pc+1, read_32(cpu, get_arg(cpu, 2)));
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void PUSHA(CPU *cpu) {
    for (int i = 0; i < len(REGISTERS_NAMES); ++i) {
        HardwareStackPush(cpu, GetRegisterValue(cpu, REGISTERS_NAMES[i]));
    }
    cpu->pc++;
}

void POPA(CPU *cpu) {
    for (int i = len(REGISTERS_NAMES)-1; i >= 0; --i) {
        EditRegister(cpu, REGISTERS_NAMES[i], HardwareStackPop(cpu));
    }
    cpu->pc++;
}

void LEAN(CPU *cpu) {
    set_value(cpu, 
              cpu->pc+1,
              get_value(cpu, cpu->pc+calculate_arg_len(cpu, cpu->pc+1))+BYTECODE_START_ADDR+1
              );
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void FFP(CPU *cpu) {
    U32 size = get_value(cpu, cpu->pc + 1);
    U32 start_addr = 0;
    
    for (U32 i = start_addr; i < MAX_MEMORY_SIZE - size; i++) {
        int found = 1;
        for (U32 j = 0; j < size; j++) {
            if (cpu->memory.Addressable[i + j].value != 0) {
                found = 0;
                i += j;
                break;
            }
        }
        if (found) {
            set_value(cpu, cpu->pc + 1, i);
            cpu->pc += calculate_instruction_len(cpu, cpu->pc, 1);
            return;
        }
    }
}

void MOVB(CPU *cpu) {
    U8 byte = get_byte_value(cpu, cpu->pc + calculate_arg_len(cpu, cpu->pc + 1));
    set_byte_value(cpu, cpu->pc + 1, byte);
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void MOVW(CPU *cpu) {
    U32 value = get_arg(cpu, 2);
    
    U8  byte1 = value & 0xff;
    U16 byte2 = ((value>>8) & 0xff) << 8;
    
    set_byte_value(cpu, cpu->pc+1, byte1);
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
    error(cpu, "movw not implemented at processor");
}

void MOVD(CPU *cpu) {
    U16 src_addr = cpu->pc + calculate_arg_len(cpu, cpu->pc + 1);
    U8 byte1 = get_byte_value(cpu, src_addr);
    U8 byte2 = get_byte_value(cpu, src_addr + 1);
    U8 byte3 = get_byte_value(cpu, src_addr + 2);
    U8 byte4 = get_byte_value(cpu, src_addr + 3);
    set_byte_value(cpu, cpu->pc + 1, byte1);
    set_byte_value(cpu, cpu->pc + 1 + 1, byte2);
    set_byte_value(cpu, cpu->pc + 1 + 2, byte3);
    set_byte_value(cpu, cpu->pc + 1 + 3, byte4);
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
    error(cpu, "movd not implemented at processor");
}

void MOVST(CPU *cpu) {
    cpu->memory.HardwareStack[get_arg(cpu, 1)].value = get_arg(cpu, 2);
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void SMP(CPU *cpu) {
    cpu->memory.Addressable[get_arg(cpu, 1)].permission = get_arg(cpu, 2);
    cpu->pc += calculate_instruction_len(cpu, cpu->pc, 2);
}

void (*INSTR[])() = {
    &MOV,    &ADD,    &SUB,    &MUL,    &DIV,
    &MOD,    &INC,    &DEC,    &AND,    &OR,
    &XOR,    &NOT,    &SHL,    &SHR,    &PUSH,
    &POP,    &LEA,    &JMP,    &CALL,   &RET,
    &JE,     &JNE,    &JG,     &JL,     &JGE,
    &JLE,    &CMP,    &NOP,    &HLT,    &INT,
    &TRAP,   &STR,    &LDR,    &PUSHA,  &POPA,
    &LEAN,   &FFP,    &MOVB,   &MOVW,   &MOVD, 
    &MOVST,  &SMP
};

int main(int argc, char **argv) {
    char *executable;
    cc_setargs(argc, argv);
    cc_disable_usage();
    cc_set_description("Type -h to see help message. \nUsage: ./cpu -f <filename> [options]");
    cc_set_minimum_flags(1);
    if (cc_argexp("-d", "--debug"))
        DEBUG_MODE = 1;
    if (cc_argexp("-h", "--help")) {
        printf("\
Options: \n \
    -f  --filename       Specify the executable \n \
    -d  --debug          Debug mode \n \
    -bs --bytecode-start Specify address in memory where bytecode starts \n \
    -cs --cpu-start      Specify the address in memory where CPU will start\n");
        exit(0);
    }
    if (cc_argexp("-bs", "--bytecode-start"))
        BYTECODE_START_ADDR = strtol(cc_getarg("-bs"), NULL, 10);
    if (cc_argexp("-cs", "--cpu-start"))
        CPU_START_ADDR = strtol(cc_getarg("-cs"), NULL, 10);
    if (cc_argexp("-f", "--filename"))
        executable = cc_getarg("-f");
    if (!executable) {
        printf("No file provided, use -f <filename>\n");
        exit(EXIT_FAILURE);
    }
    
#if VIDEOOUTPUT
    ctx = x11_init(1200, 900, "Dodik Display");
    ctx->char_size = 3;
    x11_fill(ctx, BG_COLOR[0], BG_COLOR[1], BG_COLOR[2]);
#endif

    CPU cpu = {
        .running = 1,
        .pc = CPU_START_ADDR,
    };

    memset(&cpu.reg, 0, sizeof(cpu.reg));
    
    I16 f = open(executable, O_RDONLY);
    unsigned char bytes[MAX_MEMORY_SIZE];
    ssize_t bytes_read = read(f, bytes, sizeof(bytes));
    close(f);
    
    for (size_t i = 0; i < bytes_read; ++i) {
        cpu.memory.Addressable[BYTECODE_START_ADDR+i].value = bytes[i];
    }
           
    while (cpu.running) {
        U8 opcode = cpu.memory.Addressable[cpu.pc].value;
        if (opcode < sizeof(INSTR)/sizeof(INSTR[0])) {
            /* printf("executing %02x instruction at %04x\n", opcode, cpu.pc); */
            INSTR[opcode](&cpu);
        } else {
            printf("Illegal instruction %02x at position %04x\n", opcode, cpu.pc);
            cpu.running = 0;
        }
        /* usleep(30000); */
    }
#if VIDEOOUTPUT
    x11_close(ctx);
#endif
    if (DEBUG_MODE) SystemDump(&cpu);
    return 0;
}
