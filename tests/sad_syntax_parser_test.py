#!/usr/bin/env python3

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler.syntax_parser import SyntaxParser
from compiler.lexer.lexer import Lexer
from compiler.node.program_node import ProgramNode
from compiler.node.decl_node import DeclNode
from compiler.node.assign_node import AssignNode
from compiler.node.if_node import IfNode
from compiler.node.while_node import WhileNode
from compiler.node.binary_op_node import BinaryOpNode
from compiler.node.unary_op_node import UnaryOpNode
from compiler.node.number_node import NumberNode
from compiler.node.bool_node import BooleanNode
from compiler.llvm_specifics.data_type import DataType
from compiler.llvm_specifics.operator import Operator


def parse_code(source: str) -> ProgramNode:
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = SyntaxParser(tokens)
    return parser.parse_program()


class TestSyntaxParserFailingCases(unittest.TestCase):

    def test_missing_variable_border(self):
        source = "# 😀 🐷 x @ 10 #\n# ... 🐖x🐖 ... #"
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("expected", str(context.exception).lower())

    def test_missing_assignment_operator(self):
        source = "# 😀 🐷 🐖x🐖 10 #\n# ... 🐖x🐖 ... #"
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("assignment", str(context.exception).lower())

    def test_missing_line_border(self):
        source = "😀 🐷 🐖x🐖 @ 10\n# ... 🐖x🐖 ... #"
        with self.assertRaises(ValueError) as context:
            parse_code(source)

    def test_missing_newline_between_statements(self):
        source = "# 😀 🐷 🐖x🐖 @ 10 # # 😀 🐷 🐖y🐖 @ 20 #\n# ... 🐖x🐖 ... #"
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("newline", str(context.exception).lower())

    def test_empty_program(self):
        source = "# ... 42 ... #"
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("empty", str(context.exception).lower())

    def test_missing_return_statement(self):
        source = "# 😀 🐷 🐖x🐖 @ 10 #"
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("return", str(context.exception).lower())

    def test_code_after_return(self):
        source = "# 😀 🐷 🐖x🐖 @ 10 #\n# ... 🐖x🐖 ... #\n# 🐖x🐖 @ 20 #"
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("return", str(context.exception).lower())

    def test_malformed_number(self):
        source = "# 😀 🐷 🐖x🐖 @ 12.5 #\n# ... 🐖x🐖 ... #"
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("number", str(context.exception).lower())


    def test_unmatched_bracket(self):
        source = "# 😀 🐷 🐖x🐖 @ ** 10 ❤️ 5 #\n# ... 🐖x🐖 ... #"
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("bracket", str(context.exception).lower())

    def test_missing_block_delimiter(self):
        source = """# 😀 🐷 🐖x🐖 @ 10 #
# SAVE 🐖x🐖 > 5 #
# 🐖x🐖 @ 20 #
# ... 🐖x🐖 ... #"""
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("block", str(context.exception).lower())

    def test_if_without_condition(self):
        source = """# 😀 🐷 🐖x🐖 @ 10 #
# SAVE #
# 🐖🐖🐖 #
# 🐖x🐖 @ 20 #
# 🐖🐖🐖 #
# ... 🐖x🐖 ... #"""
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("if condition", str(context.exception).lower())

    def test_while_without_condition(self):
        source = """# 😀 🐷 🐖counter🐖 @ 0 #
# OINK #
# 🐖🐖🐖 #
# 🐖counter🐖 @ 🐖counter🐖 ❤️ 1 #
# 🐖🐖🐖 #
# ... 🐖counter🐖 ... #"""
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("while condition", str(context.exception).lower())

    def test_mismatched_mood_line_borders(self):
        source = "#~ 😀 🐷 🐖x🐖 @ 10 #\n# ... 🐖x🐖 ... #"
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("mood line", str(context.exception).lower())

    def test_invalid_variable_name_characters(self):
        source = "# 😀 🐷 🐖x123🐖 @ 10 #\n# ... 🐖x123🐖 ... #"
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("variable", str(context.exception).lower())

    def test_missing_mutability_specifier(self):
        source = "# 🐷 🐖x🐖 @ 10 #\n# ... 🐖x🐖 ... #"
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("mutability", str(context.exception).lower())

    def test_missing_type_specifier(self):
        source = "# 😀 🐖x🐖 @ 10 #\n# ... 🐖x🐖 ... #"
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("type", str(context.exception).lower())

    def test_elif_without_if(self):
        source = """# 😀 🐷 🐖x🐖 @ 10 #
# HURT 🐖x🐖 > 5 #
# 🐖🐖🐖 #
# 🐖x🐖 @ 20 #
# 🐖🐖🐖 #
# ... 🐖x🐖 ... #"""
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("elif without if", str(context.exception).lower())

    def test_else_without_if(self):
        source = """# 😀 🐷 🐖x🐖 @ 10 #
# KILL #
# 🐖🐖🐖 #
# 🐖x🐖 @ 20 #
# 🐖🐖🐖 #
# ... 🐖x🐖 ... #"""
        with self.assertRaises(ValueError) as context:
            parse_code(source)
        self.assertIn("else without if", str(context.exception).lower())

    def test_incomplete_expression(self):
        source = "# 😀 🐷 🐖x🐖 @ 10 ❤️ #\n# ... 🐖x🐖 ... #"
        with self.assertRaises(ValueError) as context:
            parse_code(source)

    

if __name__ == '__main__':
    unittest.main(verbosity=2)