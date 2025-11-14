#!/usr/bin/env python3
from compiler.node.program_node import ProgramNode
from compiler.node.return_node import ReturnNode
from compiler.node.stmt_node import StmtNode
from compiler.token.token_class import Token
from compiler.token.token_type import TokenType
from .control_flow_parser import ControlFlowParser


class SyntaxParser(ControlFlowParser):
    def __init__(self, tokens: list[Token]):
        super().__init__(tokens)

    def parse_program(self) -> ProgramNode:
        self._skip_newlines()
        struct_declarations = self._parse_struct_declarations()
        function_declarations = self._parse_function_declarations()
        statements = self._parse_statements()
        return_statement = self._parse_program_return()
        self._check_program_end()
        return ProgramNode(struct_declarations, function_declarations, statements, return_statement)

    def _parse_struct_declarations(self):
        declarations = []
        while self._is_struct_declaration():
            declarations.append(self._parse_struct_declaration())
            self._skip_newlines()
        return declarations

    def _parse_function_declarations(self):
        declarations = []
        while self._is_function_declaration():
            declarations.append(self._parse_function_declaration())
            self._skip_newlines()
        return declarations

    def _is_struct_declaration(self) -> bool:
        if not self._peek() or self._peek().token_type != TokenType.SIMPLE_LINE_BORDER:
            return False
        saved = self.current_token_index
        self._eat()
        result = self._peek() and self._peek().token_type == TokenType.STRUCT
        self.current_token_index = saved
        return result

    def _is_function_declaration(self) -> bool:
        if not self._peek() or self._peek().token_type != TokenType.SIMPLE_LINE_BORDER:
            return False
        saved = self.current_token_index
        self._eat()
        next_token = self._peek()
        
        if next_token and next_token.token_type.is_data_type():
            self._eat()
            result = self._peek() and self._peek().token_type == TokenType.FUNCTION
            self.current_token_index = saved
            return result
        
        self.current_token_index = saved
        return False

    def _parse_statements(self) -> list[StmtNode]:
        statements = []
        while True:
            token = self._peek()
            
            if not statements and token and token.token_type == TokenType.THE_END:
                raise ValueError("Program cannot be empty")
            
            if not token or token.token_type == TokenType.THE_END:
                if statements:
                    raise ValueError('Program must end with "# ... expr ... #"')
            
            self._define_line_type(token)
            token = self._peek()
            
            if token.token_type == TokenType.RETURN:
                break
            
            statement = self._parse_statement()
            if statement:
                statements.append(statement)
        
        return statements

    def _parse_program_return(self) -> ReturnNode:
        self._expect_token(TokenType.RETURN)
        return_statement = ReturnNode(self._parse_expression())
        self._expect_token(TokenType.RETURN)
        self._expect_line_end()
        return return_statement

    def _check_program_end(self):
        if self._peek() and self._peek().token_type != TokenType.THE_END:
            raise ValueError(f"Unexpected content after return at line {self._peek().line}")
