import sys
from token import *

def split_src(src, delims):
    bol = 0
    res = []
    
    string = False
    
    for i, ch in enumerate(src):
        if ch in ['"', "'"]: string = not string
        else:
            if ch in delims:
                if not string:
                    res.append(src[bol:i])
                    res.append(ch)
                    bol = i + 1
                
    
    if bol < len(src):
        res.append(src[bol:])
        
    res = [i for i in res if i not in " "]
    
    for i, part in enumerate(res):
        if (part in '=<>|&~!+-*/%^' and res[i+1] == '=') or (part in "+-" and res[i+1] in "+-"):
            res[i] += res[i+1]
            del res[i + 1]
            
    return res

def get_part_type(part):
    part = part.strip()
    if not part: return -1
    try:
        int(part)
        return 1
    except ValueError: pass
    try:
        float(part)
        return 2
    except ValueError: pass
    return -1

def check_in_class(class_, s):
    found = False
    for i in [i for i in dir(class_) if not i.startswith("__") and not i.endswith("__")]:
        if getattr(class_, i) == s:
            found = True
    return found

def get_opers_in_string(class_):
    res = ""
    for i in [i for i in dir(class_) if not i.startswith("__") and not i.endswith("__")]:
        res += getattr(class_, i)
    return "".join(set(res))

def get_keyword_token(keyword: str):
    keyword_to_toktype = {
        'auto'     : TokType.KEYWORD_AUTO,
        'break'    : TokType.KEYWORD_BREAK,
        'case'     : TokType.KEYWORD_CASE,
        'const'    : TokType.KEYWORD_CONST,
        'continue' : TokType.KEYWORD_CONTINUE,
        'default'  : TokType.KEYWORD_DEFAULT,
        'double'   : TokType.KEYWORD_DOUBLE,
        'else'     : TokType.KEYWORD_ELSE,
        'enum'     : TokType.KEYWORD_ENUM,
        'extern'   : TokType.KEYWORD_EXTERN,
        'var'      : TokType.KEYWORD_VAR,
        'fn'       : TokType.KEYWORD_FN,
        'for'      : TokType.KEYWORD_FOR,
        'if'       : TokType.KEYWORD_IF,
        'register' : TokType.KEYWORD_REGISTER,
        'return'   : TokType.KEYWORD_RETURN,
        'static'   : TokType.KEYWORD_STATIC,
        'struct'   : TokType.KEYWORD_STRUCT,
        'match'    : TokType.KEYWORD_MATCH,
        'typedef'  : TokType.KEYWORD_TYPEDEF,
        'union'    : TokType.KEYWORD_UNION,
        'volatile' : TokType.KEYWORD_VOLATILE,
        'while'    : TokType.KEYWORD_WHILE,
        'foreach'  : TokType.KEYWORD_FOREACH,
    }
    return keyword_to_toktype.get(keyword)

class Lexer:
    def __init__(self, src, filename):
        self.tokens = []
        self.src = src
        self.filename = filename
        self.delims = " .,:;(){}[]\"\'+-*/%=!&|<>^~?\n"
        self.src_split = split_src(src, self.delims)
        
    def make_all_tokens(self):
        pos = 0
        for i in self.src_split:
            if i == '\n': pos += 1
            self.tokens.append(self.make_token(i, pos))
            
        self.tokens.append(Token(TokType.EOF, "", pos))
        
    def make_token(self, part, pos):
        if part in C_KEYWORDS:
            return Token(get_keyword_token(part), part, pos)
        elif get_part_type(part) == 1:
            return Token(TokType.INTEGER_LITERAL, part, pos)
        elif part.startswith("0x"):
            return Token(TokType.INTEGER_LITERAL, int(part[2:], 16), pos)
        elif part.startswith("0b"):
            return Token(TokType.INTEGER_LITERAL, int(part[2:], 2), pos)
        elif get_part_type(part) == 2:
            return Token(TokType.FLOAT_LITERAL, part, pos)
        elif part.startswith("'") and part.endswith("'"):
            return Token(TokType.CHAR_LITERAL, part, pos)
        elif part.startswith('"') and part.endswith('"'):
            return Token(TokType.STRING_LITERAL, part, pos)
        elif part.startswith('<') and part.endswith('>'):
            return Token(TokType.ARROW_STRING_LITERAL, part, pos)
        elif part == ';':
            return Token(TokType.SEMICOLON, part, pos)
        elif part == ',':
            return Token(TokType.COMMA, part, pos)
        elif part == '.':
            return Token(TokType.DOT, part, pos)
        elif part == ':':
            return Token(TokType.COLON, part, pos)
        elif part == '=':
            return Token(TokType.ASSIGN, part, pos)
        elif part == '+':
            return Token(TokType.PLUS, part, pos)
        elif part == '-':
            return Token(TokType.MINUS, part, pos)
        elif part == '*':
            return Token(TokType.MULTIPLY, part, pos)
        elif part == '/':
            return Token(TokType.DIVIDE, part, pos)
        elif part == '%':
            return Token(TokType.MODULO, part, pos)
        elif part == '==':
            return Token(TokType.EQ, part, pos)
        elif part == '!=':
            return Token(TokType.NE, part, pos)
        elif part == '<':
            return Token(TokType.LT, part, pos)
        elif part == '>':
            return Token(TokType.GT, part, pos)
        elif part == '<=':
            return Token(TokType.LE, part, pos)
        elif part == '>=':
            return Token(TokType.GE, part, pos)
        elif part == '&&':
            return Token(TokType.AND, part, pos)
        elif part == '||':
            return Token(TokType.OR, part, pos)
        elif part == '!':
            return Token(TokType.NOT, part, pos)
        elif part == '&':
            return Token(TokType.BIT_AND, part, pos)
        elif part == '|':
            return Token(TokType.BIT_OR, part, pos)
        elif part == '^':
            return Token(TokType.BIT_XOR, part, pos)
        elif part == '~':
            return Token(TokType.BIT_NOT, part, pos)
        elif part == '<<':
            return Token(TokType.SHIFT_LEFT, part, pos)
        elif part == '>>':
            return Token(TokType.SHIFT_RIGHT, part, pos)
        elif part == '+=':
            return Token(TokType.PLUS_ASSIGN, part, pos)
        elif part == '-=':
            return Token(TokType.MINUS_ASSIGN, part, pos)
        elif part == '*=':
            return Token(TokType.MULTIPLY_ASSIGN, part, pos)
        elif part == '/=':
            return Token(TokType.DIVIDE_ASSIGN, part, pos)
        elif part == '%=':
            return Token(TokType.MODULO_ASSIGN, part, pos)
        elif part == '&=':
            return Token(TokType.AND_ASSIGN, part, pos)
        elif part == '|=':
            return Token(TokType.OR_ASSIGN, part, pos)
        elif part == '^=':
            return Token(TokType.XOR_ASSIGN, part, pos)
        elif part == '<<=':
            return Token(TokType.SHIFT_LEFT_ASSIGN, part, pos)
        elif part == '>>=':
            return Token(TokType.SHIFT_RIGHT_ASSIGN, part, pos)
        elif part == '++':
            return Token(TokType.INCREMENT, part, pos)
        elif part == '--':
            return Token(TokType.DECREMENT, part, pos)
        elif part == '&':
            return Token(TokType.ADDRESS, part, pos)
        elif part == '*':
            return Token(TokType.DEREFERENCE, part, pos)
        elif part == '->':
            return Token(TokType.ARROW, part, pos)
        elif part == '?':
            return Token(TokType.QUESTION, part, pos)
        elif part == '(':
            return Token(TokType.LPAREN, part, pos)
        elif part == ')':
            return Token(TokType.RPAREN, part, pos)
        elif part == '[':
            return Token(TokType.LBRACE, part, pos)
        elif part == ']':
            return Token(TokType.RBRACE, part, pos)
        elif part == '{':
            return Token(TokType.LBODY, part, pos)
        elif part == '}':
            return Token(TokType.RBODY, part, pos)
        elif part[0] == '#':
            return Token(TokType.DIRECTIVE, part[1:], pos)
        elif part == '\n':
            return Token(TokType.NEWLINE, part, pos)
        else:
            return Token(TokType.ID, part, pos)
