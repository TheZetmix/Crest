from lexer import *
from token import *
from error import *
import os

class Preprocessor:
    def __init__(self, lexer, included_files=None):
        self.new_tokens = lexer.tokens
        self.pos = 0
        self.current = self.new_tokens[self.pos]
        
        self.included = included_files if included_files else []
        
        while self.new_tokens[self.pos].type != TokType.EOF:
            if self.current.type == TokType.KEYWORD_USING:
                self.include_via_using()
            if self.current.literal == "::":
                new_method = "namespace_" + self.new_tokens[self.pos-1].literal + "_included_" + self.new_tokens[self.pos+1].literal
                del self.new_tokens[self.pos-1:self.pos+2]
                self.new_tokens[self.pos-2] = Token(TokType.ID, new_method, self.current.pos)
                
            self.next()
    
    def include_via_using(self):
        start_pos = self.pos
        self.next()
        
        include_libname = "./"
        while self.current.type != TokType.SEMICOLON:
            include_libname += self.current.literal
            self.next()
        use_libname = self.new_tokens[self.pos-1].literal
        include_libname += ".crs"
        if not os.path.exists(include_libname):
            error(f"file not found, line {self.current.pos}")
        
        self.expect(TokType.SEMICOLON)
        end_pos = self.pos
        del self.new_tokens[start_pos:end_pos]
        
        if include_libname not in self.included:
            self.included.append(include_libname)
            with open(include_libname, "r") as f:
                f = f.read()
                lexer = Lexer(f, include_libname)
                lexer.make_all_tokens()
                
                preprocessor = Preprocessor(lexer, self.included)
                for i, tok in enumerate(lexer.tokens): # process func defs
                    if tok.type == TokType.KEYWORD_FN:
                        method_new_name = f"namespace_{use_libname}_included_{lexer.tokens[i+1].literal}"
                        lexer.tokens[i+1] = Token(TokType.ID, method_new_name, tok.pos)
                lexer.tokens = preprocessor.new_tokens
                
            insert_len = len(lexer.tokens)
            self.new_tokens[start_pos:start_pos] = lexer.tokens[0:-2]
            self.pos = start_pos + insert_len
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
