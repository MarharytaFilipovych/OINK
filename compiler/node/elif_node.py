#!/usr/bin/env python3
from .condition_node import ConditionNode
from .stmt_node import StmtNode
from .expr_node import ExprNode
from .code_block_node import CodeBlockNode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visitor.ast_visitor import ASTVisitor

class ElifNode(ConditionNode):
    def __init__(self, condition: ExprNode, then_block: CodeBlockNode, line: int):
        super().__init__(condition, then_block, line)

    def accept(self, visitor: 'ASTVisitor'):
        return visitor.visit_elif_statement(self)
