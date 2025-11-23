#!/usr/bin/env python3

from ..llvm_specifics.data_type import DataType
from ..node.function_decl_node import FunctionDeclNode, FunctionParam
from ..token.token_class import Token
from ..token.token_type import TokenType
from .token_reader import TokenReader
from .type_parser import TypeParser


class FunctionParser:
    def __init__(self, reader: TokenReader, type_parser: TypeParser, parse_code_block_callback):
        self.reader = reader
        self.type_parser = type_parser
        self.parse_code_block = parse_code_block_callback

    def parse_function_like(self, is_member=False) -> FunctionDeclNode:
        self.reader.define_line_type(self.reader.peek())
        return_type = self.type_parser.parse_type()
        func_name_token = self.__parse_function_name(is_member)
        params = self.parse_function_params()
        self.reader.expect_line_end()
        body = self.parse_code_block()
        self.__validate_function_return(func_name_token, return_type, body, is_member)
        return FunctionDeclNode(func_name_token.value, params, return_type, body, func_name_token.line)

    def __parse_function_name(self, is_member) -> 'Token':
        keyword = TokenType.MEMBER_FUNCTION if is_member else TokenType.FUNCTION
        self.reader.expect_token(keyword)
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        func_name_token = self.reader.expect_token(TokenType.VARIABLE)
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        return func_name_token

    @staticmethod
    def __validate_function_return(func_name_token, return_type, body, is_member):
        if return_type != DataType.VOID and body.return_node is None:
            kind = "Member function" if is_member else "Function"
            raise ValueError(
                f"{kind} \"{func_name_token.value}\" with return type must have a return statement at line {func_name_token.line}!")

    def parse_function_declaration(self) -> FunctionDeclNode:
        return self.parse_function_like(False)

    def parse_member_function_declaration(self) -> FunctionDeclNode:
        return self.parse_function_like(True)

    def parse_function_params(self) -> list[FunctionParam]:
        params = []
        while self.reader.peek() and self.reader.peek().token_type == TokenType.BRACKET:
            self.reader.eat()
            param_type = self.type_parser.parse_type()
            self.reader.expect_token(TokenType.VARIABLE_BORDER)
            param_name_token = self.reader.expect_token(TokenType.VARIABLE)
            self.reader.expect_token(TokenType.VARIABLE_BORDER)
            self.reader.expect_token(TokenType.BRACKET)
            params.append(FunctionParam(param_type, param_name_token.value))
        return params