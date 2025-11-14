#!/usr/bin/env python3
from typing import Optional
from compiler.token.token_type import TokenType
from compiler.token.token_class import Token


class BaseParser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_token_index = 0
        self.in_mood_line = False

    def _peek(self, count: int = 0) -> Optional[Token]:
        index = self.current_token_index + count
        return self.tokens[index] if index < len(self.tokens) else None

    def _eat(self) -> Optional[Token]:
        token = self._peek()
        if token:
            self.current_token_index += 1
        return token

    def _expect_token(self, token_type: TokenType) -> Token:
        token = self._peek()
        if not token:
            raise ValueError(f"Expected {token_type.name} but reached end of input!")

        if token.token_type != token_type:
            raise ValueError(f"Expected {token_type.name} but got {token.token_type.name} "
                           f"at line {token.line}")

        return self._eat()

    def _skip_newlines(self):
        while self._peek() and self._peek().token_type == TokenType.NEWLINE:
            self._eat()

    def _define_line_type(self, token: Token):
        if not token:
            raise ValueError("Expected a statement but found nothing!")
        
        if token.token_type == TokenType.MOOD_LINE_BORDER_START:
            self.in_mood_line = True
            self._eat()
        elif token.token_type == TokenType.SIMPLE_LINE_BORDER:
            self._eat()

    def _expect_line_end(self):
        if self.in_mood_line:
            self._expect_token(TokenType.MOOD_LINE_BORDER_END)
            self.in_mood_line = False
        else:
            self._expect_token(TokenType.SIMPLE_LINE_BORDER)
        self._expect_newline_or_end()

    def _expect_newline_or_end(self):
        token = self._peek()
        if token and token.token_type not in [TokenType.NEWLINE, TokenType.THE_END]:
            raise ValueError(f"Expected newline after statement at line {token.line}")
        if token and token.token_type == TokenType.NEWLINE:
            self._eat()

    def _skip_line_start(self):
        token = self._peek()
        if token and token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]:
            if token.token_type == TokenType.MOOD_LINE_BORDER_START:
                self.in_mood_line = True
            self._eat()

    def _peek_for_token_after_line_start(self, target_type: TokenType) -> bool:
        saved_index = self.current_token_index
        token = self._peek()
        
        if token and token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]:
            self.current_token_index += 1
            token = self._peek()
            result = token and token.token_type == target_type
        else:
            result = False
        
        self.current_token_index = saved_index
        return result
