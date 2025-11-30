#!/usr/bin/env python3
from typing import Union
from .token_reader import TokenReader
from ..llvm_specifics.data_type import DataType
from ..node.factor_node import FactorNode
from ..node.number_node import NumberNode
from ..node.bool_node import BooleanNode
from ..token.token_type import TokenType
from ..constants import FALSE, LAMBDA


class TypeParser:
    def __init__(self, reader: TokenReader, declared_structs: set[str]):
        self.reader = reader
        self.declared_structs = declared_structs

    def parse_type(self) -> Union[DataType, str]:
        token = self.reader.peek()
        if not token:
            raise ValueError("Expected a type but got nothing!")
        if token.token_type == TokenType.LAMBDA:
            return self.__parse_lambda_type()
        if token.token_type == TokenType.VARIABLE_BORDER:
            return self.__parse_struct_type()
        if token.token_type.is_data_type():
            return self.__parse_builtin_type(token)
        raise ValueError(f"Expected type declaration at line {token.line}!")

    def __parse_lambda_type(self) -> str:
        self.reader.eat()
        return LAMBDA

    def __parse_struct_type(self) -> str:
        self.reader.eat()
        struct_token = self.reader.expect_token(TokenType.VARIABLE)
        struct_name = struct_token.value
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        if struct_name not in self.declared_structs:
            raise ValueError(f"Unknown type {struct_name} at line {struct_token.line}!")
        return struct_name

    def __parse_builtin_type(self, token):
        self.reader.eat()
        match token.token_type:
            case TokenType.I16_TYPE:
                return DataType.I16
            case TokenType.I32_TYPE:
                return DataType.I32
            case TokenType.I64_TYPE:
                return DataType.I64
            case TokenType.BOOL:
                return DataType.BOOL
            case TokenType.VOID:
                return DataType.VOID
            case TokenType.STRING_TYPE:
                return DataType.STRING
        return None

    @staticmethod
    def get_default_for_type(data_type: Union[DataType, str]) -> FactorNode:
        if isinstance(data_type, str):
            raise ValueError(f"Cannot provide default value for type {data_type}")
        if data_type == DataType.BOOL:
            return BooleanNode(FALSE)
        elif data_type in [DataType.I16, DataType.I32, DataType.I64]:
            return NumberNode("0")
        else:
            raise ValueError(f"No default value defined for {data_type.name.lower()}")