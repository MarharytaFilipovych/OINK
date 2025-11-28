#!/usr/bin/env python3
from .expr_node import ExprNode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from visitor.ast_visitor import ASTVisitor

class InterpolatedStringNode(ExprNode):
    def __init__(self, parts: list, line: int):
        self.parts = parts
        self.line = line

    def accept(self, visitor: 'ASTVisitor'):
        return visitor.visit_interpolated_string(self)