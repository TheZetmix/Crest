from enum import Enum, auto

C_KEYWORDS = {
    'auto', 'break', 'case', 'const', 'continue', 'default',
    'double', 'else', 'enum', 'extern', 'var', 'fn', 'for', 'if',
    'register', 'return', 'static',
    'struct', 'match', 'typedef', 'union', 'volatile', 'while', 'foreach'
}

class TokType(Enum):
    KEYWORD_AUTO         = auto()
    KEYWORD_BREAK        = auto()
    KEYWORD_CASE         = auto()
    KEYWORD_CONST        = auto()
    KEYWORD_CONTINUE     = auto()
    KEYWORD_DEFAULT      = auto()
    KEYWORD_DOUBLE       = auto()
    KEYWORD_ELSE         = auto()
    KEYWORD_ENUM         = auto()
    KEYWORD_EXTERN       = auto()
    KEYWORD_VAR          = auto()
    KEYWORD_FN           = auto()
    KEYWORD_FOR          = auto()
    KEYWORD_IF           = auto()
    KEYWORD_REGISTER     = auto()
    KEYWORD_RETURN       = auto()
    KEYWORD_STATIC       = auto()
    KEYWORD_STRUCT       = auto()
    KEYWORD_MATCH        = auto()
    KEYWORD_TYPEDEF      = auto()
    KEYWORD_UNION        = auto()
    KEYWORD_VOLATILE     = auto()
    KEYWORD_WHILE        = auto()
    KEYWORD_FOREACH      = auto()
    
    ID                   = auto()
    DIRECTIVE            = auto()
    
    INTEGER_LITERAL      = auto()
    FLOAT_LITERAL        = auto()
    CHAR_LITERAL         = auto()
    STRING_LITERAL       = auto()
    ARROW_STRING_LITERAL = auto()
    
    SEMICOLON            = auto() # ;
    COMMA                = auto() # ,
    DOT                  = auto() # .
    COLON                = auto() # :
    
    ASSIGN               = auto() # =
    PLUS                 = auto() # +
    MINUS                = auto() # -
    MULTIPLY             = auto() # *
    DIVIDE               = auto() # /
    MODULO               = auto() # %
    
    EQ                   = auto() # =
    NE                   = auto() # !
    LT                   = auto() # <
    GT                   = auto() # >
    LE                   = auto() # <
    GE                   = auto() # >
    
    AND                  = auto() # &
    OR                   = auto() # |
    NOT                  = auto() # !
    
    BIT_AND              = auto() # &
    BIT_OR               = auto() # |
    BIT_XOR              = auto() # ^
    BIT_NOT              = auto() # ~
    SHIFT_LEFT           = auto() # <<
    SHIFT_RIGHT          = auto() # >>
    
    PLUS_ASSIGN          = auto() # +=
    MINUS_ASSIGN         = auto() # -=
    MULTIPLY_ASSIGN      = auto() # *=
    DIVIDE_ASSIGN        = auto() # /=
    MODULO_ASSIGN        = auto() # %=
    AND_ASSIGN           = auto() # &=
    OR_ASSIGN            = auto() # |=
    XOR_ASSIGN           = auto() # ^=
    SHIFT_LEFT_ASSIGN    = auto() # <=
    SHIFT_RIGHT_ASSIGN   = auto() # >=
    
    INCREMENT            = auto() # +
    DECREMENT            = auto() # -
    
    ADDRESS              = auto() # &
    DEREFERENCE          = auto() # *
    
    ARROW                = auto() # -
    QUESTION             = auto() # ?
    
    LPAREN               = auto() # (
    RPAREN               = auto() # )
    LBRACE               = auto() # [
    RBRACE               = auto() # ]
    LBODY                = auto() # {
    RBODY                = auto() # }
    
    EOF                  = auto()
    NEWLINE              = auto()
    UNKNOWN              = auto()

class Token:
    def __init__(self, type, literal, pos):
        self.type = type
        self.literal = literal
        self.pos = pos
