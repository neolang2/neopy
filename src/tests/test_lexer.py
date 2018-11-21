import unittest
from unittest import mock
from compiler.lexer import Token, TokenKind, Lexer
import os


class TestArgParser(unittest.TestCase):
    def __get_path(self, filename):
        return os.path.join(os.path.dirname(__file__), filename)

    def test_lexer_on_inputfile(self):
        path = self.__get_path("example.nl")
        lexer = Lexer()
        lexer.lex(filename=path)
        expected_tokens = [Token(TokenKind.TOK_EXTERN, "extern"),
                           Token(TokenKind.TOK_IDENTIFIER, "random"),
                           Token(ord("("), "("),
                           Token(TokenKind.TOK_IDENTIFIER, "x"),
                           Token(ord(")"), ")"),
                           Token(TokenKind.TOK_FUNC, "func"),
                           Token(TokenKind.TOK_IDENTIFIER, "random"),
                           Token(ord("("), "("),
                           Token(ord(")"), ")"),
                           Token(TokenKind.TOK_IDENTIFIER, "return"),
                           Token(TokenKind.TOK_NUMBER, "4"),
                           Token(TokenKind.TOK_IDENTIFIER, "x"),
                           Token(ord("="), "="),
                           Token(TokenKind.TOK_IDENTIFIER, "random"),
                           Token(ord("("), "("),
                           Token(ord(")"), ")"),
                           Token(TokenKind.TOK_IDENTIFIER, "y"),
                           Token(ord("="), "="),
                           Token(TokenKind.TOK_IDENTIFIER, "x"),
                           Token(ord("*"), "*"),
                           Token(TokenKind.TOK_NUMBER, "2.718"),
                           Token(TokenKind.TOK_EOF, "")
                           ]
        for i in range(0, len(lexer.tokens)):
            with self.subTest((expected_tokens[i], lexer.tokens[i])):
                self.assertTrue(expected_tokens[i] == lexer.tokens[i])
