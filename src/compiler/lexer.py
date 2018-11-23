from enum import Enum
from io import StringIO


class TokenKind(Enum):
    KEYWORD = 0
    IDENTIFIER = 1
    CONSTANT = 2
    OPERATOR = 3
    EOF = 4
    ERROR = 5


class Token:
    def __init__(self, tokenKind: TokenKind, metadata=None):
        self.tokenKind = tokenKind
        self.metadata = metadata
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{} : {}".format(self.tokenKind, self.metadata)

    def __eq__(self, other):
        if other == None:
            return False
        return (self.tokenKind == other.tokenKind) and (self.metadata == other.metadata)
        #return self.__dict__ == other.__dict__



class Lexer:
    class _State:

        def run(self, curChar: str):
            raise NotImplementedError

        def next(self, nextChar: str) -> ('_State', Token):
            raise NotImplementedError

        @staticmethod
        def isValid(inChar: str):
            raise NotImplementedError

        @staticmethod
        def isStarter(inChar: str):
            raise NotImplementedError

    def __init__(self, inFile=None, inString=None):
        self.tokens = []
        self.currentState = Lexer._StateWhitespace()

        if inFile == None and inString != None:
            for c in inString:
                self.runState(c)
        elif inString == None and inFile != None:
            c = inFile.read(1)
            while c:
                if c == '#':
                    print(c)
                self.runState(c)
                c = inFile.read(1)
        else:
            raise ValueError("Requires either a file or string")
        self.tokens.append(Token(TokenKind.EOF))

    def runState(self, c: str):
        self.currentState, curToken = self.currentState.next(c)
        self.currentState.run(c)
        while curToken != None:
            self.tokens.append(curToken)
            self.currentState, curToken = self.currentState.next(c)
            self.currentState.run(c)

    class _StateWhitespace(_State):

        @staticmethod
        def isValid(inChar: str):
            return inChar.isspace()

        @staticmethod
        def isStarter(inChar: str):
            return inChar.isspace()

        def run(self, curChar: str):
            pass

        def next(self, nextChar: str) -> ('_State', Token):
            if Lexer._StateWhitespace.isValid(nextChar):
                return self, None
            elif Lexer._StateConstant.isStarter(nextChar):
                return Lexer._StateConstant(), None
            elif Lexer._StateIdentifier.isStarter(nextChar):
                return Lexer._StateIdentifier(), None
            elif Lexer._StateOperator.isStarter(nextChar):
                return Lexer._StateOperator(), None
            else:
                return Lexer._StateError(), None

    class _StateIdentifier(_State):

        KEYWORD_STRINGS = ["func", "extern", "int", "byte", "return"]

        def __init__(self):
            self.identifierString = ""

        @staticmethod
        def isStarter(inChar: str):
            return (inChar.isalpha() or (inChar == '_'))

        @staticmethod
        def isValid(inChar: str):
            return (inChar.isalnum() or (inChar == '_'))

        def run(self, curChar: str):
            if len(self.identifierString) == 0:
                self.identifierString = curChar

        def next(self, nextChar: str) -> ('_State', Token):  # TODO doesn't check for whitespaces
            if self.isValid(nextChar):
                self.identifierString += nextChar
                return self, None
            else:
                for word in Lexer._StateIdentifier.KEYWORD_STRINGS:
                    if self.identifierString == word:
                        return (Lexer._StateWhitespace(), Token(TokenKind.KEYWORD, self.identifierString))
                return Lexer._StateWhitespace(), Token(TokenKind.IDENTIFIER, self.identifierString)
            # else:
            #     return Lexer._StateWhitespace(), Token(TokenKind.ERROR, "Invalid charcater")

    class _StateConstant(_State):
        def __init__(self):
            self.constantString = ""

        @staticmethod
        def isStarter(inChar: str):
            return ord('1') <= ord(inChar) <= ord('9')

        @staticmethod
        def isValid(inChar: str):
            return inChar.isdigit()

        def run(self, curChar: str):
            if len(self.constantString) == 0:
                self.constantString = curChar

        def next(self, nextChar: str) -> ('_State', Token):
            if Lexer._StateConstant.isValid(nextChar):
                self.constantString += nextChar
                return self, None
            else:
                return Lexer._StateWhitespace(), Token(TokenKind.CONSTANT, int(self.constantString))

    class _StateOperator(_State):

        def __init__(self):
            self.operatorString = ""

        operatorStrings = ["+", "-", "*", "/", "%", "(", ")", "{", "}", "="]
        operatorStarters = [op[0] for op in operatorStrings]

        @staticmethod
        def isStarter(inChar: str):
            return (inChar in Lexer._StateOperator.operatorStarters)

        @staticmethod
        def isValid(inChar: str):
            return any(inChar in x for x in Lexer._StateOperator.operatorStrings)

        def run(self, curChar: str):
            if len(self.operatorString) == 0:
                self.operatorString = curChar

        def next(self, nextChar: str) -> ('_State', Token):
            if Lexer._StateOperator.isValid(nextChar):
                self.operatorString += nextChar
                return self, None
            else:
                return Lexer._StateWhitespace(), Token(TokenKind.OPERATOR, self.operatorString)

    class _StateComment(_State):
        
        @staticmethod
        def isStarter(inChar: str):
            return inChar == '#'
        
        @staticmethod
        def isValid(inChar: str):
            return (inChar == '#' or inChar == '*')
        
        def run(self, curChar: str):
            pass
        
        def next(self, nextChar: str) -> ('_State', Token):
            if Lexer._StateLineComment.isStarter(nextChar):
                return Lexer._StateLineComment(), None
            elif Lexer._StateLongComment.isStarter(nextChar):
                return Lexer._StateLongComment(), None
            else:
                return Lexer._StateWhitespace(), Token(TokenKind.ERROR, "Expected comment")

    class _StateLineComment(_State):
        @staticmethod
        def isStarter(inChar: str):
            return inChar == '#'
        
        @staticmethod
        def isValid(inChar: str):
            return (inChar != '\n')
        
        def run(self, curChar: str):
            pass
        
        def next(self, nextChar: str) -> ('_State', Token):
            if Lexer._StateLineComment.isValid(nextChar):
                return self, None
            return Lexer._StateWhitespace, None
    
    class _StateLongComment(_State):
        @staticmethod
        def isStarter(inChar: str):
            return inChar == '*'
        
        @staticmethod
        def isValid(inChar: str):
            pass
        
        def run(self, curChar: str):
            pass
        
        def next(self, nextChar: str) -> ('_State', Token):
            if nextChar == '*':
                self.waitingForEnd = True
            if self.waitingForEnd:
                if nextChar == '#':
                    return Lexer._StateWhitespace, None
            return self, None

    class _StateError(_State):
        @staticmethod
        def isStarter(inChar: str):
            pass
        
        @staticmethod
        def isValid(inChar: str):
            pass
        
        def run(self, curChar: str):
            self.errorChar = curChar
        
        def next(self, nextChar: str):
            return Lexer._StateWhitespace(), Token(TokenKind.ERROR, self.errorChar)