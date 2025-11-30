#!/usr/bin/env python3
from typing import Union
from ..node.intr_string_node import InterpolatedStringNode
from ..node.string_node import StringNode
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
from ..llvm_specifics.data_type import DataType
from ..node.lambda_node import LambdaNode, LambdaParam
from ..constants import get_token_display_name


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
        token = self.reader.peek()
        if token and token.token_type == TokenType.STRING:
            return self.__parse_string_or_interpolated()
        if token and token.token_type == TokenType.LAMBDA:
            return self.parse_lambda()
        token = self.reader.eat()
        if not token:
            self.__raise_no_value_error()
        return self.__handle_value_token(token)

    def __parse_string_or_interpolated(self):
        parts = []
        line = self.reader.peek().line

        while self.reader.peek() and self.reader.peek().token_type in [TokenType.STRING, TokenType.INTERP_STRING]:
            token = self.reader.peek()
            
            if token.token_type == TokenType.STRING:
                string_token = self.reader.eat()
                parts.append(('text', string_token.value))
            elif token.token_type == TokenType.INTERP_STRING:
                self.reader.eat()
                expr = self.parse_expression()
                parts.append(('expr', expr))
                self.reader.expect_token(TokenType.INTERP_STRING)

        if len(parts) == 1 and parts[0][0] == 'text':
            return StringNode(parts[0][1], line)
        
        return InterpolatedStringNode(parts, line)

    def __raise_no_value_error(self):
        line = self.reader.peek() - 1 if self.reader.peek() > 1 else self.reader.peek()
        raise ValueError(
            f"You should have written sth, "
            f"but you decided to abandon your work at line {line}!")

    def __handle_value_token(self, token) -> Union[FactorNode, ExprNode]:
        match token.token_type:
            case TokenType.NUMBER:
                return NumberNode(token.value)
            case TokenType.VARIABLE_BORDER:
                return self.parse_variable_or_call()
            case TokenType.TRUE | TokenType.FALSE:
                return self.__parse_boolean_token(token)
            case TokenType.EXPRESSION_GROUP:
                expr = self.parse_expression()
                self.reader.expect_token(TokenType.EXPRESSION_GROUP)
                return expr
            case _:
                raise ValueError(
                    f"You should have used sth valuable "
                    f"at line {token.line}, not \"{token.value}\" ({get_token_display_name(token.token_type.name)})!"
                )

    def __parse_boolean_token(self, token) -> BooleanNode:
        value = token.value
        if self.reader.in_mood_line:
            value = FALSE if value == TRUE else TRUE
        return BooleanNode(value)

    def parse_variable_or_call(self) -> Union[FactorNode, ExprNode]:
        var_token = self.reader.expect_token(TokenType.VARIABLE)
        var_name = var_token.value
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        
        is_separator_pattern = (
            self.reader.peek() and self.reader.peek().token_type == TokenType.BRACKET and 
            self.reader.peek(1) and self.reader.peek(1).token_type == TokenType.BRACKET)
        
        if self.__is_struct_initialization(var_name):
            return self.parse_struct_init(var_name, var_token.line)
            
        if self.__is_member_access():
            return self.__parse_member_access(var_name, var_token.line)
        
        if self.__is_function_call() and not is_separator_pattern:
            return self.parse_function_call_expr(var_name, var_token.line)
            
        return self.parse_function_call_expr(var_name, var_token.line) \
            if self.__is_function_call() and not is_separator_pattern \
            else IDNode(var_name, var_token.line)

    def __is_struct_initialization(self, var_name: str) -> bool:
        return var_name in self.declared_structs and self.reader.peek() and self.reader.peek().token_type == TokenType.BRACKET

    def __is_member_access(self) -> bool:
        return self.reader.peek() and self.reader.peek().token_type == TokenType.MEMBER_ACCESS

    def __parse_member_access(self, var_name: str, line: int) -> Union[MemberAccessNode, ExprNode]:
        self.reader.eat()
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        member_token = self.reader.expect_token(TokenType.VARIABLE)
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        return self.parse_member_function_call(var_name, member_token.value, line) \
        if self.reader.peek() and self.reader.peek().token_type == TokenType.BRACKET \
        else MemberAccessNode(var_name, member_token.value, line)
        
    def __is_function_call(self) -> bool:
        next_token = self.reader.peek()
        if next_token and next_token.token_type == TokenType.BRACKET:
            token_after_bracket = self.reader.peek(1)
            if token_after_bracket and token_after_bracket.token_type in [
                TokenType.RETURN,
                TokenType.SIMPLE_LINE_BORDER,
                TokenType.MOOD_LINE_BORDER_END]:
                return False
            return True
        return False

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
        if self.__should_parse_first_argument():
            arguments.append(self.parse_value())
            self.__parse_additional_arguments(arguments)
        return arguments

    def __should_parse_first_argument(self) -> bool:
        token = self.reader.peek()
        if not token:
            return False
        if token.token_type == TokenType.BRACKET:
            return False
        return True

    def __parse_additional_arguments(self, arguments: list[ExprNode]):
        i = len(arguments)
        while True:
            i += 1
            saved_index = self.reader.current_token_index
            if self.reader.peek() and self.reader.peek().token_type == TokenType.BRACKET and \
               self.reader.peek(1) and self.reader.peek(1).token_type == TokenType.BRACKET:
                self.reader.eat()
                self.reader.eat()
                arguments.append(self.parse_value())
            else:
                self.reader.current_token_index = saved_index
                break

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
            implicit_arg = prev_call
            self.reader.expect_token(TokenType.BRACKET)
            arguments = self.parse_arguments()
            self.reader.expect_token(TokenType.BRACKET)
            arguments.insert(0, implicit_arg)
            prev_call = FunctionCallNode(func_token.value, arguments, line, None)
        return prev_call

    def parse_struct_init(self, struct_name: str, line: int) -> StructInitNode:
        self.reader.expect_token(TokenType.BRACKET)
        init_exprs = self.parse_arguments()        
        self.reader.expect_token(TokenType.BRACKET)
        return StructInitNode(struct_name, init_exprs, line)

    def parse_lambda(self) -> LambdaNode:
        lambda_token = self.reader.expect_token(TokenType.LAMBDA)
        self.reader.expect_token(TokenType.BRACKET)
        params = self.__parse_lambda_parameters()
        self.reader.expect_token(TokenType.BRACKET)
        self.reader.expect_token(TokenType.LAMBDA)
        body = self.parse_expression()
        self.reader.expect_token(TokenType.LAMBDA)
        return LambdaNode(params, body, lambda_token.line)

    def __parse_lambda_parameters(self) -> list:
        params = []
        if self.reader.peek() and self.reader.peek().token_type != TokenType.BRACKET:
            params.append(self.parse_lambda_param())
            while True:
                saved_index = self.reader.current_token_index
                
                if self.reader.peek() and self.reader.peek().token_type == TokenType.BRACKET and \
                   self.reader.peek(1) and self.reader.peek(1).token_type == TokenType.BRACKET:
                    self.reader.eat()
                    self.reader.eat()
                    params.append(self.parse_lambda_param())
                else:
                    self.reader.current_token_index = saved_index
                    break
        return params

    def parse_lambda_param(self) -> LambdaParam:
        param_type = self.__parse_lambda_param_type()
        param_name = self.__parse_lambda_param_name()
        return LambdaParam(param_type, param_name)

    def __parse_lambda_param_type(self):
        token = self.reader.peek()
        if not token or not (token.token_type.is_data_type() or token.token_type == TokenType.VARIABLE_BORDER):
            raise ValueError(f"Expected type in lambda parameter at line {token.line if token else 'unknown'}!")

        if token.token_type == TokenType.VARIABLE_BORDER:
            self.reader.eat()
            type_token = self.reader.expect_token(TokenType.VARIABLE)
            param_type = type_token.value
            self.reader.expect_token(TokenType.VARIABLE_BORDER)
        else:
            type_token = self.reader.eat()
            param_type = {
                TokenType.I16_TYPE: DataType.I16,
                TokenType.I32_TYPE: DataType.I32,
                TokenType.I64_TYPE: DataType.I64,
                TokenType.BOOL: DataType.BOOL
            }.get(type_token.token_type, DataType.I32)

        return param_type

    def __parse_lambda_param_name(self):
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        name_token = self.reader.expect_token(TokenType.VARIABLE)
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        return name_token.value