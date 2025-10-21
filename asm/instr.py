auto_counter = 0
def auto(reset=False):
    global auto_counter
    if reset: auto_counter = 0
    res = auto_counter
    auto_counter+=1
    return res

INSTRUCTIONS_OPS = {
    "mov"     : f"{auto():02x}",  # move data between registers/memory
    "add"     : f"{auto():02x}",  # arithmetic addition
    "sub"     : f"{auto():02x}",  # arithmetic subtraction
    "mul"     : f"{auto():02x}",  # unsigned multiplication
    "div"     : f"{auto():02x}",  # unsigned division
    "mod"     : f"{auto():02x}",  # modulus operation
    "inc"     : f"{auto():02x}",  # increment operand by 1
    "dec"     : f"{auto():02x}",  # decrement operand by 1
    "and"     : f"{auto():02x}",  # bitwise AND
    "or"      : f"{auto():02x}",  # bitwise OR
    "xor"     : f"{auto():02x}",  # bitwise XOR
    "not"     : f"{auto():02x}",  # bitwise NOT
    "shl"     : f"{auto():02x}",  # shift left
    "shr"     : f"{auto():02x}",  # shift right (logical)
    "push"    : f"{auto():02x}",  # push onto stack
    "pop"     : f"{auto():02x}",  # pop from stack
    "lea"     : f"{auto():02x}",  # load effective address
    "jmp"     : f"{auto():02x}",  # unconditional jump
    "call"    : f"{auto():02x}",  # call subroutine
    "ret"     : f"{auto():02x}",  # return from subroutine
    "je"      : f"{auto():02x}",  # jump if equal
    "jne"     : f"{auto():02x}",  # jump if not equal
    "jg"      : f"{auto():02x}",  # jump if greater (signed)
    "jl"      : f"{auto():02x}",  # jump if less (signed)
    "jge"     : f"{auto():02x}",  # jump if greater or equal (signed)
    "jle"     : f"{auto():02x}",  # jump if less or equal (signed)
    "cmp"     : f"{auto():02x}",  # compare operands
    "nop"     : f"{auto():02x}",  # no operation
    "hlt"     : f"{auto():02x}",  # halt execution
    "int"     : f"{auto():02x}",  # software interrupt
    "trap"    : f"{auto():02x}",  # breakpoint
    "str"     : f"{auto():02x}",  # store value in memory
    "ldr"     : f"{auto():02x}",  # load value from memory
    "pusha"   : f"{auto():02x}",  # push all registers
    "popa"    : f"{auto():02x}",  # pop all registers
    "lean"    : f"{auto():02x}",  # load number
    "ffp"     : f"{auto():02x}",  # find free place
    "movb"    : f"{auto():02x}",  # move byte
    "movw"    : f"{auto():02x}",  # move word
    "movd"    : f"{auto():02x}",  # move dword
    "movst"   : f"{auto():02x}",  # move to stack
    "smp"     : f"{auto():02x}",  # set memory permission
}

REGISTERS = [
    "r0",  "r1",  "r2",  "r3", 
    "r4",  "r5",  "r6",  "r7", 
    "r8",  "r9",  "r10", "r11", 
    "r12", "r13", "r14", "r15", 
    "r16", "r17", "r18", "r19", 
    "r20", "r21", "r22", "r23", 
    "r24", "r25", "r26", "r27", 
    "r28", "r29", "r30", "r31", 
    
    "f0", "f1", "f2", "f3", 
    "f4", "f5", "f6", "f7",
    "hsp", "rsp" 
]
