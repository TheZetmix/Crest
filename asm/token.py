auto_counter = 0
def auto(reset=False):
    global auto_counter
    if reset: auto_counter = 0
    res = auto_counter
    auto_counter+=1
    return res

class TokType:
    INSTRUCTION   = auto()
    DIRECTIVE     = auto()
    REGISTER      = auto()
    POINTER       = auto()
    NUMBER        = auto()
    HEX_NUMBER    = auto()
    STRING        = auto()
    CHAR          = auto()
    BYTE          = auto()
    LABEL_DEF     = auto()
    LABEL_USE     = auto()
    COLON         = auto()
    COMMA         = auto()
    NEWLINE       = auto()

class Token:
    def __init__(self, type, literal, pos):
        self.type    = type
        self.literal = literal
        self.pos     = pos
    
    def __repr__(self):
        type_names = {
            TokType.INSTRUCTION : "INSTRUCTION",
            TokType.DIRECTIVE   : "DIRECTIVE  ",
            TokType.REGISTER    : "REGISTER   ",
            TokType.POINTER     : "POINTER    ",
            TokType.NUMBER      : "NUMBER     ",
            TokType.HEX_NUMBER  : "HEX_NUMBER ",
            TokType.STRING      : "STRING     ",
            TokType.BYTE        : "BYTE       ",
            TokType.LABEL_DEF   : "LABEL_DEF  ",
            TokType.LABEL_USE   : "LABEL_USE  ",
            TokType.COLON       : "COLON      ",
            TokType.COMMA       : "COMMA      ",
            TokType.NEWLINE     : "NEWLINE    ",
        }
        return (f"{type_names.get(self.type, 'UNKNOWN'):<12} "
                f"{repr(self.literal):<20} "
                f"{str(self.pos):<10} ")
