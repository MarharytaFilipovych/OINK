#!/usr/bin/env python3
from typing import Optional
from compiler.node.if_node import IfNode
from compiler.node.elif_node import ElifNode
from compiler.node.while_node import WhileNode
from compiler.node.code_block_node import CodeBlockNode
from compiler.node.return_node import ReturnNode
from compiler.node.stmt_node import StmtNode
from compiler.node.unary_op_node import UnaryOpNode
from compiler.token.token_type import TokenType
from compiler.constants import NOT
from .function_call_parser import FunctionCallParser


class ControlFlowParser(FunctionCallParser):
    def _parse_if_statement(self) -> IfNode:
        if_token = self._expect_token(TokenType.IF)
        condition = self._parse_condition("If", if_token.line)

        then_block = self._parse_code_block()
        elif_blocks = self._parse_elif_blocks()
        else_block = self._try_parse_else_block()

        return IfNode(condition, then_block, elif_blocks, else_block, if_token.line)

    def _parse_elif_block(self) -> ElifNode:
        self._skip_line_start()
        elif_token = self._expect_token(TokenType.ELIF)

        condition = self._parse_condition("Elif", elif_token.line)
        then_block = self._parse_code_block()

        return ElifNode(condition, then_block, elif_token.line)

    def _parse_while_statement(self) -> WhileNode:
        while_token = self._expect_token(TokenType.WHILE)
        condition = self._parse_condition("While", while_token.line)
        body = self._parse_code_block()
        return WhileNode(condition, body, while_token.line)

    def _parse_condition(self, keyword: str, line: int):
        if not self._peek() or self._peek().token_type in (
            TokenType.MOOD_LINE_BORDER_END,
            TokenType.SIMPLE_LINE_BORDER,):
            raise ValueError(f"{keyword} condition missing at line {line}")
        condition = self._parse_expression()
        if self.in_mood_line:
            condition = UnaryOpNode(NOT, condition)
        return condition

    def _parse_elif_blocks(self):
        blocks = []
        while self._peek_for_token_after_line_start(TokenType.ELIF):
            blocks.append(self._parse_elif_block())
        return blocks

    def _try_parse_else_block(self) -> Optional[CodeBlockNode]:
        if not self._peek_for_token_after_line_start(TokenType.ELSE):
            return None
        self._skip_line_start()
        self._eat()
        return self._parse_code_block()

    def _parse_code_block(self) -> CodeBlockNode:
        self._expect_line_end()
        self._skip_line_start()
        self._expect_token(TokenType.BLOCK_BORDER)
        self._expect_line_end()

        statements, return_node = self._parse_block_contents()

        self._skip_line_start()
        self._expect_token(TokenType.BLOCK_BORDER)
        self._expect_line_end()

        scope_id = self.next_scope_id
        self.next_scope_id += 1

        return CodeBlockNode(statements, return_node, scope_id)

    def _parse_block_contents(self) -> tuple[list[StmtNode], Optional[ReturnNode]]:
        statements = []
        return_node = None

        while True:
            token = self._peek()
            if not token:
                raise ValueError("Code block must be closed with 🐖🐖🐖")
            if token.token_type in (
                TokenType.SIMPLE_LINE_BORDER,
                TokenType.MOOD_LINE_BORDER_START,):
                if self._is_block_end():
                    break
            self._define_line_type(token)
            token = self._peek()
            if token.token_type == TokenType.RETURN:
                return_node = self._parse_return()
                self._expect_line_end()
                break
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        return statements, return_node

    def _is_block_end(self) -> bool:
        saved = self.current_token_index
        self._eat()
        next_token = self._peek()
        self.current_token_index = saved
        return next_token and next_token.token_type == TokenType.BLOCK_BORDER

    def _parse_return(self) -> ReturnNode:
        self._expect_token(TokenType.RETURN)
        expr = self._parse_expression()
        return ReturnNode(expr)
