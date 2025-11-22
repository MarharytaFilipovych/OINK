#!/usr/bin/env python3
from .factor_node import FactorNode
from .expr_node import ExprNode
from ..llvm_specifics.data_type import DataType
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..visitor.ast_visitor import ASTVisitor

class LambdaParam:
    def __init__(self, param_type: Union[DataType, str], name: str):
        self.param_type = param_type
        self.name = name

class LambdaNode(FactorNode):
    def __init__(self, params: list[LambdaParam], body: ExprNode, line: int):
        super().__init__("")
        self.params = params
        self.body = body
        self.line = line
        self.lambda_id = None

    def accept(self, visitor: 'ASTVisitor'):
        return visitor.visit_lambda(self)