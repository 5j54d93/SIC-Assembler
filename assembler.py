import sys
import pass1
import pass2

if len(sys.argv) != 2:
    print("Usage: python3 assembler.py <source file>")
    sys.exit()

# read .asm file
try:
    with open(sys.argv[1], "r") as fp:
        lines = fp.readlines()
except:
    lines = None

# PASS 1
SYMTAB, STARTING, programLength = pass1.creatSYMTAB(lines)

# creat a blank .obj file
objFile = open(sys.argv[1].replace("asm", "obj"), "w")

# PASS 2
pass2.generateObjectFile(objFile, SYMTAB, lines, STARTING, programLength)
