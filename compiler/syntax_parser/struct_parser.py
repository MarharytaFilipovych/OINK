#!/usr/bin/env python3

from ..node.struct_decl_node import StructDeclNode, StructField
from ..node.function_decl_node import FunctionDeclNode
from ..token.token_type import TokenType
from .token_reader import TokenReader
from .type_parser import TypeParser


class StructParser:
    def __init__(self, reader: TokenReader, declared_structs: set[str], type_parser: TypeParser, parse_member_function_callback):
        self.reader = reader
        self.declared_structs = declared_structs
        self.type_parser = type_parser
        self.parse_member_function_declaration = parse_member_function_callback

    def parse_struct_declaration(self) -> StructDeclNode:
        self.reader.define_line_type(self.reader.peek())

        struct_token, struct_name = self.__parse_struct_header()
        self.__expect_block_border()
        fields, member_functions = self.parse_struct_body()
        self.__expect_block_border()

        return StructDeclNode(struct_name, fields, member_functions, struct_token.line)

    def __parse_struct_header(self) -> tuple:
        struct_token = self.reader.expect_token(TokenType.STRUCT)
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        name_token = self.reader.expect_token(TokenType.VARIABLE)
        struct_name = name_token.value
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        self.reader.expect_line_end()

        if struct_name in self.declared_structs:
            raise ValueError(f"Struct {struct_name} was already declared at line {name_token.line}!")

        self.declared_structs.add(struct_name)
        return struct_token, struct_name

    def __expect_block_border(self):
        self.reader.define_line_type(self.reader.peek())
        self.reader.expect_token(TokenType.BLOCK_BORDER)
        self.reader.expect_line_end()

    def parse_struct_body(self) -> tuple[list[StructField], list[FunctionDeclNode]]:
        fields = []
        member_functions = []

        while True:
            token = self.reader.peek()
            if not token:
                raise ValueError("Struct block must be closed with 🖖🖖🖖!")

            if token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]:
                # FIX: Check if the next token is the block delimiter (meaning it's the closing line)
                if self.reader.peek(1) and self.reader.peek(1).token_type == TokenType.BLOCK_BORDER:
                    break # Found the closing block line, exit loop
                if self.__is_member_function_start():
                    member_functions.append(self.parse_member_function_declaration())
                else:
                    self.reader.define_line_type(token)
                    fields.append(self.parse_struct_field())
            else:
                break

        return fields, member_functions

    def __is_member_function_start(self) -> bool:
        saved_index = self.reader.current_token_index
        self.reader.eat()
        next_token = self.reader.peek()

        if next_token and next_token.token_type == TokenType.BLOCK_BORDER:
            self.reader.current_token_index = saved_index
            return False

        if next_token and next_token.token_type.is_data_type():
            self.reader.eat()
            if self.reader.peek() and self.reader.peek().token_type == TokenType.MEMBER_FUNCTION:
                self.reader.current_token_index = saved_index
                return True

        self.reader.current_token_index = saved_index
        return False

    def parse_struct_field(self) -> StructField:
        mutability_token = self.reader.peek()
        can_mutate = mutability_token.token_type == TokenType.MUT
        if mutability_token.token_type in [TokenType.MUT, TokenType.CONST]:
            self.reader.eat()
        field_type = self.type_parser.parse_type()
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        field_name_token = self.reader.expect_token(TokenType.VARIABLE)
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        self.reader.expect_line_end()
        return StructField(field_type, field_name_token.value, can_mutate)