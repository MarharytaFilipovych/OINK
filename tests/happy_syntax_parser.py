#!/usr/bin/env python3
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler.node.function_call_node import FunctionCallNode
from compiler.syntax_parser.syntax_parser import SyntaxParser
from compiler.lexer.lexer import Lexer
from compiler.node.program_node import ProgramNode
from compiler.node.decl_node import DeclNode
from compiler.node.assign_node import AssignNode
from compiler.node.if_node import IfNode
from compiler.node.while_node import WhileNode
from compiler.node.binary_op_node import BinaryOpNode
from compiler.node.struct_decl_node import StructDeclNode
from compiler.node.function_decl_node import FunctionDeclNode
from compiler.llvm_specifics.data_type import DataType
from compiler.node.print_node import PrintNode
from compiler.node.read_node import ReadNode
from compiler.node.lambda_node import LambdaNode
from compiler.node.unary_op_node import UnaryOpNode
from compiler.node.number_node import NumberNode

def parse_code(source: str) -> ProgramNode:
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = SyntaxParser(tokens)
    return parser.parse_program()

class SyntaxParserHappyTest(unittest.TestCase):
    test_cases = []

    @classmethod
    def add_test_case(cls, name, source, assertion_func):
        cls.test_cases.append((name, source, assertion_func, False))

    def test_all_cases(self):
        results = []
        for name, source, assertion, expect_failure in self.test_cases:
            try:
                ast = parse_code(source)
                assertion(self, ast)
                if expect_failure:
                    results.append((name, "FAIL (was expected to fail)"))
                else:
                    results.append((name, "PASS"))
            except Exception as e:
                if expect_failure:
                    results.append((name, "PASS (expected failure)"))
                else:
                    results.append((name, f"FAIL ({type(e).__name__}: {e})"))

        print("\nTest Summary:")
        for test_name, status in results:
            print(f"{test_name}: {status}")

        unexpected_failures = [s for _, s in results if s.startswith("FAIL (") and "expected failure" not in s]
        if unexpected_failures:
            self.fail(f"{len(unexpected_failures)} tests failed unexpectedly: {unexpected_failures}")


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

def assert_struct_declaration(self, ast):
    self.assertEqual(len(ast.struct_declarations), 1)
    struct = ast.struct_declarations[0]
    self.assertIsInstance(struct, StructDeclNode)
    self.assertEqual(struct.variable, "Point")

def assert_struct_with_fields(self, ast):
    struct = ast.struct_declarations[0]
    self.assertEqual(len(struct.fields), 2)
    self.assertEqual(struct.fields[0].name, "x")
    self.assertEqual(struct.fields[1].name, "y")

def assert_function_declaration(self, ast):
    self.assertEqual(len(ast.function_declarations), 1)
    func = ast.function_declarations[0]
    self.assertIsInstance(func, FunctionDeclNode)
    self.assertEqual(func.variable, "add")

def assert_function_with_params(self, ast):
    func = ast.function_declarations[0]
    self.assertEqual(len(func.params), 2)
    self.assertEqual(func.params[0].name, "a")
    self.assertEqual(func.params[1].name, "b")

def assert_function_return_type(self, ast):
    func = ast.function_declarations[0]
    self.assertEqual(func.return_type, DataType.I32)

def assert_struct_with_member_function(self, ast):
    struct = ast.struct_declarations[0]
    self.assertEqual(len(struct.member_functions), 1)
    self.assertEqual(struct.member_functions[0].variable, "getX")

def assert_void_function(self, ast):
    func = ast.function_declarations[0]
    self.assertEqual(func.return_type, DataType.VOID)

def assert_struct_field_types(self, ast):
    struct = ast.struct_declarations[0]
    self.assertEqual(struct.fields[0].field_type, DataType.I32)
    self.assertEqual(struct.fields[1].field_type, DataType.I32)

def assert_function_with_struct_param(self, ast):
    self.assertEqual(len(ast.function_declarations), 1)
    func = ast.function_declarations[0]
    self.assertEqual(len(func.params), 1)
    self.assertEqual(func.params[0].name, "p")
    self.assertEqual(func.params[0].param_type, "Point") 

def assert_struct_member_function_call(self, ast):
    self.assertEqual(len(ast.statement_nodes), 2)
    decl = ast.statement_nodes[1]
    self.assertIsInstance(decl, DeclNode)
    self.assertEqual(decl.variable, "result")
    func_call = decl.expr_node
    self.assertIsInstance(func_call, FunctionCallNode)
    self.assertEqual(func_call.value, "getValue")
    self.assertEqual(func_call.object_name, "c")

def assert_read_i32(self, ast):
    read_stmt = ast.statement_nodes[1]
    self.assertIsInstance(read_stmt, ReadNode)
    self.assertEqual(read_stmt.variable, "x")

def assert_print_expression(self, ast):
    print_stmt = ast.statement_nodes[1]
    self.assertIsInstance(print_stmt, PrintNode)
    self.assertIsNotNone(print_stmt.expr_node)

def assert_chained_function_calls(self, ast):
    decl = ast.statement_nodes[0]
    self.assertIsInstance(decl, DeclNode)
    func_call = decl.expr_node
    self.assertIsInstance(func_call, FunctionCallNode)
    self.assertEqual(func_call.value, "double")
    self.assertEqual(len(func_call.arguments), 1)
    self.assertIsInstance(func_call.arguments[0], FunctionCallNode)
    self.assertEqual(func_call.arguments[0].value, "getValue")

def assert_simple_lambda_structure(self, ast):
    decl = ast.statement_nodes[0]
    self.assertIsInstance(decl, DeclNode)
    lambda_node = decl.expr_node
    self.assertIsInstance(lambda_node, LambdaNode)
    self.assertEqual(len(lambda_node.params), 1)
    self.assertEqual(lambda_node.params[0].name, "x")
    self.assertEqual(lambda_node.params[0].param_type, DataType.I32)

def assert_lambda_with_multiple_params(self, ast):
    decl = ast.statement_nodes[0]
    lambda_node = decl.expr_node
    self.assertIsInstance(lambda_node, LambdaNode)
    self.assertEqual(len(lambda_node.params), 2)
    self.assertEqual(lambda_node.params[0].name, "a")
    self.assertEqual(lambda_node.params[1].name, "b")

def assert_lambda_with_no_params(self, ast):
    decl = ast.statement_nodes[0]
    lambda_node = decl.expr_node
    self.assertIsInstance(lambda_node, LambdaNode)
    self.assertEqual(len(lambda_node.params), 0)

def assert_lambda_body_is_binary_op(self, ast):
    decl = ast.statement_nodes[0]
    lambda_node = decl.expr_node
    self.assertIsInstance(lambda_node.body, BinaryOpNode)

def assert_lambda_body_is_comparison(self, ast):
    decl = ast.statement_nodes[0]
    lambda_node = decl.expr_node
    self.assertIsInstance(lambda_node.body, BinaryOpNode)
    self.assertTrue(lambda_node.body.operator.is_for_comparison())

def assert_lambda_body_is_unary(self, ast):
    decl = ast.statement_nodes[0]
    lambda_node = decl.expr_node
    self.assertIsInstance(lambda_node.body, UnaryOpNode)

def assert_lambda_body_is_number(self, ast):
    decl = ast.statement_nodes[0]
    lambda_node = decl.expr_node
    self.assertIsInstance(lambda_node.body, NumberNode)

def assert_lambda_with_i16_param(self, ast):
    decl = ast.statement_nodes[0]
    lambda_node = decl.expr_node
    self.assertEqual(lambda_node.params[0].param_type, DataType.I16)

def assert_lambda_with_bool_param(self, ast):
    decl = ast.statement_nodes[0]
    lambda_node = decl.expr_node
    self.assertEqual(lambda_node.params[0].param_type, DataType.BOOL)

def assert_lambda_with_mixed_types(self, ast):
    decl = ast.statement_nodes[0]
    lambda_node = decl.expr_node
    self.assertEqual(len(lambda_node.params), 2)
    self.assertEqual(lambda_node.params[0].param_type, DataType.I16)
    self.assertEqual(lambda_node.params[1].param_type, DataType.I32)

def assert_lambda_call_in_return(self, ast):
    decl = ast.statement_nodes[0]
    self.assertIsInstance(decl, DeclNode)
    self.assertEqual(decl.data_type, "lambda")

all_tests = [
    ("simple_declaration_with_initialization", "# 😀 🐷 🐖x🐖 @ 42 #\n# ... 🐖x🐖 ... #", assert_simple_decl_with_init),
    ("immutable_declaration", "# 😭 🐷 🐖constant🐖 @ 100 #\n# ... 🐖constant🐖 ... #", assert_immutable_decl),
    ("simple_assignment", "# 😀 🐷 🐖x🐖 @ 10 #\n# 🐖x🐖 @ 20 #\n# ... 🐖x🐖 ... #", assert_simple_assignment),
    ("if_statement_simple", "# 😀 🐷 🐖x🐖 @ 10 #\n# SAVE 🐖x🐖 > 5 #\n# 🐖🐖🐖 #\n# 🐖x🐖 @ 20 #\n# 🐖🐖🐖 #\n# ... 🐖x🐖 ... #", assert_if_simple),
    ("while_loop", "# 😀 🐷 🐖counter🐖 @ 0 #\n# OINK 🐖counter🐖 < 5 #\n# 🐖🐖🐖 #\n# 🐖counter🐖 @ 🐖counter🐖 ❤️ 1 #\n# 🐖🐖🐖 #\n# ... 🐖counter🐖 ... #", assert_while_loop),
    ("struct_declaration", "# BOAR 🐖Point🐖 #\n# 🐖🐖🐖 #\n# 😀 🐷 🐖x🐖 #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_struct_declaration),
    ("struct_with_fields", "# BOAR 🐖Point🐖 #\n# 🐖🐖🐖 #\n# 😀 🐷 🐖x🐖 #\n# 😀 🐷 🐖y🐖 #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_struct_with_fields),
    ("function_declaration", "# 🐷 PIG 🐖add🐖 #\n# 🐖🐖🐖 #\n# ... 0 ... #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_function_declaration),
    ("function_with_params", "# 🐷 PIG 🐖add🐖 ** 🐷 🐖a🐖 ** ** 🐷 🐖b🐖 ** #\n# 🐖🐖🐖 #\n# ... 🐖a🐖 ❤️ 🐖b🐖 ... #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_function_with_params),
    ("function_return_type", "# 🐷 PIG 🐖getValue🐖 #\n# 🐖🐖🐖 #\n# ... 42 ... #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_function_return_type),
    ("struct_with_member_function", "# BOAR 🐖Point🐖 #\n# 🐖🐖🐖 #\n# 😀 🐷 🐖x🐖 #\n# 🐷 PIGLET 🐖getX🐖 #\n# 🐖🐖🐖 #\n# ... 🐖x🐖 ... #\n# 🐖🐖🐖 #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_struct_with_member_function),
    ("void_function", "# 😑 PIG 🐖print🐖 #\n# 🐖🐖🐖 #\n# ... #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_void_function),
    ("struct_field_types", "# BOAR 🐖Point🐖 #\n# 🐖🐖🐖 #\n# 😀 🐷 🐖x🐖 #\n# 😀 🐷 🐖y🐖 #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_struct_field_types),
    ("function_with_struct_param", "# BOAR 🐖Point🐖 #\n# 🐖🐖🐖 #\n# 😀 🐷 🐖x🐖 #\n# 🐖🐖🐖 #\n# 🐷 PIG 🐖process🐖 ** 🐖Point🐖 🐖p🐖 ** #\n# 🐖🐖🐖 #\n# ... 🐖p🐖 _ 🐖x🐖 ... #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_function_with_struct_param),
    ("struct_member_function_call", "# BOAR 🐖Counter🐖 #\n# 🐖🐖🐖 #\n# 😀 🐷 🐖val🐖 #\n# 🐷 PIGLET 🐖getValue🐖 #\n# 🐖🐖🐖 #\n# ... 🐖val🐖 ... #\n# 🐖🐖🐖 #\n# 🐖🐖🐖 #\n# 😀 🐖Counter🐖 🐖c🐖 @ 🐖Counter🐖 ** 5 ** #\n# 😀 🐷 🐖result🐖 @ 🐖c🐖 _ 🐖getValue🐖 ** ** #\n# ... 🐖result🐖 ... #", assert_struct_member_function_call),
    ("chained_function_calls", "# 🐷 PIG 🐖getValue🐖 #\n# 🐖🐖🐖 #\n# ... 10 ... #\n# 🐖🐖🐖 #\n# 🐷 PIG 🐖double🐖 ** 🐷 🐖x🐖 ** #\n# 🐖🐖🐖 #\n# ... 🐖x🐖 💞 2 ... #\n# 🐖🐖🐖 #\n# 😀 🐷 🐖result🐖 @ 🐖getValue🐖 ** ** _ 🐖double🐖 ** ** # \n# ... 🐖result🐖 ... #", assert_chained_function_calls),
    ("simple_lambda_one_param", "# 😀 🥩 🐖square🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 💞 🐖x🐖 🥩 #\n# ... 0 ... #", assert_simple_lambda_structure),
    ("lambda_two_params", "# 😀 🥩 🐖add🐖 @ 🥩 ** 🐷 🐖a🐖 ** ** 🐷 🐖b🐖 ** 🥩 🐖a🐖 ❤️ 🐖b🐖 🥩 #\n# ... 0 ... #", assert_lambda_with_multiple_params),
    ("lambda_no_params", "# 😀 🥩 🐖const🐖 @ 🥩 ** ** 🥩 42 🥩 #\n# ... 0 ... #", assert_lambda_with_no_params),
    ("lambda_with_arithmetic_body", "# 😀 🥩 🐖calc🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 💞 2 ❤️ 1 🥩 #\n# ... 0 ... #", assert_lambda_body_is_binary_op),
    ("lambda_with_comparison_body", "# 😀 🥩 🐖check🐖 @ 🥩 ** 🐷 🐖n🐖 ** 🥩 🐖n🐖 > 0 🥩 #\n# ... 0 ... #", assert_lambda_body_is_comparison),
    ("lambda_with_not_body", "# 😀 🥩 🐖negate🐖 @ 🥩 ** wow 🐖b🐖 ** 🥩 💩 🐖b🐖 🥩 #\n# ... 0 ... #", assert_lambda_body_is_unary),
    ("lambda_constant_body", "# 😀 🥩 🐖getConst🐖 @ 🥩 ** ** 🥩 100 🥩 #\n# ... 0 ... #", assert_lambda_body_is_number),
    ("lambda_with_i16_type", "# 😀 🥩 🐖small🐖 @ 🥩 ** 🐽 🐖n🐖 ** 🥩 🐖n🐖 ❤️ 1 🥩 #\n# ... 0 ... #", assert_lambda_with_i16_param),
    ("lambda_with_bool_type", "# 😀 🥩 🐖toggle🐖 @ 🥩 ** wow 🐖flag🐖 ** 🥩 💩 🐖flag🐖 🥩 #\n# ... 0 ... #", assert_lambda_with_bool_param),
    ("lambda_with_mixed_param_types", "# 😀 🥩 🐖combine🐖 @ 🥩 ** 🐽 🐖a🐖 ** ** 🐷 🐖b🐖 ** 🥩 🐖a🐖 ❤️ 🐖b🐖 🥩 #\n# ... 0 ... #", assert_lambda_with_mixed_types),
    ("lambda_called_in_return", "# 😀 🥩 🐖square🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 💞 🐖x🐖 🥩 #\n# ... 🐖square🐖 ** 5 ** ... #", assert_lambda_call_in_return),
]

for name, source, func in all_tests:
    SyntaxParserHappyTest.add_test_case(name, source, func)

if __name__ == "__main__":
    unittest.main(verbosity=2)