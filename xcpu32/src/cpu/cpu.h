// cpu.h
#pragma once
#include <stdint.h>
#include <string.h>

#define MAX_MEMORY_SIZE UINT16_MAX

char *REGISTERS_NAMES[] = {
    "r0",  "r1",  "r2",  "r3", // registers
    "r4",  "r5",  "r6",  "r7", 
    "r8",  "r9",  "r10", "r11", 
    "r12", "r13", "r14", "r15", 
    "r16", "r17", "r18", "r19", 
    "r20", "r21", "r22", "r23", 
    "r24", "r25", "r26", "r27", 
    "r28", "r29", "r30", "r31", 
    
    "f0", "f1", "f2", "f3", // flags
    "f4", "f5", "f6", "f7",
    "hsp", "rsp" // stack pointers
};

typedef struct {
    
    uint32_t r0,  r1,  r2,  r3; 
    uint32_t r4,  r5,  r6,  r7; 
    uint32_t r8,  r9,  r10, r11; 
    uint32_t r12, r13, r14, r15; 
    uint32_t r16, r17, r18, r19; 
    uint32_t r20, r21, r22, r23; 
    uint32_t r24, r25, r26, r27; 
    uint32_t r28, r29, r30, r31; 
    
    uint8_t f0, f1, f2, f3, f4, f5, f6, f7;
    uint16_t hsp, rsp;
    
} Register;

typedef struct {

    uint8_t value;
    uint8_t permission;
    char tag[32];

} AddressableMemory;

typedef struct {

    uint32_t value;
    
} HardwareEntry;

typedef struct {

    uint16_t value;
    
} ReturnEntry;

typedef struct {
    
    AddressableMemory  Addressable  [MAX_MEMORY_SIZE];
    ReturnEntry        ReturnStack  [MAX_MEMORY_SIZE];
    HardwareEntry      HardwareStack[MAX_MEMORY_SIZE];
    
} Memory;

typedef struct {

    Register reg;
    Memory memory;
    uint32_t pc;
    uint8_t running;

} CPU;

uint32_t GetRegisterValue(CPU *cpu, char *name) {
    // General purpose registers
    if (!strcmp(name, "r0")) return cpu->reg.r0;
    else if (!strcmp(name, "r1")) return cpu->reg.r1;
    else if (!strcmp(name, "r2")) return cpu->reg.r2;
    else if (!strcmp(name, "r3")) return cpu->reg.r3;
    else if (!strcmp(name, "r4")) return cpu->reg.r4;
    else if (!strcmp(name, "r5")) return cpu->reg.r5;
    else if (!strcmp(name, "r6")) return cpu->reg.r6;
    else if (!strcmp(name, "r7")) return cpu->reg.r7;
    else if (!strcmp(name, "r8")) return cpu->reg.r8;
    else if (!strcmp(name, "r9")) return cpu->reg.r9;
    else if (!strcmp(name, "r10")) return cpu->reg.r10;
    else if (!strcmp(name, "r11")) return cpu->reg.r11;
    else if (!strcmp(name, "r12")) return cpu->reg.r12;
    else if (!strcmp(name, "r13")) return cpu->reg.r13;
    else if (!strcmp(name, "r14")) return cpu->reg.r14;
    else if (!strcmp(name, "r15")) return cpu->reg.r15;
    else if (!strcmp(name, "r16")) return cpu->reg.r16;
    else if (!strcmp(name, "r17")) return cpu->reg.r17;
    else if (!strcmp(name, "r18")) return cpu->reg.r18;
    else if (!strcmp(name, "r19")) return cpu->reg.r19;
    else if (!strcmp(name, "r20")) return cpu->reg.r20;
    else if (!strcmp(name, "r21")) return cpu->reg.r21;
    else if (!strcmp(name, "r22")) return cpu->reg.r22;
    else if (!strcmp(name, "r23")) return cpu->reg.r23;
    else if (!strcmp(name, "r24")) return cpu->reg.r24;
    else if (!strcmp(name, "r25")) return cpu->reg.r25;
    else if (!strcmp(name, "r26")) return cpu->reg.r26;
    else if (!strcmp(name, "r27")) return cpu->reg.r27;
    else if (!strcmp(name, "r28")) return cpu->reg.r28;
    else if (!strcmp(name, "r29")) return cpu->reg.r29;
    else if (!strcmp(name, "r30")) return cpu->reg.r30;
    else if (!strcmp(name, "r31")) return cpu->reg.r31;
    else if (!strcmp(name, "f0")) return cpu->reg.f0;
    else if (!strcmp(name, "f1")) return cpu->reg.f1;
    else if (!strcmp(name, "f2")) return cpu->reg.f2;
    else if (!strcmp(name, "f3")) return cpu->reg.f3;
    else if (!strcmp(name, "f4")) return cpu->reg.f4;
    else if (!strcmp(name, "f5")) return cpu->reg.f5;
    else if (!strcmp(name, "f6")) return cpu->reg.f6;
    else if (!strcmp(name, "f7")) return cpu->reg.f7;
    else if (!strcmp(name, "hsp")) return cpu->reg.hsp;
    else if (!strcmp(name, "rsp")) return cpu->reg.rsp;
    
    return 0; // or handle error for unknown register
}

void EditRegister(CPU *cpu, char *name, uint32_t value) {
    if (!strcmp(name, "r0")) cpu->reg.r0 = value;
    else if (!strcmp(name, "r1")) cpu->reg.r1 = value;
    else if (!strcmp(name, "r2")) cpu->reg.r2 = value;
    else if (!strcmp(name, "r3")) cpu->reg.r3 = value;
    else if (!strcmp(name, "r4")) cpu->reg.r4 = value;
    else if (!strcmp(name, "r5")) cpu->reg.r5 = value;
    else if (!strcmp(name, "r6")) cpu->reg.r6 = value;
    else if (!strcmp(name, "r7")) cpu->reg.r7 = value;
    else if (!strcmp(name, "r8")) cpu->reg.r8 = value;
    else if (!strcmp(name, "r9")) cpu->reg.r9 = value;
    else if (!strcmp(name, "r10")) cpu->reg.r10 = value;
    else if (!strcmp(name, "r11")) cpu->reg.r11 = value;
    else if (!strcmp(name, "r12")) cpu->reg.r12 = value;
    else if (!strcmp(name, "r13")) cpu->reg.r13 = value;
    else if (!strcmp(name, "r14")) cpu->reg.r14 = value;
    else if (!strcmp(name, "r15")) cpu->reg.r15 = value;
    else if (!strcmp(name, "r16")) cpu->reg.r16 = value;
    else if (!strcmp(name, "r17")) cpu->reg.r17 = value;
    else if (!strcmp(name, "r18")) cpu->reg.r18 = value;
    else if (!strcmp(name, "r19")) cpu->reg.r19 = value;
    else if (!strcmp(name, "r20")) cpu->reg.r20 = value;
    else if (!strcmp(name, "r21")) cpu->reg.r21 = value;
    else if (!strcmp(name, "r22")) cpu->reg.r22 = value;
    else if (!strcmp(name, "r23")) cpu->reg.r23 = value;
    else if (!strcmp(name, "r24")) cpu->reg.r24 = value;
    else if (!strcmp(name, "r25")) cpu->reg.r25 = value;
    else if (!strcmp(name, "r26")) cpu->reg.r26 = value;
    else if (!strcmp(name, "r27")) cpu->reg.r27 = value;
    else if (!strcmp(name, "r28")) cpu->reg.r28 = value;
    else if (!strcmp(name, "r29")) cpu->reg.r29 = value;
    else if (!strcmp(name, "r30")) cpu->reg.r30 = value;
    else if (!strcmp(name, "r31")) cpu->reg.r31 = value;
    else if (!strcmp(name, "f0")) cpu->reg.f0 = (uint8_t)value;
    else if (!strcmp(name, "f1")) cpu->reg.f1 = (uint8_t)value;
    else if (!strcmp(name, "f2")) cpu->reg.f2 = (uint8_t)value;
    else if (!strcmp(name, "f3")) cpu->reg.f3 = (uint8_t)value;
    else if (!strcmp(name, "f4")) cpu->reg.f4 = (uint8_t)value;
    else if (!strcmp(name, "f5")) cpu->reg.f5 = (uint8_t)value;
    else if (!strcmp(name, "f6")) cpu->reg.f6 = (uint8_t)value;
    else if (!strcmp(name, "f7")) cpu->reg.f7 = (uint8_t)value;
    else if (!strcmp(name, "hsp")) cpu->reg.hsp = (uint16_t)value;
    else if (!strcmp(name, "rsp")) cpu->reg.rsp = (uint16_t)value;
}

void RetStackPush(CPU *cpu, uint16_t value) {
    cpu->memory.ReturnStack[cpu->reg.rsp].value = value;
    cpu->reg.rsp++;
}

uint16_t RetStackPop(CPU *cpu) {
    cpu->reg.rsp--;
    return cpu->memory.ReturnStack[cpu->reg.rsp].value;
}

void HardwareStackPush(CPU *cpu, uint32_t value) {
    cpu->memory.HardwareStack[cpu->reg.hsp].value = value;
    cpu->reg.hsp++;
}

uint32_t HardwareStackPop(CPU *cpu) {
    cpu->reg.hsp--;
    return cpu->memory.HardwareStack[cpu->reg.hsp].value;
}
