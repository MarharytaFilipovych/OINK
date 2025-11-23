#!/usr/bin/env python3
from .token.token_type import TokenType

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
    "PIG": TokenType.FUNCTION,
    "PIGLET": TokenType.MEMBER_FUNCTION,
    "BOAR": TokenType.STRUCT,
}

SPECIAL_CHARS = {
    '@': TokenType.ASSIGNMENT,
    '>': TokenType.GREATER,
    '<': TokenType.LESS,
    '_': TokenType.MEMBER_ACCESS,
}

MULTI_CHAR_TOKENS = {
    '...': TokenType.RETURN,
    '#~': TokenType.MOOD_LINE_BORDER_START,
    '~#': TokenType.MOOD_LINE_BORDER_END,
    '**': TokenType.BRACKET,
    '#': TokenType.SIMPLE_LINE_BORDER,
    'eat😋': TokenType.READ,
    'print🤮': TokenType.PRINT
}

EMOJI_TOKENS = {
    '🐖': TokenType.VARIABLE_BORDER,
    '🐽': TokenType.I16_TYPE,
    '🐷': TokenType.I32_TYPE,
    '🐗': TokenType.I64_TYPE,
    '😀': TokenType.MUT,
    '😭': TokenType.CONST,
    '😑': TokenType.VOID,
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
    '👀👀👀': TokenType.MULTILINE_COMMENT,
    '🥩': TokenType.LAMBDA,
    '👺': TokenType.STRING_TYPE,
    '🥓': TokenType.QUOTE
}

MULTILINE_COMMENT = '👀👀👀'
COMMENT = '👀'
VARIABLE_ALLOWED_SIGN = '&'
NEWLINE = '\n'
UNDERLINE = "_"
MINUS = "-"
I16_MIN = -32768
I16_MAX = 32767
I32_MIN = -2147483648
I32_MAX = 2147483647
FALSE = "HATE"
TRUE = "LOVE"
NOT = "💩"
GLOBAL_SCOPE = "global"
I64_MAX = 2**63 - 1
I64_MIN = -2**63
LAMBDA = "lambda"
QUOTE = "🥓"
STRING = "string"