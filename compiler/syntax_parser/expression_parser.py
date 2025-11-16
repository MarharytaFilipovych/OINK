#!/usr/bin/env python3
from typing import Union

from ..constants import FALSE, TRUE, NOT
from ..node.expr_node import ExprNode
from ..node.factor_node import FactorNode
from ..node.number_node import NumberNode
from ..node.bool_node import BooleanNode
from ..node.unary_op_node import UnaryOpNode
from ..node.binary_op_node import BinaryOpNode
from ..node.id_node import IDNode
from ..node.function_call_node import FunctionCallNode
from ..node.struct_init_node import StructInitNode
from ..node.member_access_node import MemberAccessNode
from ..llvm_specifics.operator import Operator
from ..token.token_type import TokenType
from .token_reader import TokenReader


class ExpressionParser:
    def __init__(self, reader: TokenReader, declared_structs: set[str]):
        self.reader = reader
        self.declared_structs = declared_structs

    def parse_expression(self) -> ExprNode:
        return self.parse_logical_or()

    def parse_logical_or(self) -> ExprNode:
        left = self.parse_logical_and()
        while self.reader.peek() and self.reader.peek().token_type == TokenType.OR:
            self.reader.eat()
            right = self.parse_logical_and()
            left = BinaryOpNode(left, Operator.OR, right)
        return left

    def parse_logical_and(self) -> ExprNode:
        left = self.parse_comparison()
        while self.reader.peek() and self.reader.peek().token_type == TokenType.AND:
            self.reader.eat()
            right = self.parse_comparison()
            left = BinaryOpNode(left, Operator.AND, right)
        return left

    def parse_comparison(self) -> ExprNode:
        left = self.parse_additive()
        token = self.reader.peek()
        if token and token.token_type.if_for_comparision():
            op_token = self.reader.eat()
            operator = Operator.from_string(op_token.value)
            if self.reader.in_mood_line:
                operator = operator.invert()
            right = self.parse_additive()
            left = BinaryOpNode(left, operator, right)
        return left

    def parse_additive(self) -> ExprNode:
        left = self.parse_multiplicative()
        while True:
            token = self.reader.peek()
            if not token or not token.token_type.is_additive_operator():
                break
            op_token = self.reader.eat()
            operator = Operator.from_string(op_token.value)
            if self.reader.in_mood_line:
                operator = operator.invert()
            right = self.parse_multiplicative()
            left = BinaryOpNode(left, operator, right)
        return left

    def parse_multiplicative(self) -> ExprNode:
        left = self.parse_unary()

        while True:
            token = self.reader.peek()
            if not token or not token.token_type.is_multiplicative_operator():
                break

            op_token = self.reader.eat()
            operator = Operator.from_string(op_token.value)

            if self.reader.in_mood_line:
                operator = operator.invert()

            right = self.parse_unary()
            left = BinaryOpNode(left, operator, right)

        return left

    def parse_unary(self) -> Union[FactorNode, UnaryOpNode]:
        token = self.reader.peek()

        if token and token.token_type == TokenType.NOT:
            self.reader.eat()
            operand = self.parse_unary()
            return UnaryOpNode(NOT, operand)

        return self.parse_value()

    def parse_value(self) -> Union[FactorNode, ExprNode]:
        token = self.reader.eat()

        if not token:
            raise ValueError(
                "You should have used either a number, a variable, or a boolean, "
                "but you decided to abandon your work!")

        match token.token_type:
            case TokenType.NUMBER:
                return NumberNode(token.value)
            case TokenType.VARIABLE_BORDER:
                return self.parse_variable_or_call()
            case TokenType.TRUE | TokenType.FALSE:
                value = token.value
                if self.reader.in_mood_line:
                    value = FALSE if value == TRUE else TRUE
                return BooleanNode(value)
            case TokenType.BRACKET:
                expr = self.parse_expression()
                self.reader.expect_token(TokenType.BRACKET)
                return expr
            case _:
                raise ValueError(
                    f"You should have used either a number, a variable, or a boolean "
                    f"at line {token.line}, not {token.value}!")

    def parse_variable_or_call(self) -> Union[FactorNode, ExprNode]:
        var_token = self.reader.expect_token(TokenType.VARIABLE)
        var_name = var_token.value
        self.reader.expect_token(TokenType.VARIABLE_BORDER)

        if var_name in self.declared_structs and self.reader.peek() and self.reader.peek().token_type == TokenType.BRACKET:
            return self.parse_struct_init(var_name, var_token.line)

        if self.reader.peek() and self.reader.peek().token_type == TokenType.MEMBER_ACCESS:
            self.reader.eat()
            self.reader.expect_token(TokenType.VARIABLE_BORDER)
            member_token = self.reader.expect_token(TokenType.VARIABLE)
            self.reader.expect_token(TokenType.VARIABLE_BORDER)

            if self.reader.peek() and self.reader.peek().token_type == TokenType.BRACKET:
                return self.parse_member_function_call(var_name, member_token.value, var_token.line) \
                if self.reader.peek() and self.reader.peek().token_type == TokenType.BRACKET \
                else MemberAccessNode(var_name, member_token.value, var_token.line)

        return self.parse_function_call_expr(var_name, var_token.line) \
             if self.reader.peek() and self.reader.peek().token_type == TokenType.BRACKET \
                else IDNode(var_name, var_token.line)

    def parse_function_call_expr(self, func_name: str = None, line: int = None) -> FunctionCallNode:
        if func_name is None:
            self.reader.expect_token(TokenType.VARIABLE_BORDER)
            func_token = self.reader.expect_token(TokenType.VARIABLE)
            func_name = func_token.value
            line = func_token.line
            self.reader.expect_token(TokenType.VARIABLE_BORDER)

        self.reader.expect_token(TokenType.BRACKET)
        arguments = self.parse_arguments()
        self.reader.expect_token(TokenType.BRACKET)

        result = FunctionCallNode(func_name, arguments, line, None)
        if self.reader.peek() and self.reader.peek().token_type == TokenType.MEMBER_ACCESS:
            result = self.parse_function_chain(result, line)
        return result

    def parse_arguments(self) -> list[ExprNode]:
        arguments = []
        if self.reader.peek() and self.reader.peek().token_type != TokenType.BRACKET:
            arguments.append(self.parse_expression())
            while self.reader.peek() and self.reader.peek().token_type == TokenType.BRACKET:
                saved_index = self.reader.current_token_index
                self.reader.eat()

                if self.reader.peek() and self.reader.peek().token_type == TokenType.BRACKET:
                    self.reader.eat()
                    arguments.append(self.parse_expression())
                else:
                    self.reader.current_token_index = saved_index
                    break
        return arguments

    def parse_member_function_call(self, object_name: str, func_name: str, line: int) -> FunctionCallNode:
        self.reader.expect_token(TokenType.BRACKET)
        arguments = self.parse_arguments()
        self.reader.expect_token(TokenType.BRACKET)

        if self.reader.peek() and self.reader.peek().token_type == TokenType.MEMBER_ACCESS:
            result = FunctionCallNode(func_name, arguments, line, object_name)
            return self.parse_function_chain(result, line)

        return FunctionCallNode(func_name, arguments, line, object_name)

    def parse_function_chain(self, prev_call: FunctionCallNode, line: int) -> FunctionCallNode:
        while self.reader.peek() and self.reader.peek().token_type == TokenType.MEMBER_ACCESS:
            self.reader.eat()
            self.reader.expect_token(TokenType.VARIABLE_BORDER)
            func_token = self.reader.expect_token(TokenType.VARIABLE)
            self.reader.expect_token(TokenType.VARIABLE_BORDER)
            self.reader.expect_token(TokenType.BRACKET)
            arguments = self.parse_arguments()
            self.reader.expect_token(TokenType.BRACKET)
            arguments.insert(0, prev_call)
            prev_call = FunctionCallNode(func_token.value, arguments, line, None)
        return prev_call

    def parse_struct_init(self, struct_name: str, line: int) -> StructInitNode:
        self.reader.expect_token(TokenType.BRACKET)
        init_exprs = self.parse_arguments()
        self.reader.expect_token(TokenType.BRACKET)
        return StructInitNode(struct_name, init_exprs, line)