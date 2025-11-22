#!/usr/bin/env python3
from ..node.program_node import ProgramNode
from ..node.decl_node import DeclNode
from ..node.assign_node import AssignNode
from ..node.id_node import IDNode
from ..node.code_block_node import CodeBlockNode
from ..node.stmt_node import StmtNode
from ..node.if_node import IfNode
from ..node.while_node import WhileNode
from ..node.expr_node import ExprNode
from ..node.binary_op_node import BinaryOpNode
from ..node.unary_op_node import UnaryOpNode
from ..node.member_access_node import MemberAccessNode
from ..node.struct_init_node import StructInitNode
from ..node.function_call_node import FunctionCallNode
from ..node.print_node import PrintNode
from ..node.read_node import ReadNode
from ..constants import UNDERLINE

class VariableUsageAnalyzer:
    def __init__(self):
        self.declared_vars: set[str] = set()
        self.used_vars: set[str] = set()

    def analyze_program(self, node: ProgramNode):
        for stmt in node.statement_nodes:
            self._analyze_statement(stmt)
        if node.return_node and node.return_node.expr_node:
            self._analyze_expression(node.return_node.expr_node)

    def _analyze_statement(self, node: StmtNode):
        if isinstance(node, DeclNode):
            self.declared_vars.add(node.variable)
            if node.expr_node:
                self._analyze_expression(node.expr_node)
        elif isinstance(node, AssignNode):
            if UNDERLINE in node.variable:
                parts = node.variable.split(UNDERLINE)
                self.used_vars.add(parts[0])
            self._analyze_expression(node.expr_node)
        elif isinstance(node, IfNode):
            self._analyze_expression(node.condition)
            self._analyze_code_block(node.block)
            for elif_node in node.elif_blocks:
                self._analyze_expression(elif_node.condition)
                self._analyze_code_block(elif_node.block)
            if node.else_block:
                self._analyze_code_block(node.else_block)
        elif isinstance(node, WhileNode):
            self._analyze_expression(node.condition)
            self._analyze_code_block(node.block)
        elif isinstance(node, FunctionCallNode):
            self._analyze_expression(node)
        elif isinstance(node, PrintNode):
            self._analyze_expression(node.expr_node)
        elif isinstance(node, ReadNode):
            self.used_vars.add(node.variable)

    def _analyze_code_block(self, block: CodeBlockNode):
        for stmt in block.statements:
            self._analyze_statement(stmt)
        if block.return_node and block.return_node.expr_node:
            self._analyze_expression(block.return_node.expr_node)

    def _analyze_expression(self, node: ExprNode):
        if isinstance(node, IDNode):
            self.used_vars.add(node.value)
        elif isinstance(node, BinaryOpNode):
            self._analyze_expression(node.left)
            self._analyze_expression(node.right)
        elif isinstance(node, UnaryOpNode):
            self._analyze_expression(node.operand)
        elif isinstance(node, FunctionCallNode):
            if node.object_name:
                self.used_vars.add(node.object_name)
            for arg in node.arguments:
                self._analyze_expression(arg)
        elif isinstance(node, MemberAccessNode):
            self.used_vars.add(node.value)
        elif isinstance(node, StructInitNode):
            for expr in node.init_expressions:
                self._analyze_expression(expr)

    def get_unused_variables(self) -> set[str]:
        return self.declared_vars - self.used_vars
