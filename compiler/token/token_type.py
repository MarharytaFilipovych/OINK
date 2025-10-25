#!/usr/bin/env python3
from enum import Enum, auto


class TokenType(Enum):
    I16_TYPE = auto()  # 🐽
    I32_TYPE = auto()  # 🐷
    I64_TYPE = auto()  # 🐗
    BOOL = auto()      # wow
    
    MUT = auto()       # 😀
    IMMUT = auto()     # 😭
    
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
    
    LEFT_PAREN = auto()   # **
    RIGHT_PAREN = auto()  # **
    
    LINE_START = auto()   # #
    LINE_END = auto()     # #
    MOOD_START = auto()   # #~
    MOOD_END = auto()     # ~#
    
    BLOCK_DELIM = auto()  # 🐖🐖🐖
    
    PIG_SNOUT = auto()    # 🐽
    
    VARIABLE = auto()
    NUMBER = auto()
    NEWLINE = auto()
    THE_END = auto()

    COMMENT = auto()           # 👀 (single line)
    MULTILINE_COMMENT = auto() # 👀👀👀