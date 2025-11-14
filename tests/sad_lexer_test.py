#!/usr/bin/env python3
import unittest
import sys
import os
from happy_lexer_test import get_lexemes

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler.token.token_type import TokenType
from sad_syntax_parser_test import ExceptionCheckingTestCase

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
        ("invalid_assignment", "# 🐖x🐖 = 10 #\n"),
        ("unclosed_multiline_comment", "👀👀👀\nThis comment never ends\n# 😀 🐷 🐖x🐖 @ 10 #\n"),
        ("standalone_ampersand", "# 😀 🐷 🐖x🐖 @ 10 & 5 #\n"),
        ("invalid_bracket", "# 🐖x🐖 @ ( 🐖a🐖 ❤️ 🐖b🐖 ) #\n"),
        ("invalid_mutability_marker", "# 🎉 🐷 🐖x🐖 @ 10 #\n"),
    ]

    def test_all_failing_cases(self):
        for name, code in self.failing_cases:
            with self.subTest(name=name):
                if name == "unclosed_multiline_comment":
                    lexems = get_lexemes(code)
                    var_tokens = [t for t in lexems if t.token_type == TokenType.VARIABLE]
                    self.assertEqual(len(var_tokens), 0)                
                else:
                    with self.assertRaises(ValueError) as self.context:
                        get_lexemes(code)


if __name__ == '__main__':
    unittest.main(verbosity=2)
