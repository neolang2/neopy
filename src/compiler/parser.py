#!/usr/bin/env python
import compiler.lexer as lexer
import ply.yacc as yacc

# Get the token map
tokens = lexer.tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIVIDE', 'MOD'),
)


class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf

    def __str__(self):
        return "({}, [{}], {})".format(self.type, ', '.join(str(child) for child in self.children), self.leaf)


'''
# varriable assignment
# function statement
function decleration
code block
return statement
# function call
# math expression
'''
start = 'compilation_unit'


def p_compilation_unit_1(p):
    '''compilation_unit : variable_declaration
                        | function_declaration'''
    p[0] = Node("compilation_unit", leaf=p[1])


def p_compilation_unit_2(p):
    '''compilation_unit : compilation_unit variable_declaration 
                        | compilation_unit function_declaration'''
    p[0] = Node("compilation_unit", [p[2], p[1]],None)


def p_primary_expresssion_1(p):
    '''primary_expression : NUMBER
                          | ID'''
    p[0] = Node("primary_expression", leaf=p[1])


def p_postfix_expression_1(p):
    '''postfix_expression : primary_expression'''
    p[0] = Node("postfix_expression", leaf=p[1])


def p_postfix_expression_2(p):
    '''postfix_expression : postfix_expression LPAREN RPAREN'''
    p[0] = Node("postfix_expression", [p[2], p[3]], p[1])


def p_postfix_expression_3(p):
    '''postfix_expression : postfix_expression LPAREN argument_list RPAREN'''
    p[0] = Node("postfix_expression", [p[2], p[3], p[4]], p[1])


def p_argument_list_1(p):
    '''argument_list : postfix_expression'''
    p[0] = Node("argument_list", [], p[1])


def p_argument_list_2(p):
    '''argument_list : argument_list COMMA postfix_expression'''
    p[0] = Node("argument_list", [p[1], p[2]], p[3])


def p_expression_1(p):
    '''expression : postfix_expression'''
    p[0] = Node("expression", leaf=p[1])


def p_expression_2(p):
    ''' expression : expression PLUS expression
                   | expression MINUS expression
                   | expression MULT expression
                   | expression DIVIDE expression
                   | expression MOD expression'''
    p[0] = Node("expression", [p[3], p[1]], p[2])


def p_expression_3(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = Node("expression", [p[3], p[1]], p[2])


def p_type(p):
    '''type : BYTE
            | INT
            | VOID'''
    p[0] = Node("type", leaf=p[1])


def p_assignment_expression(p):
    '''assignment_expression : expression'''
    p[0] = Node("variable_declaration", [], p[1])


def p_variable_declaration(p):
    '''variable_declaration : type ID ASSIGN assignment_expression SEMICOLON'''
    p[0] = Node("variable_declaration", [p[1], p[2], p[4]], p[3])


def p_function_declaration(p):
    '''function_declaration : FUNC ID LPAREN RPAREN type code_block'''
    p[0] = Node("function_declaration", [p[1], p[2], p[3], p[4], p[5]], p[6])


def p_function_declaration_2(p):
    '''function_declaration : FUNC ID LPAREN parameter_list RPAREN type code_block'''
    p[0] = Node("function_declaration", [
                p[1], p[2], p[3], p[4], p[5], p[6]], p[7])


def p_parameter_list(p):
    '''parameter_list : type ID'''
    pass


def p_parameter_list_2(p):
    '''parameter_list : parameter_list COMMA parameter_list'''
    pass


def p_code_block(p):
    '''code_block : LBRACE RBRACE'''
    pass


def p_empty(p):
    'empty : '
    pass


def p_error(p):
    print("Whoa. We're hosed")
    if not p:
        print("End of File!")
        return

# Build the grammar


plyparser = yacc.yacc()


class Parser:
    def __init__(self, inFile=None, inString=None, debug=0):
        plyparser.error = 0
        self.nodes = []

        if inFile == None and inString != None:
            self.nodes = plyparser.parse(inString, debug=debug)

        elif inString == None and inFile != None:
            self.nodes = plyparser.parse(inFile.read(), debug=debug)
        else:
            raise ValueError("Requires either a file or string")

    def getNodes(self):
        if plyparser.error:
            return None
        return self.nodes
