#!/usr/bin/env python3
from .lexer_state import LexerState
from ..token.token_type import TokenType
from ..token.token_class import Token
from .lexer_constants import *


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.current_position = 0
        self.line = 1
        self.index = 1
        self.tokens = []
        self.state = LexerState.INITIAL

        self.current_token_start = 0
        self.current_token_start_line = 1
        self.current_token_start_index = 1

    def __is_whitespace(self, char: str):
        return char is not None and char in WHITESPACE

    def __add_token(self, token_type: TokenType, value: str, line: int = None, index: int = None):
        line = line if line is not None else self.line
        index = index if index is not None else self.index
        self.tokens.append(Token(token_type, value, line, index))

    def __peek_ahead(self, length: int) -> str:
        end_pos = self.current_position + length
        if end_pos <= len(self.source):
            return self.source[self.current_position:end_pos]
        return ""

    def __start_new_token(self, new_state: LexerState):
        self.state = new_state
        self.current_token_start = self.current_position
        self.current_token_start_line = self.line
        self.current_token_start_index = self.index
        self.__move_to_next_char()

    def __move_to_next_char(self, count: int = 1):
        i = 0
        while i < count and self.current_position < len(self.source):
            if self.source[self.current_position] == NEWLINE:
                self.line += 1
                self.index = 1
            else:
                self.index += 1
            self.current_position += 1
            i += 1

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
                    self.__manage_comment_state(char)
                case LexerState.MULTILINE_COMMENT:
                    self.__manage_multiline_comment_state()
                    
        self.__build_current_token()
        self.tokens.append(Token(TokenType.THE_END, "", self.line, self.index))
        return self.tokens

    def __manage_initial_state(self, char):
        if char == NEWLINE:
            self.__add_token(TokenType.NEWLINE, NEWLINE)
            self.__move_to_next_char()
            return

        if self.__is_whitespace(char):
            self.__move_to_next_char()
            return

        if self.__try_multi_char_token():
            return

        if self.__try_emoji_token():
            return

        if char in SPECIAL_CHARS:
            self.__add_token(SPECIAL_CHARS[char], char)
            self.__move_to_next_char()
            return

        if char == '-' and self.__peek_ahead(2) and self.__peek_ahead(2)[1].isdigit():
            self.__start_new_token(LexerState.NUMBER)
            return

        if char.isalpha():
            self.__start_new_token(LexerState.VARIABLE)
            return

        if char.isdigit():
            self.__start_new_token(LexerState.NUMBER)
            return

        raise ValueError(
            f"I did not expect character '{char}' to be "
            f"placed at line {self.line}, column {self.index}!!!")

    def __try_multi_char_token(self) -> bool:
        for length in [3, 2]:
            sequence = self.__peek_ahead(length)
            if sequence in MULTI_CHAR_TOKENS:
                self.__add_token(MULTI_CHAR_TOKENS[sequence], sequence)
                self.__move_to_next_char(length)
                return True
        return False

    def __try_emoji_token(self) -> bool:
        if ord(self.source[self.current_position]) <= 127:
            return False

        if self.__peek_ahead(9) == MULTILINE_COMMENT:
            self.state = LexerState.MULTILINE_COMMENT
            self.__move_to_next_char(9)
            return True
        
        if self.__peek_ahead(3) == COMMENT:
            self.state = LexerState.COMMENT
            self.__move_to_next_char(3)
            return True

        for length in [9, 6, 3, 2, 1]:
            sequence = self.__peek_ahead(length)
            if sequence in EMOJI_TOKENS:
                self.__add_token(EMOJI_TOKENS[sequence], sequence)
                self.__move_to_next_char(len(sequence))
                return True
        
        return False

    def __manage_identifier_state(self, char: str):
        if char.isalpha() or char == VARIABLE_ALLOWED_SIGHN:
            self.__move_to_next_char()
        else:
            self.__build_current_token()
            self.state = LexerState.INITIAL

    def __manage_number_state(self, char: str):
        if char.isdigit():
            self.__move_to_next_char()
        else:
            self.__build_current_token()
            self.state = LexerState.INITIAL

    def __build_identifier_token(self, value: str):
        token_type = KEYWORDS.get(value, TokenType.VARIABLE)
        self.__add_token(token_type, value, self.current_token_start_line, self.current_token_start_index)

    def __build_number_token(self, value: str):
        if not value.lstrip('-').isdigit():
             raise ValueError(
                f"Do you think that this is a correct number: '{value}'? It is not!!!"
                f"You placed that awful thing at line {self.current_token_start_line} "
                f"and column {self.current_token_start_index}." )
        self.__add_token(TokenType.NUMBER, value, self.current_token_start_line, self.current_token_start_index)

    def __build_current_token(self):
        if self.state == LexerState.INITIAL:
            return
        value = self.source[self.current_token_start:self.current_position]
        match self.state:
            case LexerState.VARIABLE:
                self.__build_identifier_token(value)
            case LexerState.NUMBER:
                self.__build_number_token(value)
    
    def __manage_comment_state(self, char: str):
        if char == NEWLINE:
            self.state = LexerState.INITIAL
        else:
            self.__move_to_next_char()

    def __manage_multiline_comment_state(self):
        if self.__peek_ahead(9) == MULTILINE_COMMENT:
            self.__move_to_next_char(9)
            self.state = LexerState.INITIAL
        else:
            self.__move_to_next_char()
