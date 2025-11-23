#!/usr/bin/env python3
from typing import Optional
from ..token.token_type import TokenType
from ..token.token_class import Token


class TokenReader:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_token_index = 0
        self.in_mood_line = False

    def peek(self, count: int = 0) -> Optional[Token]:
        return self.tokens[self.current_token_index + count] if self.current_token_index + count < len(
            self.tokens) else None

    def eat(self) -> Optional[Token]:
        token = self.peek()
        if token:
            self.current_token_index += 1
        return token

    def expect_token(self, token_type: TokenType) -> Token:
        token = self.peek()
        if not token:
            raise ValueError(f"I expected a token of the type {token_type.name.lower()} but found nothing!")
        if token.token_type != token_type:
            raise ValueError(
                f"I expected a token of the type \"{token_type.name.lower()}\""
                f" but got \"{token.token_type.name.lower()}\" -> ({token.value}) at line {token.line} and index {token.index}!")
        return self.eat()

    def skip_newlines(self):
        while self.peek() and self.peek().token_type == TokenType.NEWLINE:
            self.eat()

    def define_line_type(self, token: Token):
        if not token:
            raise ValueError("Expected a statement, got nothing!")

        if token.token_type == TokenType.MOOD_LINE_BORDER_START:
            self.in_mood_line = True
            self.eat()
        elif token.token_type == TokenType.SIMPLE_LINE_BORDER:
            self.eat()

    def expect_line_end(self):
        if self.in_mood_line:
            self.expect_token(TokenType.MOOD_LINE_BORDER_END)
            self.in_mood_line = False
        else:
            self.expect_token(TokenType.SIMPLE_LINE_BORDER)
        self.expect_newline_or_end()

    def expect_newline_or_end(self):
        token = self.peek()
        if token and token.token_type not in [TokenType.NEWLINE, TokenType.THE_END]:
            raise ValueError(f"Expected newline or end, but got \"{token.value}\" of"
                             f" the type {token.token_type.name.lower()}at line {token.line}")
        if token and token.token_type == TokenType.NEWLINE:
            self.eat()

    def skip_line_start(self):
        token = self.peek()
        if token and token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]:
            if token.token_type == TokenType.MOOD_LINE_BORDER_START:
                self.in_mood_line = True
            self.eat()