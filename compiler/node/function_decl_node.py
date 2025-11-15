#!/usr/bin/env python3
from .stmt_node import StmtNode
from .code_block_node import CodeBlockNode
from ..llvm_specifics.data_type import DataType
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..visitor.ast_visitor import ASTVisitor

class FunctionParam:
    def __init__(self, param_type: DataType, name: str):
        self.param_type = param_type
        self.name = name

class FunctionDeclNode(StmtNode):
    def __init__(self, func_name: str, params: list[FunctionParam], 
                 return_type: Union[DataType, str], body: CodeBlockNode, line: int):
        super().__init__(func_name, None, line)
        self.params = params
        self.return_type = return_type
        self.body = body

    def accept(self, visitor: 'ASTVisitor'):
        return visitor.visit_function_declaration(self)
