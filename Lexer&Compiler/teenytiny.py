from lex import *
from parse import *
import sys

def main():
    print("Teeny Tiny Compiler")

    with open('hello.tiny', 'r') as inputFile:
        file = inputFile.read()

    lexer = Lexer(file)
    parser = Parser(lexer)

    parser.program()
    print("Parsing is completed")

main()
