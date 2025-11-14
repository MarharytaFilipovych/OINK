#!/usr/bin/env python3
from .stmt_node import StmtNode
from ..llvm_specifics.data_type import DataType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visitor.ast_visitor import ASTVisitor
    from .function_decl_node import FunctionDeclNode

class StructField:
    def __init__(self, field_type: DataType, name: str, mutable: bool):
        self.field_type = field_type
        self.name = name
        self.mutable = mutable

class StructDeclNode(StmtNode):
    def __init__(self, struct_name: str, fields: list[StructField], 
                 member_functions: list['FunctionDeclNode'], line: int):
        super().__init__(struct_name, None, line)
        self.fields = fields
        self.member_functions = member_functions

    def accept(self, visitor: 'ASTVisitor'):
        return visitor.visit_struct_declaration(self)
