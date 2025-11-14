#!/usr/bin/env python3
from typing import Union
from ..node.function_call_node import FunctionCallNode
from ..node.struct_init_node import StructInitNode
from ..node.id_node import IDNode
from ..node.factor_node import FactorNode
from ..node.expr_node import ExprNode
from ..token.token_type import TokenType
from .statement_parser import StatementParser
from ..node.member_access_node import MemberAccessNode


class FunctionCallParser(StatementParser):
    def _parse_function_call_statement(self) -> FunctionCallNode:
        return self._parse_function_call_expr()

    def _parse_variable_or_call(self) -> Union[FactorNode, ExprNode]:
        var_token = self._expect_token(TokenType.VARIABLE)
        self._expect_token(TokenType.VARIABLE_BORDER)

        if self._peek() and self._peek().token_type == TokenType.MEMBER_ACCESS:
            return self._parse_member_access_or_call(var_token)

        if self._peek() and self._peek().token_type == TokenType.BRACKET:
            return self._parse_function_call_expr(var_token.value, var_token.line)

        if var_token.value in self.declared_structs and self._peek() and self._peek().token_type == TokenType.BRACKET:
            return self._parse_struct_init(var_token.value, var_token.line)

        return IDNode(var_token.value, var_token.line)

    def _parse_member_access_or_call(self, var_token):
        self._eat()
        self._expect_token(TokenType.VARIABLE_BORDER)
        member_token = self._expect_token(TokenType.VARIABLE)
        self._expect_token(TokenType.VARIABLE_BORDER)
        return self._parse_member_function_call(var_token.value, member_token.value, var_token.line) \
                if self._peek() and self._peek().token_type == TokenType.BRACKET \
                else MemberAccessNode(var_token.value, member_token.value, var_token.line)

    def _parse_function_call_expr(self, func_name: str = None, line: int = None) -> FunctionCallNode:
        if func_name is None:
            self._expect_token(TokenType.VARIABLE_BORDER)
            func_token = self._expect_token(TokenType.VARIABLE)
            func_name = func_token.value
            line = func_token.line
            self._expect_token(TokenType.VARIABLE_BORDER)

        arguments = self._parse_arguments()
        result = FunctionCallNode(func_name, arguments, line, None)

        if self._peek() and self._peek().token_type == TokenType.MEMBER_ACCESS:
            result = self._parse_function_chain(result, line)

        return result

    def _parse_member_function_call(self, object_name: str, func_name: str, line: int) -> FunctionCallNode:
        arguments = self._parse_arguments()
        result = FunctionCallNode(func_name, arguments, line, object_name)

        if self._peek() and self._peek().token_type == TokenType.MEMBER_ACCESS:
            result = self._parse_function_chain(result, line)

        return result

    def _parse_arguments(self):
        self._expect_token(TokenType.BRACKET)
        arguments = []

        if self._peek() and self._peek().token_type != TokenType.BRACKET:
            arguments.append(self._parse_expression())

            while self._peek() and self._peek().token_type == TokenType.BRACKET:
                saved_index = self.current_token_index
                self._eat()
                if self._peek() and self._peek().token_type == TokenType.BRACKET:
                    self.current_token_index = saved_index
                    break
                self._eat()
                arguments.append(self._parse_expression())

        self._expect_token(TokenType.BRACKET)
        return arguments

    def _parse_function_chain(self, prev_call: FunctionCallNode, line: int) -> FunctionCallNode:
        while self._peek() and self._peek().token_type == TokenType.MEMBER_ACCESS:
            self._eat()
            self._expect_token(TokenType.VARIABLE_BORDER)
            func_token = self._expect_token(TokenType.VARIABLE)
            self._expect_token(TokenType.VARIABLE_BORDER)
            prev_call = FunctionCallNode(func_token.value, [prev_call], line, None)
        return prev_call

    def _parse_struct_init(self, struct_name: str, line: int) -> StructInitNode:
        init_exprs = self._parse_arguments()
        return StructInitNode(struct_name, init_exprs, line)
