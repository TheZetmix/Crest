from lexer import *
from token import *
from error import *
import os

class Preprocessor:
    def __init__(self, lexer, included_files=None):
        self.new_tokens = [i for i in lexer.tokens]
        self.pos = 0
        self.lexer = lexer
        self.current = self.new_tokens[self.pos]
        
        self.included = included_files if included_files else []
        
        while self.new_tokens[self.pos].type != TokType.EOF:
            if self.current.type == TokType.KEYWORD_USING:
                self.include_via_using()
            if self.current.literal == "::":
                self.remove()
                
            self.next()
    
    def include_via_using(self):
        self.remove()
        
        include_libname = '/'.join((os.getcwd() + "/" + self.lexer.filename).split('/')[:-1]) + '/'
        while self.current.type != TokType.SEMICOLON:
            include_libname += self.current.literal
            self.remove()
        use_libname = self.new_tokens[self.pos-1].literal
        include_libname += ".crs"
        if not os.path.exists(include_libname):
            error(f"file not found, line {self.current.pos}")
        self.remove(expect=TokType.SEMICOLON)
        
        
        
    def insert(self, pos, to_insert):
        self.new_tokens[pos:pos] = to_insert
    
    def remove(self, expect=None):
        if expect != None and self.current.type != expect:
            error(f"expected {expect}, got {self.current.literal}, line {self.current.pos}")
        del self.new_tokens[self.pos]
        self.current = self.new_tokens[self.pos]
    
    def next(self):
        self.pos += 1
        self.current = self.new_tokens[self.pos]
    
    def expect(self, type):
        if self.current.type == TokType.NEWLINE and not \
           (type == TokType.SEMICOLON):
            self.next()
        if self.pos < len(self.new_tokens) and self.current.type == type:
            self.pos += 1
            self.current = self.new_tokens[self.pos]
        else:
            error(f"expected {type}, got {repr(self.current.literal)}, line {self.current.pos+1}")
