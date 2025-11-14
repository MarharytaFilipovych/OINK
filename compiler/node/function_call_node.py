#!/usr/bin/env python3
from .factor_node import FactorNode
from .expr_node import ExprNode
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..visitor.ast_visitor import ASTVisitor

class FunctionCallNode(FactorNode):
    def __init__(self, func_name: str, arguments: list[ExprNode], line: int,
                 object_name: Optional[str] = None):
        super().__init__(func_name)
        self.arguments = arguments
        self.line = line
        self.object_name = object_name
        
    def accept(self, visitor: 'ASTVisitor'):
        return visitor.visit_function_call(self)
