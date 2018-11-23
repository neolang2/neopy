import unittest
from unittest import mock
from compiler.handler import compile_files
from compiler.lexer import Token, TokenKind, Lexer
import os


class TestLexer(unittest.TestCase):
    def __get_path(self, filename):
        return os.path.join(os.path.dirname(__file__), filename)

    def   test_lexer_on_inputfile(self):
        path = self.__get_path("example.nl")
        with open(path, "r") as f:
            lexer = Lexer(inFile=f)
        expected_tokens = [Token(TokenKind.KEYWORD, "extern"),
                           Token(TokenKind.IDENTIFIER, "random"),
                           Token(TokenKind.OPERATOR, "("),
                           Token(TokenKind.IDENTIFIER, "x"),
                           Token(TokenKind.OPERATOR, ")"),
                           Token(TokenKind.KEYWORD, "func"),
                           Token(TokenKind.IDENTIFIER, "random"),
                           Token(TokenKind.OPERATOR, "("),
                           Token(TokenKind.OPERATOR, ")"),
                           Token(TokenKind.IDENTIFIER, "return"),
                           Token(TokenKind.CONSTANT, "4"),
                           Token(TokenKind.IDENTIFIER, "x"),
                           Token(TokenKind.OPERATOR, "="),
                           Token(TokenKind.IDENTIFIER, "random"),
                           Token(TokenKind.OPERATOR, "("),
                           Token(TokenKind.OPERATOR, ")"),
                           Token(TokenKind.IDENTIFIER, "y"),
                           Token(TokenKind.OPERATOR, "="),
                           Token(TokenKind.IDENTIFIER, "x"),
                           Token(TokenKind.OPERATOR, "*"),
                           Token(TokenKind.CONSTANT, "2718"),
                           Token(TokenKind.EOF, "")
                           ]
        for i in range(0, len(lexer.tokens)):
            with self.subTest((expected_tokens[i], lexer.tokens[i])):
                self.assertEqual(expected_tokens[i], lexer.tokens[i])
                #self.assertTrue(expected_tokens[i] == lexer.tokens[i])
