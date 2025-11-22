#!/usr/bin/env python3
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler.syntax_parser.syntax_parser import SyntaxParser
from compiler.lexer.lexer import Lexer
from compiler.node.program_node import ProgramNode

def parse_code(source: str) -> ProgramNode:
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = SyntaxParser(tokens)
    return parser.parse_program()

class ExceptionCheckingTestCase(unittest.TestCase):
    def tearDown(self):
        if hasattr(self, "context") and getattr(self.context, "exception", None):
            self.assertTrue(self.context.exception)

class SyntaxParserSadTest(ExceptionCheckingTestCase):

    failing_cases = [
        ("missing_variable_border", "# 😀 🐷 x @ 10 #\n# ... 🐖x🐖 ... #"),
        ("missing_assignment_operator", "# 😀 🐷 🐖x🐖 10 #\n# ... 🐖x🐖 ... #"),
        ("missing_line_border", "😀 🐷 🐖x🐖 @ 10\n# ... 🐖x🐖 ... #"),
        ("missing_newline_between_statements", "# 😀 🐷 🐖x🐖 @ 10 # # 😀 🐷 🐖y🐖 @ 20 #\n# ... 🐖x🐖 ... #"),
        ("empty_program", "# ... 42 ... #"),
        ("missing_return_statement", "# 😀 🐷 🐖x🐖 @ 10 #"),
        ("code_after_return", "# 😀 🐷 🐖x🐖 @ 10 #\n# ... 🐖x🐖 ... #\n# 🐖x🐖 @ 20 #"),
        ("malformed_number", "# 😀 🐷 🐖x🐖 @ 12.5 #\n# ... 🐖x🐖 ... #"),
        ("unmatched_bracket", "# 😀 🐷 🐖x🐖 @ ** 10 ❤️ 5 #\n# ... 🐖x🐖 ... #"),
        ("missing_block_delimiter",
         """# 😀 🐷 🐖x🐖 @ 10 #
# SAVE 🐖x🐖 > 5 #
# 🐖x🐖 @ 20 #
# ... 🐖x🐖 ... #"""),
        ("if_without_condition",
         """# 😀 🐷 🐖x🐖 @ 10 #
# SAVE #
# 🐖🐖🐖 #
# 🐖x🐖 @ 20 #
# 🐖🐖🐖 #
# ... 🐖x🐖 ... #"""),
        ("while_without_condition",
         """# 😀 🐷 🐖counter🐖 @ 0 #
# OINK #
# 🐖🐖🐖 #
# 🐖counter🐖 @ 🐖counter🐖 ❤️ 1 #
# 🐖🐖🐖 #
# ... 🐖counter🐖 ... #"""),
        ("mismatched_mood_line_borders", "#~ 😀 🐷 🐖x🐖 @ 10 #\n# ... 🐖x🐖 ... #"),
        ("invalid_variable_name_characters", "# 😀 🐷 🐖x123🐖 @ 10 #\n# ... 🐖x123🐖 ... #"),
        ("missing_mutability_specifier", "# 🐷 🐖x🐖 @ 10 #\n# ... 🐖x🐖 ... #"),
        ("missing_type_specifier", "# 😀 🐖x🐖 @ 10 #\n# ... 🐖x🐖 ... #"),
        ("elif_without_if",
         """# 😀 🐷 🐖x🐖 @ 10 #
# HURT 🐖x🐖 > 5 #
# 🐖🐖🐖 #
# 🐖x🐖 @ 20 #
# 🐖🐖🐖 #
# ... 🐖x🐖 ... #"""),
        ("else_without_if",
         """# 😀 🐷 🐖x🐖 @ 10 #
# KILL #
# 🐖🐖🐖 #
# 🐖x🐖 @ 20 #
# 🐖🐖🐖 #
# ... 🐖x🐖 ... #"""),
        ("incomplete_expression", "# 😀 🐷 🐖x🐖 @ 10 ❤️ #\n# ... 🐖x🐖 ... #"),
        ("struct_without_name",
         """# BOAR #
# 🐖🐖🐖 #
# 😀 🐷 🐖x🐖 #
# 🐖🐖🐖 #
# ... 0 ... #"""),
        ("struct_without_closing_block",
         """# BOAR 🐖Point🐖 #
# 🐖🐖🐖 #
# 😀 🐷 🐖x🐖 #
# ... 0 ... #"""),
        ("function_without_name",
         """# 🐷 PIG #
# 🐖🐖🐖 #
# ... 0 ... #
# 🐖🐖🐖 #
# ... 0 ... #"""),
        ("function_without_return_type",
         """# PIG 🐖test🐖 #
# 🐖🐖🐖 #
# ... 0 ... #
# 🐖🐖🐖 #
# ... 0 ... #"""),
        ("function_without_return_statement",
         """# 🐷 PIG 🐖test🐖 #
# 🐖🐖🐖 #
# 😀 🐷 🐖x🐖 @ 10 #
# 🐖🐖🐖 #
# ... 0 ... #"""),
        ("member_function_outside_struct",
         """# 🐷 PIGLET 🐖test🐖 #
# 🐖🐖🐖 #
# ... 0 ... #
# 🐖🐖🐖 #
# ... 0 ... #"""),
        ("duplicate_struct_name",
         """# BOAR 🐖Point🐖 #
# 🐖🐖🐖 #
# 😀 🐷 🐖x🐖 #
# 🐖🐖🐖 #
# BOAR 🐖Point🐖 #
# 🐖🐖🐖 #
# 😀 🐷 🐖y🐖 #
# 🐖🐖🐖 #
# ... 0 ... #"""),
        ("function_param_without_type",
         """# 🐷 PIG 🐖test🐖 ** 🐖x🐖 ** #
# 🐖🐖🐖 #
# ... 0 ... #
# 🐖🐖🐖 #
# ... 0 ... #"""),
 ("mood_line_without_end", "#~ 🐖x🐖 @ 10 ❤️ 5 #"),  
    ("if_without_block", "# SAVE 🐖x🐖 > 0 #"),  
    ("elif_without_if_block", "# HURT 🐖x🐖 > 0 #\n# 🐖🐖🐖 #"),  
    ("else_without_if_block", "# KILL #\n# 🐖🐖🐖 #"),  
    ("function_without_body", "# 🐷 PIG 🐖doSomething🐖 ** 🐷 🐖x🐖 ** #"),  
    ("struct_with_duplicate_field", "# BOAR 🐖Point🐖 #\n# 🐖🐖🐖 #\n# 😀 🐷 🐖x🐖 #\n# 😀 🐷 🐖x🐖 #\n# 🐖🐖🐖 #"),  
    ("function_call_without_arguments", "# 😀 🐷 🐖res🐖 @ 🐖add🐖 ** ** #"),  
    ("function_call_with_wrong_chain", "# 😀 🐷 🐖res🐖 @ 🐖get🐖 _ #"),  
    ("variable_shadowing_in_scope", "# 😀 🐷 🐖x🐖 @ 1 #\n# 😀 🐷 🐖x🐖 @ 2 #"),  
    ("reassign_constant", "# 😭 🐷 🐖c🐖 @ 5 #\n# 🐖c🐖 @ 10 #"),  
    ("struct_member_access_invalid", "# 😀 🐷 🐖res🐖 @ 🐖p🐖 _ 🐖nonExistent🐖 #"),  
    ("mismatched_function_param_types", "# 🐷 PIG 🐖add🐖 ** 🐽 🐖a🐖 ** ** 🐷 🐖b🐖 ** #\n# 🐖🐖🐖 #\n# ... 🐖a🐖 ❤️ 🐖b🐖 ... #\n# 🐖🐖🐖 #"),
    ("lambda_missing_meat_start", "# 😀 🥩 🐖f🐖 @ ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 🥩 #\n# ... 0 ... #"),
    ("lambda_missing_meat_middle", "# 😀 🥩 🐖f🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🐖x🐖 🥩 #\n# ... 0 ... #"),
    ("lambda_missing_meat_end", "# 😀 🥩 🐖f🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 #\n# ... 0 ... #"),
    ("lambda_missing_param_type", "# 😀 🥩 🐖f🐖 @ 🥩 ** 🐖x🐖 ** 🥩 🐖x🐖 🥩 #\n# ... 0 ... #"),
    ("lambda_missing_param_name", "# 😀 🥩 🐖f🐖 @ 🥩 ** 🐷 ** 🥩 🐖x🐖 🥩 #\n# ... 0 ... #"),
    ("lambda_missing_param_brackets", "# 😀 🥩 🐖f🐖 @ 🥩 🐷 🐖x🐖 🥩 🐖x🐖 🥩 #\n# ... 0 ... #"),
    ("lambda_with_statement_in_body", "# 😀 🥩 🐖f🐖 @ 🥩 ** ** 🥩 # SAVE 1 # 🥩 #\n# ... 0 ... #"),
    ("lambda_without_body", "# 😀 🥩 🐖f🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🥩 #\n# ... 0 ... #"),
    ("lambda_param_missing_border", "# 😀 🥩 🐖f🐖 @ 🥩 ** 🐷 x ** 🥩 🐖x🐖 🥩 #\n# ... 0 ... #"),
    ("lambda_type_as_param", "# 😀 🥩 🐖f🐖 @ 🥩 ** 🥩 🐖g🐖 ** 🥩 1 🥩 #\n# ... 1 ... #"),
    ("lambda_uninitialized_declaration", "# 😀 🥩 🐖f🐖 #\n# ... 1 ... #"),
    ("lambda_missing_variable_border", "# 😀 🥩 🐖f🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 x 🥩 #\n# ... 0 ... #"),
    ("lambda_extra_meat_emoji", "# 😀 🥩 🐖f🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 🥩 🥩 #\n# ... 0 ... #"),
    ("lambda_wrong_bracket_type", "# 😀 🥩 🐖f🐖 @ 🥩 ( 🐷 🐖x🐖 ) 🥩 🐖x🐖 🥩 #\n# ... 0 ... #"),
    ("lambda_with_unclosed_param_bracket", "# 😀 🥩 🐖f🐖 @ 🥩 ** 🐷 🐖x🐖 🥩 🐖x🐖 🥩 #\n# ... 0 ... #"),
    ]

    def test_all_failing_cases(self):
        results = []
        for name, source in self.failing_cases:
            try:
                with self.assertRaises(ValueError):
                    parse_code(source)
                results.append((name, "PASS"))
            except Exception as e:
                results.append((name, f"FAIL ({type(e).__name__}: {e})"))

        print("\nSyntax Parser Sad Test Summary:")
        for test_name, status in results:
            print(f"{test_name}: {status}")

        failures = [s for _, s in results if s.startswith("FAIL")]
        if failures:
            self.fail(f"{len(failures)} tests did not raise expected exceptions: {failures}")

if __name__ == '__main__':
    unittest.main(verbosity=2)