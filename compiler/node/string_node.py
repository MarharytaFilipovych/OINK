#!/usr/bin/env python3
from .factor_node import FactorNode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visitor.ast_visitor import ASTVisitor

class StringNode(FactorNode):
    def __init__(self, value: str, line: int):
        super().__init__(value)
        self.line = line

    def accept(self, visitor: 'ASTVisitor'):
        return visitor.visit_string(self)