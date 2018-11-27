import unittest
from unittest import mock
from compiler.parser import Parser, Node
import os

class TestParser(unittest.TestCase):

    def __get_path(self, filename):
        return os.path.join(os.path.dirname(__file__), filename)

    def test_parser_on_inputfile(self):
        path = self.__get_path("example3.nl")
        with open(path, "r") as f:
            parser = Parser(inFile=f, debug=0)
        expected_nodes = Node("compilation_unit", [
                Node("external_declaration", [
                    Node("declaration", [
                        Node("declaration_specifier", [
                            Node("type")]), 
                        Node("init_declarator_list", [
                                Node("init_declarator", [
                                    Node("declarator", [
                                        Node("x")]),
                                    Node("="), 
                                    Node("assignment_expression", [
                                        Node("math_expression", [
                                            Node("postfix_expression", [
                                                Node("primary_expression", [
                                                    Node("4")])])])])])]), 
                        Node(";")])])])
        nodes = parser.getNodes()
        print(nodes)