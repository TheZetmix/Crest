from lexer import *
from token import *
from error import *
import os

class Preprocessor:
    def __init__(self, lexer, included_files=None):
        self.new_tokens = lexer.tokens[:]
        self.pos = 0
        self.lexer = lexer
        self.current = self.new_tokens[self.pos]
        
        self.included = included_files if included_files else []
        
        while self.new_tokens[self.pos].type != TokType.EOF:
            if self.current.type == TokType.KEYWORD_USING:
                self.include_via_using()
            elif self.current.type == TokType.NAMESPACE_DEREF:
                self.remove()
            else:
                self.next()
        
        lexer.tokens = self.new_tokens
        lexer.pos = 0
        lexer.current = lexer.tokens[0]
        
    def include_via_using(self):
        self.remove()
        
        include_libname = '/'.join((os.getcwd() + "/" + self.lexer.filename).split('/')[:-1]) + '/'
        while self.current.type != TokType.SEMICOLON:
            include_libname += self.current.literal
            self.remove()
        include_libname += ".crs"
        
        # TODO: refactor this, if there is no such thing - recursive preprocessor will concatenate filepaths between each other
        include_libname = '/' + include_libname.split('//')[-1]
        
        if not os.path.exists(include_libname):
            error(f"file {include_libname} not found, line {self.current.pos}")
        self.remove(expect=TokType.SEMICOLON)
        
        if include_libname not in self.included:
            self.included.append(include_libname)
            f = open(include_libname, 'r').read()
            included_lexer = Lexer(f, include_libname)
            included_lexer.make_all_tokens()
            
            included_preprocessor = Preprocessor(included_lexer, included_files=self.included)
            included_lexer.tokens = included_preprocessor.new_tokens
            
            self.insert(self.pos, included_lexer.tokens[:-1])
            
    
    def insert(self, pos, to_insert):
        self.new_tokens[pos:pos] = to_insert
        self.current = self.new_tokens[self.pos]
        
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
