from token import *
from lexer import *
from instr import *
import sys

LABEL_BASE_ADDRESS = 0

def get_token_len(token):
    if token.type == TokType.INSTRUCTION:  return 1 # 00 (mov)
    elif token.type == TokType.REGISTER:   return 2 # 52 00 (reg eax)
    elif token.type == TokType.POINTER:    return 1 # 50
    elif token.type == TokType.NUMBER:     return 5 # 53 00 00 00 10
    elif token.type == TokType.HEX_NUMBER: return 5 # 53 00 00 de ad
    elif token.type == TokType.LABEL_USE:  return 5 # 53 00 00 de ad
    elif token.type == TokType.STRING:     return len(token.literal) # "Hello": 5
    elif token.type == TokType.CHAR:       return 5 # 53 00 00 00 20 ' '
    elif token.type == TokType.BYTE:       return 1 # 24
    else:                                  return 0

def format_byte(num):
    return f"{num:02x}"

def find_label_by_name(name, labels):
    for i in range(0, len(labels)):
        if labels[i].name == name:
            return i
    return -1
    
class Label:
    def __init__(self, name, pc):
        self.name = name
        self.pc = pc

class Compiler:
    def __init__(self, lexer, filename):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.bytecode_len = 0
        self.bytecode = []
        self.labels = []
        self.validate_all_instructions()
        
        for i in self.tokens:
            self.bytecode_len += get_token_len(i)
            if i.type == TokType.LABEL_DEF:
                self.labels.append(Label(i.literal, self.bytecode_len));
    
        for j in range(len(self.tokens)):
            i = self.tokens[j]
            if i.type == TokType.INSTRUCTION:
                self.bytecode.append(INSTRUCTIONS_OPS[i.literal])
            if i.type == TokType.REGISTER:
                self.bytecode.append("52")
                self.bytecode.append(format_byte(REGISTERS.index(i.literal)))
            if i.type == TokType.POINTER:
                self.bytecode.append("50")
            if i.type == TokType.NUMBER:
                self.bytecode.append("53")
                hex_num = f"{int(i.literal):08x}"
                self.bytecode.append(hex_num[0:2])
                self.bytecode.append(hex_num[2:4])
                self.bytecode.append(hex_num[4:6])
                self.bytecode.append(hex_num[6:8])
            if i.type == TokType.HEX_NUMBER:
                self.bytecode.append("53")
                hex_num = f"{int(i.literal[2:], 16):08x}"
                self.bytecode.append(hex_num[0:2])
                self.bytecode.append(hex_num[2:4])
                self.bytecode.append(hex_num[4:6])
                self.bytecode.append(hex_num[6:8])
            if i.type == TokType.STRING:
                for j in i.literal:
                    self.bytecode.append(format_byte(ord(j)))
            if i.type == TokType.CHAR:
                self.bytecode.append("53")
                hex_num = f"{ord(i.literal):08x}"
                self.bytecode.append(hex_num[0:2])
                self.bytecode.append(hex_num[2:4])
                self.bytecode.append(hex_num[4:6])
                self.bytecode.append(hex_num[6:8])
            if i.type == TokType.BYTE:
                self.bytecode.append(i.literal[2:])
            if i.type == TokType.LABEL_USE:
                label_pc = find_label_by_name(i.literal, self.labels)
                if label_pc == -1:
                    ERROR(i.pos, f"identifier '{i.literal}' not found")
                self.bytecode.append("53")
                hex_num = f"{self.labels[label_pc].pc:08x}"
                self.bytecode.append(hex_num[0:2])
                self.bytecode.append(hex_num[2:4])
                self.bytecode.append(hex_num[4:6])
                self.bytecode.append(hex_num[6:8])
                
        with open(filename, "wb") as f:
            f.write(bytes.fromhex("".join(self.bytecode)))
            
        print(f"compilation finished: wrote {len(self.bytecode)} bytes")

    def validate_all_instructions(self):
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            if token.type == TokType.INSTRUCTION:
                args = self.lexer.get_instruction_args(i)
                validate_instruction(token.literal, args, token.pos)
                i += len(args)
            i += 1

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f: f = f.read()
    a = Lexer(f, sys.argv[1])
    b = Compiler(a, sys.argv[-1])
