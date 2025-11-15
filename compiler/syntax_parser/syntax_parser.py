#!/usr/bin/env python3

from typing import Optional, Union
from ..constants import NOT
from ..llvm_specifics.data_type import DataType
from ..node.function_call_node import FunctionCallNode
from ..node.unary_op_node import UnaryOpNode
from ..token.token_class import Token
from ..token.token_type import TokenType
from .token_reader import TokenReader
from .type_parser import TypeParser
from .expression_parser import ExpressionParser
from ..node.program_node import ProgramNode
from ..node.stmt_node import StmtNode
from ..node.function_decl_node import FunctionDeclNode, FunctionParam
from ..node.struct_decl_node import StructDeclNode, StructField
from ..node.code_block_node import CodeBlockNode
from ..node.return_node import ReturnNode
from ..node.io_nodes import ReadNode, PrintNode
from ..node.assign_node import AssignNode
from ..node.decl_node import DeclNode
from ..node.if_node import IfNode
from ..node.elif_node import ElifNode
from ..node.while_node import WhileNode


class SyntaxParser:
    def __init__(self, tokens: list[Token]):
        self.reader = TokenReader(tokens)
        self.next_scope_id = 1
        self.declared_structs: set[str] = set()
        self.type_parser = TypeParser(self.reader, self.declared_structs)
        self.expr_parser = ExpressionParser(self.reader, self.declared_structs)

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
        while self.peek_and_check_struct():
            struct_declarations.append(self.parse_struct_declaration())
            self.reader.skip_newlines()
        function_declarations = []
        while self.peek_and_check_function():
            function_declarations.append(self.parse_function_declaration())
            self.reader.skip_newlines()
        statements = self.parse_statements()
        if not struct_declarations and not function_declarations and not statements:
            raise ValueError("Program cannot be empty! You have to write something before the return statement!")
        return_statement = self.parse_program_return()
        self.check_program_end()
        return ProgramNode(struct_declarations, function_declarations, statements, return_statement)

    def peek_and_check_struct(self) -> bool:
        if not self.reader.peek() or self.reader.peek().token_type != TokenType.SIMPLE_LINE_BORDER:
            return False
        return self.check_with_save(lambda: self.reader.eat() or (self.reader.peek() and self.reader.peek().token_type == TokenType.STRUCT))

    def peek_and_check_function(self) -> bool:
        if not self.reader.peek() or self.reader.peek().token_type != TokenType.SIMPLE_LINE_BORDER:
            return False

        def check_fn():
            self.reader.eat()
            next_token = self.reader.peek()
            if next_token and next_token.token_type.is_data_type():
                self.reader.eat()
                return self.reader.peek() and self.reader.peek().token_type == TokenType.FUNCTION
            return False

        return self.check_with_save(check_fn)

    def parse_struct_declaration(self) -> StructDeclNode:
        self.reader.define_line_type(self.reader.peek())
        struct_token = self.reader.expect_token(TokenType.STRUCT)
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        name_token = self.reader.expect_token(TokenType.VARIABLE)
        struct_name = name_token.value
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        self.reader.expect_line_end()
        if struct_name in self.declared_structs:
            raise ValueError(f"Struct '{struct_name}' already declared at line {name_token.line}!")
        self.declared_structs.add(struct_name)
        self.reader.define_line_type(self.reader.peek())
        self.reader.expect_token(TokenType.BLOCK_BORDER)
        self.reader.expect_line_end()
        fields, member_functions = self.parse_struct_body()
        self.reader.define_line_type(self.reader.peek())
        self.reader.expect_token(TokenType.BLOCK_BORDER)
        self.reader.expect_line_end()
        return StructDeclNode(struct_name, fields, member_functions, struct_token.line)

    def parse_struct_body(self) -> tuple[list[StructField], list[FunctionDeclNode]]:
        fields = []
        member_functions = []
        while True:
            token = self.reader.peek()
            if not token:
                raise ValueError("Struct block must be closed with 🐖🐖🐖!")
            if token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]:
                saved_index = self.reader.current_token_index
                self.reader.eat()
                next_token = self.reader.peek()
                if next_token and next_token.token_type == TokenType.BLOCK_BORDER:
                    self.reader.current_token_index = saved_index
                    break
                if next_token and next_token.token_type.is_data_type():
                    saved_index2 = self.reader.current_token_index
                    self.reader.eat()
                    if self.reader.peek() and self.reader.peek().token_type == TokenType.MEMBER_FUNCTION:
                        self.reader.current_token_index = saved_index
                        member_functions.append(self.parse_member_function_declaration())
                        continue
                    else:
                        self.reader.current_token_index = saved_index
                self.reader.current_token_index = saved_index
                self.reader.define_line_type(token)
                fields.append(self.parse_struct_field())
            else:
                break
        return fields, member_functions

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

    def parse_function_like(self, is_member=False) -> FunctionDeclNode:
        self.reader.define_line_type(self.reader.peek())
        return_type = self.type_parser.parse_type()
        keyword = TokenType.MEMBER_FUNCTION if is_member else TokenType.FUNCTION
        self.reader.expect_token(keyword)
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        func_name_token = self.reader.expect_token(TokenType.VARIABLE)
        func_name = func_name_token.value
        self.reader.expect_token(TokenType.VARIABLE_BORDER)
        params = self.parse_function_params()
        self.reader.expect_line_end()
        body = self.parse_code_block()
        if return_type != DataType.VOID and body.return_node is None:
            kind = "Member function" if is_member else "Function"
            raise ValueError(f"{kind} '{func_name}' with return type must have a return statement at line {func_name_token.line}!")
        return FunctionDeclNode(func_name, params, return_type, body, func_name_token.line)

    def parse_function_declaration(self) -> FunctionDeclNode:
        return self.parse_function_like(False)

    def parse_member_function_declaration(self) -> FunctionDeclNode:
        return self.parse_function_like(True)

    def parse_function_params(self) -> list[FunctionParam]:
        params = []
        while self.reader.peek() and self.reader.peek().token_type == TokenType.BRACKET:
            self.reader.eat()
            param_type = self.type_parser.parse_type()
            self.reader.expect_token(TokenType.VARIABLE_BORDER)
            param_name_token = self.reader.expect_token(TokenType.VARIABLE)
            self.reader.expect_token(TokenType.VARIABLE_BORDER)
            self.reader.expect_token(TokenType.BRACKET)
            params.append(FunctionParam(param_type, param_name_token.value))
        return params

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
                                 f"this token: {token.token_type}")
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

    def parse_program_return(self) -> ReturnNode:
        self.reader.expect_token(TokenType.RETURN)
        return_statement = self.expr_parser.parse_expression()
        self.reader.expect_token(TokenType.RETURN)
        self.reader.expect_line_end()
        return ReturnNode(return_statement)

    def check_program_end(self):
        if self.reader.peek() and self.reader.peek().token_type != TokenType.THE_END:
            raise ValueError(f"I did not want you to place this awful content "
                             f"after the return statement at line {self.reader.peek().line}: {self.reader.peek().value}!")

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
        if token and token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START] and self.peek_token(1) and self.peek_token(1).token_type == TokenType.ELSE:
            self.reader.eat()
            block = self.parse_code_block()
            return block
        self.reader.current_token_index = saved_index
        return None

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
            if token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]:
                saved_index = self.reader.current_token_index
                self.reader.eat()
                next_token = self.reader.peek()
                if next_token and next_token.token_type == TokenType.BLOCK_BORDER:
                    self.reader.current_token_index = saved_index
                    break
                self.reader.current_token_index = saved_index
            self.reader.define_line_type(token)
            token = self.reader.peek()
            if token.token_type == TokenType.RETURN:
                return_node = self.parse_return()
                self.reader.expect_line_end()
                break
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        return statements, return_node

    def parse_return(self) -> ReturnNode:
        self.reader.expect_token(TokenType.RETURN)
        next_token_type = self.reader.peek().token_type if self.reader.peek() else None
        if next_token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_END]:
            return ReturnNode(None)
        expr = self.expr_parser.parse_expression()
        self.reader.expect_token(TokenType.RETURN)
        return ReturnNode(expr)
