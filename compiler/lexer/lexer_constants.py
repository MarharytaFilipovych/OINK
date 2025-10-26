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
    '...': TokenType.RETURN,         # 3 chars - check first
    '#~': TokenType.MOOD_LINE_BORDER_START,  # 2 chars
    '~#': TokenType.MOOD_LINE_BORDER_END,    # 2 chars  
    '**': TokenType.BRACKET,         # 2 chars
    '#': TokenType.SIMPLE_LINE_BORDER,       # 1 char - check last
}

EMOJI_TOKENS = {
    '🐖': TokenType.VARIABLE_BORDER,  # ✅ CHANGED - pig face for variable borders
    '🐽': TokenType.I16_TYPE,  # ✅ CHANGED - pig snout for i16 type
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