#!/usr/bin/env python3
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler.lexer.lexer import Lexer
from compiler.token.token_type import TokenType

def get_lexemes(source: str):
    lexer = Lexer(source)
    return lexer.tokenize()


class TestLexerHappyPath(unittest.TestCase):

    test_cases = []

    @classmethod
    def add_test_case(cls, name, source, assertion_func):
        cls.test_cases.append((name, source, assertion_func))

    def test_all_cases(self):
        results = []
        for name, source, assertion in self.test_cases:
            try:
                with self.subTest(name=name):
                    lexemes = get_lexemes(source)
                    assertion(self, lexemes)
                results.append((name, "PASS"))
            except AssertionError as e:
                results.append((name, f"FAIL ({e})"))
            except Exception as e:
                results.append((name, f"ERROR ({type(e).__name__}: {e})"))

        print("\nTest Summary:")
        for test_name, status in results:
            print(f"{test_name}: {status}")

        failures = [s for _, s in results if s.startswith("FAIL") or s.startswith("ERROR")]
        if failures:
            self.fail(f"{len(failures)} tests failed or errored. See summary above.")


def assert_simple_declaration(self, lexemes):
    mut_token = [t for t in lexemes if t.token_type == TokenType.MUT][0]
    type_token = [t for t in lexemes if t.token_type == TokenType.I32_TYPE][0]
    var_token = [t for t in lexemes if t.token_type == TokenType.VARIABLE][0]

    self.assertEqual(mut_token.value, "😀")
    self.assertEqual(type_token.value, "🐷")
    self.assertEqual(var_token.value, "x")

def assert_arithmetic_operators(self, lexemes):
    plus_token = [t for t in lexemes if t.token_type == TokenType.PLUS][0]
    minus_token = [t for t in lexemes if t.token_type == TokenType.MINUS][0]
    mult_token = [t for t in lexemes if t.token_type == TokenType.MULTIPLY][0]
    div_token = [t for t in lexemes if t.token_type == TokenType.DIVIDE][0]

    self.assertEqual(plus_token.value, "❤️")
    self.assertEqual(minus_token.value, "💔")
    self.assertEqual(mult_token.value, "💞")
    self.assertEqual(div_token.value, "💕")

def assert_comparison_operators(self, lexemes):
    eq_token = [t for t in lexemes if t.token_type == TokenType.EQUALS][0]
    neq_token = [t for t in lexemes if t.token_type == TokenType.NOT_EQUALS][0]
    ge_token = [t for t in lexemes if t.token_type == TokenType.GREATER_EQUAL][0]
    le_token = [t for t in lexemes if t.token_type == TokenType.LESS_EQUAL][0]

    self.assertEqual(eq_token.value, "🌸🌸")
    self.assertEqual(neq_token.value, "💩🌸")
    self.assertEqual(ge_token.value, "🌸>")
    self.assertEqual(le_token.value, "🌸<")

def assert_logical_operators(self, lexemes):
    not_token = [t for t in lexemes if t.token_type == TokenType.NOT][0]
    and_token = [t for t in lexemes if t.token_type == TokenType.AND][0]
    or_token = [t for t in lexemes if t.token_type == TokenType.OR][0]

    self.assertEqual(not_token.value, "💩")
    self.assertEqual(and_token.value, "hru")
    self.assertEqual(or_token.value, "bruh")

def assert_boolean_literals(self, lexemes):
    true_token = [t for t in lexemes if t.token_type == TokenType.TRUE][0]
    false_token = [t for t in lexemes if t.token_type == TokenType.FALSE][0]

    self.assertEqual(true_token.value, "LOVE")
    self.assertEqual(false_token.value, "HATE")

def assert_control_flow_keywords(self, lexemes):
    if_token = [t for t in lexemes if t.token_type == TokenType.IF][0]
    elif_token = [t for t in lexemes if t.token_type == TokenType.ELIF][0]
    else_token = [t for t in lexemes if t.token_type == TokenType.ELSE][0]
    while_token = [t for t in lexemes if t.token_type == TokenType.WHILE][0]

    self.assertEqual(if_token.value, "SAVE")
    self.assertEqual(elif_token.value, "HURT")
    self.assertEqual(else_token.value, "KILL")
    self.assertEqual(while_token.value, "OINK")

def assert_block_delimiters(self, lexemes):
    block_tokens = [t for t in lexemes if t.token_type == TokenType.BLOCK_BORDER]
    self.assertEqual(len(block_tokens), 2)

def assert_mood_line_borders(self, lexemes):
    mood_start = [t for t in lexemes if t.token_type == TokenType.MOOD_LINE_BORDER_START][0]
    mood_end = [t for t in lexemes if t.token_type == TokenType.MOOD_LINE_BORDER_END][0]
    self.assertEqual(mood_start.value, "#~")
    self.assertEqual(mood_end.value, "~#")

def assert_return_statement(self, lexemes):
    return_tokens = [t for t in lexemes if t.token_type == TokenType.RETURN]
    self.assertEqual(len(return_tokens), 2)

def assert_all_data_types(self, lexemes):
    i16_token = [t for t in lexemes if t.token_type == TokenType.I16_TYPE][0]
    i32_token = [t for t in lexemes if t.token_type == TokenType.I32_TYPE][0]
    i64_token = [t for t in lexemes if t.token_type == TokenType.I64_TYPE][0]
    bool_token = [t for t in lexemes if t.token_type == TokenType.BOOL][0]

    self.assertEqual(i16_token.value, "🐽")
    self.assertEqual(i32_token.value, "🐷")
    self.assertEqual(i64_token.value, "🐗")
    self.assertEqual(bool_token.value, "wow")

def assert_brackets(self, lexemes):
    bracket_tokens = [t for t in lexemes if t.token_type == TokenType.BRACKET]
    self.assertEqual(len(bracket_tokens), 2)
    self.assertEqual(bracket_tokens[0].value, "**")
    self.assertEqual(bracket_tokens[1].value, "**")

def assert_single_line_comment(self, lexemes):
    var_token = [t for t in lexemes if t.token_type == TokenType.VARIABLE][0]
    self.assertEqual(var_token.value, "x")

def assert_multiline_comment(self, lexemes):
    var_token = [t for t in lexemes if t.token_type == TokenType.VARIABLE][0]
    self.assertEqual(var_token.value, "x")

def assert_struct_keyword(self, lexemes):
    struct_token = [t for t in lexemes if t.token_type == TokenType.STRUCT][0]
    self.assertEqual(struct_token.value, "BOAR")

def assert_function_keyword(self, lexemes):
    func_token = [t for t in lexemes if t.token_type == TokenType.FUNCTION][0]
    self.assertEqual(func_token.value, "PIG")

def assert_member_function_keyword(self, lexemes):
    mem_func_token = [t for t in lexemes if t.token_type == TokenType.MEMBER_FUNCTION][0]
    self.assertEqual(mem_func_token.value, "PIGLET")

def assert_lambda_keyword(self, lexemes):
    lambda_tokens = [t for t in lexemes if t.token_type == TokenType.LAMBDA]
    self.assertGreaterEqual(len(lambda_tokens), 3)

def assert_member_access(self, lexemes):
    member_access_token = [t for t in lexemes if t.token_type == TokenType.MEMBER_ACCESS][0]
    self.assertEqual(member_access_token.value, "_")

def assert_read_keyword(self, lexemes):
    read_token = [t for t in lexemes if t.token_type == TokenType.READ][0]
    self.assertEqual(read_token.value, "eat😋")

def assert_print_keyword(self, lexemes):
    print_token = [t for t in lexemes if t.token_type == TokenType.PRINT][0]
    self.assertEqual(print_token.value, "print🤮")

def assert_string_literal_basic(self, lexemes):
    string_tokens = [t for t in lexemes if t.token_type == TokenType.STRING]
    self.assertEqual(len(string_tokens), 1)
    self.assertEqual(string_tokens[0].value, "Hello World")

def assert_string_literal_with_escapes(self, lexemes):
    string_tokens = [t for t in lexemes if t.token_type == TokenType.STRING]
    self.assertEqual(len(string_tokens), 1)
    self.assertTrue("\n" in string_tokens[0].value or "\t" in string_tokens[0].value)

def assert_string_in_print(self, lexemes):
    print_token = [t for t in lexemes if t.token_type == TokenType.PRINT][0]
    string_token = [t for t in lexemes if t.token_type == TokenType.STRING][0]
    self.assertEqual(print_token.value, "print🤮")
    self.assertEqual(string_token.value, "Test Message")

def assert_empty_string(self, lexemes):
    string_tokens = [t for t in lexemes if t.token_type == TokenType.STRING]
    self.assertEqual(len(string_tokens), 1)
    self.assertEqual(string_tokens[0].value, "")

def assert_string_with_special_chars(self, lexemes):
    string_tokens = [t for t in lexemes if t.token_type == TokenType.STRING]
    self.assertEqual(len(string_tokens), 1)
    self.assertIn("!", string_tokens[0].value)

def assert_multiple_strings(self, lexemes):
    string_tokens = [t for t in lexemes if t.token_type == TokenType.STRING]
    self.assertEqual(len(string_tokens), 2)

def assert_string_tokens_present(self, lexemes):
    string_tokens = [t for t in lexemes if t.token_type == TokenType.STRING]
    self.assertGreaterEqual(len(string_tokens), 1)

def assert_expression_group(self, lexemes):
    expr_group_tokens = [t for t in lexemes if t.token_type == TokenType.EXPRESSION_GROUP]
    self.assertEqual(len(expr_group_tokens), 2)

test_cases = [
    ("simple_declaration", "# 😀 🐷 🐖x🐖 @ 10 #\n", assert_simple_declaration),
    ("arithmetic_operators", "# 😀 🐷 🐖result🐖 @ 🐖a🐖 ❤️ 🐖b🐖 💔 🐖c🐖 💞 🐖d🐖 💕 🐖e🐖 #\n", assert_arithmetic_operators),
    ("comparison_operators", "# 😀 wow 🐖check🐖 @ 🐖x🐖 🌸🌸 🐖y🐖 bruh 🐖a🐖 💩🌸 🐖b🐖 hru 🐖c🐖 🌸> 🐖d🐖 hru 🐖e🐖 🌸< 🐖f🐖 #\n", assert_comparison_operators),
    ("logical_operators", "# 😀 wow 🐖result🐖 @ 💩 🐖x🐖 hru 🐖y🐖 bruh 🐖z🐖 #\n", assert_logical_operators),
    ("boolean_literals", "# 😀 wow 🐖t🐖 @ LOVE #\n# 😀 wow 🐖f🐖 @ HATE #\n", assert_boolean_literals),
    ("control_flow_keywords", "# SAVE 🐖x🐖 > 0 #\n# 🐖🐖🐖 #\n# HURT 🐖x🐖 < 0 #\n# 🐖🐖🐖 #\n# KILL #\n# 🐖🐖🐖 #\n# OINK 🐖i🐖 < 10 #\n# 🐖🐖🐖 #\n", assert_control_flow_keywords),
    ("block_delimiters", "# 🐖🐖🐖 #\n# 🐖🐖🐖 #\n", assert_block_delimiters),
    ("mood_line_borders", "#~ 😀 🐷 🐖x🐖 @ 10 ~#\n", assert_mood_line_borders),
    ("return_statement", "# ... 42 ... #\n", assert_return_statement),
    ("all_data_types", "# 😀 🐽 🐖small🐖 @ 10 #\n# 😀 🐷 🐖medium🐖 @ 20 #\n# 😀 🐗 🐖large🐖 @ 30 #\n# 😀 wow 🐖flag🐖 @ LOVE #\n", assert_all_data_types),
    ("brackets", "# 😀 🐷 🐖x🐖 @ ** 10 ❤️ 5 ** #\n", assert_brackets),
    ("single_line_comment", "👀 This is a comment\n# 😀 🐷 🐖x🐖 @ 10 #\n", assert_single_line_comment),
    ("multiline_comment", "👀👀👀\nThis is a\nmultiline comment\n👀👀👀\n# 😀 🐷 🐖x🐖 @ 10 #\n", assert_multiline_comment),
    ("struct_keyword", "# BOAR 🐖Point🐖 #\n", assert_struct_keyword),
    ("function_keyword", "# 🐷 PIG 🐖test🐖 #\n", assert_function_keyword),
    ("member_function_keyword", "# 🐷 PIGLET 🐖getValue🐖 #\n", assert_member_function_keyword),
    ("lambda_keyword", "# 😀 🥩 🐖f🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 🥩 #\n", assert_lambda_keyword),
    ("member_access", "# 😀 🐷 🐖val🐖 @ 🐖obj🐖 _ 🐖method🐖 #\n", assert_member_access),
    ("read_keyword", "# eat😋 🐖x🐖 #\n", assert_read_keyword),
    ("print_keyword", "# print🤮 🐖x🐖 #\n", assert_print_keyword),
    ("string_literal_basic", "# print🤮 🥓Hello World🥓 #\n", assert_string_literal_basic),
    ("string_literal_with_escapes", "# print🤮 🥓Line1\\nLine2\\tTabbed🥓 #\n", assert_string_literal_with_escapes),
    ("string_in_print", "# print🤮 🥓Test Message🥓 #\n", assert_string_in_print),
    ("empty_string", "# print🤮 🥓🥓 #\n", assert_empty_string),
    ("string_with_special_chars", "# print🤮 🥓Hello! @#$%🥓 #\n", assert_string_with_special_chars),
    ("multiple_strings", "# print🤮 🥓First🥓 #\n# print🤮 🥓Second🥓 #\n", assert_multiple_strings),
    ("string_tokens_present", "# print🤮 🥓Test🥓 #\n", assert_string_tokens_present),
    ("expression_group", "# 😀 🐷 🐖x🐖 @ 🌳 10 ❤️ 5 🌳 #\n", assert_expression_group),
]

for name, code, func in test_cases:
    TestLexerHappyPath.add_test_case(name, code, func)


if __name__ == "__main__":
    unittest.main(verbosity=2)