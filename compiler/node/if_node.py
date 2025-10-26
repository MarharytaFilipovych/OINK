#!/usr/bin/env python3
from .elif_node import ElifNode
from .stmt_node import StmtNode
from .expr_node import ExprNode
from .code_block_node import CodeBlockNode
from typing import TYPE_CHECKING, Optional
from .condition_node import ConditionNode

if TYPE_CHECKING:
    from ..visitor.ast_visitor import ASTVisitor

class IfNode(ConditionNode):
    def __init__(self, condition: ExprNode,
                  then_block: CodeBlockNode,
                  elif_blocks: list[ElifNode],
                  else_block: Optional[CodeBlockNode], line: int):
        super().__init__("", condition, then_block, line)
        self.elif_blocks = elif_blocks
        self.else_block = else_block

    def accept(self, visitor: 'ASTVisitor'):
        return visitor.visit_if_statement(self)
