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
    '#~': TokenType.MOOD_START,
    '~#': TokenType.MOOD_END,
    '...': TokenType.RETURN,
    '**': TokenType.LEFT_PAREN,
    '#': TokenType.LINE_START,
}

EMOJI_TOKENS = {
    '🐽': TokenType.PIG_SNOUT,
    '🐷': TokenType.I32_TYPE,
    '🐗': TokenType.I64_TYPE,
    '😀': TokenType.MUT,
    '😭': TokenType.IMMUT,
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
    '🐖🐖🐖': TokenType.BLOCK_DELIM,
    '👀👀👀': TokenType.MULTILINE_COMMENT
}

MULTILINE_COMMENT = '👀👀👀'  
COMMENT = '👀'
VARIABLE_ALLOWED_SIGHN = '&'
NEWLINE = '\n'