from parser import *
from lexer  import *
from token  import *

if __name__ == "__main__":
    file = open(sys.argv[1], "r").read()
    da_lexa = Lexer(file, sys.argv[1])
    da_lexa.make_all_tokens()
    fucking_parser = Parser(da_lexa)
    
