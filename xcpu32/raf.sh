#!/bin/bash
find . -type f \( -name "*.c" -o -name "*.h" -o -name "*.asm" -o -name "*.py" \) -exec sh -c 'echo "==> {} <=="; cat {}' \;
