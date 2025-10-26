#!/usr/bin/env python3
from ..token.token_type import TokenType

WHITESPACE = ' \t\r'

KEYWORDS = {
    "SAVE": TokenType.IF,
    "HURT": TokenType.ELIF,
    "KILL": TokenType.ELSE,
    "OINK": TokenType.WHILE,
    "LOVE": TokenType.TRUE,
    "HATE": TokenType.FALSE,
    "wow": TokenType.BOOL,
    "hru": TokenType.AND,
    "bruh": TokenType.OR,
}

SPECIAL_CHARS = {
    '@': TokenType.ASSIGNMENT,
    '>': TokenType.GREATER,
    '<': TokenType.LESS
}

MULTI_CHAR_TOKENS = {
    '#~': TokenType.MOOD_LINE_BORDER,
    '~#': TokenType.MOOD_END,
    '...': TokenType.RETURN,
    '**': TokenType.BRACKET,
    '#': TokenType.SIMPLE_LINE_BORDER,
}

EMOJI_TOKENS = {
    '🐽': TokenType.VARIABLE_BORDER,
    '🐷': TokenType.I32_TYPE,
    '🐗': TokenType.I64_TYPE,
    '😀': TokenType.MUT,
    '😭': TokenType.CONST,
    '❤️': TokenType.PLUS,
    '💔': TokenType.MINUS,
    '💞': TokenType.MULTIPLY,
    '💕': TokenType.DIVIDE,
    '💩': TokenType.NOT,
    '👀': TokenType.COMMENT,
    '🌸🌸': TokenType.EQUALS,
    '💩🌸': TokenType.NOT_EQUALS,
    '🌸>': TokenType.GREATER_EQUAL,
    '🌸<': TokenType.LESS_EQUAL,
    '🐖🐖🐖': TokenType.BLOCK_BORDER,
    '👀👀👀': TokenType.MULTILINE_COMMENT
}

MULTILINE_COMMENT = '👀👀👀'  
COMMENT = '👀'
VARIABLE_ALLOWED_SIGHN = '&'
NEWLINE = '\n'