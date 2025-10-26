#!/usr/bin/env python3
from enum import Enum, auto


class TokenType(Enum):
    I16_TYPE = auto()  # 🐽
    I32_TYPE = auto()  # 🐷
    I64_TYPE = auto()  # 🐗
    BOOL = auto()      # wow
    
    MUT = auto()       # 😀
    CONST = auto()     # 😭
    
    IF = auto()        # SAVE
    ELIF = auto()      # HURT
    ELSE = auto()      # KILL
    WHILE = auto()     # OINK
    RETURN = auto()    # ... expr ...
    
    PLUS = auto()      # ❤️
    MINUS = auto()     # 💔
    MULTIPLY = auto()  # 💞
    DIVIDE = auto()    # 💕
    
    EQUALS = auto()        # 🌸🌸
    NOT_EQUALS = auto()    # 💩🌸
    GREATER = auto()       # >
    LESS = auto()          # <
    GREATER_EQUAL = auto() # 🌸>
    LESS_EQUAL = auto()    # 🌸<
    
    NOT = auto()       # 💩
    AND = auto()       # hru
    OR = auto()        # bruh
    
    TRUE = auto()      # LOVE
    FALSE = auto()     # HATE
    
    ASSIGNMENT = auto() # @
    
    BRACKET = auto()   # **
    
    SIMPLE_LINE_BORDER = auto()       # #
    MOOD_LINE_BORDER_START = auto()   # #~
    MOOD_LINE_BORDER_END = auto()     # ~#
    
    BLOCK_BORDER = auto()  # 🐖🐖🐖
    
    VARIABLE_BORDER = auto()    # 🐖
    
    VARIABLE = auto()
    NUMBER = auto()
    NEWLINE = auto()
    THE_END = auto()

    COMMENT = auto()           # 👀 (single line)
    MULTILINE_COMMENT = auto() # 👀👀👀

    def if_for_comparision(self) -> bool:
        return self in {TokenType.EQUALS, TokenType.NOT_EQUALS, TokenType.GREATER,
                        TokenType.LESS, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL}
    
    def is_arithmetic_operator(self) -> bool:
        return self in {TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE}
    
    def is_logical_operator(self) -> bool:
        return self in {TokenType.AND, TokenType.OR}
    
    def is_additive_operator(self) -> bool:
        return self in {TokenType.PLUS, TokenType.MINUS}
    
    def is_multiplicative_operator(self) -> bool:
        return self in {TokenType.MULTIPLY, TokenType.DIVIDE}
    
    def is_border(self) -> bool:
        return self in {TokenType.BLOCK_BORDER, 
                        TokenType.SIMPLE_LINE_BORDER, 
                        TokenType.MOOD_LINE_BORDER_START,
                        TokenType.MOOD_LINE_BORDER_END}  # ✅ ADDED THIS LINE