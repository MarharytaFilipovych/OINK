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
    
    def test_simple_declaration(self):
        code = "# 😀 🐷 🐖x🐖 @ 42 #\n"
        lexemes = get_lexemes(code)
        
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
        self.assertEqual(lexemes.value, "42")


    def test_simple_declaration_without_assignment(self):
        code = "# 😀 🐷 🐖x🐖#\n"
        lexemes = get_lexemes(code)
        
        expected_types = [
            TokenType.SIMPLE_LINE_BORDER,
            TokenType.MUT,
            TokenType.I32_TYPE,
            TokenType.VARIABLE_BORDER,
            TokenType.VARIABLE,
            TokenType.VARIABLE_BORDER,
            TokenType.SIMPLE_LINE_BORDER,
            TokenType.NEWLINE,
            TokenType.THE_END
        ]

        actual_types = [t.token_type for t in lexemes]
        self.assertEqual(actual_types, expected_types)
        self.assertEqual(lexemes[1].value, "😀")
        self.assertEqual(lexemes[2].value, "🐷")
    
    def test_negative_number(self):
        code = "# 😀 🐷 🐖x🐖 @ -100 #\n"
        lexemes = get_lexemes(code)
        number_token = [t for t in lexemes if t.token_type == TokenType.NUMBER][0]
        self.assertEqual(number_token.value, "-100")
    
    def test_variable_with_ampersand(self):
        code = "# 😀 🐷 🐖my&var🐖 @ 10 #\n"
        lexemes = get_lexemes(code)        
        var_token = [t for t in lexemes if t.token_type == TokenType.VARIABLE][0]
        self.assertEqual(var_token.value, "my&var")
    
    def test_all_operators(self):
        code = "# 🐖a🐖 ❤️ 🐖b🐖 💔 🐖c🐖 💞 🐖d🐖 💕 🐖e🐖 #\n"
        lexemes = get_lexemes(code)

        operator_tokens = [t for t in lexemes if t.token_type in [
            TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE
        ]]

        self.assertEqual(len(operator_tokens), 4)
    
    def test_comparison_operators(self):
        code = "# 🐖a🐖 🌸🌸 🐖b🐖 💩🌸 🐖c🐖 > 🐖d🐖 < 🐖e🐖 🌸> 🐖f🐖 🌸< 🐖g🐖 #\n"
        lexemes = get_lexemes(code)
        
        comparison_tokens = [t for t in lexemes if t.token_type.if_for_comparision()]
        self.assertEqual(len(comparison_tokens), 6)
    
    def test_logical_operators(self):
        code = "# 🐖a🐖 hru 🐖b🐖 bruh 🐖c🐖 #\n"
        lexemes = get_lexemes(code)
        
        and_token = [t for t in lexemes if t.token_type == TokenType.AND][0]
        or_token = [t for t in lexemes if t.token_type == TokenType.OR][0]
        self.assertEqual(and_token.value, "hru")
        self.assertEqual(or_token.value, "bruh")
    
    def test_boolean_literals(self):
        code = "# 😀 wow 🐖flag🐖 @ LOVE #\n# 😀 wow 🐖flag2🐖 @ HATE #\n"
        lexemes = get_lexemes(code)
        
        bool_tokens = [t for t in lexemes if t.token_type in [TokenType.TRUE, TokenType.FALSE]]
        self.assertEqual(len(bool_tokens), 2)
        self.assertEqual(bool_tokens[0].value, "LOVE")
        self.assertEqual(bool_tokens[1].value, "HATE")
    
    def test_control_flow_keywords(self):
        code = "# SAVE 🐖x🐖 > 5 #\n# HURT 🐖x🐖 🌸🌸 0 #\n# KILL #\n# OINK 🐖x🐖 < 10 #\n"
        lexemes = get_lexemes(code)

        if_token = [t for t in get_lexemes if t.token_type == TokenType.IF][0]
        elif_token = [t for t in get_lexemes if t.token_type == TokenType.ELIF][0]
        else_token = [t for t in get_lexemes if t.token_type == TokenType.ELSE][0]
        while_token = [t for t in get_lexemes if t.token_type == TokenType.WHILE][0]
        
        self.assertEqual(if_token.value, "SAVE")
        self.assertEqual(elif_token.value, "HURT")
        self.assertEqual(else_token.value, "KILL")
        self.assertEqual(while_token.value, "OINK")
    
    def test_block_delimiters(self):
        code = "# 🐖🐖🐖 #\n# 🐖🐖🐖 #\n"
        lexemes = get_lexemes(code)
        
        block_tokens = [t for t in lexemes if t.token_type == TokenType.BLOCK_BORDER]
        self.assertEqual(len(block_tokens), 2)
    
    def test_mood_line_borders(self):
        code = "#~ 🐖x🐖 @ 🐖x🐖 ❤️ 5 ~#\n"
        lexemes = get_lexemes(code)
        
        mood_start = [t for t in lexemes if t.token_type == TokenType.MOOD_LINE_BORDER_START][0]
        mood_end = [t for t in lexemes if t.token_type == TokenType.MOOD_LINE_BORDER_END][0]
        
        self.assertEqual(mood_start.value, "#~")
        self.assertEqual(mood_end.value, "~#")
    
    def test_return_statement(self):
        code = "# ... 🐖x🐖 ... #\n"
        lexemes = get_lexemes(code)
        
        return_tokens = [t for t in lexemes if t.token_type == TokenType.RETURN]
        self.assertEqual(len(return_tokens), 2)
    
    def test_all_data_types(self):
        code = "# 😀 🐽 🐖a🐖 @ 1 #\n# 😀 🐷 🐖b🐖 @ 2 #\n# 😀 🐗 🐖c🐖 @ 3 #\n# 😀 wow 🐖d🐖 @ LOVE #\n"
        lexemes = get_lexemes(code)
        
        i16_token = [t for t in lexemes if t.token_type == TokenType.I16_TYPE][0]
        i32_token = [t for t in lexemes if t.token_type == TokenType.I32_TYPE][0]
        i64_token = [t for t in lexemes if t.token_type == TokenType.I64_TYPE][0]
        bool_token = [t for t in lexemes if t.token_type == TokenType.BOOL][0]
        
        self.assertEqual(i16_token.value, "🐽")
        self.assertEqual(i32_token.value, "🐷")
        self.assertEqual(i64_token.value, "🐗")
        self.assertEqual(bool_token.value, "wow")
    
    def test_brackets(self):
        code = "# 🐖x🐖 @ ** 🐖a🐖 ❤️ 🐖b🐖 ** #\n"
        lexemes = get_lexemes(code)
        
        bracket_tokens = [t for t in lexemes if t.token_type == TokenType.BRACKET]
        self.assertEqual(len(bracket_tokens), 2)
    
    def test_single_line_comment(self):
        code = "👀 This is a comment\n# 😀 🐷 🐖x🐖 @ 10 #\n"
        lexemes = get_lexemes(code)
        for lex in lexemes:
            print(lex)

        
        var_token = [t for t in lexemes if t.token_type == TokenType.VARIABLE][0]
        print(var_token)
        self.assertEqual(var_token.value, "x")
    
    def test_multiline_comment(self):
        code = "👀👀👀\nThis is a\nmulti-line comment\n👀👀👀\n# 😀 🐷 🐖x🐖 @ 10 #\n"
        lexemes = get_lexemes(code)
        
        var_token = [t for t in lexemes if t.token_type == TokenType.VARIABLE][0]
        self.assertEqual(var_token.value, "x")

if __name__ == '__main__':
    unittest.main(verbosity=2)