#!/usr/bin/env python3
from typing import Union
from compiler.node.expr_node import ExprNode
from compiler.node.factor_node import FactorNode
from compiler.node.unary_op_node import UnaryOpNode
from compiler.node.binary_op_node import BinaryOpNode
from compiler.node.number_node import NumberNode
from compiler.node.bool_node import BooleanNode
from compiler.llvm_specifics.data_type import DataType
from compiler.llvm_specifics.operator import Operator
from compiler.token.token_type import TokenType
from compiler.constants import NOT, FALSE, TRUE
from .base_parser import BaseParser


class ExpressionParser(BaseParser):
    def _parse_type(self) -> Union[DataType, str]:
        token = self._eat()
        type_map = {
            TokenType.I16_TYPE: DataType.I16,
            TokenType.I32_TYPE: DataType.I32,
            TokenType.I64_TYPE: DataType.I64,
            TokenType.BOOL: DataType.BOOL,
            TokenType.VOID: DataType.VOID
        }
        
        if token.token_type in type_map:
            return type_map[token.token_type]
        
        if token.token_type == TokenType.VARIABLE:
            return token.value
        
        raise ValueError(f"Expected type declaration at line {token.line}")

    @staticmethod
    def _set_default_for_type(data_type: Union[DataType, str]) -> FactorNode:
        if isinstance(data_type, str):
            raise ValueError(f"Cannot set default value for struct type {data_type}")
        if data_type == DataType.BOOL:
            return BooleanNode(FALSE)
        elif data_type in [DataType.I16, DataType.I32, DataType.I64]:
            return NumberNode("0")
        raise ValueError(f"No default value for {data_type}")

    def _parse_expression(self) -> ExprNode:
        return self._parse_logical_or()

    def _parse_logical_or(self) -> ExprNode:
        left = self._parse_logical_and()
        while self._peek() and self._peek().token_type == TokenType.OR:
            self._eat()
            right = self._parse_logical_and()
            left = BinaryOpNode(left, Operator.OR, right)
        return left

    def _parse_logical_and(self) -> ExprNode:
        left = self._parse_comparison()
        while self._peek() and self._peek().token_type == TokenType.AND:
            self._eat()
            right = self._parse_comparison()
            left = BinaryOpNode(left, Operator.AND, right)
        return left

    def _parse_comparison(self) -> ExprNode:
        left = self._parse_additive()
        token = self._peek()
        
        if token and token.token_type.if_for_comparision():
            op_token = self._eat()
            operator = Operator.from_string(op_token.value)
            if self.in_mood_line:
                operator = operator.invert()
            right = self._parse_additive()
            left = BinaryOpNode(left, operator, right)
        
        return left

    def _parse_additive(self) -> ExprNode:
        left = self._parse_multiplicative()
        
        while self._peek() and self._peek().token_type.is_additive_operator():
            op_token = self._eat()
            operator = Operator.from_string(op_token.value)
            if self.in_mood_line:
                operator = operator.invert()
            right = self._parse_multiplicative()
            left = BinaryOpNode(left, operator, right)
        
        return left

    def _parse_multiplicative(self) -> ExprNode:
        left = self._parse_unary()
        
        while self._peek() and self._peek().token_type.is_multiplicative_operator():
            op_token = self._eat()
            operator = Operator.from_string(op_token.value)
            if self.in_mood_line:
                operator = operator.invert()
            right = self._parse_unary()
            left = BinaryOpNode(left, operator, right)
        
        return left

    def _parse_unary(self) -> Union[FactorNode, UnaryOpNode]:
        token = self._peek()
        if token and token.token_type == TokenType.NOT:
            self._eat()
            operand = self._parse_unary()
            return UnaryOpNode(NOT, operand)
        return self._parse_value()

    def _parse_value(self) -> Union[FactorNode, ExprNode]:
        token = self._eat()
        if not token:
            raise ValueError("Expected value but reached end of input")

        if token.token_type == TokenType.NUMBER:
            return NumberNode(token.value)
        elif token.token_type == TokenType.VARIABLE_BORDER:
            return self._parse_variable_or_call()
        elif token.token_type in [TokenType.TRUE, TokenType.FALSE]:
            value = FALSE if (token.value == TRUE and self.in_mood_line) else token.value
            value = TRUE if (token.value == FALSE and self.in_mood_line) else value
            return BooleanNode(value)
        elif token.token_type == TokenType.BRACKET:
            expr = self._parse_expression()
            self._expect_token(TokenType.BRACKET)
            return expr
        
        raise ValueError(f"Unexpected token at line {token.line}: {token.value}")

    def _parse_variable_or_call(self) -> Union[FactorNode, ExprNode]:
        raise NotImplementedError("Subclass must implement _parse_variable_or_call")