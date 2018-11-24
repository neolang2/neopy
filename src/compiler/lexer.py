from enum import Enum
from io import StringIO
import ply.lex as lex


class Token(lex.LexToken):
    def __init__(self, toktype, value, lineno):
        self.type = toktype
        self.value = value
        self.lineno = lineno
        self.lexpos = -1

    def __eq__(self, other):
        # return True
        return self.type == other.type
        # return (self.type == other.type) and (self.value == other.value) and (self.lineno == other.lineno)


keywords = {
    'byte': 'BYTE',
    'int': 'INT',
    'return': 'RETURN',
    'func': 'FUNC',
}

tokens = [
    'NUMBER', 'PLUS', 'MINUS', 'MULT', 'DIVIDE', 'LPAREN',
    'RPAREN', 'ID', 'COMMA', 'SEMICOLON', 'LBRACE',
    'RBRACE', 'ASSIGN',
] + list(keywords.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ASSIGN = r'='


t_ignore = ' \t'


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        t.type = 'ERROR'
        t.value = "Number error ({})".format(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'ID')
    return t


def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/|//.*)'
    t.lexer.lineno += t.value.count('\n')


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    t.value = "Illegal character '{}'".format(t.value[0])
    t.type = 'ERROR'
    return t


plylexer = lex.lex()


class Lexer:
    def __init__(self, inFile=None, inString=None):
        self.tokens = []

        if inFile == None and inString != None:
            plylexer.input(inString)
        elif inString == None and inFile != None:
            plylexer.input(inFile.read())
        else:
            raise ValueError("Requires either a file or string")

        while True:
            curToken = plylexer.token()
            if not curToken:
                break
            self.tokens.append(curToken)

    def getTokens(self):
        return self.tokens
