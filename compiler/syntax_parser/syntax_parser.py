#!/usr/bin/env python3
from typing import Union, Optional
from ..node.assign_node import AssignNode
from ..node.binary_op_node import BinaryOpNode
from ..node.code_block_node import CodeBlockNode
from ..node.decl_node import DeclNode
from ..node.expr_node import ExprNode
from ..node.factor_node import FactorNode
from ..node.id_node import IDNode
from ..node.if_node import IfNode
from ..node.elif_node import ElifNode
from ..node.while_node import WhileNode
from ..node.number_node import NumberNode
from ..node.program_node import ProgramNode
from ..node.return_node import ReturnNode
from ..node.stmt_node import StmtNode
from ..node.function_decl_node import FunctionDeclNode, FunctionParam
from ..node.function_call_node import FunctionCallNode
from ..node.struct_decl_node import StructDeclNode, StructField
from ..node.struct_init_node import StructInitNode
from ..node.member_access_node import MemberAccessNode
from ..node.io_nodes import ReadNode, PrintNode
from ..llvm_specifics.data_type import DataType
from ..llvm_specifics.operator import Operator
from ..node.bool_node import BooleanNode
from ..node.unary_op_node import UnaryOpNode
from ..token.token_type import TokenType
from ..token.token_class import Token
from ..constants import NOT, FALSE, TRUE


class SyntaxParser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_token_index = 0
        self.next_scope_id = 1
        self.in_mood_line = False
        self.declared_structs: set[str] = set()

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

    def __skip_newlines(self):
        while self.__peek() and self.__peek().token_type == TokenType.NEWLINE:
            self.__eat()

    def __define_line_type(self, token: Token):
        if not token:
            raise ValueError("Why did you decide to abandon your work?! I want a statement!")
        
        if token and token.token_type == TokenType.MOOD_LINE_BORDER_START:  
            self.in_mood_line = True
            self.__eat()
        elif token and token.token_type == TokenType.SIMPLE_LINE_BORDER:
            self.__eat()

    def __expect_line_end(self):
        token = self.__peek()
        if self.in_mood_line:
            self.__expect_token(TokenType.MOOD_LINE_BORDER_END) 
            self.in_mood_line = False
        else:
            self.__expect_token(TokenType.SIMPLE_LINE_BORDER)
        self.__expect_newline_or_end()

    def __expect_newline_or_end(self):
        token = self.__peek()
        if token and token.token_type not in [TokenType.NEWLINE, TokenType.THE_END]:
            raise ValueError(
                f"Each instruction must be on its own line! "
                f"You were expected to place a newline after the"
                f" instruction at line {token.line}, but you placed this: {token.value}")
        if token and token.token_type == TokenType.NEWLINE:
            self.__eat()

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
            case TokenType.VOID:
                return DataType.VOID
            case _:
                raise ValueError(f"I expected some type declaration at line {token.line}!")

    @staticmethod
    def __set_default_for_type(data_type: DataType) -> FactorNode:
        if data_type == DataType.BOOL:
            return BooleanNode(FALSE)
        elif data_type in [DataType.I16, DataType.I32, DataType.I64]:
            return NumberNode("0")
        else:
            raise ValueError(f"No default value defined for {data_type}")

    def parse_program(self) -> ProgramNode:
        self.__skip_newlines()
        
        struct_declarations = []
        function_declarations = []
        
        while self.__peek() and self.__peek().token_type == TokenType.SIMPLE_LINE_BORDER:
            saved_index = self.current_token_index
            self.__eat()
            if self.__peek() and self.__peek().token_type == TokenType.STRUCT:
                self.current_token_index = saved_index
                struct_declarations.append(self.__parse_struct_declaration())
                self.__skip_newlines()
            else:
                self.current_token_index = saved_index
                break
        
        while self.__peek() and self.__peek().token_type == TokenType.SIMPLE_LINE_BORDER:
            saved_index = self.current_token_index
            self.__eat()
            next_token = self.__peek()
            if next_token and next_token.token_type.is_data_type():
                saved_index2 = self.current_token_index
                self.__eat() 
                if self.__peek() and self.__peek().token_type == TokenType.FUNCTION:
                    self.current_token_index = saved_index
                    function_declarations.append(self.__parse_function_declaration())
                    self.__skip_newlines()
                else:
                    self.current_token_index = saved_index
                    break
            else:
                self.current_token_index = saved_index
                break
        
        statements = self.__parse_statements()
        if not struct_declarations and not function_declarations and not statements:
            raise ValueError("Program cannot be empty! You have to write something before the return statement!")
        return_statement = self.__parse_program_return()
        self.__check_program_end()

        return ProgramNode(struct_declarations, function_declarations, statements, return_statement)

    def __parse_struct_declaration(self) -> StructDeclNode:
        self.__define_line_type(self.__peek())
        struct_token = self.__expect_token(TokenType.STRUCT)
        self.__expect_token(TokenType.VARIABLE_BORDER)
        name_token = self.__expect_token(TokenType.VARIABLE)
        struct_name = name_token.value
        self.__expect_token(TokenType.VARIABLE_BORDER)
        self.__expect_line_end()
        
        if struct_name in self.declared_structs:
            raise ValueError(f"Struct '{struct_name}' already declared at line {name_token.line}!")
        self.declared_structs.add(struct_name)
        
        self.__define_line_type(self.__peek())
        self.__expect_token(TokenType.BLOCK_BORDER)
        self.__expect_line_end()
        
        fields = []
        member_functions = []
        
        while True:
            token = self.__peek()
            if not token:
                raise ValueError("Struct block must be closed with 🐖🐖🐖!")
            
            if token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]:
                saved_index = self.current_token_index
                self.__eat()
                next_token = self.__peek()
                
                if next_token and next_token.token_type == TokenType.BLOCK_BORDER:
                    self.current_token_index = saved_index
                    break
                
                if next_token and next_token.token_type.is_data_type():
                    saved_index2 = self.current_token_index
                    self.__eat()  # eat type
                    if self.__peek() and self.__peek().token_type == TokenType.MEMBER_FUNCTION:
                        self.current_token_index = saved_index
                        member_functions.append(self.__parse_member_function_declaration())
                        continue
                    else:
                        self.current_token_index = saved_index
                
                self.current_token_index = saved_index
                self.__define_line_type(token)
                
                mutability_token = self.__peek()
                can_mutate = mutability_token.token_type == TokenType.MUT
                if mutability_token.token_type in [TokenType.MUT, TokenType.CONST]:
                    self.__eat()
                
                field_type = self.__parse_type()
                self.__expect_token(TokenType.VARIABLE_BORDER)
                field_name_token = self.__expect_token(TokenType.VARIABLE)
                self.__expect_token(TokenType.VARIABLE_BORDER)
                self.__expect_line_end()
                
                fields.append(StructField(field_type, field_name_token.value, can_mutate))
            else:
                break
        
        self.__define_line_type(self.__peek())
        self.__expect_token(TokenType.BLOCK_BORDER)
        self.__expect_line_end()
        
        return StructDeclNode(struct_name, fields, member_functions, struct_token.line)

    def __parse_function_declaration(self) -> FunctionDeclNode:
        self.__define_line_type(self.__peek())
        return_type = self.__parse_type()
        self.__expect_token(TokenType.FUNCTION)
        self.__expect_token(TokenType.VARIABLE_BORDER)
        func_name_token = self.__expect_token(TokenType.VARIABLE)
        func_name = func_name_token.value
        self.__expect_token(TokenType.VARIABLE_BORDER)
        
        params = []
        while self.__peek() and self.__peek().token_type == TokenType.BRACKET:
            self.__eat()
            param_type = self.__parse_type()
            self.__expect_token(TokenType.VARIABLE_BORDER)
            param_name_token = self.__expect_token(TokenType.VARIABLE)
            self.__expect_token(TokenType.VARIABLE_BORDER)
            self.__expect_token(TokenType.BRACKET) 
            params.append(FunctionParam(param_type, param_name_token.value))
        
        self.__expect_line_end()
        
        body = self.__parse_code_block()
        
        return FunctionDeclNode(func_name, params, return_type, body, func_name_token.line)

    def __parse_member_function_declaration(self) -> FunctionDeclNode:
        self.__define_line_type(self.__peek())
        return_type = self.__parse_type()
        self.__expect_token(TokenType.MEMBER_FUNCTION)
        self.__expect_token(TokenType.VARIABLE_BORDER)
        func_name_token = self.__expect_token(TokenType.VARIABLE)
        func_name = func_name_token.value
        self.__expect_token(TokenType.VARIABLE_BORDER)
        
        params = []
        while self.__peek() and self.__peek().token_type == TokenType.BRACKET:
            self.__eat()  # **
            param_type = self.__parse_type()
            self.__expect_token(TokenType.VARIABLE_BORDER)
            param_name_token = self.__expect_token(TokenType.VARIABLE)
            self.__expect_token(TokenType.VARIABLE_BORDER)
            self.__expect_token(TokenType.BRACKET)  # **
            params.append(FunctionParam(param_type, param_name_token.value))
        
        self.__expect_line_end()
        
        body = self.__parse_code_block()
        
        return FunctionDeclNode(func_name, params, return_type, body, func_name_token.line)
    
    def __parse_statements(self) -> list[StmtNode]:
        statements = []

        while True:
            token = self.__peek()

            if not token or token.token_type == TokenType.THE_END:
                # If we hit the end and statements exist, the final return is missing.
                if len(statements) > 0:
                    raise ValueError('Program must end with "# ... expr ... #"!')
                break

            self.__define_line_type(token)
            
            token = self.__peek()
            if token.token_type == TokenType.RETURN:
                break # <--- Correctly break here, final return follows

            statement = self.__parse_statement()
            
            if statement:
                statements.append(statement)

        return statements

    def __parse_statement(self) -> Optional[StmtNode]:
        token = self.__peek()
        stmt = None
        consumes_own_line_end = False

        match token.token_type:
            case TokenType.MUT | TokenType.CONST:
                stmt = self.__parse_declaration()
            case TokenType.VARIABLE_BORDER:
                saved_index = self.current_token_index
                self.__eat()  
                var_token = self.__expect_token(TokenType.VARIABLE)
                self.__eat() 
                
                next_token = self.__peek()
                if next_token and next_token.token_type == TokenType.MEMBER_ACCESS:
                    self.current_token_index = saved_index
                    stmt = self.__parse_assignment_or_call()
                elif next_token and next_token.token_type == TokenType.BRACKET:
                    # Function call
                    self.current_token_index = saved_index
                    stmt = self.__parse_function_call_statement()
                else:
                    # Assignment
                    self.current_token_index = saved_index
                    stmt = self.__parse_assignment()
            case TokenType.IF:
                stmt = self.__parse_if_statement()
                consumes_own_line_end = True
            case TokenType.WHILE:
                stmt = self.__parse_while_statement()
                consumes_own_line_end = True
            case TokenType.READ:
                stmt = self.__parse_read_statement()
            case TokenType.PRINT:
                stmt = self.__parse_print_statement()
            case TokenType.BLOCK_BORDER:
                self.__eat()
            case _:
                raise ValueError(f"You should have either declared a variable, assigned this cutie to sth, "
                    f"or used control flow at line {token.line}, but you decided to use "
                    f"this token: {token.token_type}")

        if not consumes_own_line_end:
            self.__expect_line_end()
        return stmt

    def __parse_read_statement(self) -> ReadNode:
        read_token = self.__expect_token(TokenType.READ)
        self.__expect_token(TokenType.VARIABLE_BORDER)
        var_token = self.__expect_token(TokenType.VARIABLE)
        self.__expect_token(TokenType.VARIABLE_BORDER)
        return ReadNode(var_token.value, read_token.line)

    def __parse_print_statement(self) -> PrintNode:
        print_token = self.__expect_token(TokenType.PRINT)
        expr = self.__parse_expression()
        return PrintNode(expr, print_token.line)

    def __parse_function_call_statement(self) -> FunctionCallNode:
        return self.__parse_function_call_expr()

    def __parse_assignment_or_call(self) -> StmtNode:
        self.__expect_token(TokenType.VARIABLE_BORDER)
        var_token = self.__expect_token(TokenType.VARIABLE)
        self.__expect_token(TokenType.VARIABLE_BORDER)
        
        if self.__peek() and self.__peek().token_type == TokenType.MEMBER_ACCESS:
            self.__eat()
            self.__expect_token(TokenType.VARIABLE_BORDER)
            member_token = self.__expect_token(TokenType.VARIABLE)
            self.__expect_token(TokenType.VARIABLE_BORDER)
            
            if self.__peek() and self.__peek().token_type == TokenType.BRACKET:
                return self.__parse_member_function_call(var_token.value, member_token.value, var_token.line)
            else:
                self.__expect_token(TokenType.ASSIGNMENT)
                value_expr = self.__parse_expression()
                return AssignNode(f"{var_token.value}_{member_token.value}", value_expr, var_token.line)
        else:
            self.__expect_token(TokenType.ASSIGNMENT)
            value_expr = self.__parse_expression()
            return AssignNode(var_token.value, value_expr, var_token.line)

    def __parse_member_function_call(self, object_name: str, func_name: str, line: int) -> FunctionCallNode:
        self.__expect_token(TokenType.BRACKET) 
        
        arguments = []
        if self.__peek() and self.__peek().token_type != TokenType.BRACKET:
            arguments.append(self.__parse_expression())
            
            while self.__peek() and self.__peek().token_type == TokenType.BRACKET:
                saved_index = self.current_token_index
                self.__eat() 
                if self.__peek() and self.__peek().token_type == TokenType.BRACKET:
                    self.current_token_index = saved_index
                    break
                self.__eat() 
                arguments.append(self.__parse_expression())
        
        self.__expect_token(TokenType.BRACKET) 
        
        if self.__peek() and self.__peek().token_type == TokenType.MEMBER_ACCESS:
            result = FunctionCallNode(func_name, arguments, line, object_name)
            return self.__parse_function_chain(result, line)
        
        return FunctionCallNode(func_name, arguments, line, object_name)

    def __parse_function_chain(self, prev_call: FunctionCallNode, line: int) -> FunctionCallNode:
        while self.__peek() and self.__peek().token_type == TokenType.MEMBER_ACCESS:
            self.__eat()  # _
            self.__expect_token(TokenType.VARIABLE_BORDER)
            func_token = self.__expect_token(TokenType.VARIABLE)
            self.__expect_token(TokenType.VARIABLE_BORDER)
            
            prev_call = FunctionCallNode(func_token.value, [prev_call], line, None)
        
        return prev_call

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

    def __parse_assignment(self) -> AssignNode:
        self.__expect_token(TokenType.VARIABLE_BORDER)
        variable_token = self.__expect_token(TokenType.VARIABLE)
        variable = variable_token.value
        self.__expect_token(TokenType.VARIABLE_BORDER)
        self.__expect_token(TokenType.ASSIGNMENT)
        value_expr = self.__parse_expression()
        return AssignNode(variable, value_expr, variable_token.line)

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
                return self.__parse_variable_or_call()
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

    def __parse_variable_or_call(self) -> Union[FactorNode, ExprNode]:
        var_token = self.__expect_token(TokenType.VARIABLE)
        self.__expect_token(TokenType.VARIABLE_BORDER)
        
        if self.__peek() and self.__peek().token_type == TokenType.MEMBER_ACCESS:
            self.__eat()
            self.__expect_token(TokenType.VARIABLE_BORDER)
            member_token = self.__expect_token(TokenType.VARIABLE)
            self.__expect_token(TokenType.VARIABLE_BORDER)
            
            if self.__peek() and self.__peek().token_type == TokenType.BRACKET:
                return self.__parse_member_function_call(var_token.value, member_token.value, var_token.line)
            else:
                return MemberAccessNode(var_token.value, member_token.value, var_token.line)
        
        if self.__peek() and self.__peek().token_type == TokenType.BRACKET:
            return self.__parse_function_call_expr(var_token.value, var_token.line)
        
        if var_token.value in self.declared_structs and self.__peek() and self.__peek().token_type == TokenType.BRACKET:
            return self.__parse_struct_init(var_token.value, var_token.line)
        
        return IDNode(var_token.value, var_token.line)

    def __parse_function_call_expr(self, func_name: str = None, line: int = None) -> FunctionCallNode:
        if func_name is None:
            self.__expect_token(TokenType.VARIABLE_BORDER)
            func_token = self.__expect_token(TokenType.VARIABLE)
            func_name = func_token.value
            line = func_token.line
            self.__expect_token(TokenType.VARIABLE_BORDER)
        
        self.__expect_token(TokenType.BRACKET)
        
        arguments = []
        if self.__peek() and self.__peek().token_type != TokenType.BRACKET:
            arguments.append(self.__parse_expression())
            
            while self.__peek() and self.__peek().token_type == TokenType.BRACKET:
                saved_index = self.current_token_index
                self.__eat()  
                if self.__peek() and self.__peek().token_type == TokenType.BRACKET:
                    self.current_token_index = saved_index
                    break
                self.__eat() 
                arguments.append(self.__parse_expression())
        
        self.__expect_token(TokenType.BRACKET)  
        
        result = FunctionCallNode(func_name, arguments, line, None)
        
        if self.__peek() and self.__peek().token_type == TokenType.MEMBER_ACCESS:
            result = self.__parse_function_chain(result, line)
        
        return result

    def __parse_struct_init(self, struct_name: str, line: int) -> StructInitNode:
        self.__expect_token(TokenType.BRACKET) 
        
        init_exprs = []
        if self.__peek() and self.__peek().token_type != TokenType.BRACKET:
            init_exprs.append(self.__parse_expression())
            
            while self.__peek() and self.__peek().token_type == TokenType.BRACKET:
                saved_index = self.current_token_index
                self.__eat() 
                if self.__peek() and self.__peek().token_type == TokenType.BRACKET:
                    self.current_token_index = saved_index
                    break
                self.__eat() 
                init_exprs.append(self.__parse_expression())
        
        self.__expect_token(TokenType.BRACKET) 
        
        return StructInitNode(struct_name, init_exprs, line)

    def __parse_program_return(self) -> ReturnNode:
        self.__expect_token(TokenType.RETURN)
        return_statement = self.__parse_expression()
        self.__expect_token(TokenType.RETURN)
        self.__expect_line_end()
        return return_statement

    def __check_program_end(self):
        if self.__peek() and self.__peek().token_type != TokenType.THE_END:
            raise ValueError(f"I did not want you to place this awful content "
                f"after the return statement at line {self.__peek().line}: {self.__peek().value}!")

    def __parse_if_statement(self) -> IfNode:
        if_token = self.__expect_token(TokenType.IF)
        if not self.__peek() or self.__peek().token_type in [TokenType.MOOD_LINE_BORDER_END, TokenType.SIMPLE_LINE_BORDER]:
            raise ValueError(f"If condition missing at line {if_token.line}!")

        condition = self.__parse_expression()
        
        if self.in_mood_line:
            condition = UnaryOpNode(NOT, condition)
        
        self.__expect_line_end() 
        
        then_block = self.__parse_code_block()
        
        elif_blocks = []
        while self.__peek_for_elif():
            elif_blocks.append(self.__parse_elif_block())

        else_block = self.__try_parse_else_block()

        return IfNode(condition, then_block, elif_blocks, else_block, if_token.line)

    def __peek_for_elif(self) -> bool:
        saved_index = self.current_token_index
        
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
        self.__skip_line_start()
        elif_token = self.__expect_token(TokenType.ELIF)
        if not self.__peek() or self.__peek().token_type in [TokenType.MOOD_LINE_BORDER_END, TokenType.SIMPLE_LINE_BORDER]:
            raise ValueError(f"Elif condition missing at line {elif_token.line}!")
        condition = self.__parse_expression()
        
        if self.in_mood_line:
            condition = UnaryOpNode(NOT, condition)
            
        self.__expect_line_end()
            
        then_block = self.__parse_code_block()
        
        return ElifNode(condition, then_block, elif_token.line)

    def __parse_while_statement(self) -> WhileNode:
        while_token = self.__expect_token(TokenType.WHILE)
        if not self.__peek() or self.__peek().token_type in [TokenType.MOOD_LINE_BORDER_END, TokenType.SIMPLE_LINE_BORDER]:
            raise ValueError(f"While condition missing at line {while_token.line}!")
        condition = self.__parse_expression()
        
        if self.in_mood_line:
            condition = UnaryOpNode(NOT, condition)
        
        self.__expect_line_end()
        
        body = self.__parse_code_block()

        return WhileNode(condition, body, while_token.line)

    def __try_parse_else_block(self) -> Optional[CodeBlockNode]:
        saved_index = self.current_token_index
        
        token = self.__peek()
        if token and token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]:
            self.current_token_index += 1
            token = self.__peek()
            if token and token.token_type == TokenType.ELSE:
                self.__eat()
                block = self.__parse_code_block()
                return block
        
        self.current_token_index = saved_index
        return None

    def __skip_line_start(self):
        token = self.__peek()
        if token and token.token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_START]: 
            if token.token_type == TokenType.MOOD_LINE_BORDER_START: 
                self.in_mood_line = True
            self.__eat()

    def __parse_code_block(self) -> CodeBlockNode:
        self.__skip_line_start()
        self.__expect_token(TokenType.BLOCK_BORDER)
        self.__expect_token(TokenType.SIMPLE_LINE_BORDER) 
        self.__expect_newline_or_end()

        statements, return_node = self.__parse_block_contents()

        self.__skip_line_start() 
        self.__expect_token(TokenType.BLOCK_BORDER)  
        self.__expect_token(TokenType.SIMPLE_LINE_BORDER) 
        self.__expect_newline_or_end()

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
                self.__expect_line_end()
                break

            statement = self.__parse_statement()
            if statement:
                statements.append(statement)

        return statements, return_node

    def __parse_return(self) -> ReturnNode:
        self.__expect_token(TokenType.RETURN) # Consumes the first '...'
        
        # FIX: Check if the next token is the end of the line border token (# or ~#). 
        # This signifies a void return: # ... # or #~ ... ~#
        next_token_type = self.__peek().token_type if self.__peek() else None
        
        if next_token_type in [TokenType.SIMPLE_LINE_BORDER, TokenType.MOOD_LINE_BORDER_END]:
            # This is the VOID return: # ... # or #~ ... ~#
            return ReturnNode(None) 

        # Non-void return: # ... expr ... # or #~ ... expr ... ~#
        expr = self.__parse_expression()
        self.__expect_token(TokenType.RETURN) # Consumes the second '...'
        return ReturnNode(expr)






