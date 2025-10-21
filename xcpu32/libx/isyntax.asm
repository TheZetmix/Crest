jmp LIBXISYNTAX_END

define repeat .loop_%AUTO%:
define while(lvalue, j, rvalue) cmp rvalue, rvalue \ j .loop_%AUTO% #NEWMACROID

LIBXISYNTAX_END:
