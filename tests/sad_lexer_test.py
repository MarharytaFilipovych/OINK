#!/usr/bin/env python3
import unittest
import sys
import os
from happy_lexer_test import get_lexemes

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler.token.token_type import TokenType

class ExceptionCheckingTestCase(unittest.TestCase):
    def tearDown(self):
        if hasattr(self, "context") and getattr(self.context, "exception", None):
            self.assertTrue(self.context.exception)

class TestLexerFailingCases(ExceptionCheckingTestCase):
    failing_cases = [
        ("invalid_character", "# 😀 🐷 🐖x🐖 @ 10 $ #\n"),
        ("invalid_unicode_emoji", "# 😀 🐷 🐖x🐖 @ 10 🎉 #\n"),
        ("number_with_letters", "# 😀 🐷 🐖x🐖 @ 12a34 #\n"),
        ("number_with_multiple_minus", "# 😀 🐷 🐖x🐖 @ --10 #\n"),
        ("number_with_decimal", "# 😀 🐷 🐖x🐖 @ 12.5 #\n"),
        ("variable_starting_with_number", "# 😀 🐷 🐖123abc🐖 @ 10 #\n"),
        ("variable_with_invalid_char", "# 😀 🐷 🐖my$var🐖 @ 10 #\n"),
        ("invalid_operator", "# 🐖x🐖 @ 🐖a🐖 + 🐖b🐖 #\n"),
        ("invalid_mutability_marker", "# 🎉 🐷 🐖x🐖 @ 10 #\n"),
        ("unclosed_multiline_comment", "👀👀👀\nThis comment never ends\n# 😀 🐷 🐖x🐖 @ 10 #\n"),
        ("standalone_ampersand", "# 😀 🐷 🐖x🐖 @ 10 & 5 #\n"),
        ("invalid_bracket", "# 🐖x🐖 @ ( 🐖a🐖 ❤️ 🐖b🐖 ) #\n"),
        ("invalid_void_emoji", "# 😊 PIG 🐖test🐖 #\n"),
         ("invalid_variable_start_symbol", "# 😀 🐷 🐖1x🐖 @ 10 #"),
        ("variable_with_dash", "# 😀 🐷 🐖my-var🐖 @ 10 #"),
        ("unknown_operator", "# 😀 🐷 🐖x🐖 @ 10 ✨ 5 #"),

    ]

    def test_all_failing_cases(self):
        results = []
        for name, code in self.failing_cases:
            try:
                if name == "unclosed_multiline_comment":
                    lexems = get_lexemes(code)
                    var_tokens = [t for t in lexems if t.token_type == TokenType.VARIABLE]
                    if len(var_tokens) == 0:
                        results.append((name, "PASS"))
                    else:
                        results.append((name, "FAIL"))
                else:
                    with self.assertRaises(ValueError):
                        get_lexemes(code)
                    results.append((name, "PASS"))
            except Exception as e:
                results.append((name, f"FAIL ({type(e).__name__}: {e})"))

        print("\nFailing Lexer Test Summary:")
        for test_name, status in results:
            print(f"{test_name}: {status}")

        unexpected_failures = [s for _, s in results if s.startswith("FAIL")]
        if unexpected_failures:
            self.fail(f"{len(unexpected_failures)} failing tests did not behave as expected: {unexpected_failures}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
