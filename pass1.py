import sys
import sic


def decomposeLine(tokens, index):
    match(len(tokens)):
        case(1):
            if tokens[0] in sic.OPTAB or tokens[0] in sic.DIRECTIVE:
                return [None, tokens[0], None]
            else:
                print("Line " + "#" + index +
                      ": a wrong opcode or directive.")
                sys.exit()
        case(2):
            if tokens[0] in sic.OPTAB or tokens[0] in sic.DIRECTIVE:
                return [None, tokens[0], tokens[1]]
            elif tokens[1] in sic.OPTAB or tokens[1] in sic.DIRECTIVE:
                return [tokens[0], tokens[1], None]
            else:
                print("Line " + "#" + index +
                      ": a wrong opcode or directive.")
                sys.exit()
        case(3):
            if tokens[1] in sic.OPTAB or tokens[1] in sic.DIRECTIVE:
                return [tokens[0], tokens[1], tokens[2]]
            else:
                print("Line " + "#" + index +
                      ": a wrong opcode or directive.")
                sys.exit()


def creatSYMTAB(lines):
    SYMTAB = {}

    for index, line in enumerate(lines):
        # check tokens in line
        if len(line) > 0 and line[0] == '.' or len(line) > 0 and line[0] == '\n':
            continue

        # generate 3 tokens from line
        tokens = line.split()
        tokens = decomposeLine(tokens, index)

        # creat symbol table
        if tokens[1] == "START":
            STARTING = int(tokens[2], 16)
            LOCCTR = STARTING
        elif tokens[0] != None:
            if tokens[0] in SYMTAB:
                print("Line " + "#" + index +
                      ": duplicate " + tokens[0] + ".")
                sys.exit()
            SYMTAB[tokens[0]] = LOCCTR

        if tokens[1] in sic.OPTAB or tokens[1] == "WORD":
            LOCCTR = LOCCTR + 3
        else:
            match(tokens[1]):
                case("RESW"):
                    LOCCTR = LOCCTR + int(tokens[2]) * 3
                case("RESB"):
                    LOCCTR = LOCCTR + int(tokens[2])
                case("BYTE"):
                    if tokens[2][0] == 'C':
                        LOCCTR = LOCCTR + (len(tokens[2]) - 3)
                    if tokens[2][0] == 'X':
                        LOCCTR = LOCCTR + int(((len(tokens[2]) - 3)/2))

        if tokens[1] == "END":
            programLength = LOCCTR - STARTING

    return SYMTAB, STARTING, programLength
