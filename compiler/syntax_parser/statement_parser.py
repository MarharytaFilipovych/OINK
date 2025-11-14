#!/usr/bin/env python3
from typing import Optional
from compiler.node.stmt_node import StmtNode
from compiler.node.decl_node import DeclNode
from compiler.node.assign_node import AssignNode
from compiler.node.io_nodes import ReadNode, PrintNode
from compiler.token.token_type import TokenType
from .declaration_parser import DeclarationParser


class StatementParser(DeclarationParser):
    def _parse_statement(self) -> Optional[StmtNode]:
        token = self._peek()
        stmt = None
        consumes_own_line_end = False

        if token.token_type in [TokenType.MUT, TokenType.CONST]:
            stmt = self._parse_declaration()
        elif token.token_type == TokenType.VARIABLE_BORDER:
            stmt = self._parse_variable_statement()
        elif token.token_type == TokenType.IF:
            stmt = self._parse_if_statement()
            consumes_own_line_end = True
        elif token.token_type == TokenType.WHILE:
            stmt = self._parse_while_statement()
            consumes_own_line_end = True
        elif token.token_type == TokenType.READ:
            stmt = self._parse_read_statement()
        elif token.token_type == TokenType.PRINT:
            stmt = self._parse_print_statement()
        elif token.token_type == TokenType.BLOCK_BORDER:
            self._eat()
        else:
            raise ValueError(f"Unexpected token at line {token.line}: {token.token_type}")

        if not consumes_own_line_end:
            self._expect_line_end()
        return stmt

    def _parse_variable_statement(self) -> StmtNode:
        saved_index = self.current_token_index
        self._eat()
        self._expect_token(TokenType.VARIABLE)
        self._eat()
        
        next_token = self._peek()
        self.current_token_index = saved_index
        
        if next_token and next_token.token_type == TokenType.MEMBER_ACCESS:
            return self._parse_assignment_or_call()
        elif next_token and next_token.token_type == TokenType.BRACKET:
            return self._parse_function_call_statement()
        else:
            return self._parse_assignment()

    def _parse_declaration(self) -> DeclNode:
        can_mutate = self._peek().token_type == TokenType.MUT
        self._eat()
        var_type = self._parse_type()
        self._expect_token(TokenType.VARIABLE_BORDER)
        token_variable = self._expect_token(TokenType.VARIABLE)
        self._expect_token(TokenType.VARIABLE_BORDER)

        if self._peek() and self._peek().token_type == TokenType.ASSIGNMENT:
            self._eat()
            init_expr = self._parse_expression()
        else:
            init_expr = self._set_default_for_type(var_type)

        return DeclNode(token_variable.value, init_expr, token_variable.line, can_mutate, var_type)

    def _parse_assignment(self) -> AssignNode:
        self._expect_token(TokenType.VARIABLE_BORDER)
        variable_token = self._expect_token(TokenType.VARIABLE)
        self._expect_token(TokenType.VARIABLE_BORDER)
        self._expect_token(TokenType.ASSIGNMENT)
        value_expr = self._parse_expression()
        return AssignNode(variable_token.value, value_expr, variable_token.line)

    def _parse_assignment_or_call(self) -> StmtNode:
        self._expect_token(TokenType.VARIABLE_BORDER)
        var_token = self._expect_token(TokenType.VARIABLE)
        self._expect_token(TokenType.VARIABLE_BORDER)
        
        if self._peek() and self._peek().token_type == TokenType.MEMBER_ACCESS:
            self._eat()
            self._expect_token(TokenType.VARIABLE_BORDER)
            member_token = self._expect_token(TokenType.VARIABLE)
            self._expect_token(TokenType.VARIABLE_BORDER)
            
            if self._peek() and self._peek().token_type == TokenType.BRACKET:
                return self._parse_member_function_call(var_token.value, member_token.value, var_token.line)
            else:
                self._expect_token(TokenType.ASSIGNMENT)
                value_expr = self._parse_expression()
                return AssignNode(f"{var_token.value}_{member_token.value}", value_expr, var_token.line)
        else:
            self._expect_token(TokenType.ASSIGNMENT)
            value_expr = self._parse_expression()
            return AssignNode(var_token.value, value_expr, var_token.line)

    def _parse_read_statement(self) -> ReadNode:
        read_token = self._expect_token(TokenType.READ)
        self._expect_token(TokenType.VARIABLE_BORDER)
        var_token = self._expect_token(TokenType.VARIABLE)
        self._expect_token(TokenType.VARIABLE_BORDER)
        return ReadNode(var_token.value, read_token.line)

    def _parse_print_statement(self) -> PrintNode:
        print_token = self._expect_token(TokenType.PRINT)
        expr = self._parse_expression()
        return PrintNode(expr, print_token.line)

    def _parse_function_call_statement(self):
        raise NotImplementedError("Subclass must implement _parse_function_call_statement")

    def _parse_member_function_call(self, object_name: str, func_name: str, line: int):
        raise NotImplementedError("Subclass must implement _parse_member_function_call")

    def _parse_if_statement(self):
        raise NotImplementedError("Subclass must implement _parse_if_statement")

    def _parse_while_statement(self):
        raise NotImplementedError("Subclass must implement _parse_while_statement")
