import unittest
from unittest import mock
from compiler.parser import Parser, Node
import os


class TestParser(unittest.TestCase):

    def __get_path(self, filename):
        return os.path.join(os.path.dirname(__file__), filename)

    def test_parser_on_inputfile(self):
        path = self.__get_path("example2.nl")
        with open(path, "r") as f:
            parser = Parser(inFile=f,debug=1)
        print(parser.getNodes())
        # parser.getNodes().print()

