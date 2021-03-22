import enum
import sys

class Lexer:
    def __init__(self, input):
        self.source = input + '\n' # Source code to lex as a string
        self.curChar = '' # Current character in the string
        self.curPos = -1 # Current position in the string
        self.nextChar()
        self.numberline = 1
    
    # Process the next character
    def nextChar(self):
        self.curPos += 1
        if (self.curPos >= len(self.source)):
            self.curChar = '\0' #EOF
        else:
            self.curChar = self.source[self.curPos]

    # Return the lookahead character
    def peek(self):
        if(self.curPos + 1 >= len(self.source)):
            return '\0'
        return self.source[self.curPos + 1]

    # Invalid token found, print error message and exit
    def abort(self, message):
        sys.exit("Lexing error. " + message)

    # Skip whitespace except newlines, which we will use to indicate the end of a statement
    def skipWhiteSpace(self):
        while (self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r'):
            self.nextChar()

    # Skip comments in the code
    def skipComment(self):
        if(self.curChar == '#'):
            while(self.curChar != '\n'):
                self.nextChar()

    # Return the next token
    def getToken(self):
        self.skipWhiteSpace()
        self.skipComment()
        token = None
        # Check the furst character of this token to see if we can decide what it is
        # IF it is a multiple character, we will proccess the rest
        if (self.curChar == '+'):
            token = Token(self.curChar, TokenType.PLUS)

        elif (self.curChar == '-'):
            token = Token(self.curChar, TokenType.MINUS)

        elif (self.curChar == '*'):
            token = Token(self.curChar, TokenType.ASTERISK)

        elif (self.curChar == '/'):
            token = Token(self.curChar, TokenType.SLASH)

        elif(self.curChar == '='):
            # Check whether this token is = or ==
            if(self.peek() == '='):
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        
        elif(self.curChar == '>'):
            # Check whether this is > or >=
            if(self.peek() == '='):
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        
        elif(self.curChar == '<'):
            # Check wheter this is a token is < or <=
            if(self.peek() == '<'):
                lastChar = self.curChar
                self.nextChar()
                token = Token(self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        
        elif(self.curChar == '!'):
            if(self.peek() == '='):
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek() + " at line: " + str(self.numberline))

        elif(self.curChar == '\"'):
            # Get characters between quotations
            self.nextChar()
            startPos = self.curPos

            while(self.curChar != '\"'):
                # Don't allow special characters in the string 
                # We will be using C's printf on this string
                if(self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%'):
                    self.abort("Illegal character in string" + " at line: " + str(self.numberline))
                self.nextChar()
            
            tokText = self.source[startPos : self.curPos] # Get the substring
            token = Token(tokText, TokenType.STRING)
        
        elif (self.curChar.isdigit()):
            # Leading characters is a digit, so it must be a number
            # Get all consecutive digits and decimal if there is one
            startPos = self.curPos
            while(self.peek().isdigit()):
                self.nextChar()
            if(self.peek() == '.'): # DECIMAL
                self.nextChar()

                # MUST have at least one digit after decimal
                if(not self.peek().isdigit()):
                    # ERROR!
                    self.abort("Illegal character in number." + " at line: " + str(self.numberline))
                while(self.peek().isdigit()):
                    self.nextChar()
            
            tokText = self.source[startPos : self.curPos + 1] # Get the substring
            token = Token(tokText, TokenType.NUMBER)

        elif(self.curChar.isalpha()):
            # Leading character is a letter, so this must be and idetifier or a keyword
            # Get all consecutive apha numeric characters
            startPos = self.curPos
            while(self.peek().isalnum()):
                self.nextChar()
            # Check if the token is in the list of keywords
            tokText = self.source[startPos : self.curPos + 1] # Get the substring
            keyword = Token.checkIfKeyword(tokText)
            if(keyword == None):    # IDENTIFIER
                token = Token(tokText, TokenType.IDENT)
            else:   # KEYWORD
                token = Token(tokText, keyword)

        elif (self.curChar == '\n'):
            token = Token(self.curChar, TokenType.NEWLINE)
            self.numberline += 1

        elif (self.curChar == '\0'):
            token = Token('', TokenType.EOF)

        else:
            # Unknown token!
            self.abort("Unkonw Token: " + self.curChar + " at line: " + str(self.numberline))
			
        self.nextChar()
        return token

class Token:
    def __init__(self ,tokenText, tokenKind):
        self.text = tokenText # Token's actual text
        self.kind = tokenKind # Token type to be classified as

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Relies on all keywords enum being 1XX
            if(kind.name == tokenText and kind.value >= 100 and kind.value < 200):
                return kind
        return None

#TokenType is our enum for all the types of tokens.
class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3

    # KEYWORDS

    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111

    # OPERATORS

    EQ = 201  
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211