#!/usr/bin/env python3
from .stmt_node import StmtNode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visitor.ast_visitor import ASTVisitor

class ReadNode(StmtNode):
    def __init__(self, variable: str, line: int):
        super().__init__(variable, None, line)

    def accept(self, visitor: 'ASTVisitor'):
        visitor.visit_read(self)
