#!/usr/bin/env python3
from .ast_node import ASTNode
from .return_node import ReturnNode
from .stmt_node import StmtNode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visitor.ast_visitor import ASTVisitor
    from .struct_decl_node import StructDeclNode
    from .function_decl_node import FunctionDeclNode

class ProgramNode(ASTNode):
    def __init__(self, struct_declarations: list['StructDeclNode'],
                 function_declarations: list['FunctionDeclNode'],
                 statement_nodes: list[StmtNode],
                 return_node: ReturnNode):
        self.struct_declarations = struct_declarations
        self.function_declarations = function_declarations
        self.statement_nodes = statement_nodes
        self.return_node = return_node

    def accept(self, visitor: 'ASTVisitor'):
        return visitor.visit_program(self)
