from parser import *
from lexer  import *
from token  import *
import argparse
import os

def tohex(value):
    return f"0x{int(value):02x}"

class CodeGen:
    def __init__(self, parser):
        self.parser = parser
        self.ir = parser.ir
        
        self.output = []
        
        for i in self.ir:
            self.gen_from_node(i)
        
    def gen_from_node(self, node):
        match node[0]:
            case "Continue":
                self.output.append("continue;")
            case "Break":
                self.output.append("break;")
            case "StructDef":
                self.output.append("typedef struct")
                self.output.append("{")
                for i in node[1]["fields"]:
                    self.output.append(i[1])
                    self.output.append(i[0])
                    self.output.append(";")
                self.output.append(f"}} {node[1]["name"]}")
                self.output.append(';')
            case "MatchCase":
                if node[1]["expr"] != None: # TODO: refactor this line
                    expr = [i for i in node[1]["expr"] if i != "||"] # <-
                    for i in expr:
                        self.output.append("case")
                        self.output.append(i)
                        self.output.append(":")
                    self.output.append("{")
                else:
                    self.output.append("default")
                    self.output.append(":")
                    self.output.append("{")
            case "Match":
                self.output.append("switch")
                self.output.append("(")
                for i in node[1]["expr"]:
                    self.output.append(i)
                self.output.append(")")
                self.output.append("{")
            case "InlineC":
                self.output.append(node[1]["string"])
            case "IncludeC":
                for i in node[1]["libs"]:
                    self.output.append(f"# include {i}\n")
            case "ExprAssign":
                match node[1]["op"]:
                    case "++" | "--":
                        for i in node[1]["lvalue"]:
                            self.output.append(i)
                        self.output.append(node[1]["op"])
                    case _:
                        for i in node[1]["lvalue"]:
                            self.output.append(i)
                        self.output.append(node[1]["op"])
                        for i in node[1]["rvalue"]:
                            self.output.append(i)
                self.output.append(";")
            case "For":
                self.output.append("for")
                self.output.append("(")
                self.output.append(node[1]["iter"][1])
                self.output.append(node[1]["iter"][0])
                self.output.append("=")
                for i in node[1]["assign_expr"]:
                    self.output.append(i)
                self.output.append(";")
                for i in node[1]["expr"]:
                    self.output.append(i)
                self.output.append(";")
                for i in node[1]["iter_modification"]:
                    self.output.append(i)
                self.output.append(")")
                self.output.append("{")
            case "Foreach":
                iterator = "_iterator_obj_" + node[1]["iterator"] + "_" + node[1]["array"]
                self.output.append("for")
                self.output.append("(")
                self.output.append(f"size_t {iterator} = 0 ; {iterator} <")
                self.output.append("sizeof(")
                self.output.append(node[1]["array"])
                self.output.append(")")
                self.output.append("/ sizeof(")
                self.output.append(node[1]["array"])
                self.output.append("[0])")
                self.output.append(f'; {iterator}++')
                self.output.append(")")
                self.output.append("{")
                self.output.append(node[1]["type"])
                self.output.append(node[1]["iterator"])
                self.output.append("=")
                self.output.append(node[1]["array"])
                self.output.append(f"[{iterator}]")
                self.output.append(";")
            case "Directive":
                self.output.append("#")
                self.output.append(node[1]["id"])
                for i in node[1]["content"]:
                    self.output.append(i)
                self.output.append("\n")
            case "While":
                self.output.append("while")
                self.output.append("(")
                for i in node[1]["expr"]:
                    self.output.append(i)
                self.output.append(")")
                self.output.append("{")
            case "IfStatement":
                self.output.append("if")
                self.output.append("(")
                for i in node[1]["expr"]:
                    self.output.append(i)
                self.output.append(")")
                self.output.append("{")
            case "Else":
                self.output.append("else")
                self.output.append("{")
            case "ElseIfStatement":
                self.output.append("else")
                self.output.append("if")
                self.output.append("(")
                for i in node[1]["expr"]:
                    self.output.append(i)
                self.output.append(")")
                self.output.append("{")
            case "VarDef":
                self.output.append(node[1]["type"])
                self.output.append(node[1]["name"])
                if node[1]["expr"]:
                    self.output.append('=')
                    for i in node[1]["expr"]:
                        self.output.append(i)
                self.output.append(';');
            case "IdAssign":
                self.output.append(node[1]["name"])
                self.output.append("=")
                for i in node[1]["expr"]:
                    self.output.append(i)
                self.output.append(";")
            case "FuncDef":
                self.output.append(node[1]["type"])
                self.output.append(node[1]["name"])
                self.output.append('(')
                for i in node[1]["args"]:
                    self.output.append(i[1]["type"])
                    self.output.append(i[1]["name"])
                    if i != node[1]["args"][-1]:
                        self.output.append(',')
                self.output.append(')')
                self.output.append('{')
            case "Return":
                self.output.append('return')
                for i in node[1]["expr"]:
                    self.output.append(i)
                self.output.append(';')
            case "BodyExit":
                match node[1]["parent"][0]:
                    case "MatchCase":
                        self.output.append('break ; }')
                    case _:
                        self.output.append('}')
            case "FuncCall":
                self.output.append(node[1]["name"])
                self.output.append('(')
                for i, arg in enumerate(node[1]["args"]):
                    if len(arg) > 1:
                        for j in arg:
                            self.output.append(j)
                    else:
                        self.output.append(arg[0])
                    if i != len(node[1]["args"])-1:
                        self.output.append(',')
                self.output.append(')')
                self.output.append(';')
            
            
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--file",   "-f", required=True)
    arg_parser.add_argument("--output", "-o")
    arg_parser.add_argument("--link",   "-l", action="append")
    arg_parser.add_argument("--debug",  "-d", action="store_true")
    arg_parser.add_argument("--compiler")
    args = arg_parser.parse_args()
    
    file = open(args.file, "r").read()
    
    lexer = Lexer(file, args.file)
    lexer.make_all_tokens()
    parser = Parser(lexer)
    gen = CodeGen(parser)
    if args.debug:
        print(args)
        print("ir:")
        for i in gen.ir:
            node_name = i[0]
            print(node_name, " " * (12 - len(node_name)), i[1])
        print("generated:")
        output = [i if i not in ';{}' else f"{i}\n" for i in gen.output ]
        for i in output:
            print(i, end=' ' if '\n' not in i else '')
            
    with open(f"{args.file}.c", "w") as f:
        f.write(' '.join(gen.output))
        
    if args.compiler: # TODO: refactor this block
        compile_cmd = args.compiler + f" {args.file}.c" + f" -o {args.output}" if args.output else ""
    else:
        compile_cmd = "clang" + f" {args.file}.c" + f" -o {args.output}" if args.output else ""
    if args.link:
        for i in args.link:
            compile_cmd += f" -l{i}"
    if args.debug: print(compile_cmd)
    os.system(compile_cmd)
    os.system(f"rm {args.file}.c")
    
