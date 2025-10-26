#!/usr/bin/env python3
from .stmt_node import StmtNode
from .expr_node import ExprNode
from .code_block_node import CodeBlockNode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visitor.ast_visitor import ASTVisitor

class ConditionNode(StmtNode):
    def __init__(self, condition: ExprNode, block: CodeBlockNode,line: int):
        super().__init__("", condition, line)
        self.condition = condition
        self.block = block

    def accept(self, visitor: 'ASTVisitor'):
        pass
