#!/usr/bin/env python3
from .lexer_state import LexerState
from ..token.token_class import Token
from ..constants import *
from ..token.token_type import TokenType


class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.tokens = []
        self.current_position = 0
        self.state = LexerState.INITIAL
        self.line = 1
        self.index = 1
        self.current_token_start = 0
        self.current_token_start_line = 0
        self.current_token_start_index = 0
        self.line_has_content = False

    def __add_token(self, token_type: TokenType, value: str, line: int = None, index: int = None):
        line = self.line if line is None else line
        index = self.index if index is None else index
        self.tokens.append(Token(token_type, value, line, index))

    def __start_new_token(self, new_state: LexerState):
        self.state = new_state
        self.current_token_start = self.current_position
        self.current_token_start_line = self.line
        self.current_token_start_index = self.index
        self.__move_to_next_char()

    @staticmethod
    def __is_whitespace(char: str) -> bool:
        return char in WHITESPACE

    def __peek_ahead(self, n: int = 1) -> str:
        end = self.current_position + n
        return self.source[self.current_position:end] if end <= len(self.source) else ""

    def __move_to_next_char(self, i: int = 1):
        while i > 0 and self.current_position < len(self.source):
            if self.source[self.current_position] == NEWLINE:
                self.line += 1
                self.index = 1
            else:
                self.index += 1
            self.current_position += 1
            i -= 1

    def __try_multi_char_token(self):
        return self.__try_token_from_dict(MULTI_CHAR_TOKENS)

    def __try_emoji_token(self):
        return self.__try_token_from_dict(EMOJI_TOKENS, check_ascii=True)

    def __try_multi_char_expr_token(self):
        return self.__try_token_from_dict(MULTI_CHAR_TOKENS)

    def __try_emoji_expr_token(self):
        return self.__try_token_from_dict(EMOJI_TOKENS, check_ascii=True)

    def __try_token_from_dict(self, token_dict, check_ascii=False):
        if check_ascii and ord(self.source[self.current_position]) <= 127:
            return False
        max_len = max(len(t) for t in token_dict)
        for length in range(max_len, 0, -1):
            seq = self.__peek_ahead(length)
            if seq in token_dict:
                self.__add_token(token_dict[seq], seq)
                self.__move_to_next_char(len(seq))
                return True
        return False

    def __manage_identifier_state(self, char: str):
        if char.isalpha() or char == VARIABLE_ALLOWED_SIGN:
            self.__move_to_next_char()
        else:
            self.__build_current_token()
            self.state = LexerState.INITIAL

    def __manage_number_state(self, char: str):
        if char.isdigit():
            self.__move_to_next_char()
            return
        if char.isalpha() or char == VARIABLE_ALLOWED_SIGN:
            value = self.source[self.current_token_start:self.current_position + 1]
            raise ValueError(
                f"Do you think that this is a correct number: '{value}'? It is not!!!"
                f" You placed that awful thing at line {self.current_token_start_line} "
                f"and column {self.current_token_start_index}.")
        self.__build_current_token()
        self.state = LexerState.INITIAL

    def __manage_string_state(self):
        parts = []
        current_part = []
        while self.current_position < len(self.source):
            if self.__check_quote():
                self.__add_string_part(parts, current_part)
                self.__finalize_string(parts)
                return
            if self.__check_interp_start():
                self.__add_string_part(parts, current_part)
                current_part = []
                self.__process_interpolation(parts)
                continue
            if self.__check_newline():
                raise ValueError(
                    f"Unclosed string literal at line {self.current_token_start_line}! "
                    f"String must be closed with 🥓 on the same line.")
            current_part.append(self.source[self.current_position])
            self.__move_to_next_char()
        raise ValueError(f"Unclosed string literal starting at line {self.current_token_start_line}!")

    def __check_quote(self):
        return self.__peek_ahead(len(QUOTE)) == QUOTE

    def __check_interp_start(self):
        return self.__peek_ahead(len(INTERP_STRING)) == INTERP_STRING

    def __check_newline(self):
        return self.source[self.current_position] == NEWLINE

    def __add_string_part(self, parts, current_part):
        if current_part:
            text = ''.join(current_part)
            parts.append((TEXT, self.__process_escape_sequences(text)))

    def __finalize_string(self, parts):
        if not parts:
            self.__add_token(TokenType.STRING, "", self.current_token_start_line, self.current_token_start_index)
        elif len(parts) == 1 and parts[0][0] == TEXT:
            self.__add_token(TokenType.STRING, parts[0][1], self.current_token_start_line, self.current_token_start_index)
        else:
            self.__add_interpolated_tokens(parts)
        self.__move_to_next_char(len(QUOTE))
        self.state = LexerState.INITIAL

    def __add_interpolated_tokens(self, parts):
        if parts[0][0] == EXPR:
            self.__add_token(TokenType.STRING, "")
        for part_type, content in parts:
            if part_type == TEXT:
                self.__add_token(TokenType.STRING, content)
            elif part_type == EXPR:
                self.__add_token(TokenType.INTERP_STRING, "")
                self.tokens.extend(content)
                self.__add_token(TokenType.INTERP_STRING, "")
        if parts[-1][0] == EXPR:
            self.__add_token(TokenType.STRING, "")

    def __process_interpolation(self, parts):
        self.__move_to_next_char(len(INTERP_STRING))
        expr_tokens = []
        depth = 0
        while self.current_position < len(self.source):
            if self.__peek_ahead(len(INTERP_STRING)) == INTERP_STRING and depth == 0:
                parts.append((EXPR, expr_tokens))
                self.__move_to_next_char(len(INTERP_STRING))
                return
            expr_token = self.__tokenize_single_expression()
            if expr_token:
                expr_tokens.append(expr_token)
        raise ValueError(f"Unclosed interpolation in string at line {self.current_token_start_line}!")

    def __tokenize_single_expression(self):
        char = self.source[self.current_position]
        if self.__is_whitespace(char):
            self.__move_to_next_char()
            return None
        if char.isdigit() or (char == MINUS and self.current_position + 1 < len(self.source) and self.source[self.current_position + 1].isdigit()):
            return self.__tokenize_number()
        if char.isalpha() or char == VARIABLE_ALLOWED_SIGN:
            return self.__tokenize_identifier()
        if self.__try_multi_char_expr_token() or self.__try_emoji_expr_token():
            return self.tokens.pop()
        if char in SPECIAL_CHARS:
            token = Token(SPECIAL_CHARS[char], char, self.line, self.index)
            self.__move_to_next_char()
            return token
        raise ValueError(f"Unexpected character in interpolation: '{char}' at line {self.line}")

    def __tokenize_number(self):
        start, start_line, start_index = self.current_position, self.line, self.index
        if self.source[self.current_position] == MINUS:
            self.__move_to_next_char()
        while self.current_position < len(self.source) and self.source[self.current_position].isdigit():
            self.__move_to_next_char()
        value = self.source[start:self.current_position]
        return Token(TokenType.NUMBER, value, start_line, start_index)

    def __tokenize_identifier(self):
        start, start_line, start_index = self.current_position, self.line, self.index
        while self.current_position < len(self.source):
            char = self.source[self.current_position]
            if char.isalnum() or char == VARIABLE_ALLOWED_SIGN:
                self.__move_to_next_char()
            else:
                break
        value = self.source[start:self.current_position]
        return Token(KEYWORDS.get(value, TokenType.VARIABLE), value, start_line, start_index)

    def __process_escape_sequences(self, value: str) -> str:
        result, i = [], 0
        while i < len(value):
            if value[i] == '\\':
                if i + 1 >= len(value):
                    raise ValueError(f"Invalid escape sequence at end of string at line {self.current_token_start_line}!")
                next_char = value[i + 1]
                if next_char == 'n':
                    result.append('\n')
                elif next_char == 't':
                    result.append('\t')
                elif next_char == '\\':
                    result.append('\\')
                else:
                    raise ValueError(f"Invalid escape sequence '\\{next_char}' in string at line {self.current_token_start_line}!")
                i += 2
            else:
                result.append(value[i])
                i += 1
        return ''.join(result)

    def __build_current_token(self):
        if self.state == LexerState.INITIAL:
            return
        value = self.source[self.current_token_start:self.current_position]
        match self.state:
            case LexerState.VARIABLE:
                self.__add_token(KEYWORDS.get(value, TokenType.VARIABLE), value, self.current_token_start_line, self.current_token_start_index)
            case LexerState.NUMBER:
                self.__add_token(TokenType.NUMBER, value, self.current_token_start_line, self.current_token_start_index)

    def __manage_comment_state(self):
        while self.current_position < len(self.source) and self.source[self.current_position] != NEWLINE:
            self.__move_to_next_char()
        self.state = LexerState.INITIAL
        self.line_has_content = False

    def __manage_multiline_comment_state(self):
        while self.current_position < len(self.source):
            if self.__peek_ahead(len(MULTILINE_COMMENT)) == MULTILINE_COMMENT:
                self.__move_to_next_char(len(MULTILINE_COMMENT))
                self.state = LexerState.INITIAL
                return
            self.__move_to_next_char()

    def tokenize(self) -> list[Token]:
        while self.current_position < len(self.source):
            char = self.source[self.current_position]
            match self.state:
                case LexerState.INITIAL:
                    self.__manage_initial_state(char)
                case LexerState.VARIABLE:
                    self.__manage_identifier_state(char)
                case LexerState.NUMBER:
                    self.__manage_number_state(char)
                case LexerState.COMMENT:
                    self.__manage_comment_state()
                case LexerState.MULTILINE_COMMENT:
                    self.__manage_multiline_comment_state()
                case LexerState.STRING:
                    self.__manage_string_state()
        self.__build_current_token()
        self.tokens.append(Token(TokenType.THE_END, "", self.line, self.index))
        return self.tokens

    def __manage_initial_state(self, char):
        if self.__handle_newline(char):
            return
        if self.__handle_whitespace(char):
            return
        if self.__handle_multiline_comment():
            return
        if self.__handle_comment():
            return
        if self.__handle_string():
            return
        self.line_has_content = True
        if self.__handle_multi_or_emoji_token():
            return
        if self.__handle_special_char(char):
            return
        if self.__handle_number_start(char):
            return
        if self.__handle_variable_start(char):
            return
        if self.__handle_digit_start(char):
            return
        raise ValueError(
            f"I did not expect character \"{char}\" to be placed at line {self.line}, column {self.index}!!!")

    def __handle_newline(self, char) -> bool:
        if char == NEWLINE:
            if self.line_has_content:
                self.__add_token(TokenType.NEWLINE, NEWLINE)
            self.line_has_content = False
            self.__move_to_next_char()
            return True
        return False

    def __handle_whitespace(self, char) -> bool:
        if self.__is_whitespace(char):
            self.__move_to_next_char()
            return True
        return False

    def __handle_multiline_comment(self) -> bool:
        if self.__peek_ahead(len(MULTILINE_COMMENT)) == MULTILINE_COMMENT:
            self.state = LexerState.MULTILINE_COMMENT
            self.__move_to_next_char(len(MULTILINE_COMMENT))
            return True
        return False

    def __handle_comment(self) -> bool:
        if self.__peek_ahead(len(COMMENT)) == COMMENT:
            self.state = LexerState.COMMENT
            self.__move_to_next_char(len(COMMENT))
            return True
        return False

    def __handle_string(self) -> bool:
        if self.__peek_ahead(len(QUOTE)) == QUOTE:
            self.line_has_content = True
            self.state = LexerState.STRING
            self.current_token_start = self.current_position + len(QUOTE)
            self.current_token_start_line = self.line
            self.current_token_start_index = self.index + 1
            self.__move_to_next_char(len(QUOTE))
            return True
        return False

    def __handle_multi_or_emoji_token(self) -> bool:
        return self.__try_multi_char_token() or self.__try_emoji_token()

    def __handle_special_char(self, char) -> bool:
        if char in SPECIAL_CHARS:
            self.__add_token(SPECIAL_CHARS[char], char)
            self.__move_to_next_char()
            return True
        return False

    def __handle_number_start(self, char) -> bool:
        if char == MINUS and self.__peek_ahead(2) and self.__peek_ahead(2)[1].isdigit():
            self.__start_new_token(LexerState.NUMBER)
            return True
        return False

    def __handle_variable_start(self, char) -> bool:
        if char.isalpha():
            self.__start_new_token(LexerState.VARIABLE)
            return True
        return False

    def __handle_digit_start(self, char) -> bool:
        if char.isdigit():
            self.__start_new_token(LexerState.NUMBER)
            return True
        return False
