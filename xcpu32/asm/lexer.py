from token import *
from instr import *
from error import *
import sys
import re
import os

constants = {}

def lex_split(s, separators):
    escaped_separators = re.escape(separators)
    pattern = f'("[^"]*")|([{escaped_separators}])|([^{escaped_separators}"]+)'
    matches = re.finditer(pattern, s)
    result = []
    for match in matches:
        part = match.group(1) or match.group(2) or match.group(3)
        if part:
            result.append(part)
    return result
1

class Lexer:
    def __init__(self, src, src_file_path):
        self.src = src
        self.tokens = []
        line = 0
        delims = ":*,\n ()"
        src_split = [i for i in lex_split(self.src, delims) if i not in " "]
        comment = False
        i = 0
        while i < len(src_split):
            if src_split[i] == ';':
                comment = not comment
                del src_split[i]
            elif comment:
                del src_split[i]
            else:
                i += 1
        
        i = 0
        while i < len(src_split):
            part = src_split[i]
            if part == "include":
                src_dir = os.path.dirname(os.path.abspath(src_file_path))
                include_filename = src_split[i+1][1:-1]
                include_path = os.path.join(src_dir, include_filename)
                with open(include_path, "r") as f:
                    f_content = f.read()
                    new_file_split = [j for j in lex_split(f_content, delims) if j not in " "]
                    del src_split[i:i+2]
                    src_split = src_split[:i] + new_file_split + src_split[i:]
                    line -= f_content.count('\n')
                i += len(new_file_split)
            i += 1
        for i, part in enumerate(src_split):
            if part == "define":
                if src_split[i+1] in constants:
                    ERROR("preprocess", f"{src_split[i+1]} redefined")
                args = []
                j = 0
                if src_split[i+2] == '(':
                    while src_split[i+3+j] != ')':
                        if src_split[i+3+j] != ',':
                            args.append(src_split[i+3+j])
                        j+=1
                d_len = 0
                while src_split[i+d_len] != "\n":
                    if src_split[i+d_len] == '\\':
                        if src_split[i+d_len+1] == '\n': del src_split[i+d_len+1]
                    d_len+=1;
                val = src_split[i+2:i+2+d_len-2]
                if args: val = val[j+2:]
                constants[src_split[i+1]] = {"args": args, "body": val}
                del src_split[i:i+d_len]
        
        for i, tok in enumerate(src_split):
            if tok in constants:
                macro = constants[tok]
                macro_args = macro["args"]
                replacement = []
                j = 1
                if i + j < len(src_split) and src_split[i + j] == '(':
                    j += 1
                    while i + j < len(src_split) and src_split[i + j] != ')':
                        if src_split[i + j] != ',':
                            replacement.append(src_split[i + j])
                        j += 1
                    j += 1
                
                if "".join(macro_args) == '...': # variadic args
                    raise Exception("not implemented")
                elif len(replacement) != len(macro_args):
                    ERROR("preprocess", 
                          f"wrong number of arguments for {tok}; expected {len(macro_args)}, got {len(replacement)}")
                
                del src_split[i:i+j]
                
                for elem in reversed(macro["body"]):
                    if elem in macro_args:
                        idx = macro_args.index(elem)
                        src_split.insert(i, replacement[idx])
                    elif elem == '\\':
                        src_split.insert(i, "\n")
                    else:
                        src_split.insert(i, elem)
        cur_line = 0
        for i, tok in enumerate(src_split):
            if "%AUTO%" in tok:
                src_split[i]= tok.replace("%AUTO%", str(cur_line))
            if tok == '#NEWMACROID':
                del src_split[i]
                cur_line += 1
        
        i = -1
        while i < len(src_split):
            token = src_split[i]
            if token in INSTRUCTIONS_OPS:
                self.tokens.append(Token(TokType.INSTRUCTION, token, line))
            elif token in REGISTERS:
                self.tokens.append(Token(TokType.REGISTER, token, line))
            elif token[0] == '%':
                self.tokens.append(Token(TokType.DIRECTIVE, token[1:], line))
            elif token == '\n':
                self.tokens.append(Token(TokType.NEWLINE, token, line))
                line += 1
            elif token == ':':
                self.tokens.append(Token(TokType.COLON, token, line))
            elif token == ',':
                self.tokens.append(Token(TokType.COMMA, token, line))
            elif token == '*':
                self.tokens.append(Token(TokType.POINTER, token, line))
            elif bool(re.fullmatch(r'^-?\d+(\.\d+)?$', token)):
                self.tokens.append(Token(TokType.NUMBER, token, line))
            elif token.startswith("0x"):
                self.tokens.append(Token(TokType.HEX_NUMBER, token, line))
            elif i + 1 < len(src_split) and src_split[i + 1] == ':':
                self.tokens.append(Token(TokType.LABEL_DEF, token, line))
            elif token == "byte":
                self.tokens.append(Token(TokType.BYTE, src_split[i+1], line))
                src_split.pop(i+1)
            elif token.startswith('"'):
                if len(token) < 2 or not token.endswith('"'):
                    ERROR(line, "unclosed string literal")
                self.tokens.append(Token(TokType.STRING, token[1:-1], line))
            elif token.startswith('\''):
                self.tokens.append(Token(TokType.CHAR, token[1:-1], line))
                if len(token) < 2 or not token.endswith("'"):
                    ERROR(line, "unclosed char literal")
            else:
                self.tokens.append(Token(TokType.LABEL_USE, token, line))
            
            i += 1
        
        for i in self.tokens:
            print(i.literal, end=" " if i.literal != "\n" else "")
            
    def get_instruction_args(self, start_idx):
        args = []
        i = start_idx + 1
        while i < len(self.tokens):
            token = self.tokens[i]
            if token.type in [TokType.INSTRUCTION, TokType.NEWLINE]:
                break
            if token.type not in [TokType.COMMA, TokType.COLON, TokType.POINTER]:
                args.append(token)
            i += 1
        return args
