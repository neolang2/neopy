#!/usr/bin/env python3
from enum import Enum
from io import StringIO

# enum for token kinds
class TokenKind(Enum):
    TOK_EOF = -1,
    TOK_FUNC = -2,
    TOK_EXTERN = -3,
    TOK_IDENTIFIER = -4,
    TOK_NUMBER = -5,

# token class containing a kind and some metadatas
class Token:
    def __init__(self, kind, metadata):
        self.kind = kind
        self.metadata = metadata

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

# the actuall lexer class
class Lexer:
    def __init__(self):
        self.lastchar = ' '
        self.idenstr = ""
        self.tokens = []
        self.file = None

    # get the next character from the stream
    def __getChar(self):
        return self.file.read(1)

    # parse the file into tokens
    def lex(self, filename=None, in_string=None):
       # if string is given, create a stream from that, otherwise open a file from the given name
        if(in_string != None):
             self.file = StringIO(in_string)
        elif(filename != None):
            self.file = open(filename)
        else:
            raise ValueError
        cur_token = None
        # loop over stream until EOF
        while True:
            cur_token = self._getToken()
            self.tokens.append(cur_token)
            if cur_token.kind == TokenKind.TOK_EOF:
                break
        self.file.close()

    def _is_whitespace(self, in_char: str):
        return (len(in_char) == 1) and in_char.isspace()

    def _is_number_beginning(self, in_char: str):
        return (len(in_char) == 1) and (in_char.isdigit())

    def _is_valid_number_char(self, in_char: str):
        return (len(in_char) == 1) and (in_char.isdigit())

    def _is_identifier_beginning(self, in_char: str):
        return (len(in_char) == 1) and (in_char.isalpha())

    def _is_valid_identifier_char(self, in_char: str):
        return (len(in_char) == 1) and (in_char.isalnum())    

    # get the next token in the stream
    def _getToken(self):
        # ignore white space
        while(self._is_whitespace(self.lastchar)):
            self.lastchar = self.__getChar()
        # check to see if lexer should look for a keyword or identifier
        if(self._is_identifier_beginning(self.lastchar)):
            idenstr = self.lastchar
            self.lastchar = self.__getChar()
            # 
            while(self.lastchar.isalnum()):
                idenstr += self.lastchar
                self.lastchar = self.__getChar()
            ret_tok_kind = None
            # match idenstr with a keyword, if not make it an identifier
            if(idenstr == "func"):
                ret_tok_kind = TokenKind.TOK_FUNC
            elif(idenstr == "extern"):
                ret_tok_kind = TokenKind.TOK_EXTERN
            else:
                ret_tok_kind = TokenKind.TOK_IDENTIFIER
            return Token(ret_tok_kind, idenstr)
        if(self.lastchar.isdigit()):
            idenstr = ""
            # loop over number
            while True:
                idenstr += self.lastchar
                self.lastchar = self.__getChar()
                #
                if not (self.lastchar.isdigit() or self.lastchar == '.'):
                    break
            return Token(TokenKind.TOK_NUMBER, idenstr)
        # 
        if(self.lastchar == '#'):
            # 
            while True:
                self.lastchar = self.__getChar()
                if (self.lastchar == '' or self.lastchar == '\n' or self.lastchar == '\r'):
                    break
            # 
            if (self.lastchar != ''):
                return self._getToken()
        # 
        if(self.lastchar == ''):
            return Token(TokenKind.TOK_EOF, '')
        # 
        ret_char = self.lastchar
        self.lastchar = self.__getChar()
        return Token(ord(ret_char), ret_char)
