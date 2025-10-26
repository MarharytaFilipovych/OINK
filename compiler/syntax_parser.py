#!/usr/bin/env python3
from typing import Union, Optional

from .node.assign_node import AssignNode
from .node.binary_op_node import BinaryOpNode
from .node.code_block_node import CodeBlockNode
from .node.decl_node import DeclNode
from .node.expr_node import ExprNode
from .node.factor_node import FactorNode
from .node.id_node import IDNode
from .node.if_node import IfNode
from .node.elif_node import ElifNode
from .node.while_node import WhileNode
from .node.number_node import NumberNode
from .node.program_node import ProgramNode
from .node.return_node import ReturnNode
from .node.stmt_node import StmtNode
from .llvm_specifics.data_type import DataType
from .llvm_specifics.operator import Operator
from .node.bool_node import BooleanNode
from .node.unary_op_node import UnaryOpNode
from .token.token_type import TokenType
from .token.token_class import Token
from .constants import NOT, FALSE, TRUE


class SyntaxParser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_token_index = 0
        self.next_scope_id = 1
        self.in_mood_line = False

    def __peek(self, count: int = 0) -> Token:
        return self.tokens[self.current_token_index + count] if self.current_token_index + count < len(self.tokens) else None

    def __eat(self) -> Optional[Token]:
        token = self.__peek()
        if token:
            self.current_token_index += 1
        return token

    def __expect_token(self, token_type: TokenType) -> Token:
        token = self.__peek()
        if not token:
            raise ValueError(f"I expected a token of the type {token_type.name} but you decided to abandon this promising code!")

        if token.token_type != token_type:
            raise ValueError(f"I expected a token of the type {token_type.name} but you gave me {token.token_type.name} "
                f"at line {token.line} and index {token.index}")

        return self.__eat()

    def parse_program(self) -> ProgramNode:
        statements = self.__parse_statements()
        return_statement = self.__parse_program_return()
        self.__check_program_end()

        return ProgramNode(statements, return_statement)

    def __parse_statements(self) -> list[StmtNode]:
        statements = []

        while True:
            token = self.__peek()
            if len(statements) == 0 and token and token.token_type == TokenType.THE_END:
                raise ValueError("Program cannot be empty! You have to write something before the return statement!")
            
            if not token or token.token_type == TokenType.THE_END:
                raise ValueError('Program must end with "# ... expr ... #"!')
                
            self.__define_line_type(token)
            
            token = self.__peek()
            if token.token_type == TokenType.RETURN:
                break

            statement = self.__parse_statement()
            if statement:
                statements.append(statement)

        return statements

    def __parse_program_return(self) -> ReturnNode:
        return_statement = self.__parse_return()
        self.__expect_line_end()
        return return_statement

    def __check_program_end(self):
        if self.__peek() and self.__peek().token_type != TokenType.THE_END:
            raise ValueError(f"I did not want you to place this awful content "
                f"after the return statement at line {self.__peek().line}: {self.__peek().value}!")

    def __parse_statement(self) -> Optional[StmtNode]:
        token = self.__peek()
        stmt = None

        match token.token_type:
            case TokenType.MUT | TokenType.CONST:
                stmt = self.__parse_declaration()
            case TokenType.VARIABLE_BORDER:
                stmt = self.__parse_assignment()
            case TokenType.IF:
                stmt = self.__parse_if_statement()
            case TokenType.WHILE:
                stmt = self.__parse_while_statement()
            case TokenType.BLOCK_BORDER:
                self.__eat()
            case _:
                raise ValueError(f"You should have either declared a variable, assigned this cutie to sth, "
                    f"or used control flow at line {token.line}, but you decided to use "
                    f"this token: {token.value}")

        self.__expect_line_end()
        return stmt
    
    def __expect_line_end(self):
        token = self.__peek()
        if self.in_mood_line:
            self.__expect_token(TokenType.MOOD_LINE_BORDER_END) 
            self.in_mood_line = False
        elif token and token.token_type == TokenType.SIMPLE_LINE_BORDER:
            self.__eat()
        self.__expect_newline_or_end()

    def __define_line_type(self, token: Token):
        if not token:
            raise ValueError("Why did you decide to abandon your work?! I want a statement!")
        
        if token and token.token_type == TokenType.MOOD_LINE_BORDER_START:  
            self.in_mood_line = True
            self.__eat()
        elif token and token.token_type == TokenType.SIMPLE_LINE_BORDER:
            self.__eat()

    def __expect_newline_or_end(self):
        token = self.__peek()
        if token and token.token_type not in [TokenType.NEWLINE, TokenType.THE_END]:
            raise ValueError(
                f"Each instruction must be on its own line! "
                f"You were expected to place a newline after the"
                f" instruction at line {token.line}, but you placed this: {token.value}")
        if token and token.token_type == TokenType.NEWLINE:
            self.__eat()

    def __parse_declaration(self) -> DeclNode:
        mutability_token = self.__peek()
        can_mutate = mutability_token.token_type == TokenType.MUT
        self.__eat()

        var_type = self.__parse_type()

        self.__expect_token(TokenType.VARIABLE_BORDER)
        token_variable = self.__expect_token(TokenType.VARIABLE)
        variable = token_variable.value
        self.__expect_token(TokenType.VARIABLE_BORDER)

        token = self.__peek()
        if token and token.token_type == TokenType.ASSIGNMENT:
            self.__eat()
            init_expr = self.__parse_expression()
        else:
            init_expr = None

        return DeclNode(variable, init_expr, token_variable.line, can_mutate, var_type)

    def __parse_type(self) -> DataType:
        token = self.__eat()
        match token.token_type:
            case TokenType.I16_TYPE:
                return DataType.I16
            case TokenType.I32_TYPE:
                return DataType.I32
            case TokenType.I64_TYPE:
                return DataType.I64
            case TokenType.BOOL:
                return DataType.BOOL
            case _:
                raise ValueError(f"I expected some type declaration at line {token.line}!")

    def __parse_assignment(self) -> AssignNode:
        self.__expect_token(TokenType.VARIABLE_BORDER)
        variable_token = self.__expect_token(TokenType.VARIABLE)
        variable = variable_token.value
        self.__expect_token(TokenType.VARIABLE_BORDER)
        self.__expect_token(TokenType.ASSIGNMENT)
        value_expr = self.__parse_expression()
        return AssignNode(variable, value_expr, variable_token.line)

    def __parse_if_statement(self) -> IfNode:
        print("I WAS HERE IN IF")

        if_token = self.__expect_token(TokenType.IF)
        condition = self.__parse_expression()
        
        if self.in_mood_line:
            condition = UnaryOpNode(NOT, condition)
        
        then_block = self.__parse_code_block()
        
        elif_blocks = []
        while self.__peek(2) and self.__peek().token_type == TokenType.ELIF:
            elif_blocks.append(self.__parse_elif_block())
        print("AND I WAS HERE IN IF, current token: {}", self.__peek().token_type)

        else_block = self.__try_parse_else_block()

        return IfNode(condition, then_block, elif_blocks, else_block, if_token.line)

    def __parse_elif_block(self) -> ElifNode:
        self.__expect_line_end()
        self.__skip_line_start()
        elif_token = self.__expect_token(TokenType.ELIF)
        condition = self.__parse_expression()
        self.__expect_line_end()
        then_block = self.__parse_code_block()
        
        return ElifNode(condition, then_block, elif_token.line)

    def __parse_while_statement(self) -> WhileNode:
        while_token = self.__expect_token(TokenType.WHILE)
        condition = self.__parse_expression()
        
        if self.in_mood_line:
            condition = UnaryOpNode(NOT, condition)
        
        self.__expect_line_end()

        body = self.__parse_code_block()

        return WhileNode(condition, body, while_token.line)

    def __try_parse_else_block(self) -> Optional[CodeBlockNode]:
        self.__expect_line_end()
        print("AND I WAS HERE IN ELSE, current token: {}", self.__peek(2).token_type)
        if not self.__peek(2) or self.__peek(2).token_type != TokenType.ELSE:
            return None
        print("I WAS HERE")
        self.__skip_line_start()
        self.__expect_token(TokenType.ELSE)
        self.__expect_line_end()

        return self.__parse_code_block()

    def __skip_line_start(self):
        token = self.__peek()
        if token and token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]: 
            if token.token_type == TokenType.MOOD_LINE_BORDER_START: 
                self.in_mood_line = True
            self.__eat()

    def __parse_code_block(self) -> CodeBlockNode:
        self.__skip_line_start()
        self.__expect_token(TokenType.BLOCK_BORDER)
        self.__expect_line_end()

        statements, return_node = self.__parse_block_contents()

        self.__skip_line_start()
        self.__expect_token(TokenType.BLOCK_BORDER)
        self.__expect_line_end()
        
        scope_id = self.next_scope_id
        self.next_scope_id += 1
        return CodeBlockNode(statements, return_node, scope_id)

    def __parse_block_contents(self) -> tuple[list[StmtNode], Optional[ReturnNode]]:
        statements = []
        return_node = None

        while True:
            token = self.__peek()

            if not token:
                raise ValueError("Code block must be closed with 🐖🐖🐖!")

            if token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]: 
                saved_index = self.current_token_index
                self.__eat()
                next_token = self.__peek()
                if next_token and next_token.token_type == TokenType.BLOCK_BORDER:
                    self.current_token_index = saved_index
                    break
                self.current_token_index = saved_index
                
            self.__define_line_type(token)
            
            token = self.__peek()
            if token.token_type == TokenType.RETURN:
                return_node = self.__parse_return()
                self.__expect_newline_or_end()
                break

            statement = self.__parse_statement()
            if statement:
                statements.append(statement)
            self.__expect_newline_or_end()

        return statements, return_node

    def __parse_return(self) -> ReturnNode:
        self.__expect_token(TokenType.RETURN)
        expr = self.__parse_expression()
        self.__expect_token(TokenType.RETURN)
        return ReturnNode(expr)

    def __parse_expression(self) -> ExprNode:
        return self.__parse_logical_or()

    def __parse_logical_or(self) -> ExprNode:
        left = self.__parse_logical_and()
        
        while self.__peek() and self.__peek().token_type == TokenType.OR:
            self.__eat()
            right = self.__parse_logical_and()
            left = BinaryOpNode(left, Operator.OR, right)
        
        return left

    def __parse_logical_and(self) -> ExprNode:
        left = self.__parse_comparison()
        
        while self.__peek() and self.__peek().token_type == TokenType.AND:
            self.__eat()
            right = self.__parse_comparison()
            left = BinaryOpNode(left, Operator.AND, right)
        
        return left

    def __parse_comparison(self) -> ExprNode:
        left = self.__parse_additive()
        
        token = self.__peek()
        if token and token.token_type.if_for_comparision():
            op_token = self.__eat()
            operator = Operator.from_string(op_token.value)
            
            if self.in_mood_line:
                operator = operator.invert()
            
            right = self.__parse_additive()
            left = BinaryOpNode(left, operator, right)
        
        return left

    def __parse_additive(self) -> ExprNode:
        left = self.__parse_multiplicative()
        
        while True:
            token = self.__peek()
            if not token or not token.token_type.is_additive_operator():
                break
            
            op_token = self.__eat()
            operator = Operator.from_string(op_token.value)
            
            if self.in_mood_line:
                operator = operator.invert()
            
            right = self.__parse_multiplicative()
            left = BinaryOpNode(left, operator, right)
        
        return left

    def __parse_multiplicative(self) -> ExprNode:
        left = self.__parse_unary()
        
        while True:
            token = self.__peek()
            if not token or not token.token_type.is_multiplicative_operator():
                break
            
            op_token = self.__eat()
            operator = Operator.from_string(op_token.value)
            
            if self.in_mood_line:
                operator = operator.invert()
            
            right = self.__parse_unary()
            left = BinaryOpNode(left, operator, right)
        
        return left

    def __parse_unary(self) -> Union[FactorNode, UnaryOpNode]:
        token = self.__peek()

        if token and token.token_type == TokenType.NOT:
            self.__eat()
            operand = self.__parse_unary()
            return UnaryOpNode(NOT, operand)

        return self.__parse_value()

    def __parse_value(self) -> Union[FactorNode, ExprNode]:
        token = self.__eat()

        if not token:
            raise ValueError(
                "You should have used either a number, a variable, or a boolean, "
                "but you decided to abandon your work!")

        match token.token_type:
            case TokenType.NUMBER:
                return NumberNode(token.value)
            case TokenType.VARIABLE_BORDER:
                var_token = self.__expect_token(TokenType.VARIABLE)
                self.__expect_token(TokenType.VARIABLE_BORDER)
                return IDNode(var_token.value, var_token.line)
            case TokenType.TRUE | TokenType.FALSE:
                value = token.value
                if self.in_mood_line:
                    value = FALSE if value == TRUE else TRUE
                return BooleanNode(value)
            case TokenType.BRACKET:
                expr = self.__parse_expression()
                self.__expect_token(TokenType.BRACKET) 
                return expr
            case _:
                raise ValueError(
                    f"You should have used either a number, a variable, or a boolean "
                    f"at line {token.line}, not {token.value}!")

    @staticmethod
    def __set_default_for_type(data_type: DataType) -> FactorNode:
        if data_type == DataType.BOOL:
            return BooleanNode(FALSE)
        elif data_type in [DataType.I16, DataType.I32, DataType.I64]:
            return NumberNode("0")
        else:
            raise ValueError(f"No default value defined for {data_type}")
