#!/usr/bin/env python3
from .factor_node import FactorNode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visitor.ast_visitor import ASTVisitor

class MemberAccessNode(FactorNode):
    def __init__(self, object_name: str, member_name: str, line: int):
        super().__init__(object_name)
        self.member_name = member_name
        self.line = line

    def accept(self, visitor: 'ASTVisitor'):
        return visitor.visit_member_access(self)