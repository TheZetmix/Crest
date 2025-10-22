from lexer import *
from token import *
from error import *

class Preprocessor:
    def __init__(self, lexer):
        self.modified_lexer = lexer
