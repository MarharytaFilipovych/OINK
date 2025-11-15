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
            self.assertTrue(self.context.exception, "Expected exception missing!")


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
         """# 🐷 PIG 🐖add🐖 ** 🐖a🐖 ** #
# 🐖🐖🐖 #
# ... 🐖a🐖 ... #
# 🐖🐖🐖 #
# ... 0 ... #"""),
        ("mismatched_function_brackets",
         """# 🐷 PIG 🐖add🐖 ** 🐷 🐖a🐖 #
# 🐖🐖🐖 #
# ... 🐖a🐖 ... #
# 🐖🐖🐖 #
# ... 0 ... #"""),
("struct_field_without_type",
         """# BOAR 🐖Point🐖 #
# 🐖🐖🐖 #
# 😀 🐖x🐖 #
# 🐖🐖🐖 #
# ... 0 ... #"""),
        ("function_param_without_type",
         """# 🐷 PIG 🐖test🐖 ** 🐖x🐖 ** #
# 🐖🐖🐖 #
# ... 0 ... #
# 🐖🐖🐖 #
# ... 0 ... #"""),
        ("member_function_without_return",
         """# BOAR 🐖Point🐖 #
# 🐖🐖🐖 #
# 😀 🐷 🐖x🐖 #
# 🐷 PIGLET 🐖getX🐖 #
# 🐖🐖🐖 #
# 🐖🐖🐖 #
# 🐖🐖🐖 #
# ... 0 ... #"""),
        ("read_without_variable",
         """# eat😋 #
# ... 0 ... #"""),
        ("print_without_expression",
         """# print🤮 #
# ... 0 ... #""")
    ]

    def test_all_failing_cases(self):
        for name, source in self.failing_cases:
            with self.subTest(name=name):
                with self.assertRaises(ValueError) as self.context:
                    parse_code(source)


if __name__ == '__main__':
    unittest.main(verbosity=2)
