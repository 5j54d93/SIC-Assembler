# SIC Assembler

[![CodeQL](https://github.com/5j54d93/SIC-Assembler/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/5j54d93/SIC-Assembler/actions/workflows/codeql-analysis.yml)
![GitHub](https://img.shields.io/github/license/5j54d93/SIC-Assembler)
![GitHub Repo stars](https://img.shields.io/github/stars/5j54d93/SIC-Assembler)
![packages](https://img.shields.io/badge/Python-%3E%3D%20v3.10-blue)
![GitHub repo size](https://img.shields.io/github/repo-size/5j54d93/SIC-Assembler)

An assembler for SIC（Simplified Instructional Computer）in Python.

- `assembler.py`：main program
- `pass1.py`：Create SYMTAB（Symbol Table）
- `pass2.py`：Write object file
- `sic.py`：store SIC instruction set and directive

## How To Use

1. Download this repository via `git clone`

```shell
git clone https://github.com/5j54d93/SIC-Assembler
```

2. Change directories to this repository via `cd` or drag this folder and drop in terminal

```shell
cd SIC-Assembler
```

3. Run `assembler.py`

```shell
python3 assembler.py <source file>
```

## Example

run `python3 assembler.py addexample.asm` in terminal to convert `.asm` to `.obj`

### `addexample.asm`

```asm
ADDEX	START	1000
FIRST	LDA	THREE
        ADD	FIVE
        STA	RESULT
        RSUB
THREE	WORD	3
FIVE	WORD	5
RESULT	RESW	1
        END	FIRST
```

### `addexample.obj`

```obj
HADDEX 001000000015
T0010001200100C18100F0C10124C0000000003000005
E001000
```

## License：MIT

This package is [MIT licensed](https://github.com/5j54d93/SIC-Assembler/blob/main/LICENSE).
