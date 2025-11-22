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
    expected_types = [
        TokenType.SIMPLE_LINE_BORDER,
        TokenType.MUT,
        TokenType.I32_TYPE,
        TokenType.VARIABLE_BORDER,
        TokenType.VARIABLE,
        TokenType.VARIABLE_BORDER,
        TokenType.ASSIGNMENT,
        TokenType.NUMBER,
        TokenType.SIMPLE_LINE_BORDER,
        TokenType.NEWLINE,
        TokenType.THE_END
    ]
    actual_types = [t.token_type for t in lexemes]
    self.assertEqual(actual_types, expected_types)
    self.assertEqual(lexemes[1].value, "😀")
    self.assertEqual(lexemes[2].value, "🐷")
    self.assertEqual(lexemes[4].value, "x")
    self.assertEqual(lexemes[7].value, "42")

def assert_negative_number(self, lexemes):
    number_token = [t for t in lexemes if t.token_type == TokenType.NUMBER][0]
    self.assertEqual(number_token.value, "-100")

def assert_variable_with_ampersand(self, lexemes):
    var_token = [t for t in lexemes if t.token_type == TokenType.VARIABLE][0]
    self.assertEqual(var_token.value, "my&var")

def assert_all_operators(self, lexemes):
    operator_tokens = [t for t in lexemes if t.token_type in [
        TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE
    ]]
    self.assertEqual(len(operator_tokens), 4)

def assert_comparison_operators(self, lexemes):
    comparison_tokens = [t for t in lexemes if t.token_type.if_for_comparision()]
    self.assertEqual(len(comparison_tokens), 6)

def assert_logical_operators(self, lexemes):
    and_token = [t for t in lexemes if t.token_type == TokenType.AND][0]
    or_token = [t for t in lexemes if t.token_type == TokenType.OR][0]
    self.assertEqual(and_token.value, "hru")
    self.assertEqual(or_token.value, "bruh")

def assert_boolean_literals(self, lexemes):
    bool_tokens = [t for t in lexemes if t.token_type in [TokenType.TRUE, TokenType.FALSE]]
    self.assertEqual(len(bool_tokens), 2)
    self.assertEqual(bool_tokens[0].value, "LOVE")
    self.assertEqual(bool_tokens[1].value, "HATE")

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
    member_func_token = [t for t in lexemes if t.token_type == TokenType.MEMBER_FUNCTION][0]
    self.assertEqual(member_func_token.value, "PIGLET")

def assert_struct_with_fields(self, lexemes):
    struct_token = [t for t in lexemes if t.token_type == TokenType.STRUCT]
    var_tokens = [t for t in lexemes if t.token_type == TokenType.VARIABLE]
    self.assertEqual(len(struct_token), 1)
    self.assertTrue(len(var_tokens) >= 2)

def assert_function_with_params(self, lexemes):
    func_token = [t for t in lexemes if t.token_type == TokenType.FUNCTION]
    bracket_tokens = [t for t in lexemes if t.token_type == TokenType.BRACKET]
    self.assertEqual(len(func_token), 1)
    self.assertTrue(len(bracket_tokens) >= 2)

def assert_void_return_type(self, lexemes):
    void_token = [t for t in lexemes if t.token_type == TokenType.VOID][0]
    self.assertEqual(void_token.value, "😑")

def assert_member_access_operator(self, lexemes):
    member_tokens = [t for t in lexemes if t.token_type == TokenType.MEMBER_ACCESS]
    self.assertTrue(len(member_tokens) >= 1)

def assert_struct_declaration_complete(self, lexemes):
    struct_token = [t for t in lexemes if t.token_type == TokenType.STRUCT]
    block_tokens = [t for t in lexemes if t.token_type == TokenType.BLOCK_BORDER]
    self.assertEqual(len(struct_token), 1)
    self.assertEqual(len(block_tokens), 2)

def assert_print_statement(self, lexemes):
    expected_types = [TokenType.SIMPLE_LINE_BORDER, TokenType.PRINT, TokenType.VARIABLE_BORDER, TokenType.VARIABLE, TokenType.VARIABLE_BORDER, TokenType.SIMPLE_LINE_BORDER]
    actual_types = [t.token_type for t in lexemes]
    self.assertTrue(all(t1 == t2 for t1, t2 in zip(expected_types, actual_types)))
    self.assertEqual(lexemes[1].value, "print🤮")
    self.assertEqual(lexemes[3].value, "input&var")

def assert_read_statement(self, lexemes):
    read_token = [t for t in lexemes if t.token_type == TokenType.READ]
    var_token = [t for t in lexemes if t.token_type == TokenType.VARIABLE]
    self.assertEqual(len(read_token), 1)
    self.assertTrue(len(var_token) >= 1)
    self.assertEqual(read_token[0].value, "eat😋")
    self.assertEqual(var_token[0].value, "input&var")

def assert_lambda_type_declaration(self, lexemes):
    lambda_tokens = [t for t in lexemes if t.token_type == TokenType.LAMBDA]
    self.assertEqual(len(lambda_tokens), 1)
    self.assertEqual(lambda_tokens[0].value, "🥩")

def assert_simple_lambda_expression(self, lexemes):
    lambda_tokens = [t for t in lexemes if t.token_type == TokenType.LAMBDA]
    self.assertEqual(len(lambda_tokens), 4)
    bracket_tokens = [t for t in lexemes if t.token_type == TokenType.BRACKET]
    self.assertTrue(len(bracket_tokens) >= 2)

def assert_lambda_with_multiple_params(self, lexemes):
    lambda_tokens = [t for t in lexemes if t.token_type == TokenType.LAMBDA]
    self.assertEqual(len(lambda_tokens), 4)
    var_tokens = [t for t in lexemes if t.token_type == TokenType.VARIABLE]
    self.assertTrue(len(var_tokens) >= 2)

def assert_lambda_with_no_params(self, lexemes):
    lambda_tokens = [t for t in lexemes if t.token_type == TokenType.LAMBDA]
    self.assertEqual(len(lambda_tokens), 4)
    bracket_tokens = [t for t in lexemes if t.token_type == TokenType.BRACKET]
    self.assertTrue(len(bracket_tokens) >= 2)

def assert_lambda_with_operators(self, lexemes):
    lambda_tokens = [t for t in lexemes if t.token_type == TokenType.LAMBDA]
    self.assertEqual(len(lambda_tokens), 4)
    operator_tokens = [t for t in lexemes if t.token_type in [
        TokenType.PLUS, TokenType.MULTIPLY
    ]]
    self.assertTrue(len(operator_tokens) >= 1)

def assert_lambda_with_comparison(self, lexemes):
    lambda_tokens = [t for t in lexemes if t.token_type == TokenType.LAMBDA]
    self.assertEqual(len(lambda_tokens), 4)
    comparison_tokens = [t for t in lexemes if t.token_type == TokenType.GREATER]
    self.assertEqual(len(comparison_tokens), 1)

def assert_lambda_with_logical_operators(self, lexemes):
    lambda_tokens = [t for t in lexemes if t.token_type == TokenType.LAMBDA]
    self.assertEqual(len(lambda_tokens), 4)
    and_tokens = [t for t in lexemes if t.token_type == TokenType.AND]
    self.assertTrue(len(and_tokens) >= 1)

def assert_lambda_with_unary_operator(self, lexemes):
    lambda_tokens = [t for t in lexemes if t.token_type == TokenType.LAMBDA]
    self.assertEqual(len(lambda_tokens), 4)
    not_tokens = [t for t in lexemes if t.token_type == TokenType.NOT]
    self.assertEqual(len(not_tokens), 1)

def assert_nested_lambda_boundaries(self, lexemes):
    lambda_tokens = [t for t in lexemes if t.token_type == TokenType.LAMBDA]
    self.assertEqual(len(lambda_tokens), 4)
    bracket_tokens = [t for t in lexemes if t.token_type == TokenType.BRACKET]
    self.assertTrue(len(bracket_tokens) >= 4)

def assert_lambda_with_different_types(self, lexemes):
    lambda_tokens = [t for t in lexemes if t.token_type == TokenType.LAMBDA]
    self.assertEqual(len(lambda_tokens), 4)
    i16_tokens = [t for t in lexemes if t.token_type == TokenType.I16_TYPE]
    i32_tokens = [t for t in lexemes if t.token_type == TokenType.I32_TYPE]
    self.assertTrue(len(i16_tokens) + len(i32_tokens) >= 2)


all_tests = [
    ("simple_declaration", "# 😀 🐷 🐖x🐖 @ 42 #\n", assert_simple_declaration),
    ("negative_number", "# 😀 🐷 🐖x🐖 @ -100 #\n", assert_negative_number),
    ("variable_with_ampersand", "# 😀 🐷 🐖my&var🐖 @ 10 #\n", assert_variable_with_ampersand),
    ("all_operators", "# 🐖a🐖 ❤️ 🐖b🐖 💔 🐖c🐖 💞 🐖d🐖 💕 🐖e🐖 #\n", assert_all_operators),
    ("comparison_operators", "# 🐖a🐖 🌸🌸 🐖b🐖 💩🌸 🐖c🐖 > 🐖d🐖 < 🐖e🐖 🌸> 🐖f🐖 🌸< 🐖g🐖 #\n", assert_comparison_operators),
    ("logical_operators", "# 🐖a🐖 hru 🐖b🐖 bruh 🐖c🐖 #\n", assert_logical_operators),
    ("boolean_literals", "# 😀 wow 🐖flag🐖 @ LOVE #\n# 😀 wow 🐖flag2🐖 @ HATE #\n", assert_boolean_literals),
    ("control_flow_keywords", "# SAVE 🐖x🐖 > 5 #\n# HURT 🐖x🐖 🌸🌸 0 #\n# KILL #\n# OINK 🐖x🐖 < 10 #\n", assert_control_flow_keywords),
    ("block_delimiters", "# 🐖🐖🐖 #\n# 🐖🐖🐖 #\n", assert_block_delimiters),
    ("mood_line_borders", "#~ 🐖x🐖 @ 🐖x🐖 ❤️ 5 ~#\n", assert_mood_line_borders),
    ("return_statement", "# ... 🐖x🐖 ... #\n", assert_return_statement),
    ("all_data_types", "# 😀 🐽 🐖a🐖 @ 1 #\n# 😀 🐷 🐖b🐖 @ 2 #\n# 😀 🐗 🐖c🐖 @ 3 #\n# 😀 wow 🐖d🐖 @ LOVE #\n", assert_all_data_types),
    ("brackets", "# 🐖x🐖 @ ** 🐖a🐖 ❤️ 🐖b🐖 ** #\n", assert_brackets),
    ("single_line_comment", "👀 This is a comment\n# 😀 🐷 🐖x🐖 @ 10 #\n", assert_single_line_comment),
    ("multiline_comment", "👀👀👀\nThis is a\nmulti-line comment\n👀👀👀\n# 😀 🐷 🐖x🐖 @ 10 #\n", assert_multiline_comment),
    ("struct_keyword", "# BOAR 🐖Point🐖 #\n", assert_struct_keyword),
    ("function_keyword", "# 🐷 PIG 🐖add🐖 #\n", assert_function_keyword),
    ("member_function_keyword", "# 🐷 PIGLET 🐖getValue🐖 #\n", assert_member_function_keyword),
    ("struct_with_fields", "# BOAR 🐖Point🐖 #\n# 🐖🐖🐖 #\n# 😀 🐷 🐖x🐖 #\n# 😀 🐷 🐖y🐖 #\n# 🐖🐖🐖 #\n", assert_struct_with_fields),
    ("function_with_params", "# 🐷 PIG 🐖add🐖 ** 🐷 🐖a🐖 ** ** 🐷 🐖b🐖 ** #\n", assert_function_with_params),
    ("void_return_type", "# 😑 PIG 🐖print🐖 #\n", assert_void_return_type),
    ("member_access_operator", "# 🐖p🐖 _ 🐖x🐖 #\n", assert_member_access_operator),
    ("struct_declaration_complete", "# BOAR 🐖Point🐖 #\n# 🐖🐖🐖 #\n# 😀 🐷 🐖x🐖 #\n# 🐖🐖🐖 #\n", assert_struct_declaration_complete),
    ( "print_statement", "# print🤮 🐖input&var🐖 #", assert_print_statement),
    ( "read_statement","# 😀 🐷 🐖input&var🐖 #\n# eat😋 🐖input&var🐖 #",assert_read_statement),
    ("lambda_type_keyword", "# 😀 🥩 🐖f🐖 #\n", assert_lambda_type_declaration),
    ("simple_lambda_one_param", "# 😀 🥩 🐖square🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 💞 🐖x🐖 🥩 #\n", assert_simple_lambda_expression),
    ("lambda_multiple_params", "# 😀 🥩 🐖add🐖 @ 🥩 ** 🐷 🐖a🐖 ** ** 🐷 🐖b🐖 ** 🥩 🐖a🐖 ❤️ 🐖b🐖 🥩 #\n", assert_lambda_with_multiple_params),
    ("lambda_no_params", "# 😀 🥩 🐖const🐖 @ 🥩 ** ** 🥩 42 🥩 #\n", assert_lambda_with_no_params),
    ("lambda_with_arithmetic", "# 😀 🥩 🐖calc🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 💞 2 ❤️ 1 🥩 #\n", assert_lambda_with_operators),
    ("lambda_with_comparison", "# 😀 🥩 🐖check🐖 @ 🥩 ** 🐷 🐖n🐖 ** 🥩 🐖n🐖 > 0 🥩 #\n", assert_lambda_with_comparison),
    ("lambda_with_logical_and", "# 😀 🥩 🐖validate🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 > 0 hru 🐖x🐖 < 100 🥩 #\n", assert_lambda_with_logical_operators),
    ("lambda_with_not_operator", "# 😀 🥩 🐖negate🐖 @ 🥩 ** wow 🐖b🐖 ** 🥩 💩 🐖b🐖 🥩 #\n", assert_lambda_with_unary_operator),
    ("lambda_with_nested_expression", "# 😀 🥩 🐖complex🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 ** 🐖x🐖 💞 2 ** ❤️ 1 🥩 #\n", assert_nested_lambda_boundaries),
    ("lambda_with_mixed_types", "# 😀 🥩 🐖mix🐖 @ 🥩 ** 🐽 🐖a🐖 ** ** 🐷 🐖b🐖 ** 🥩 🐖a🐖 ❤️ 🐖b🐖 🥩 #\n", assert_lambda_with_different_types),
]

for name, source, func in all_tests:
    TestLexerHappyPath.add_test_case(name, source, func)


if __name__ == "__main__":
    unittest.main(verbosity=2)