import unittest
from unittest import mock
from compiler.lexer import Lexer, Token
import os


class TestLexer(unittest.TestCase):

    def __get_path(self, filename):
        return os.path.join(os.path.dirname(__file__), filename)

    def test_lexer_on_inputfile(self):
        path = self.__get_path("example.nl")
        with open(path, "r") as f:
            lexer = Lexer(inFile=f)
        expected_tokens = [Token('ID', 'x', 1),
                           Token('ASSIGN', '=', 1),
                           Token('NUMBER', 4, 1),
                           Token('SEMICOLON', ';', 1),
                           Token('FUNC', 'func', 2),
                           Token('ID', 'random', 2),
                           Token('LPAREN', '(', 2),
                           Token('RPAREN', ')', 2),
                           Token('INT', 'int', 2),
                           Token('LBRACE', '{', 2),
                           Token('RETURN', 'return', 3),
                           Token('NUMBER', '5', 3),
                           Token('SEMICOLON', ';', 3),
                           Token('RBRACE', '}', 4)]

        for i in range(0, len(lexer.tokens)):
            self.assertEqual(expected_tokens[i], lexer.tokens[i])
            # with self.subTest((expected_tokens[i], lexer.tokens[i])):
            #     self.assertEqual(expected_tokens[i], lexer.tokens[i])
            #     self.assertTrue(expected_tokenls[i] == lexer.tokens[i])
