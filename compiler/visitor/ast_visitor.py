#!/usr/bin/env python3
from abc import ABC, abstractmethod
from ..node.intr_string_node import InterpolatedStringNode
from ..node.assign_node import AssignNode
from ..node.binary_op_node import BinaryOpNode
from ..node.bool_node import BooleanNode
from ..node.code_block_node import CodeBlockNode
from ..node.decl_node import DeclNode
from ..node.function_call_node import FunctionCallNode
from ..node.function_decl_node import FunctionDeclNode
from ..node.id_node import IDNode
from ..node.if_node import IfNode
from ..node.elif_node import ElifNode
from ..node.lambda_node import LambdaNode
from ..node.print_node import PrintNode
from ..node.read_node import ReadNode
from ..node.member_access_node import MemberAccessNode
from ..node.string_node import StringNode
from ..node.struct_decl_node import StructDeclNode
from ..node.struct_init_node import StructInitNode
from ..node.while_node import WhileNode
from ..node.number_node import NumberNode
from ..node.program_node import ProgramNode
from ..node.return_node import ReturnNode
from ..node.unary_op_node import UnaryOpNode


class ASTVisitor(ABC):
    @abstractmethod
    def visit_program(self, node: ProgramNode):
        pass

    @abstractmethod
    def visit_declaration(self, node: DeclNode):
        pass

    @abstractmethod
    def visit_assign(self, node: AssignNode):
        pass

    @abstractmethod
    def visit_return(self, node: ReturnNode):
        pass

    @abstractmethod
    def visit_binary_operation(self, node: BinaryOpNode):
        pass

    @abstractmethod
    def visit_unary_operation(self, node: UnaryOpNode):
        pass

    @abstractmethod
    def visit_id(self, node: IDNode):
        pass

    @abstractmethod
    def visit_number(self, node: NumberNode):
        pass

    @abstractmethod
    def visit_boolean(self, node: BooleanNode):
        pass

    @abstractmethod
    def visit_if_statement(self, node: IfNode):
        pass

    @abstractmethod
    def visit_elif_statement(self, node: ElifNode):
        pass

    @abstractmethod
    def visit_while_loop(self, node: WhileNode):
        pass

    @abstractmethod
    def visit_code_block(self, node: CodeBlockNode):
        pass

    @abstractmethod
    def visit_function_call(self, node: FunctionCallNode):
        pass

    @abstractmethod
    def visit_function_declaration(self, node: FunctionDeclNode):
        pass

    @abstractmethod
    def visit_read(self, node: ReadNode):
        pass

    @abstractmethod
    def visit_print(self, node: PrintNode):
        pass

    @abstractmethod
    def visit_member_access(self, node: MemberAccessNode):
        pass

    @abstractmethod
    def visit_struct_declaration(self, node: StructDeclNode):
        pass

    @abstractmethod
    def visit_struct_initialization(self, node: StructInitNode):
        pass

    @abstractmethod
    def visit_lambda(self, node: LambdaNode):
        pass

    @abstractmethod
    def visit_string(self, node: StringNode):
        pass

    @abstractmethod
    def visit_interpolated_string(self, node: InterpolatedStringNode):
        pass