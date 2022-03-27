import sys
import sic


def writeHeader(objFile, programName, STARTING, programLength):
    while len(programName) < 6:
        programName += " "
    header = "H" + programName
    header += hexStrToWord(STARTING)
    header += hexStrToWord(programLength)
    header += "\n"
    objFile.write(header)


def writeText(objFile, textRecordStart, textRecord):
    textrecord = "T" + hexStrToWord(textRecordStart)

    textRecordLength = hex(int(len(textRecord)/2))[2:]
    while len(textRecordLength) < 2:
        textRecordLength = "0" + textRecordLength
    textrecord += textRecordLength.upper()

    textrecord += textRecord

    textrecord += "\n"
    objFile.write(textrecord)


def writeEnd(objFile, address):
    end = "E" + hexStrToWord(address)
    objFile.write(end)
    objFile.close()


def decomposeLine(tokens):
    match(len(tokens)):
        case(1):
            return [None, tokens[0], None]
        case(2):
            if tokens[0] in sic.OPTAB or tokens[0] in sic.DIRECTIVE:
                return [None, tokens[0], tokens[1]]
            elif tokens[1] in sic.OPTAB or tokens[1] in sic.DIRECTIVE:
                return [tokens[0], tokens[1], None]
        case(3):
            return [tokens[0], tokens[1], tokens[2]]


def hexStrToWord(hexStr):
    hexStr = hex(hexStr).upper()[2:]
    while len(hexStr) < 6:
        hexStr = "0" + hexStr
    return hexStr


def generateObjectFile(objFile, SYMTAB, lines, STARTING, programLength):
    for line in lines:
        tokens = line.split()
        if tokens[1] == "START":
            LOCCTR = int(tokens[2], 16)
            programName = tokens[0]
            break

    writeHeader(objFile, programName, LOCCTR, programLength)

    textRecord = ""
    textRecordStart = LOCCTR
    for index, line in enumerate(lines):
        # check tokens in line
        if len(line) > 0 and line[0] == '.' or len(line) > 0 and line[0] == '\n':
            continue

        # generate 3 tokens from line
        tokens = line.split()
        tokens = decomposeLine(tokens)

        if tokens[1] == "START":
            continue

        if tokens[1] in sic.OPTAB:
            opcode = tokens[1]
            operand = tokens[2]
            # generate instruction
            instruction = sic.OPTAB[opcode] * 65536
            if operand != None:
                if operand[len(operand)-2:] == ',X':
                    instruction += 32768
                    operand = operand[:len(operand)-2]
                if operand in SYMTAB:
                    instruction += SYMTAB[operand]
                else:
                    print("Line " + "#" + index +
                          ": Undefined Symbole: " + operand)
                    sys.exit()
            instruction = hexStrToWord(instruction)

            if LOCCTR + 3 - textRecordStart > 30:
                writeText(objFile, textRecordStart, textRecord)
                textRecordStart = LOCCTR
                textRecord = instruction
            else:
                textRecord += instruction
            LOCCTR += 3
        else:
            match(tokens[1]):
                case("WORD"):
                    tokens[2] = hexStrToWord(int(tokens[2]))

                    if LOCCTR + 3 - textRecordStart > 30:
                        writeText(objFile, textRecordStart, textRecord)
                        textRecordStart = LOCCTR
                        textRecord = tokens[2]
                    else:
                        textRecord += tokens[2]
                    LOCCTR += 3
                case("BYTE"):
                    if tokens[2][0] == 'X':
                        operandLength = int((len(tokens[2]) - 3)/2)
                        tokens[2] = tokens[2][2:len(tokens[2])-1]
                    elif tokens[2][0] == 'C':
                        operandLength = int(len(tokens[2]) - 3)
                        constant = ""
                        for i in range(2, len(tokens[2])-1):
                            tmp = hex(ord(tokens[2][i]))[2:]
                            if len(tmp) == 1:
                                tmp = "0" + tmp
                            tmp = tmp.upper()
                            constant += tmp
                        tokens[2] = constant

                    if LOCCTR + operandLength - textRecordStart > 30:
                        writeText(objFile, textRecordStart, textRecord)
                        textRecordStart = LOCCTR
                        textRecord = tokens[2]
                    else:
                        textRecord += tokens[2]
                    LOCCTR += operandLength
                case("RESB"):
                    LOCCTR += int(tokens[2])
                case("RESW"):
                    LOCCTR += int(tokens[2]) * 3
                case("END"):
                    if len(textRecord) > 0:
                        writeText(objFile, textRecordStart, textRecord)

                    address = STARTING
                    if tokens[2] != None:
                        address = SYMTAB[tokens[2]]

                    writeEnd(objFile, address)
                case _:
                    print("Line " + "#" + str(index) +
                          ": Invalid Instruction / Invalid Directive")
