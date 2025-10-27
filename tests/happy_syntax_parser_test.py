#!/usr/bin/env python3

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .sad_syntax_parser_test import parse_code
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


class TestSyntaxParserHappyPath(unittest.TestCase):

    def test_simple_declaration_with_initialization(self):
        source = "# 😀 🐷 🐖x🐖 @ 42 #\n# ... 🐖x🐖 ... #"
        ast = parse_code(source)
        
        self.assertIsInstance(ast, ProgramNode)
        self.assertEqual(len(ast.statement_nodes), 1)
        decl = ast.statement_nodes[0]
        self.assertIsInstance(decl, DeclNode)
        self.assertEqual(decl.variable, "x")
        self.assertEqual(decl.data_type, DataType.I32)
        self.assertTrue(decl.mutable)

    def test_declaration_without_initialization(self):
        source = "# 😀 🐷 🐖counter🐖 #\n# ... 🐖counter🐖 ... #"
        ast = parse_code(source)
        
        decl = ast.statement_nodes[0]
        self.assertIsInstance(decl, DeclNode)
        self.assertIsInstance(decl.expr_node, NumberNode)
        self.assertEqual(decl.expr_node.value, "0")

    def test_immutable_declaration(self):
        source = "# 😭 🐷 🐖constant🐖 @ 100 #\n# ... 🐖constant🐖 ... #"
        ast = parse_code(source)
        
        decl = ast.statement_nodes[0]
        self.assertIsInstance(decl, DeclNode)
        self.assertFalse(decl.mutable)

    def test_all_data_types(self):
        for type_emoji, data_type in [("🐽", DataType.I16), ("🐷", DataType.I32), 
                                       ("🐗", DataType.I64), ("wow", DataType.BOOL)]:
            with self.subTest(type=type_emoji):
                source = f"# 😀 {type_emoji} 🐖var🐖 #\n# ... 🐖var🐖 ... #"
                ast = parse_code(source)
                decl = ast.statement_nodes[0]
                self.assertEqual(decl.data_type, data_type)

    def test_simple_assignment(self):
        source = "# 😀 🐷 🐖x🐖 @ 10 #\n# 🐖x🐖 @ 20 #\n# ... 🐖x🐖 ... #"
        ast = parse_code(source)
        
        self.assertEqual(len(ast.statement_nodes), 2)
        assign = ast.statement_nodes[1]
        self.assertIsInstance(assign, AssignNode)
        self.assertEqual(assign.variable, "x")

    def test_arithmetic_expressions(self):
        operators = [("❤️", Operator.PLUS), ("💔", Operator.MINUS), 
                     ("💞", Operator.MULTIPLY), ("💕", Operator.DIVIDE)]
        
        for op_symbol, op_enum in operators:
            with self.subTest(operator=op_symbol):
                source = f"# 😀 🐷 🐖result🐖 @ 10 {op_symbol} 5 #\n# ... 🐖result🐖 ... #"
                ast = parse_code(source)
                decl = ast.statement_nodes[0]
                self.assertIsInstance(decl.expr_node, BinaryOpNode)
                self.assertEqual(decl.expr_node.operator, op_enum)

    def test_comparison_operators(self):
        operators = [("🌸🌸", Operator.EQUALS), ("💩🌸", Operator.NOT_EQUALS),
                     (">", Operator.GREATER), ("<", Operator.LESS),
                     ("🌸>", Operator.GREATER_EQUAL), ("🌸<", Operator.LESS_EQUAL)]
        
        for op_symbol, op_enum in operators:
            with self.subTest(operator=op_symbol):
                source = f"# 😀 wow 🐖result🐖 @ 10 {op_symbol} 5 #\n# ... 🐖result🐖 ... #"
                ast = parse_code(source)
                decl = ast.statement_nodes[0]
                self.assertIsInstance(decl.expr_node, BinaryOpNode)
                self.assertEqual(decl.expr_node.operator, op_enum)

    def test_logical_operators(self):
        for op_symbol, op_enum in [("hru", Operator.AND), ("bruh", Operator.OR)]:
            with self.subTest(operator=op_symbol):
                source = f"# 😀 wow 🐖result🐖 @ LOVE {op_symbol} HATE #\n# ... 🐖result🐖 ... #"
                ast = parse_code(source)
                decl = ast.statement_nodes[0]
                self.assertIsInstance(decl.expr_node, BinaryOpNode)
                self.assertEqual(decl.expr_node.operator, op_enum)

    def test_unary_not_operator(self):
        source = "# 😀 wow 🐖result🐖 @ 💩 LOVE #\n# ... 🐖result🐖 ... #"
        ast = parse_code(source)
        
        decl = ast.statement_nodes[0]
        self.assertIsInstance(decl.expr_node, UnaryOpNode)
        self.assertEqual(decl.expr_node.operator, "💩")

    def test_expression_with_brackets(self):
        source = "# 😀 🐷 🐖result🐖 @ ** 5 ❤️ 3 ** 💞 2 #\n# ... 🐖result🐖 ... #"
        ast = parse_code(source)
        
        decl = ast.statement_nodes[0]
        self.assertIsInstance(decl.expr_node, BinaryOpNode)
        self.assertEqual(decl.expr_node.operator, Operator.MULTIPLY)

    def test_complex_nested_expression(self):
        source = "# 😀 wow 🐖result🐖 @ 10 > 5 hru 20 < 30 bruh 15 🌸🌸 15 #\n# ... 🐖result🐖 ... #"
        ast = parse_code(source)
        
        decl = ast.statement_nodes[0]
        self.assertIsInstance(decl.expr_node, BinaryOpNode)
        self.assertEqual(decl.expr_node.operator, Operator.OR)
        self.assertIsInstance(decl.expr_node.left, BinaryOpNode)
        self.assertEqual(decl.expr_node.left.operator, Operator.AND)
        self.assertIsInstance(decl.expr_node.right, BinaryOpNode)
        self.assertEqual(decl.expr_node.right.operator, Operator.EQUALS)
        self.assertIsInstance(decl.expr_node.left.left, BinaryOpNode)
        self.assertEqual(decl.expr_node.left.left.operator, Operator.GREATER)
        self.assertIsInstance(decl.expr_node.left.right, BinaryOpNode)
        self.assertEqual(decl.expr_node.left.right.operator, Operator.LESS)
        # Should parse as: (10 > 5 AND 20 < 30) OR 15 == 15

    def test_if_statement_simple(self):
        source = """# 😀 🐷 🐖x🐖 @ 10 #
# SAVE 🐖x🐖 > 5 #
# 🐖🐖🐖 #
# 🐖x🐖 @ 20 #
# 🐖🐖🐖 #
# ... 🐖x🐖 ... #"""
        ast = parse_code(source)
        
        self.assertEqual(len(ast.statement_nodes), 2)
        if_stmt = ast.statement_nodes[1]
        self.assertIsInstance(if_stmt, IfNode)
        self.assertIsNotNone(if_stmt.condition)
        self.assertIsNotNone(if_stmt.block)

    def test_if_elif_else_statement(self):
        source = """# 😀 🐷 🐖x🐖 @ 5 #
# SAVE 🐖x🐖 > 10 #
# 🐖🐖🐖 #
# 🐖x🐖 @ 100 #
# 🐖🐖🐖 #
# HURT 🐖x🐖 🌸🌸 5 #
# 🐖🐖🐖 #
# 🐖x🐖 @ 50 #
# 🐖🐖🐖 #
# KILL #
# 🐖🐖🐖 #
# 🐖x🐖 @ 25 #
# 🐖🐖🐖 #
# ... 🐖x🐖 ... #"""
        ast = parse_code(source)
        
        if_stmt = ast.statement_nodes[1]
        self.assertIsInstance(if_stmt, IfNode)
        self.assertEqual(len(if_stmt.elif_blocks), 1)
        self.assertIsNotNone(if_stmt.else_block)
        self.assertIsNotNone(if_stmt.else_block.block)
        self.assertEqual(len(if_stmt.else_block.block.statements), 1)
        self.assertIsInstance(if_stmt.else_block.block.statements[0], AssignNode)
        self.assertEqual(if_stmt.else_block.block.statements[0].expr_node.value, "25")
        self.assertIsInstance(if_stmt.elif_blocks[0].block.statements[0], AssignNode)
        self.assertEqual(if_stmt.elif_blocks[0].block.statements[0].expr_node.value, "50")
        self.assertIsInstance(if_stmt.block.statements[0], AssignNode)
        self.assertEqual(if_stmt.block.statements[0].expr_node.value, "100")
        self.assertIsInstance(if_stmt.condition, BinaryOpNode)
        self.assertIsInstance(if_stmt.elif_blocks[0].condition, BinaryOpNode)
        self.assertEqual(if_stmt.condition.operator, Operator.GREATER)
        self.assertEqual(if_stmt.elif_blocks[0].condition.operator, Operator.GREATER_EQUAL)
        self.assertEqual(if_stmt.else_block.condition, None)

    def test_while_loop(self):
        source = """# 😀 🐷 🐖counter🐖 @ 0 #
# OINK 🐖counter🐖 < 5 #
# 🐖🐖🐖 #
# 🐖counter🐖 @ 🐖counter🐖 ❤️ 1 #
# 🐖🐖🐖 #
# ... 🐖counter🐖 ... #"""
        ast = parse_code(source)
        
        self.assertEqual(len(ast.statement_nodes), 2)
        while_stmt = ast.statement_nodes[1]
        self.assertIsInstance(while_stmt, WhileNode)
        self.assertIsNotNone(while_stmt.condition)
        self.assertIsNotNone(while_stmt.block)
        self.assertIsInstance(while_stmt.condition, BinaryOpNode)
        self.assertEqual(while_stmt.condition.operator, Operator.LESS)
        self.assertEqual(len(while_stmt.block.statements), 1)
        self.assertIsInstance(while_stmt.block.statements[0], AssignNode)
        self.assertIsInstance(while_stmt.block.statements[0].expr_node, BinaryOpNode)
        self.assertEqual(while_stmt.block.statements[0].expr_node.operator, Operator.PLUS)
        self.assertEqual(while_stmt.block.statements[0].expr_node.right.value, "1")
        self.assertEqual(while_stmt.block.statements[0].expr_node.left.value, "counter")
        self.assertEqual(while_stmt.block.statements[0].variable, "counter")

    def test_mood_line_arithmetic(self):
        source = "#~ 😀 🐷 🐖x🐖 @ 10 ❤️ 5 ~#\n# ... 🐖x🐖 ... #"
        ast = parse_code(source)
        
        decl = ast.statement_nodes[0]
        # In mood line, ❤️ should become 💔
        self.assertIsInstance(decl.expr_node, BinaryOpNode)
        self.assertEqual(decl.expr_node.operator, Operator.MINUS)

    def test_mood_line_comparison(self):
        source = "#~ 😀 wow 🐖result🐖 @ 10 > 5 ~#\n# ... 🐖result🐖 ... #"
        ast = parse_code(source)
        
        decl = ast.statement_nodes[0]
        # In mood line, > should become 🌸<
        self.assertIsInstance(decl.expr_node, BinaryOpNode)
        self.assertEqual(decl.expr_node.operator, Operator.LESS_EQUAL)

    def test_mood_line_boolean_literal(self):
        source = "#~ 😀 wow 🐖flag🐖 @ LOVE ~#\n# ... 🐖flag🐖 ... #"
        ast = parse_code(source)
        
        decl = ast.statement_nodes[0]
        # LOVE should become HATE in mood line
        self.assertIsInstance(decl.expr_node, BooleanNode)
        self.assertEqual(decl.expr_node.value, "HATE")

    def test_mood_line_if_condition(self):
        source = """# 😀 🐷 🐖x🐖 @ 10 #
#~ SAVE 🐖x🐖 > 5 ~#
# 🐖🐖🐖 #
# 🐖x🐖 @ 20 #
# 🐖🐖🐖 #
# ... 🐖x🐖 ... #"""
        ast = parse_code(source)
        
        if_stmt = ast.statement_nodes[1]
        self.assertIsInstance(if_stmt.condition, UnaryOpNode)

    def test_variable_with_ampersand(self):
        source = "# 😀 🐷 🐖my&variable🐖 @ 42 #\n# ... 🐖my&variable🐖 ... #"
        ast = parse_code(source)
        
        decl = ast.statement_nodes[0]
        self.assertEqual(decl.variable, "my&variable")

    def test_nested_control_flow(self):
        source = """# 😀 🐷 🐖x🐖 @ 10 #
# SAVE 🐖x🐖 > 5 #
# 🐖🐖🐖 #
# SAVE 🐖x🐖 < 15 #
# 🐖🐖🐖 #
# 🐖x🐖 @ 100 #
# 🐖🐖🐖 #
# 🐖🐖🐖 #
# ... 🐖x🐖 ... #"""
        ast = parse_code(source)
        
        if_stmt = ast.statement_nodes[1]
        self.assertIsInstance(if_stmt, IfNode)
        self.assertTrue(len(if_stmt.block.statements) > 0)
        self.assertIsInstance(if_stmt.block.statements[0], IfNode)
        nested_if = if_stmt.block.statements[0]
        self.assertIsInstance(nested_if.condition, BinaryOpNode)
        self.assertIsInstance(nested_if.block.statements[0], AssignNode)
        self.assertEqual(nested_if.block.statements[0].expr_node.value, "100")
        self.assertEqual(nested_if.condition.operator, Operator.LESS)
        self.assertEqual(if_stmt.condition.operator, Operator.GREATER)
        self.assertIsInstance(if_stmt.block.statements[0], IfNode)

    def test_large_number_i64(self):
        source = "# 😀 🐗 🐖big🐖 @ 9223372036854775807 #\n# ... 🐖big🐖 ... #"
        ast = parse_code(source)
        
        decl = ast.statement_nodes[0]
        self.assertEqual(decl.data_type, DataType.I64)

    def test_multiple_elif_blocks(self):
        source = """# 😀 🐷 🐖x🐖 @ 5 #
# SAVE 🐖x🐖 > 10 #
# 🐖🐖🐖 #
# 🐖x🐖 @ 100 #
# 🐖🐖🐖 #
# HURT 🐖x🐖 > 7 #
# 🐖🐖🐖 #
# 🐖x🐖 @ 70 #
# 🐖🐖🐖 #
# HURT 🐖x🐖 > 3 #
# 🐖🐖🐖 #
# 🐖x🐖 @ 30 #
# 🐖🐖🐖 #
# ... 🐖x🐖 ... #"""
        ast = parse_code(source)
        
        if_stmt = ast.statement_nodes[1]
        self.assertEqual(len(if_stmt.elif_blocks), 2)

    def test_empty_code_block(self):
        source = """# 😀 🐷 🐖x🐖 @ 10 #
# SAVE 🐖x🐖 > 5 #
# 🐖🐖🐖 #
# 🐖🐖🐖 #
# ... 🐖x🐖 ... #"""
        ast = parse_code(source)
        
        if_stmt = ast.statement_nodes[1]
        self.assertEqual(len(if_stmt.block.statements), 0)

    def test_deeply_nested_expressions(self):
        source = "# 😀 🐷 🐖result🐖 @ ** ** 1 ❤️ 2 ** ❤️ 3 ** #\n# ... 🐖result🐖 ... #"
        ast = parse_code(source)
        
        # Should parse without error
        self.assertIsInstance(ast, ProgramNode)


if __name__ == '__main__':
    unittest.main(verbosity=2)