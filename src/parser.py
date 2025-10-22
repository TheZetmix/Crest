from lexer import *
from token import *
from error import *
from enum import Enum, auto

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        
        self.ir = []
        self.pos = 0
        self.current = self.tokens[self.pos]
        self.entered_bodies = []
        
        while self.current.type != TokType.EOF:
            if self.current.type == TokType.KEYWORD_CONTINUE:
                self.next()
                self.expect(TokType.SEMICOLON)
                self.ir.append(self.get_ir_node("Continue"))
            if self.current.type == TokType.KEYWORD_BREAK:
                self.next()
                self.expect(TokType.SEMICOLON)
                self.ir.append(self.get_ir_node("Break"))
            if self.current.type == TokType.KEYWORD_STRUCT:
                parsed = self.parse_struct()
                self.ir.append(parsed)
            if self.current.type in [TokType.KEYWORD_CASE, TokType.KEYWORD_DEFAULT]:
                parsed = self.parse_match_case()
                self.ir.append(parsed)
                self.entered_bodies.append(parsed)
            if self.current.type == TokType.KEYWORD_MATCH:
                parsed = self.parse_match()
                self.ir.append(parsed)
                self.entered_bodies.append(parsed)
            if self.current.type == TokType.KEYWORD_FOR:
                parsed = self.parse_for()
                self.ir.append(parsed)
                self.entered_bodies.append(parsed)
            if self.current.type == TokType.LBRACE:
                if self.peek().type == TokType.NOT and \
                   self.peek(n=2).type == TokType.ID and \
                   self.peek(n=3).type == TokType.RBRACE:
                    parsed = self.parse_inline_c()
                    self.ir.append(parsed)
            if self.current.type == TokType.KEYWORD_FOREACH:
                parsed = self.parse_foreach()
                self.ir.append(parsed)
                self.entered_bodies.append(parsed)
            if self.current.type == TokType.DIRECTIVE:
                parsed = self.parse_directive()
                self.ir.append(parsed)
            if self.current.type == TokType.KEYWORD_WHILE:
                parsed = self.parse_while()
                self.ir.append(parsed)
                self.entered_bodies.append(parsed)
            if self.current.type == TokType.KEYWORD_IF:
                parsed = self.parse_if()
                self.ir.append(parsed)
                self.entered_bodies.append(parsed)
            if self.current.type == TokType.KEYWORD_ELSE:
                if self.peek().type == TokType.KEYWORD_IF:
                    parsed = self.parse_elseif()
                    self.ir.append(parsed)
                    self.entered_bodies.append(parsed)
                else:
                    parsed = self.parse_else()
                    self.ir.append(parsed)
                    self.entered_bodies.append(parsed)
            if self.current.type == TokType.KEYWORD_RETURN:
                parsed = self.parse_return()
                self.ir.append(parsed)
            if self.current.type in [
                        TokType.ASSIGN,
                        TokType.PLUS_ASSIGN,
                        TokType.MINUS_ASSIGN,
                        TokType.MULTIPLY_ASSIGN,
                        TokType.DIVIDE_ASSIGN,
                        TokType.MODULO_ASSIGN,
                        TokType.AND_ASSIGN,
                        TokType.OR_ASSIGN,
                        TokType.XOR_ASSIGN,
                        TokType.SHIFT_LEFT,
                        TokType.SHIFT_RIGHT,
                        TokType.INCREMENT,
                        TokType.DECREMENT]:
               parsed = self.parse_assign_expression();
               self.ir.append(parsed)
            if self.current.type == TokType.ID:
                if self.peek().type == TokType.LPAREN:
                    parsed = self.parse_funccall()
                    self.ir.append(parsed)
            if self.current.type == TokType.KEYWORD_VAR:
                parsed = self.parse_vardef()
                self.ir.append(parsed)
            if self.current.type == TokType.KEYWORD_FN:
                parsed = self.parse_funcdef()
                self.ir.append(parsed)
                self.entered_bodies.append(parsed)
            if self.current.type == TokType.RBODY:
                parent = self.entered_bodies.pop()
                self.ir.append(self.get_ir_node("BodyExit", parent=parent))
            self.next()
        
        return
    
    def parse_struct(self):
        self.next() # skip struct keyword
        name = self.current.literal
        self.expect(TokType.ID)
        self.expect(TokType.LBODY)
        fields = []
        while self.current.type != TokType.RBODY:
            if self.current.type == TokType.NEWLINE:
                self.next()
            elif self.current.type != TokType.RBODY:
                var_name = self.current.literal
                self.expect(TokType.ID)
                self.expect(TokType.COLON)
                type = self.parse_type()
                self.expect(TokType.SEMICOLON)
                fields.append((var_name, type))
        self.next()
        return self.get_ir_node("StructDef", name=name, fields=fields)
        
    def parse_match_case(self):
        if self.current.type == TokType.KEYWORD_DEFAULT:
            return self.get_ir_node("MatchCase", expr=None)
        self.next() # skip case keyword
        expr = []
        while self.current.type != TokType.LBODY:
            expr.append(self.current.literal)
            self.next()
        return self.get_ir_node("MatchCase", expr=expr)
    
    def parse_match(self):
        self.next() # skip match keyword
        self.expect(TokType.LPAREN) # skip (
        expr = []
        brace = 1
        while brace > 0:
            expr.append(self.current.literal)
            self.next()
            if self.current.type == TokType.LPAREN:
                brace += 1
            if self.current.type == TokType.RPAREN:
                brace -= 1
        self.expect(TokType.RPAREN) # skip )
        self.expect(TokType.LBODY) # skip {
        return self.get_ir_node("Match", expr=expr)
    
    def parse_for(self):
        self.next() # skip for keyword
        self.expect(TokType.LPAREN) # skip (
        iterator = self.current.literal
        self.expect(TokType.ID) # skip iterator id
        self.expect(TokType.COLON) # skip :
        iterator_type = self.current.literal
        self.expect(TokType.ID) # skip type
        self.expect(TokType.ASSIGN) # skip =
        assign_expr = [i.literal for i in self.parse_until(TokType.SEMICOLON)]
        self.next() # skip first ;
        expr = [i.literal for i in self.parse_until(TokType.SEMICOLON)]
        self.next() # skip second ;
        iter_modification = []
        brace = 1
        while brace > 0:
            if self.current.type == TokType.LPAREN:
                brace += 1
            if self.current.type == TokType.RPAREN:
                brace -= 1
            if brace > 0:
                iter_modification.append(self.current.literal)
            self.next()
        return self.get_ir_node("For", iter=(iterator, iterator_type), assign_expr=assign_expr, expr=expr, iter_modification=iter_modification)
    
    # this piece of shit totally sucks
    def parse_inline_c(self):
        self.next() # skip [
        self.expect(TokType.NOT) # skip !
        match self.current.literal:
            case 'c': # TODO: refactor this block
                self.expect(TokType.ID) # skip c
                self.expect(TokType.RBRACE) # skip ]
                string = ""
                if self.current.type == TokType.STRING_LITERAL:
                    string = self.current.literal[1:-1]
                elif self.current.type == TokType.LBODY:
                    self.next()
                    brace = 1
                    while brace > 0:
                        if self.current.type == TokType.LBODY:
                            brace += 1
                        if self.current.type == TokType.RBODY:
                            brace -= 1
                        if brace > 0:
                            string += self.current.literal + " "
                        self.next()
                    returned = self.get_ir_node("InlineC", string=string)
            case 'include':
                self.expect(TokType.ID) # skip include
                self.expect(TokType.RBRACE) # skip ]
                string = ""
                libs = []
                if self.current.type == TokType.STRING_LITERAL:
                    string = self.current.literal
                elif self.current.type == TokType.LBODY:
                    self.next()
                    libs = []
                    while self.current.type != TokType.RBODY:
                        libs.append(self.current.literal)
                        self.next()
                    self.next()
                    if libs: # PLEASE REFACTOR THIS
                        libs = [i for i in libs if i not in ['\n']]
                        returned = self.get_ir_node("IncludeC", libs=libs)
                    else:
                        returned = self.get_ir_node("IncludeC", libs=string)
            
        return returned
    
    def parse_assign_expression(self):
        while self.current.type not in [TokType.SEMICOLON, TokType.NEWLINE]:
            self.pos -= 1
            self.current = self.tokens[self.pos]
        self.next()
        lvalue = []
        while self.current.type not in [
                        TokType.ASSIGN,
                        TokType.PLUS_ASSIGN,
                        TokType.MINUS_ASSIGN,
                        TokType.MULTIPLY_ASSIGN,
                        TokType.DIVIDE_ASSIGN,
                        TokType.MODULO_ASSIGN,
                        TokType.AND_ASSIGN,
                        TokType.OR_ASSIGN,
                        TokType.XOR_ASSIGN,
                        TokType.SHIFT_LEFT,
                        TokType.SHIFT_RIGHT,
                        TokType.INCREMENT,
                        TokType.DECREMENT]:
            lvalue.append(self.current.literal)
            self.next()
        op = self.current.literal
        self.next()
        if op not in ["++", "--"]:
            rvalue = [i.literal for i in self.parse_until(TokType.SEMICOLON)]
        else:
            rvalue = None
        
        return self.get_ir_node("ExprAssign", lvalue=lvalue, op=op, rvalue=rvalue)
    
    def parse_foreach(self):
        self.next() # skip 'foreach' keyword
        self.expect(TokType.LPAREN) # skip (
        args = []
        to_append = []
        for i in self.parse_until(TokType.RPAREN):
            if i.type == TokType.COMMA:
                args.append(to_append)
                to_append = []
            else:
                to_append.append(i.literal)
        if to_append:
            args.append(to_append)
        
        new_args = []
        for i in args:
            if ':' in i:
                new_args.append([i[0], i[2]])
            else:
                new_args.append(i)
        
        self.expect(TokType.RPAREN) # skip )
        return self.get_ir_node("Foreach", iterator=new_args[0][0], type=new_args[0][1], array=new_args[1][0])
        
    def parse_directive(self):
        directive = self.current.literal
        self.next() # skip directive
        content = []
        while self.current.type != TokType.NEWLINE:
            content.append(self.current.literal)
            self.next()
        return self.get_ir_node("Directive", id=directive, content=content)
    
    def parse_while(self):
        self.next() # skip 'while' keyword
        self.expect(TokType.LPAREN) # skip (
        expr = []
        brace = 1
        while brace > 0:
            expr.append(self.current.literal)
            self.next()
            if self.current.type == TokType.LPAREN:
                brace += 1
            if self.current.type == TokType.RPAREN:
                brace -= 1
        self.expect(TokType.RPAREN) # skip )
        self.expect(TokType.LBODY) # skip {
        return self.get_ir_node("While", expr=expr)
    
    def parse_elseif(self):
        self.next() # skip 'else' keyword
        self.next() # skip 'if' keyword
        self.expect(TokType.LPAREN) # skip (
        expr = []
        brace = 1
        while brace > 0:
            expr.append(self.current.literal)
            self.next()
            if self.current.type == TokType.LPAREN:
                brace += 1
            if self.current.type == TokType.RPAREN:
                brace -= 1
        self.expect(TokType.RPAREN) # skip )
        self.expect(TokType.LBODY) # skip {
        return self.get_ir_node("ElseIfStatement", expr=expr)
    
    def parse_else(self):
        self.next() # skip 'else' keyword
        self.expect(TokType.LBODY) # skip 'else' keyword
        return self.get_ir_node("Else")
        
    def parse_if(self):
        self.next() # skip 'if' keyword
        self.expect(TokType.LPAREN) # skip (
        expr = []
        brace = 1
        while brace > 0:
            expr.append(self.current.literal)
            self.next()
            if self.current.type == TokType.LPAREN:
                brace += 1
            if self.current.type == TokType.RPAREN:
                brace -= 1
        self.expect(TokType.RPAREN) # skip )
        self.expect(TokType.LBODY) # skip {
        return self.get_ir_node("IfStatement", expr=expr)
    
    def parse_return(self):
        self.next() # skip 'return' keyword
        expr = [i.literal for i in self.parse_until(TokType.SEMICOLON)]
        return self.get_ir_node("Return", expr=expr)
    
    def parse_funccall(self):
        name = self.current.literal
        self.expect(TokType.ID) # skip name
        self.expect(TokType.LPAREN) # skip (
        if self.current.type == TokType.RPAREN:
            return self.get_ir_node("FuncCall", name=name, args=[])
        args = []
        bol = self.pos
        # get arguments as list of expressions
        brace = 1
        while brace > 0: # self.current.type != TokType.RPAREN:
            if self.current.type == TokType.COMMA:
                args.append([i.literal for i in self.tokens[bol:self.pos]])
                bol = self.pos + 1
            self.next()
            if self.current.type == TokType.LPAREN:
                brace += 1
            if self.current.type == TokType.RPAREN:
                brace -= 1
        
        args.append([i.literal for i in self.tokens[bol:self.pos]])
        return self.get_ir_node("FuncCall", name=name, args=args)
    
    def parse_funcdef(self):
        self.next() # skip 'fn' keyword
        name = self.current.literal
        self.expect(TokType.ID)     # skip id
        self.expect(TokType.LPAREN)
        args = []
        to_append = []
        for i in self.parse_until(TokType.RPAREN):
            if i.type == TokType.COMMA:
                args.append(to_append)
                to_append = []
            else:
                to_append.append(i.literal)
        if to_append:
            args.append(to_append)
        new_args = []
        for i in args:
            arg_name = i[0]
            arg_type = i[2]
            if arg_type == '*':
                arg_type = i[3] + arg_type
            new_args.append(self.get_ir_node("Arg", name=arg_name, type=arg_type))
        
        self.expect(TokType.RPAREN) # skip )
        self.expect(TokType.COLON)  # skip colon
        type = self.parse_type()
        self.expect(TokType.LBODY) # skip {
        return self.get_ir_node("FuncDef", name=name, args=new_args, type=type)
    
    def parse_vardef(self):
        self.next() # skip 'var' keyword
        name = self.current.literal
        self.expect(TokType.ID)    # skip id
        self.expect(TokType.COLON) # skip colon
        type = self.parse_type()
        if '[]' in type:
            name += '[]'
            type = type[0:-2]
        if self.current.type == TokType.SEMICOLON:
            expr = None
        else:
            self.expect(TokType.ASSIGN) # skip assign
            expr = [i.literal for i in self.parse_until(TokType.SEMICOLON)]
            self.expect(TokType.SEMICOLON)
        return self.get_ir_node("VarDef", name=name, expr=expr, type=type)
    
    def get_ir_node(self, node_type, **kwargs):
        return (node_type, kwargs)
    
    def parse_until(self, end_type):
        res = []
        while self.current.type != end_type:
            if self.current.literal in C_KEYWORDS:
                error(f"unexpected eof at {self.pos}, {self.current.pos+1}")
            res.append(self.current)
            self.next()
        return res
    
    def parse_type(self):
        type = self.current.literal
        if self.peek().type == TokType.LBRACE:
            self.next()
            self.next()
            self.expect(TokType.RBRACE)
            type += '[]'
        elif self.current.type == TokType.MULTIPLY:
            self.next()
            type = self.current.literal + type
            self.next()
        else:
            self.expect(TokType.ID) # skip type
        
        return type
    
    def peek(self, n=1):
        if self.pos + n < len(self.tokens):
            return self.tokens[self.pos + n]
        return None
    
    def next(self):
        if self.pos+1 < len(self.tokens):
            self.pos += 1
            self.current = self.tokens[self.pos]
        else:
            error(f"unexpected eof at {self.pos}, {self.current.pos+1}")
    
    def expect(self, type):
        if self.current.type == TokType.NEWLINE and not \
           (type == TokType.SEMICOLON):
            self.next()
        if self.pos < len(self.tokens) and self.current.type == type:
            self.pos += 1
            self.current = self.tokens[self.pos]
        else:
            error(f"expected {type}, got {repr(self.current.literal)}, line {self.current.pos}")
