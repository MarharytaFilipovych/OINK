#!/usr/bin/env python3
from .stmt_node import StmtNode
from .expr_node import ExprNode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visitor.ast_visitor import ASTVisitor

class PrintNode(StmtNode):
    def __init__(self, expr_node: ExprNode, line: int):
        super().__init__("", expr_node, line)

    def accept(self, visitor: 'ASTVisitor'):
        visitor.visit_print(self)