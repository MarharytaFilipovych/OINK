#!/usr/bin/env python3
from typing import Union
from .token_reader import TokenReader
from ..llvm_specifics.data_type import DataType
from ..node.factor_node import FactorNode
from ..node.number_node import NumberNode
from ..node.bool_node import BooleanNode
from ..token.token_type import TokenType
from ..constants import  FALSE


class TypeParser:
    def __init__(self, reader: TokenReader, declared_structs: set[str]):
        self.reader = reader
        self.declared_structs = declared_structs

    def parse_type(self) -> Union[DataType, str]:
        token = self.reader.peek()
        if not token:
            raise ValueError("Expected a type but got nothing!")

        if token.token_type == TokenType.VARIABLE_BORDER:
            self.reader.eat()
            struct_token = self.reader.expect_token(TokenType.VARIABLE)
            struct_name = struct_token.value
            self.reader.expect_token(TokenType.VARIABLE_BORDER)
            if struct_name not in self.declared_structs:
                raise ValueError(f"Unknown type {struct_name} at line {struct_token.line}!")
            return struct_name

        if token.token_type.is_data_type():
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

        raise ValueError(f"Expected type declaration at line {token.line}!")

    @staticmethod
    def get_default_for_type(data_type: DataType) -> FactorNode:
        if data_type == DataType.BOOL:
            return BooleanNode(FALSE)
        elif data_type in [DataType.I16, DataType.I32, DataType.I64]:
            return NumberNode("0")
        else:
            raise ValueError(f"No default value defined for {data_type.name.lower()}")
