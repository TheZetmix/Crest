from token import *
from instr import *
import re

INSTRUCTIONS_ARGS = {
    "mov"     : 2,
    "add"     : 2,
    "sub"     : 2,
    "mul"     : 2,
    "div"     : 2,
    "mod"     : 2,
    "inc"     : 1,
    "dec"     : 1,
    "and"     : 2,
    "or"      : 2,
    "xor"     : 2,
    "not"     : 1,
    "shl"     : 2,
    "shr"     : 2,
    "push"    : 1,
    "pop"     : 1,
    "lea"     : 2,
    "jmp"     : 1,
    "call"    : 1,
    "ret"     : 0,
    "je"      : 1,
    "jne"     : 1,
    "jg"      : 1,
    "jl"      : 1,
    "jge"     : 1,
    "jle"     : 1,
    "cmp"     : 2,
    "nop"     : 0,
    "hlt"     : 0,
    "int"     : 1,
    "trap"    : 0,
    "str"     : 2,
    "ldr"     : 2,
    "pusha"   : 0,
    "popa"    : 0,
    "lean"    : 2,
    "ffp"     : 1,
    "movb"    : 2,
    "movw"    : 2,
    "movd"    : 2,
    "movst"   : 2,
    "smp"     : 2,
}

def ERROR(line, msg):
    print(f"error at {line}: {msg}")
    exit(1)

def WARNING(line, msg):
    print(f"warning at {line}: {msg}")

def expect_token(line, tok, expected):
    if tok != expected: ERROR(line, f"expected {expected}, got {tok}")

def validate_instruction(op, args, pos):
    # Проверка на существование инструкции
    if op not in INSTRUCTIONS_ARGS:
        similar = [i for i in INSTRUCTIONS_OPS if i.startswith(op[:2])[:3]]
        hint = f" Did you mean: {', '.join(similar)}?" if similar else ""
        ERROR(pos, f"Unknown instruction '{op}'.{hint}")

    # Проверка количества аргументов
    expected_args = INSTRUCTIONS_ARGS[op]
    if len(args) != expected_args:
        ERROR(pos, f"'{op}' requires {expected_args} arguments, got {len(args)}")

    # Проверка регистров с подсказками
    for arg in args:
        if arg.type == TokType.REGISTER and arg.literal not in REGISTERS:
            # Ищем похожие регистры
            similar = [r for r in REGISTERS if r.startswith(arg.literal[0])][:3]
            hint = f" Did you mean: {', '.join(similar)}?" if similar else ""
            ERROR(pos, f"Unknown register '{arg.literal}'.{hint}")

    # Проверка чисел
    for arg in args:
        if arg.type == TokType.NUMBER:
            try:
                num = int(arg.literal)
                if not (-2147483648 <= num <= 4294967295):
                    WARNING(pos, f"Number {num} is out of 32-bit range")
            except ValueError:
                ERROR(pos, f"Invalid number format: '{arg.literal}'")

        elif arg.type == TokType.HEX_NUMBER:
            if not re.fullmatch(r'0x[0-9a-fA-F]+', arg.literal):
                ERROR(pos, f"Invalid hex number format: '{arg.literal}'")

    if op in ["add", "sub", "mul"] and args[0].type == args[1].type == TokType.NUMBER:
        WARNING(pos, "Both operands are numbers - result will be computed at compile time")
