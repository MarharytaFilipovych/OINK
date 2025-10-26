#!/usr/bin/env python3
from ..node.condition_node import ConditionNode
from ..constants import *
from .ast_visitor import ASTVisitor
from ..context import Context
from ..llvm_specifics.data_type import DataType
from ..node.assign_node import AssignNode
from ..node.binary_op_node import BinaryOpNode
from ..node.bool_node import BooleanNode
from ..node.code_block_node import CodeBlockNode
from ..node.decl_node import DeclNode
from ..node.id_node import IDNode
from ..node.if_node import IfNode
from ..node.elif_node import ElifNode
from ..node.while_node import WhileNode
from ..node.number_node import NumberNode
from ..node.program_node import ProgramNode
from ..node.return_node import ReturnNode
from ..node.unary_op_node import UnaryOpNode


class SemanticAnalyzer(ASTVisitor):
    def __init__(self):
        self.context = Context()

    def visit_program(self, node: ProgramNode):
        for n in node.statement_nodes:
            n.accept(self)
        node.return_node.accept(self)

    def visit_declaration(self, node: DeclNode):
        if not self.context.declare_variable(node.variable, node.data_type, node.mutable):
            raise ValueError( f"Variable '{node.variable}' has already been declared at line {node.line}!!!!!!!!!!")

        self.context.currently_initializing = node.variable
        expr_type = node.expr_node.accept(self)

        if not self.__is_type_compatible(expr_type, node.data_type):
            raise ValueError( f"Types do not match at line {node.line}: you cannot assign "
                f"{expr_type} to {node.data_type}! Be careful!")

        self.context.currently_initializing = None

    def visit_assign(self, node: AssignNode):
        if not self.context.is_variable_mutable(node.variable):
            raise ValueError(
                f"Sorry, but you cannot assign something new to an immutable "
                f"variable!!! Remove '{node.variable}' from line {node.line}!")

        if isinstance(node.expr_node, IDNode) and node.expr_node.value == node.variable:
            raise ValueError(f"Self-assignment like '{node.variable} = {node.variable}' is not allowed at line {node.line}!")

        data_type = self.context.get_variable_type(node.variable)
        expr_type = node.expr_node.accept(self)

        if not self.__is_type_compatible(expr_type, data_type):
            raise ValueError(f"Types do not match at line {node.line}: you cannot assign "
                f"{expr_type} to {data_type}! Be careful!")

    def visit_return(self, node: ReturnNode) -> DataType:
        return node.expr_node.accept(self)

    def visit_binary_operation(self, node: BinaryOpNode) -> DataType:
        left_type = node.left.accept(self)
        right_type = node.right.accept(self)

        if node.operator.is_for_comparison():
            return self.__compare(node, left_type, right_type)

        if node.operator.is_logical():
            return self.__do_logic(node, left_type, right_type)

        if node.operator.is_for_arithmetic():
            return self.__do_math(node, left_type, right_type)

        raise ValueError(f"Where did you take this operator from?: {node.operator}")

    def __compare(self, node: BinaryOpNode, left_type: DataType, right_type: DataType) -> DataType:
        self.__ensure_operands_are_comparable(node, left_type, right_type)
        return DataType.BOOL

    @staticmethod
    def __ensure_operands_are_comparable(node: BinaryOpNode, left_type: DataType, right_type: DataType):
        if (left_type == DataType.BOOL) != (right_type == DataType.BOOL):
            raise ValueError(f"You cannot compare using {node.operator} boolean with non-boolean!")

    def __do_logic(self, node: BinaryOpNode, left_type: DataType, right_type: DataType) -> DataType:
        self.__ensure_both_operands_are_boolean(node, left_type, right_type)
        return DataType.BOOL

    @staticmethod
    def __ensure_both_operands_are_boolean(node: BinaryOpNode, left_type: DataType, right_type: DataType):
        if left_type != DataType.BOOL or right_type != DataType.BOOL:
            raise ValueError( f"Logical operator {node.operator} requires boolean operands!")

    def __do_math(self, node: BinaryOpNode, left_type: DataType, right_type: DataType) -> DataType:
        self.__ensure_both_operands_are_numbers(node, left_type, right_type)

        if left_type == DataType.I64 or right_type == DataType.I64:
            node.result_type = DataType.I64
        elif left_type == DataType.I32 or right_type == DataType.I32:
            node.result_type = DataType.I32
        else:
            node.result_type = DataType.I16

        return node.result_type

    @staticmethod
    def __ensure_both_operands_are_numbers(node: BinaryOpNode, left_type: DataType, right_type: DataType):
        if left_type == DataType.BOOL or right_type == DataType.BOOL:
            raise ValueError(f"You cannot play math using {node.operator} on booleans!" )

    def visit_id(self, node: IDNode) -> DataType:
        if self.context.currently_initializing == node.value:
            raise ValueError(
                f"Self-assignment like '{node.value} = {node.value}' is not allowed at line {node.line}!")

        if not self.context.is_variable_declared(node.value):
            raise ValueError(
                f"Why did you decide that you are permitted to use uninitialized variables??? "
                f"You placed uninitialized '{node.value}' at line {node.line}!!!")

        return self.context.get_variable_type(node.value)

    def visit_number(self, node: NumberNode) -> DataType:
        value = int(node.value)
        
        if I16_MIN <= value <= I16_MAX:
            return DataType.I16
        elif I32_MIN <= value <= I32_MAX:
            return DataType.I32
        else:
            return DataType.I64

    def visit_boolean(self, node: BooleanNode) -> DataType:
        return DataType.BOOL

    def visit_if_statement(self, node: IfNode):
        self.__validate_condition_and_visit_block(node, "If")
        
        for elif_node in node.elif_blocks:
            elif_node.accept(self)

        if node.else_block:
            node.else_block.accept(self)

    def visit_elif_statement(self, node: ElifNode):
        self.__validate_condition_and_visit_block(node, "Elif")

    def visit_while_loop(self, node: WhileNode):
        self.__validate_condition_and_visit_block(node, "While")

    def __validate_condition_and_visit_block(self, node: ConditionNode, statement_name: str):
        condition_type = node.condition.accept(self)
        if condition_type != DataType.BOOL:
            raise ValueError(f"{statement_name} condition must be of type bool, but you placed "
                f"{condition_type} at line {node.line}! How could you????????")
        node.block.accept(self)

    def visit_code_block(self, node: CodeBlockNode):
        self.context.enter_scope()
        for n in node.statements:
            n.accept(self)
        if node.return_node:
            node.return_node.accept(self)
        self.context.exit_scope()

    def visit_unary_operation(self, node: UnaryOpNode) -> DataType:
        operand_type = node.operand.accept(self)
        if node.operator == NOT:
            if operand_type != DataType.BOOL:
                raise ValueError(f"The NOT operator {node.operator} can only be applied to the boolean values, dummy, "
                    f"but you applied it to {operand_type}! Do you think it is okay?")
            return DataType.BOOL
        raise ValueError(f"Unknown unary operator: {node.operator}")

    @staticmethod
    def __is_type_compatible(source_type: DataType, target_type: DataType) -> bool:
        if source_type == target_type:
            return True
        if source_type == DataType.I16 and target_type in [DataType.I32, DataType.I64]:
            return True
        if source_type == DataType.I32 and target_type == DataType.I64:
            return True
        return False
    
    @staticmethod
    def __set_default_for_type(data_type: DataType):
        if data_type == DataType.BOOL:
            return FALSE
        elif data_type in [DataType.I16, DataType.I32, DataType.I64]:
            return 0
        else:
            raise ValueError(f"No default value defined for {data_type}")
