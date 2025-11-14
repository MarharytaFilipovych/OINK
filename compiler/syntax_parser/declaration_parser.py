#!/usr/bin/env python3
from compiler.node.function_decl_node import FunctionDeclNode, FunctionParam
from compiler.node.struct_decl_node import StructDeclNode, StructField
from compiler.node.code_block_node import CodeBlockNode
from compiler.token.token_type import TokenType
from .expression_parser import ExpressionParser


class DeclarationParser(ExpressionParser):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.declared_structs = set()
        self.next_scope_id = 1

    def _parse_struct_declaration(self) -> StructDeclNode:
        struct_name, struct_token_line = self._parse_struct_header()
        self._parse_struct_border()
        fields, member_functions = self._parse_struct_body()
        self._parse_struct_border()
        return StructDeclNode(struct_name, fields, member_functions, struct_token_line)

    def _parse_struct_header(self) -> tuple[str, int]:
        self._define_line_type(self._peek())
        struct_token = self._expect_token(TokenType.STRUCT)
        self._expect_token(TokenType.VARIABLE_BORDER)
        name_token = self._expect_token(TokenType.VARIABLE)
        struct_name = name_token.value
        self._expect_token(TokenType.VARIABLE_BORDER)
        self._expect_line_end()
        if struct_name in self.declared_structs:
            raise ValueError(f"Struct '{struct_name}' already declared at line {name_token.line}")
        self.declared_structs.add(struct_name)
        return struct_name, struct_token.line

    def _parse_struct_border(self):
        self._define_line_type(self._peek())
        self._expect_token(TokenType.BLOCK_BORDER)
        self._expect_line_end()

    def _parse_struct_body(self):
        fields = []
        member_functions = []
        
        while True:
            token = self._peek()
            if not token:
                raise ValueError("Struct block must be closed with 🐖🐖🐖")
            
            if token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]:
                saved_index = self.current_token_index
                self._eat()
                next_token = self._peek()
                
                if next_token and next_token.token_type == TokenType.BLOCK_BORDER:
                    self.current_token_index = saved_index
                    break
                
                if self._is_member_function_declaration():
                    self.current_token_index = saved_index
                    member_functions.append(self._parse_function_declaration())
                    continue
                
                self.current_token_index = saved_index
                self._define_line_type(token)
                fields.append(self._parse_field())
            else:
                break
        
        return fields, member_functions

    def _is_member_function_declaration(self) -> bool:
        if not self._peek() or not self._peek().token_type.is_data_type():
            return False
        saved = self.current_token_index
        self._eat()
        result = self._peek() and self._peek().token_type == TokenType.MEMBER_FUNCTION
        self.current_token_index = saved
        return result

    def _parse_field(self) -> StructField:
        mutability_token = self._peek()
        can_mutate = mutability_token.token_type == TokenType.MUT
        if mutability_token.token_type in [TokenType.MUT, TokenType.CONST]:
            self._eat()
        
        field_type = self._parse_type()
        self._expect_token(TokenType.VARIABLE_BORDER)
        field_name_token = self._expect_token(TokenType.VARIABLE)
        self._expect_token(TokenType.VARIABLE_BORDER)
        self._expect_line_end()
        
        return StructField(field_type, field_name_token.value, can_mutate)

    def _parse_function_declaration(self) -> FunctionDeclNode:
        self._define_line_type(self._peek())
        return_type = self._parse_type()
        self._expect_token(TokenType.FUNCTION)
        func_name, params = self._parse_function_signature()
        self._expect_line_end()
        body = self._parse_code_block()
        return FunctionDeclNode(func_name.value, params, return_type, body, func_name.line)

    def _parse_function_signature(self):
        self._expect_token(TokenType.VARIABLE_BORDER)
        func_name_token = self._expect_token(TokenType.VARIABLE)
        self._expect_token(TokenType.VARIABLE_BORDER)
        params = self._parse_parameters()
        return func_name_token, params

    def _parse_parameters(self):
        params = []
        while self._peek() and self._peek().token_type == TokenType.BRACKET:
            self._eat()
            param_type = self._parse_type()
            self._expect_token(TokenType.VARIABLE_BORDER)
            param_name_token = self._expect_token(TokenType.VARIABLE)
            self._expect_token(TokenType.VARIABLE_BORDER)
            self._expect_token(TokenType.BRACKET)
            params.append(FunctionParam(param_type, param_name_token.value))
        return params

    def _parse_code_block(self) -> CodeBlockNode:
        raise NotImplementedError("Subclass must implement _parse_code_block")
