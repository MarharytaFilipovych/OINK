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
    '🥓': TokenType.QUOTE,
    '🌳': TokenType.EXPRESSION_GROUP,
    '🍗': TokenType.INTERP_STRING
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
INTERP_STRING = "🍗"

I1 = "i1"
I16 = "i16"
I64 = "i64"
I32 = "i32"

TOKEN_DISPLAY_NAMES = {
    "I16_TYPE": "🐽 (i16 type)",
    "I32_TYPE": "🐷 (i32 type)",
    "I64_TYPE": "🐗 (i64 type)",
    "BOOL": "wow (boolean type)",
    "VOID": "😑 (void type)",
    "STRING_TYPE": "👺 (string type)",
    "MUT": "😀 (mutable declaration)",
    "CONST": "😭 (constant declaration)", 
    "IF": "SAVE (if statement)",
    "ELIF": "HURT (else-if statement)",
    "ELSE": "KILL (else statement)",
    "WHILE": "OINK (while loop)",
    "RETURN": "... expr ... (return statement)",   
    "PLUS": "❤️ (addition)",
    "MINUS": "💔 (subtraction)",
    "MULTIPLY": "💞 (multiplication)",
    "DIVIDE": "💕 (division)", 
    "EQUALS": "🌸🌸 (equals)",
    "NOT_EQUALS": "💩🌸 (not equals)",
    "GREATER": "> (greater than)",
    "LESS": "< (less than)",
    "GREATER_EQUAL": "🌸> (greater or equal)",
    "LESS_EQUAL": "🌸< (less or equal)", 
    "NOT": "💩 (logical NOT)",
    "AND": "hru (logical AND)",
    "OR": "bruh (logical OR)",  
    "TRUE": "LOVE (true)",
    "FALSE": "HATE (false)",    
    "ASSIGNMENT": "@ (assignment)",
    "BRACKET": "** (bracket/argument delimiter)",
    "SIMPLE_LINE_BORDER": "# (line border)",
    "MOOD_LINE_BORDER_START": "#~ (mood line start)",
    "MOOD_LINE_BORDER_END": "~# (mood line end)",
    "BLOCK_BORDER": "🐖🐖🐖 (block border)",
    "VARIABLE_BORDER": "🐖 (variable border)",
    "FUNCTION": "PIG (function)",
    "MEMBER_FUNCTION": "PIGLET (member function)",
    "STRUCT": "BOAR (struct)",
    "MEMBER_ACCESS": "_ (member access)",
    "READ": "eat😋 (input)",
    "PRINT": "print🤮 (output)",
    "LAMBDA": "🥩 (lambda)",
    "QUOTE": "🥓 (string delimiter)",
    "EXPRESSION_GROUP": "🌳 (expression grouping)",
    "INTERP_STRING": "🍗 (string interpolation)",
    "VARIABLE": "variable name",
    "NUMBER": "number",
    "STRING": "string",
    "NEWLINE": "newline",
    "THE_END": "end of file",
    "COMMENT": "👀 (comment)",
    "MULTILINE_COMMENT": "👀👀👀 (multiline comment)",
}


def get_token_display_name(token_type_name: str) -> str:
    return TOKEN_DISPLAY_NAMES.get(token_type_name, token_type_name.lower())


TEXT = 'text'
EXPR = 'expr'