#!/usr/bin/env python3
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler.lexer.lexer import Lexer
from compiler.syntax_parser.syntax_parser import SyntaxParser
from compiler.visitor.semantic_analyzer.semantic_analyzer import SemanticAnalyzer
from compiler.optimizer.optimizer import Optimizer


class OptimizationTests(unittest.TestCase):
    test_cases = []

    @classmethod
    def add_test_case(cls, name, code, assertion_func):
        cls.test_cases.append((name, code, assertion_func))

    def test_all_cases(self):
        results = []
        for name, code, assertion in self.test_cases:
            try:
                with self.subTest(name=name):
                    lexer = Lexer(code)
                    tokens = lexer.tokenize()
                    parser = SyntaxParser(tokens)
                    ast = parser.parse_program()
                    semantic_analyzer = SemanticAnalyzer()
                    ast.accept(semantic_analyzer)
                    
                    optimizer = Optimizer()
                    stats = optimizer.optimize(ast)
                    
                    assertion(self, ast, stats)
                results.append((name, "PASS"))
            except AssertionError as e:
                results.append((name, f"FAIL ({e})"))
            except Exception as e:
                results.append((name, f"ERROR ({type(e).__name__}: {e})"))

        print("\nOptimization Test Summary:")
        for test_name, status in results:
            print(f"{test_name}: {status}")

        failures = [s for _, s in results if s.startswith("FAIL") or s.startswith("ERROR")]
        if failures:
            self.fail(f"{len(failures)} tests failed. See summary above.")


def assert_unused_variable_removal(self, ast, stats):
    self.assertEqual(stats['variables_removed'], 2)
    self.assertEqual(len(ast.statement_nodes), 2)

def assert_iterative_variable_removal(self, ast, stats):
    self.assertGreaterEqual(stats['variables_removed'], 3)
    self.assertEqual(len(ast.statement_nodes), 1)

def assert_function_inlining(self, ast, stats):
    self.assertEqual(stats['functions_inlined'], 1)
    self.assertEqual(len(ast.function_declarations), 0)

def assert_unused_function_removal(self, ast, stats):
    self.assertEqual(stats['functions_removed'], 1)
    self.assertEqual(len(ast.function_declarations), 1)

def assert_combined_optimizations(self, ast, stats):
    self.assertGreaterEqual(stats['variables_removed'], 1)
    self.assertEqual(stats['functions_inlined'], 1)
    self.assertEqual(stats['functions_removed'], 1)

def assert_variable_used_in_condition(self, ast, stats):
    self.assertEqual(stats['variables_removed'], 1)
    self.assertEqual(len(ast.statement_nodes), 2)

def assert_variable_used_in_loop(self, ast, stats):
    self.assertEqual(stats['variables_removed'], 1)

def assert_struct_field_usage(self, ast, stats):
    self.assertEqual(stats['variables_removed'], 1)

def assert_function_with_multiple_uses(self, ast, stats):
    self.assertEqual(stats['functions_inlined'], 0)
    self.assertEqual(stats['functions_removed'], 0)

def assert_function_with_void_return(self, ast, stats):
    self.assertEqual(stats['functions_inlined'], 0)

def assert_lambda_variable_not_removed(self, ast, stats):
    self.assertEqual(stats['variables_removed'], 0)

def assert_variable_used_in_struct_init(self, ast, stats):
    self.assertEqual(stats['variables_removed'], 1)

def assert_read_makes_variable_used(self, ast, stats):
    self.assertEqual(stats['variables_removed'], 0)

def assert_print_makes_variable_used(self, ast, stats):
    self.assertEqual(stats['variables_removed'], 0)


test_cases = [
    ("unused_variable_removal", 
     """# 😀 🐷 🐖used🐖 @ 10 #
# 😀 🐷 🐖unused&one🐖 @ 20 #
# 😀 🐷 🐖unused&two🐖 @ 30 #
# 😀 🐷 🐖result🐖 @ 🐖used🐖 ❤️ 5 #
# ... 🐖result🐖 ... #
""", assert_unused_variable_removal),
    
    ("iterative_variable_removal",
     """# 😀 🐷 🐖used🐖 @ 10 #
# 😀 🐷 🐖chain&one🐖 @ 🐖used🐖 ❤️ 5 #
# 😀 🐷 🐖chain&two🐖 @ 🐖chain&one🐖 💞 2 #
# 😀 🐷 🐖unused🐖 @ 🐖chain&two🐖 💔 1 #
# ... 🐖used🐖 ... #
""", assert_iterative_variable_removal),
    
    ("function_inlining",
     """# 🐷 PIG 🐖helper🐖 ** 🐷 🐖x🐖 ** #
# 🐖🐖🐖 #
# ... 🐖x🐖 💞 2 ... #
# 🐖🐖🐖 #
# 😀 🐷 🐖result🐖 @ 🐖helper🐖 ** 10 ** #
# ... 🐖result🐖 ... #
""", assert_function_inlining),
    
    ("unused_function_removal",
     """# 🐷 PIG 🐖used&func🐖 ** 🐷 🐖x🐖 ** #
# 🐖🐖🐖 #
# ... 🐖x🐖 ❤️ 1 ... #
# 🐖🐖🐖 #
# 🐷 PIG 🐖unused&func🐖 ** 🐷 🐖y🐖 ** #
# 🐖🐖🐖 #
# ... 🐖y🐖 💞 2 ... #
# 🐖🐖🐖 #
# 😀 🐷 🐖a🐖 @ 🐖used&func🐖 ** 5 ** #
# 😀 🐷 🐖b🐖 @ 🐖used&func🐖 ** 10 ** #
# ... 🐖a🐖 ❤️ 🐖b🐖 ... #
""", assert_unused_function_removal),
    
    ("combined_optimizations",
     """# 🐷 PIG 🐖single&use🐖 ** 🐷 🐖x🐖 ** #
# 🐖🐖🐖 #
# ... 🐖x🐖 💞 3 ... #
# 🐖🐖🐖 #
# 🐷 PIG 🐖never&used🐖 ** 🐷 🐖y🐖 ** #
# 🐖🐖🐖 #
# ... 🐖y🐖 💔 5 ... #
# 🐖🐖🐖 #
# 😀 🐷 🐖unused&var🐖 @ 100 #
# 😀 🐷 🐖result🐖 @ 🐖single&use🐖 ** 7 ** #
# ... 🐖result🐖 ... #
""", assert_combined_optimizations),

    ("variable_used_in_condition",
     """# 😀 🐷 🐖cond🐖 @ 10 #
# 😀 🐷 🐖unused🐖 @ 20 #
# SAVE 🐖cond🐖 > 5 #
# 🐖🐖🐖 #
# 😀 🐷 🐖x🐖 @ 1 #
# 🐖🐖🐖 #
# ... 0 ... #
""", assert_variable_used_in_condition),

    ("variable_used_in_loop",
     """# 😀 🐷 🐖counter🐖 @ 0 #
# 😀 🐷 🐖unused🐖 @ 50 #
# OINK 🐖counter🐖 < 5 #
# 🐖🐖🐖 #
# 🐖counter🐖 @ 🐖counter🐖 ❤️ 1 #
# 🐖🐖🐖 #
# ... 🐖counter🐖 ... #
""", assert_variable_used_in_loop),

    ("struct_field_usage",
     """# BOAR 🐖Point🐖 #
# 🐖🐖🐖 #
# 😀 🐷 🐖x🐖 #
# 🐖🐖🐖 #
# 😀 🐖Point🐖 🐖p🐖 @ 🐖Point🐖 ** 10 ** #
# 😀 🐷 🐖unused🐖 @ 100 #
# 😀 🐷 🐖val🐖 @ 🐖p🐖 _ 🐖x🐖 #
# ... 🐖val🐖 ... #
""", assert_struct_field_usage),

    ("function_multiple_uses_not_inlined",
     """# 🐷 PIG 🐖helper🐖 ** 🐷 🐖x🐖 ** #
# 🐖🐖🐖 #
# ... 🐖x🐖 ❤️ 1 ... #
# 🐖🐖🐖 #
# 😀 🐷 🐖a🐖 @ 🐖helper🐖 ** 5 ** #
# 😀 🐷 🐖b🐖 @ 🐖helper🐖 ** 10 ** #
# ... 🐖a🐖 ❤️ 🐖b🐖 ... #
""", assert_function_with_multiple_uses),

    ("void_function_not_inlined",
     """# 😑 PIG 🐖do&nothing🐖 #
# 🐖🐖🐖 #
# ... #
# 🐖🐖🐖 #
# 🐖do&nothing🐖 ** ** #
# ... 0 ... #
""", assert_function_with_void_return),

    ("lambda_variable_preserved",
     """# 😀 🥩 🐖square🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 💞 🐖x🐖 🥩 #
# 😀 🐷 🐖result🐖 @ 🐖square🐖 ** 5 ** #
# ... 🐖result🐖 ... #
""", assert_lambda_variable_not_removed),

    ("variable_used_in_struct_init",
     """# BOAR 🐖Point🐖 #
# 🐖🐖🐖 #
# 😀 🐷 🐖x🐖 #
# 🐖🐖🐖 #
# 😀 🐷 🐖val🐖 @ 10 #
# 😀 🐷 🐖unused🐖 @ 20 #
# 😀 🐖Point🐖 🐖p🐖 @ 🐖Point🐖 ** 🐖val🐖 ** #
# 😀 🐷 🐖result🐖 @ 🐖p🐖 _ 🐖x🐖 #
# ... 🐖result🐖 ... #
""", assert_variable_used_in_struct_init),

    ("read_makes_variable_used",
     """# 😀 🐷 🐖input🐖 #
# eat😋 🐖input🐖 #
# ... 🐖input🐖 ... #
""", assert_read_makes_variable_used),

    ("print_makes_variable_used",
     """# 😀 🐷 🐖output🐖 @ 42 #
# print🤮 🐖output🐖 #
# ... 0 ... #
""", assert_print_makes_variable_used),
]

for name, code, func in test_cases:
    OptimizationTests.add_test_case(name, code, func)


if __name__ == "__main__":
    unittest.main(verbosity=2)