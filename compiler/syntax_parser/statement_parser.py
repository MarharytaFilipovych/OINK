#!/usr/bin/env python3

from typing import Optional, Union
from ..constants import NOT
from ..node.function_call_node import FunctionCallNode
from ..node.print_node import PrintNode
from ..node.unary_op_node import UnaryOpNode
from ..node.stmt_node import StmtNode
from ..node.return_node import ReturnNode
from ..node.read_node import ReadNode
from ..node.assign_node import AssignNode
from ..node.decl_node import DeclNode
from ..node.if_node import IfNode
from ..node.elif_node import ElifNode
from ..node.while_node import WhileNode
from ..node.code_block_node import CodeBlockNode
from ..token.token_class import Token
from ..token.token_type import TokenType
from .token_reader import TokenReader
from .type_parser import TypeParser
from .expression_parser import ExpressionParser


class StatementParser:
    def __init__(self, reader: TokenReader, type_parser: TypeParser, expr_parser: ExpressionParser, parse_code_block_callback, peek_token_callback, check_with_save_callback):
        self.reader = reader
        self.type_parser = type_parser
        self.expr_parser = expr_parser
        self.parse_code_block = parse_code_block_callback
        self.peek_token = peek_token_callback
        self.check_with_save = check_with_save_callback

    def parse_statements(self) -> list[StmtNode]:
        statements = []
        while True:
            token = self.reader.peek()
            if not token or token.token_type == TokenType.THE_END:
                if len(statements) > 0:
                    raise ValueError('Program must end with "# ... expr ... #"!')
                break
            self.reader.define_line_type(token)
            token = self.reader.peek()
            if token.token_type == TokenType.RETURN:
                break
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        return statements

    def parse_statement(self) -> Optional[StmtNode]:
        token = self.reader.peek()
        stmt = None
        consumes_own_line_end = False
        match token.token_type:
            case TokenType.MUT | TokenType.CONST:
                stmt = self.parse_declaration()
            case TokenType.VARIABLE_BORDER:
                stmt = self.parse_variable_statement()
            case TokenType.IF:
                stmt = self.parse_if_statement()
                consumes_own_line_end = True
            case TokenType.WHILE:
                stmt = self.parse_while_statement()
                consumes_own_line_end = True
            case TokenType.READ:
                stmt = self.parse_read_statement()
            case TokenType.PRINT:
                stmt = self.parse_print_statement()
            case TokenType.BLOCK_BORDER:
                self.reader.eat()
            case _:
                raise ValueError(f"You should have either declared a variable, assigned this cutie to sth, "
                                 f"or used control flow at line {token.line}, but you decided to use "
                                 f"this token \"{token.value}\" of the type \"{token.token_type.name.lower()}\"")
        if not consumes_own_line_end:
            self.reader.expect_line_end()
        return stmt

    def parse_variable_statement(self) -> Union[StmtNode, FunctionCallNode, AssignNode]:
        saved_index = self.reader.current_token_index
        self.reader.eat()
        self.reader.expect_token(TokenType.VARIABLE)
        self.reader.eat()
        next_token = self.reader.peek()
        if next_token and next_token.token_type == TokenType.MEMBER_ACCESS:
            self.reader.current_token_index = saved_index
            return self.parse_assignment_or_call()
        elif next_token and next_token.token_type == TokenType.BRACKET:
            self.reader.current_token_index = saved_index
            return self.expr_parser.parse_function_call_expr()
        else:
            self.reader.current_token_index = saved_index
            return self.parse_assignment()

    def parse_read_statement(self) -> ReadNode:
        read_token = self.reader.expect_token(TokenType.READ)
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        var_token = self.reader.expect_token(TokenType.VARIABLE)
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        return ReadNode(var_token.value, read_token.line)

    def parse_print_statement(self) -> PrintNode:
        print_token = self.reader.expect_token(TokenType.PRINT)
        expr = self.expr_parser.parse_expression()
        return PrintNode(expr, print_token.line)

    def parse_assignment_or_call(self) -> Union[FunctionCallNode, AssignNode]:
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        var_token = self.reader.expect_token(TokenType.VARIABLE)
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        if self.reader.peek() and self.reader.peek().token_type == TokenType.MEMBER_ACCESS:
            self.reader.eat()
            self.reader.expect_token(TokenType.VARIABLE_BORDER)
            member_token = self.reader.expect_token(TokenType.VARIABLE)
            self.reader.expect_token(TokenType.VARIABLE_BORDER)
            if self.reader.peek() and self.reader.peek().token_type == TokenType.BRACKET:
                return self.expr_parser.parse_member_function_call(var_token.value, member_token.value, var_token.line)
            else:
                self.reader.expect_token(TokenType.ASSIGNMENT)
                value_expr = self.expr_parser.parse_expression()
                return AssignNode(f"{var_token.value}_{member_token.value}", value_expr, var_token.line)
        else:
            self.reader.expect_token(TokenType.ASSIGNMENT)
            value_expr = self.expr_parser.parse_expression()
            return AssignNode(var_token.value, value_expr, var_token.line)

    def parse_declaration(self) -> DeclNode:
        mutability_token = self.reader.peek()
        can_mutate = mutability_token.token_type == TokenType.MUT
        self.reader.eat()
        var_type = self.type_parser.parse_type()
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        token_variable = self.reader.expect_token(TokenType.VARIABLE)
        variable = token_variable.value
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        token = self.reader.peek()
        if token and token.token_type == TokenType.ASSIGNMENT:
            self.reader.eat()
            init_expr = self.expr_parser.parse_expression()
        else:
            if isinstance(var_type, str):
                raise ValueError(f"Struct type variables must be initialized at line {token_variable.line}!")
            init_expr = TypeParser.get_default_for_type(var_type)
        return DeclNode(variable, init_expr, token_variable.line, can_mutate, var_type)

    def parse_assignment(self) -> AssignNode:
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        variable_token = self.reader.expect_token(TokenType.VARIABLE)
        variable = variable_token.value
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        self.reader.expect_token(TokenType.ASSIGNMENT)
        value_expr = self.expr_parser.parse_expression()
        return AssignNode(variable, value_expr, variable_token.line)

    def parse_condition_block(self) -> tuple:
        if not self.reader.peek() or self.reader.peek().token_type in [TokenType.MOOD_LINE_BORDER_END, TokenType.SIMPLE_LINE_BORDER]:
            raise ValueError(f"Condition missing at line {self.reader.peek().line}!")
        condition = self.expr_parser.parse_expression()
        if self.reader.in_mood_line:
            condition = UnaryOpNode(NOT, condition)
        self.reader.expect_line_end()
        block = self.parse_code_block()
        return condition, block

    def parse_if_statement(self) -> IfNode:
        if_token = self.reader.expect_token(TokenType.IF)
        condition, then_block = self.parse_condition_block()
        elif_blocks = [self.parse_elif_block() for _ in iter(lambda: self.peek_for_elif(), False) if self.peek_for_elif()]
        else_block = self.try_parse_else_block()
        return IfNode(condition, then_block, elif_blocks, else_block, if_token.line)

    def peek_for_elif(self) -> bool:
        return self.check_with_save(lambda: self.reader.peek() and self.reader.peek().token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START] and self.peek_token(1) and self.peek_token(1).token_type == TokenType.ELIF)

    def parse_elif_block(self) -> ElifNode:
        self.reader.skip_line_start()
        elif_token = self.reader.expect_token(TokenType.ELIF)
        condition, then_block = self.parse_condition_block()
        return ElifNode(condition, then_block, elif_token.line)

    def parse_while_statement(self) -> WhileNode:
        while_token = self.reader.expect_token(TokenType.WHILE)
        condition, body = self.parse_condition_block()
        return WhileNode(condition, body, while_token.line)

    def try_parse_else_block(self) -> Optional[CodeBlockNode]:
        saved_index = self.reader.current_token_index
        token = self.reader.peek()
        if token and token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START] \
            and self.peek_token(1) and self.peek_token(1).token_type == TokenType.ELSE:
            self.reader.skip_line_start()
            self.reader.expect_token(TokenType.ELSE)
            if self.reader.peek().token_type not in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_END]:
                 raise ValueError(f"Else statement (KILL) cannot have a condition at line {self.reader.peek().line}!")
            self.reader.expect_line_end() 
            block = self.parse_code_block()
            return block
        self.reader.current_token_index = saved_index
        return None

    def parse_return(self) -> ReturnNode:
        self.reader.expect_token(TokenType.RETURN)
        next_token_type = self.reader.peek().token_type if self.reader.peek() else None
        if next_token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_END]:
            return ReturnNode(None)
        expr = self.expr_parser.parse_expression()
        self.reader.expect_token(TokenType.RETURN)
        return ReturnNode(expr)