#!/usr/bin/env python3
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler.node.intr_string_node import InterpolatedStringNode
from compiler.syntax_parser.syntax_parser import SyntaxParser
from compiler.lexer.lexer import Lexer
from compiler.node.program_node import ProgramNode
from compiler.node.decl_node import DeclNode
from compiler.node.assign_node import AssignNode
from compiler.node.if_node import IfNode
from compiler.node.while_node import WhileNode
from compiler.node.function_call_node import FunctionCallNode
from compiler.node.read_node import ReadNode
from compiler.node.print_node import PrintNode
from compiler.node.string_node import StringNode
from compiler.node.member_access_node import MemberAccessNode
from compiler.llvm_specifics.data_type import DataType

def parse_code(source: str) -> ProgramNode:
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = SyntaxParser(tokens)
    return parser.parse_program()

class TestSyntaxParserHappyPath(unittest.TestCase):
    test_cases = []

    @classmethod
    def add_test_case(cls, name, source, assertion_func):
        cls.test_cases.append((name, source, assertion_func))

    def test_all_cases(self):
        results = []
        for name, source, assertion in self.test_cases:
            try:
                with self.subTest(name=name):
                    ast = parse_code(source)
                    assertion(self, ast)
                results.append((name, "PASS"))
            except AssertionError as e:
                results.append((name, f"FAIL ({e})"))
            except Exception as e:
                results.append((name, f"ERROR ({type(e).__name__}: {e})"))

        print("\nSyntax Parser Test Summary:")
        for test_name, status in results:
            print(f"{test_name}: {status}")

        failures = [s for _, s in results if s.startswith("FAIL") or s.startswith("ERROR")]
        if failures:
            self.fail(f"{len(failures)} tests failed or errored. See summary above.")


def assert_simple_declaration(self, ast):
    self.assertEqual(len(ast.statement_nodes), 1)
    decl = ast.statement_nodes[0]
    self.assertIsInstance(decl, DeclNode)
    self.assertEqual(decl.variable, "x")

def assert_assignment(self, ast):
    self.assertEqual(len(ast.statement_nodes), 2)
    assign = ast.statement_nodes[1]
    self.assertIsInstance(assign, AssignNode)

def assert_if_statement(self, ast):
    if_stmt = ast.statement_nodes[1]
    self.assertIsInstance(if_stmt, IfNode)

def assert_while_loop(self, ast):
    while_stmt = ast.statement_nodes[1]
    self.assertIsInstance(while_stmt, WhileNode)

def assert_function_declaration(self, ast):
    self.assertEqual(len(ast.function_declarations), 1)
    func = ast.function_declarations[0]
    self.assertEqual(func.variable, "add")

def assert_function_parameters(self, ast):
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
    member_access = decl.expr_node
    self.assertTrue(isinstance(member_access, MemberAccessNode) or isinstance(member_access, FunctionCallNode))

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
    result = decl.expr_node
    self.assertTrue(isinstance(result, MemberAccessNode) or isinstance(result, FunctionCallNode))

def assert_print_string(self, ast):
    print_stmt = ast.statement_nodes[0]
    self.assertIsInstance(print_stmt, PrintNode)
    self.assertIsInstance(print_stmt.expr_node, StringNode)
    self.assertEqual(print_stmt.expr_node.value, "Hello World")

def assert_print_string_with_escapes(self, ast):
    print_stmt = ast.statement_nodes[0]
    self.assertIsInstance(print_stmt, PrintNode)
    self.assertIsInstance(print_stmt.expr_node, StringNode)
    self.assertTrue("\n" in print_stmt.expr_node.value or "\t" in print_stmt.expr_node.value)

def assert_multiple_print_strings(self, ast):
    self.assertGreaterEqual(len(ast.statement_nodes), 2)
    print_stmt1 = ast.statement_nodes[0]
    print_stmt2 = ast.statement_nodes[1]
    self.assertIsInstance(print_stmt1, PrintNode)
    self.assertIsInstance(print_stmt2, PrintNode)
    self.assertIsInstance(print_stmt1.expr_node, StringNode)
    self.assertIsInstance(print_stmt2.expr_node, StringNode)

def assert_print_empty_string(self, ast):
    print_stmt = ast.statement_nodes[0]
    self.assertIsInstance(print_stmt, PrintNode)
    self.assertIsInstance(print_stmt.expr_node, StringNode)
    self.assertEqual(print_stmt.expr_node.value, "")

def assert_print_number_then_string(self, ast):
    self.assertGreaterEqual(len(ast.statement_nodes), 2)
    print_num = ast.statement_nodes[0]
    print_str = ast.statement_nodes[1]
    self.assertIsInstance(print_num, PrintNode)
    self.assertIsInstance(print_str, PrintNode)
    self.assertIsInstance(print_str.expr_node, StringNode)

def assert_read_then_print_string(self, ast):
    self.assertGreaterEqual(len(ast.statement_nodes), 3)
    read_stmt = ast.statement_nodes[1]
    print_stmt = ast.statement_nodes[2]
    self.assertIsInstance(read_stmt, ReadNode)
    self.assertIsInstance(print_stmt, PrintNode)
    self.assertIsInstance(print_stmt.expr_node, StringNode)

def assert_interpolated_string_simple(self, ast):
    print_stmt = ast.statement_nodes[0]
    self.assertIsInstance(print_stmt, PrintNode)
    self.assertIsInstance(print_stmt.expr_node, InterpolatedStringNode)
    self.assertEqual(len(print_stmt.expr_node.parts), 3)

def assert_interpolated_string_number(self, ast):
    print_stmt = ast.statement_nodes[0]
    self.assertIsInstance(print_stmt, PrintNode)
    self.assertIsInstance(print_stmt.expr_node, InterpolatedStringNode)
    self.assertGreaterEqual(len(print_stmt.expr_node.parts), 2)

def assert_interpolated_string_variable(self, ast):
    print_stmt = ast.statement_nodes[1]
    self.assertIsInstance(print_stmt, PrintNode)
    self.assertIsInstance(print_stmt.expr_node, InterpolatedStringNode)

def assert_interpolated_string_expression(self, ast):
    print_stmt = ast.statement_nodes[0]
    self.assertIsInstance(print_stmt, PrintNode)
    self.assertIsInstance(print_stmt.expr_node, InterpolatedStringNode)

def assert_interpolated_string_multiple(self, ast):
    print_stmt = ast.statement_nodes[1]
    self.assertIsInstance(print_stmt, PrintNode)
    interp = print_stmt.expr_node
    self.assertIsInstance(interp, InterpolatedStringNode)
    self.assertGreaterEqual(len(interp.parts), 3)

def assert_interpolated_string_with_escapes(self, ast):
    print_stmt = ast.statement_nodes[0]
    self.assertIsInstance(print_stmt, PrintNode)
    self.assertIsInstance(print_stmt.expr_node, InterpolatedStringNode)

def assert_interpolated_string_nested_bracket(self, ast):
    print_stmt = ast.statement_nodes[1]
    self.assertIsInstance(print_stmt, PrintNode)
    self.assertIsInstance(print_stmt.expr_node, InterpolatedStringNode)

def assert_interpolated_only_expr(self, ast):
    print_stmt = ast.statement_nodes[0]
    self.assertIsInstance(print_stmt, PrintNode)
    self.assertIsInstance(print_stmt.expr_node, InterpolatedStringNode)

def assert_interpolated_bool_expression(self, ast):
    print_stmt = ast.statement_nodes[1]
    self.assertIsInstance(print_stmt, PrintNode)
    self.assertIsInstance(print_stmt.expr_node, InterpolatedStringNode)


test_cases = [
    ("simple_declaration", "# 😀 🐷 🐖x🐖 @ 10 #\n# ... 🐖x🐖 ... #", assert_simple_declaration),
    ("assignment", "# 😀 🐷 🐖x🐖 @ 10 #\n# 🐖x🐖 @ 20 #\n# ... 🐖x🐖 ... #", assert_assignment),
    ("if_statement", "# 😀 🐷 🐖x🐖 @ 10 #\n# SAVE 🐖x🐖 > 5 #\n# 🐖🐖🐖 #\n# 🐖x🐖 @ 20 #\n# 🐖🐖🐖 #\n# ... 🐖x🐖 ... #", assert_if_statement),
    ("while_loop", "# 😀 🐷 🐖counter🐖 @ 0 #\n# OINK 🐖counter🐖 < 5 #\n# 🐖🐖🐖 #\n# 🐖counter🐖 @ 🐖counter🐖 ❤️ 1 #\n# 🐖🐖🐖 #\n# ... 🐖counter🐖 ... #", assert_while_loop),
    ("function_declaration", "# 🐷 PIG 🐖add🐖 ** 🐷 🐖a🐖 ** ** 🐷 🐖b🐖 ** #\n# 🐖🐖🐖 #\n# ... 🐖a🐖 ❤️ 🐖b🐖 ... #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_function_declaration),
    ("function_parameters", "# 🐷 PIG 🐖add🐖 ** 🐷 🐖a🐖 ** ** 🐷 🐖b🐖 ** #\n# 🐖🐖🐖 #\n# ... 🐖a🐖 ❤️ 🐖b🐖 ... #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_function_parameters),
    ("function_return_type", "# 🐷 PIG 🐖test🐖 #\n# 🐖🐖🐖 #\n# ... 42 ... #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_function_return_type),
    ("struct_with_member_function", "# BOAR 🐖Point🐖 #\n# 🐖🐖🐖 #\n# 😀 🐷 🐖x🐖 #\n# 🐷 PIGLET 🐖getX🐖 #\n# 🐖🐖🐖 #\n# ... 🐖x🐖 ... #\n# 🐖🐖🐖 #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_struct_with_member_function),
    ("void_function", "# 😑 PIG 🐖doNothing🐖 #\n# 🐖🐖🐖 #\n# ... #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_void_function),
    ("struct_field_types", "# BOAR 🐖Point🐖 #\n# 🐖🐖🐖 #\n# 😀 🐷 🐖x🐖 #\n# 😀 🐷 🐖y🐖 #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_struct_field_types),
    ("function_with_struct_param", "# BOAR 🐖Point🐖 #\n# 🐖🐖🐖 #\n# 😀 🐷 🐖x🐖 #\n# 🐖🐖🐖 #\n# 🐷 PIG 🐖test🐖 ** 🐖Point🐖 🐖p🐖 ** #\n# 🐖🐖🐖 #\n# ... 0 ... #\n# 🐖🐖🐖 #\n# ... 0 ... #", assert_function_with_struct_param),
    ("struct_member_function_call", "# BOAR 🐖Counter🐖 #\n# 🐖🐖🐖 #\n# 😀 🐷 🐖val🐖 #\n# 🐷 PIGLET 🐖getValue🐖 #\n# 🐖🐖🐖 #\n# ... 🐖val🐖 ... #\n# 🐖🐖🐖 #\n# 🐖🐖🐖 #\n# 😀 🐖Counter🐖 🐖c🐖 @ 🐖Counter🐖 ** 5 ** #\n# 😀 🐷 🐖result🐖 @ 🐖c🐖 _ 🐖getValue🐖 #\n# ... 🐖result🐖 ... #", assert_struct_member_function_call),
    ("read_i32", "# 😀 🐷 🐖x🐖 #\n# eat😋 🐖x🐖 #\n# ... 🐖x🐖 ... #", assert_read_i32),
    ("print_expression", "# 😀 🐷 🐖x🐖 @ 10 #\n# print🤮 🐖x🐖 #\n# ... 0 ... #", assert_print_expression),
    ("chained_function_calls", "# 😀 🐷 🐖result🐖 @ 🐖getValue🐖 _ 🐖double🐖 #\n# ... 🐖result🐖 ... #", assert_chained_function_calls),
    ("print_string", "# print🤮 🥓Hello World🥓 #\n# ... 0 ... #", assert_print_string),
    ("print_string_with_escapes", "# print🤮 🥓Line1\\nLine2\\tTab🥓 #\n# ... 0 ... #", assert_print_string_with_escapes),
    ("multiple_print_strings", "# print🤮 🥓First🥓 #\n# print🤮 🥓Second🥓 #\n# ... 0 ... #", assert_multiple_print_strings),
    ("print_empty_string", "# print🤮 🥓🥓 #\n# ... 0 ... #", assert_print_empty_string),
    ("print_number_then_string", "# print🤮 42 #\n# print🤮 🥓Result🥓 #\n# ... 0 ... #", assert_print_number_then_string),
    ("read_then_print_string", "# 😀 🐷 🐖x🐖 #\n# eat😋 🐖x🐖 #\n# print🤮 🥓You entered:🥓 #\n# ... 0 ... #", assert_read_then_print_string),
    ("interpolated_string_simple", "# print🤮 🥓result: 🍗42🍗🥓 #\n# ... 0 ... #", assert_interpolated_string_simple),
    ("interpolated_string_number", "# print🤮 🥓value: 🍗100🍗🥓 #\n# ... 0 ... #", assert_interpolated_string_number),
    ("interpolated_string_variable", "# 😀 🐷 🐖x🐖 @ 10 #\n# print🤮 🥓x = 🍗🐖x🐖🍗🥓 #\n# ... 0 ... #", assert_interpolated_string_variable),
    ("interpolated_string_expression", "# print🤮 🥓sum: 🍗5❤️3🍗🥓 #\n# ... 0 ... #", assert_interpolated_string_expression),
    ("interpolated_string_multiple", "# 😀 🐷 🐖a🐖 @ 5 #\n# print🤮 🥓a=🍗🐖a🐖🍗 b=🍗10🍗🥓 #\n# ... 0 ... #", assert_interpolated_string_multiple),
    ("interpolated_string_with_escapes", "# print🤮 🥓Line1\\n🍗42🍗\\tEnd🥓 #\n# ... 0 ... #", assert_interpolated_string_with_escapes),
    ("interpolated_bool_expression", "# 😀 wow 🐖flag🐖 @ LOVE #\n# print🤮 🥓flag: 🍗🐖flag🐖🍗🥓 #\n# ... 0 ... #", assert_interpolated_bool_expression),
]

for name, code, func in test_cases:
    TestSyntaxParserHappyPath.add_test_case(name, code, func)


if __name__ == "__main__":
    unittest.main(verbosity=2)