#!/usr/bin/env python3
from enum import Enum


class Operator(Enum):
    PLUS = ('❤️', 'add')
    MINUS = ('💔', 'sub')
    MULTIPLY = ('💞', 'mul')
    DIVIDE = ('💕', 'sdiv')
    EQUALS = ("🌸🌸", 'icmp eq')
    NOT_EQUALS = ("💩🌸", 'icmp ne')
    GREATER = ('>', 'icmp sgt')
    LESS = ('<', 'icmp slt')
    GREATER_EQUAL = ('🌸>', 'icmp sge')
    LESS_EQUAL = ('🌸<', 'icmp sle')
    AND = ('hru', 'and')
    OR = ('bruh', 'or')

    def __init__(self, symbol: str, llvm_operator: str):
        self.symbol = symbol
        self.llvm_operator = llvm_operator

    @staticmethod
    def from_string(op_str: str) -> 'Operator':
        for operator in Operator:
            if operator.symbol == op_str:
                return operator
        raise ValueError(f"This operator is not supported: {op_str}")

    def to_llvm(self) -> str:
        return self.llvm_operator

    def __str__(self) -> str:
        return self.symbol

    def is_for_comparison(self) -> bool:
        return self in (Operator.EQUALS, Operator.NOT_EQUALS, 
                       Operator.GREATER, Operator.LESS,
                       Operator.GREATER_EQUAL, Operator.LESS_EQUAL)

    def is_for_arithmetic(self) -> bool:
        return self in (Operator.PLUS, Operator.MINUS, Operator.MULTIPLY, Operator.DIVIDE)
    
    def is_logical(self) -> bool:
        return self in (Operator.AND, Operator.OR)
    
    def invert(self) -> 'Operator':
        inversions = {
            Operator.PLUS: Operator.MINUS,
            Operator.MINUS: Operator.PLUS,
            Operator.MULTIPLY: Operator.DIVIDE,
            Operator.DIVIDE: Operator.MULTIPLY,
            Operator.EQUALS: Operator.NOT_EQUALS,
            Operator.NOT_EQUALS: Operator.EQUALS,
            Operator.GREATER: Operator.LESS_EQUAL,
            Operator.LESS: Operator.GREATER_EQUAL,
            Operator.GREATER_EQUAL: Operator.LESS,
            Operator.LESS_EQUAL: Operator.GREATER,
        }
        return inversions.get(self, self)