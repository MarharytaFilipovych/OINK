#!/usr/bin/env python3

from typing import Optional
from ..node.stmt_node import StmtNode
from ..node.return_node import ReturnNode
from ..node.code_block_node import CodeBlockNode
from ..token.token_class import Token
from ..token.token_type import TokenType
from .token_reader import TokenReader
from .type_parser import TypeParser
from .expression_parser import ExpressionParser
from .function_parser import FunctionParser
from .struct_parser import StructParser
from .statement_parser import StatementParser
from ..node.program_node import ProgramNode


class SyntaxParser:
    def __init__(self, tokens: list[Token]):
        self.reader = TokenReader(tokens)
        self.next_scope_id = 1
        self.declared_structs: set[str] = set()
        self.type_parser = TypeParser(self.reader, self.declared_structs)
        self.expr_parser = ExpressionParser(self.reader, self.declared_structs)
        self.function_parser = FunctionParser(self.reader, self.type_parser, self.parse_code_block)
        self.struct_parser = StructParser(self.reader, self.declared_structs, self.type_parser, self.function_parser.parse_member_function_declaration)
        self.statement_parser = StatementParser(self.reader, self.type_parser, self.expr_parser, self.parse_code_block, self.peek_token, self.check_with_save)

    def peek_token(self, offset=0) -> Optional[Token]:
        idx = self.reader.current_token_index + offset
        if idx < len(self.reader.tokens):
            return self.reader.tokens[idx]
        return None

    def check_with_save(self, check_fn) -> bool:
        saved_index = self.reader.current_token_index
        result = check_fn()
        self.reader.current_token_index = saved_index
        return result

    def parse_program(self) -> ProgramNode:
        self.reader.skip_newlines()
        struct_declarations = []
        function_declarations = []
        while self.peek_and_check_struct() or self.peek_and_check_function():
            if self.peek_and_check_struct():
                struct_declarations.append(self.struct_parser.parse_struct_declaration())
            elif self.peek_and_check_function():
                function_declarations.append(self.function_parser.parse_function_declaration())
            self.reader.skip_newlines()
        
        statements = self.statement_parser.parse_statements()
        if not struct_declarations and not function_declarations and not statements:
            raise ValueError("Program cannot be empty! You have to write something before the return statement!")
        return_statement = self.parse_program_return()
        self.check_program_end()
        return ProgramNode(struct_declarations, function_declarations, statements, return_statement)
    
    def peek_and_check_struct(self) -> bool:
        if not self.reader.peek() or self.reader.peek().token_type != TokenType.SIMPLE_LINE_BORDER:
            return False
        def check_struct_logic():
            self.reader.eat() 
            next_token = self.reader.peek()
            return next_token and next_token.token_type == TokenType.STRUCT
        return self.check_with_save(check_struct_logic)
    
    def peek_and_check_function(self) -> bool:
        if not self.reader.peek() or self.reader.peek().token_type != TokenType.SIMPLE_LINE_BORDER:
            return False
        def check_function():
            self.reader.eat()
            next_token = self.reader.peek()
            if next_token and next_token.token_type.is_data_type():
                self.reader.eat()
                return self.reader.peek() and self.reader.peek().token_type == TokenType.FUNCTION
            return False
        return self.check_with_save(check_function)

    def parse_program_return(self) -> ReturnNode:
        self.reader.expect_token(TokenType.RETURN)
        return_statement = self.expr_parser.parse_expression()
        self.reader.expect_token(TokenType.RETURN)
        self.reader.expect_line_end()
        return ReturnNode(return_statement)

    def check_program_end(self):
        if self.reader.peek() and self.reader.peek().token_type != TokenType.THE_END:
            raise ValueError(f"I did not want you to place this awful content "
                             f"after the return statement at line {self.reader.peek().line}: "
                             f"\"{self.reader.peek().value}\" of the type {self.reader.peek().token_type.name.lower()}!")

    def parse_code_block(self) -> CodeBlockNode:
        self.reader.skip_line_start()
        self.reader.expect_token(TokenType.BLOCK_BORDER)
        self.reader.expect_token(TokenType.SIMPLE_LINE_BORDER)
        self.reader.expect_newline_or_end()
        statements, return_node = self.parse_block_contents()
        self.reader.skip_line_start()
        self.reader.expect_token(TokenType.BLOCK_BORDER)
        self.reader.expect_token(TokenType.SIMPLE_LINE_BORDER)
        self.reader.expect_newline_or_end()
        scope_id = self.next_scope_id
        self.next_scope_id += 1
        return CodeBlockNode(statements, return_node, scope_id)

    def parse_block_contents(self) -> tuple[list[StmtNode], Optional[ReturnNode]]:
        statements = []
        return_node = None
        while True:
            token = self.reader.peek()
            if not token:
                raise ValueError("Code block must be closed with 🐖🐖🐖!")
            if self.__is_block_border_ahead():
                break
            self.reader.define_line_type(token)
            token = self.reader.peek()
            if token.token_type == TokenType.RETURN:
                return_node = self.statement_parser.parse_return()
                self.reader.expect_line_end()
                break
            statement = self.statement_parser.parse_statement()
            if statement:
                statements.append(statement)
        return statements, return_node

    def __is_block_border_ahead(self) -> bool:
        token = self.reader.peek()
        if token.token_type not in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]:
            return False
        saved_index = self.reader.current_token_index
        self.reader.eat()
        next_token = self.reader.peek()
        is_block_border = next_token and next_token.token_type == TokenType.BLOCK_BORDER
        self.reader.current_token_index = saved_index
        return is_block_border
