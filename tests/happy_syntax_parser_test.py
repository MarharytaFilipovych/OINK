#!/usr/bin/env python3
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sad_syntax_parser_test import parse_code
from compiler.node.program_node import ProgramNode
from compiler.node.decl_node import DeclNode
from compiler.node.assign_node import AssignNode
from compiler.node.if_node import IfNode
from compiler.node.while_node import WhileNode
from compiler.node.binary_op_node import BinaryOpNode
from compiler.llvm_specifics.data_type import DataType


class SyntaxParserHappyTest(unittest.TestCase):

    test_cases = []

    @classmethod
    def add_test_case(cls, name, source, assertion_func):
        cls.test_cases.append((name, source, assertion_func))

    def test_all_cases(self):
        for name, source, assertion in self.test_cases:
            with self.subTest(name=name):
                ast = parse_code(source)
                assertion(self, ast)


def assert_simple_decl_with_init(self, ast):
    self.assertIsInstance(ast, ProgramNode)
    self.assertEqual(len(ast.statement_nodes), 1)
    decl = ast.statement_nodes[0]
    self.assertIsInstance(decl, DeclNode)
    self.assertEqual(decl.variable, "x")
    self.assertEqual(decl.data_type, DataType.I32)
    self.assertTrue(decl.mutable)

def assert_immutable_decl(self, ast):
    decl = ast.statement_nodes[0]
    self.assertIsInstance(decl, DeclNode)
    self.assertFalse(decl.mutable)

def assert_simple_assignment(self, ast):
    self.assertEqual(len(ast.statement_nodes), 2)
    assign = ast.statement_nodes[1]
    self.assertIsInstance(assign, AssignNode)
    self.assertEqual(assign.variable, "x")

def assert_if_simple(self, ast):
    if_stmt = ast.statement_nodes[1]
    self.assertIsInstance(if_stmt, IfNode)
    self.assertIsNotNone(if_stmt.condition)
    self.assertIsNotNone(if_stmt.block)

def assert_while_loop(self, ast):
    while_stmt = ast.statement_nodes[1]
    self.assertIsInstance(while_stmt, WhileNode)
    self.assertIsInstance(while_stmt.condition, BinaryOpNode)
    self.assertEqual(len(while_stmt.block.statements), 1)


all_tests = [
    (
        "simple_declaration_with_initialization",
        "# 😀 🐷 🐖x🐖 @ 42 #\n# ... 🐖x🐖 ... #",
        assert_simple_decl_with_init
    ),
    (
        "immutable_declaration",
        "# 😭 🐷 🐖constant🐖 @ 100 #\n# ... 🐖constant🐖 ... #",
        assert_immutable_decl
    ),
    (
        "simple_assignment",
        "# 😀 🐷 🐖x🐖 @ 10 #\n# 🐖x🐖 @ 20 #\n# ... 🐖x🐖 ... #",
        assert_simple_assignment
    ),
    (
        "if_statement_simple",
        """# 😀 🐷 🐖x🐖 @ 10 #
# SAVE 🐖x🐖 > 5 #
# 🐖🐖🐖 #
# 🐖x🐖 @ 20 #
# 🐖🐖🐖 #
# ... 🐖x🐖 ... #""",
        assert_if_simple
    ),
    (
        "while_loop",
        """# 😀 🐷 🐖counter🐖 @ 0 #
# OINK 🐖counter🐖 < 5 #
# 🐖🐖🐖 #
# 🐖counter🐖 @ 🐖counter🐖 ❤️ 1 #
# 🐖🐖🐖 #
# ... 🐖counter🐖 ... #""",
        assert_while_loop
    ),
]

for name, source, func in all_tests:
    SyntaxParserHappyTest.add_test_case(name, source, func)


if __name__ == "__main__":
    unittest.main(verbosity=2)
