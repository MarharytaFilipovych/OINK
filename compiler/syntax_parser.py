#!/usr/bin/env python3
from typing import Union, Optional

from compiler.node.assign_node import AssignNode
from compiler.node.binary_op_node import BinaryOpNode
from compiler.node.code_block_node import CodeBlockNode
from compiler.node.decl_node import DeclNode
from compiler.node.expr_node import ExprNode
from compiler.node.factor_node import FactorNode
from compiler.node.id_node import IDNode
from compiler.node.if_node import IfNode
from compiler.node.elif_node import ElifNode
from compiler.node.while_node import WhileNode
from compiler.node.number_node import NumberNode
from compiler.node.program_node import ProgramNode
from compiler.node.return_node import ReturnNode
from compiler.node.stmt_node import StmtNode
from compiler.llvm_specifics.data_type import DataType
from compiler.llvm_specifics.operator import Operator
from compiler.node.bool_node import BooleanNode
from compiler.node.unary_op_node import UnaryOpNode
from compiler.token.token_type import TokenType
from compiler.token.token_class import Token
from compiler.constants import NOT, FALSE, TRUE


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
        consumes_own_line_end = False

        match token.token_type:
            case TokenType.MUT | TokenType.CONST:
                stmt = self.__parse_declaration()
            case TokenType.VARIABLE_BORDER:
                stmt = self.__parse_assignment()
            case TokenType.IF:
                stmt = self.__parse_if_statement()
                consumes_own_line_end = True  # if statements consume their own line endings
            case TokenType.WHILE:
                stmt = self.__parse_while_statement()
                consumes_own_line_end = True  # while statements consume their own line endings
            case TokenType.BLOCK_BORDER:
                self.__eat()
            case _:
                raise ValueError(f"You should have either declared a variable, assigned this cutie to sth, "
                    f"or used control flow at line {token.line}, but you decided to use "
                    f"this token: {token.token_type}")

        if not consumes_own_line_end:
            self.__expect_line_end()
        return stmt
    
    def __expect_line_end(self):
        token = self.__peek()
        if self.in_mood_line:
            self.__expect_token(TokenType.MOOD_LINE_BORDER_END) 
            self.in_mood_line = False
        else:
            self.__expect_token(TokenType.SIMPLE_LINE_BORDER)
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
            init_expr = self.__set_default_for_type(var_type)

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
        if_token = self.__expect_token(TokenType.IF)
        condition = self.__parse_expression()
        
        if self.in_mood_line:
            condition = UnaryOpNode(NOT, condition)
        
        then_block = self.__parse_code_block()
        
        elif_blocks = []
        while self.__peek_for_elif():
            elif_blocks.append(self.__parse_elif_block())

        else_block = self.__try_parse_else_block()

        return IfNode(condition, then_block, elif_blocks, else_block, if_token.line)

    def __peek_for_elif(self) -> bool:
        """Check if the next non-border token is ELIF"""
        saved_index = self.current_token_index
        
        # The code block already consumed its line ending, so we're at the next line
        # Skip line border
        token = self.__peek()
        if token and token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]:
            self.current_token_index += 1
            token = self.__peek()
            result = token and token.token_type == TokenType.ELIF
        else:
            result = False
            
        self.current_token_index = saved_index
        return result

    def __parse_elif_block(self) -> ElifNode:
        # We've already confirmed there's an elif through peek_for_elif
        # We're positioned after the closing of the previous block
        
        self.__skip_line_start()
        elif_token = self.__expect_token(TokenType.ELIF)
        condition = self.__parse_expression()
        
        if self.in_mood_line:
            condition = UnaryOpNode(NOT, condition)
            
        then_block = self.__parse_code_block()
        # parse_code_block already consumed its line ending
        
        return ElifNode(condition, then_block, elif_token.line)

    def __parse_while_statement(self) -> WhileNode:
        while_token = self.__expect_token(TokenType.WHILE)
        condition = self.__parse_expression()
        
        if self.in_mood_line:
            condition = UnaryOpNode(NOT, condition)
        
        body = self.__parse_code_block()
        # parse_code_block already consumed its line ending

        return WhileNode(condition, body, while_token.line)

    def __try_parse_else_block(self) -> Optional[CodeBlockNode]:
        """Check if the next non-border token is ELSE"""
        saved_index = self.current_token_index
        
        # Skip line border
        token = self.__peek()
        if token and token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]:
            self.current_token_index += 1
            token = self.__peek()
            if token and token.token_type == TokenType.ELSE:
                # Found ELSE, don't restore - continue parsing
                self.__eat()  # Consume ELSE token
                block = self.__parse_code_block()
                # parse_code_block already consumed its line ending
                return block
        
        # No ELSE found, restore position
        self.current_token_index = saved_index
        return None

    def __skip_line_start(self):
        token = self.__peek()
        if token and token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]: 
            if token.token_type == TokenType.MOOD_LINE_BORDER_START: 
                self.in_mood_line = True
            self.__eat()

    def __parse_code_block(self) -> CodeBlockNode:
        # After condition line: # SAVE condition #\n
        # We should be at: # 🐖🐖🐖 #\n
        
        # Expect opening delimiter line
        self.__expect_line_end()  # consumes newline after condition
        self.__skip_line_start()  # consumes #
        self.__expect_token(TokenType.BLOCK_BORDER)  # consumes 🐖🐖🐖
        self.__expect_line_end()  # consumes # and newline

        statements, return_node = self.__parse_block_contents()

        # After block contents, we should be at: # 🐖🐖🐖 #
        # The newline before this was already consumed by the last statement
        self.__skip_line_start()  # consumes #
        self.__expect_token(TokenType.BLOCK_BORDER)  # consumes 🐖🐖🐖
        self.__expect_line_end()  # consume # and newline
        
        scope_id = self.next_scope_id
        self.next_scope_id += 1
        return CodeBlockNode(statements, return_node, scope_id)

    def __parse_block_contents(self) -> tuple[list[StmtNode], Optional[ReturnNode]]:
        statements = []
        return_node = None

        while True:
            # We're at the start of a line, could be a statement or closing delimiter
            token = self.__peek()

            if not token:
                raise ValueError("Code block must be closed with 🐖🐖🐖!")

            # Check if this is the closing delimiter line
            if token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]:
                # Peek ahead to see if it's the closing block
                saved_index = self.current_token_index
                self.__eat()  # consume line border
                next_token = self.__peek()
                if next_token and next_token.token_type == TokenType.BLOCK_BORDER:
                    # This is the closing delimiter, restore position and exit
                    self.current_token_index = saved_index
                    break
                # Not a closing delimiter, restore and continue
                self.current_token_index = saved_index
            
            # Parse a statement
            self.__define_line_type(token)
            
            token = self.__peek()
            if token.token_type == TokenType.RETURN:
                return_node = self.__parse_return()
                self.__expect_line_end()
                break

            statement = self.__parse_statement()
            if statement:
                statements.append(statement)
            # __parse_statement already consumed the line ending

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
