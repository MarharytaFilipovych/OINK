#!/usr/bin/env python3
from ..node.program_node import ProgramNode
from ..node.decl_node import DeclNode
from ..node.assign_node import AssignNode
from ..node.function_decl_node import FunctionDeclNode
from ..node.function_call_node import FunctionCallNode
from ..node.code_block_node import CodeBlockNode
from ..node.stmt_node import StmtNode
from ..node.if_node import IfNode
from ..node.while_node import WhileNode
from ..node.expr_node import ExprNode
from ..node.binary_op_node import BinaryOpNode
from ..node.unary_op_node import UnaryOpNode
from ..node.struct_init_node import StructInitNode
from ..node.print_node import PrintNode
from ..node.lambda_node import LambdaNode

class FunctionUsageAnalyzer:
    def __init__(self):
        self.function_calls: dict[str, int] = {}
        self.function_definitions: dict[str, FunctionDeclNode] = {}

    def analyze_program(self, node: ProgramNode):
        for func in node.function_declarations:
            self.function_definitions[func.variable] = func
            self.function_calls[func.variable] = 0
        
        for struct in node.struct_declarations:
            for member_func in struct.member_functions:
                self._analyze_member_function(member_func)
        
        for stmt in node.statement_nodes:
            self._analyze_statement(stmt)
        
        if node.return_node and node.return_node.expr_node:
            self._analyze_expression(node.return_node.expr_node)

    def _analyze_member_function(self, func):
        for stmt in func.body.statements:
            self._analyze_statement(stmt)
        if func.body.return_node and func.body.return_node.expr_node:
            self._analyze_expression(func.body.return_node.expr_node)

    def _analyze_statement(self, node: StmtNode):
        if isinstance(node, DeclNode):
            if node.expr_node:
                self._analyze_expression(node.expr_node)
        elif isinstance(node, AssignNode):
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

    def _analyze_code_block(self, block: CodeBlockNode):
        for stmt in block.statements:
            self._analyze_statement(stmt)
        if block.return_node and block.return_node.expr_node:
            self._analyze_expression(block.return_node.expr_node)

    def _analyze_expression(self, node: ExprNode):
        if isinstance(node, BinaryOpNode):
            self._analyze_expression(node.left)
            self._analyze_expression(node.right)
        elif isinstance(node, UnaryOpNode):
            self._analyze_expression(node.operand)
        elif isinstance(node, FunctionCallNode):
            if node.value in self.function_calls and node.object_name is None:
                self.function_calls[node.value] += 1
            elif node.value not in self.function_calls and node.object_name is None:
                # This handles functions not yet defined (e.g., recursive calls, or inlining context)
                self.function_calls[node.value] = 1 
            for arg in node.arguments:
                self._analyze_expression(arg)
        elif isinstance(node, StructInitNode):
            for expr in node.init_expressions:
                self._analyze_expression(expr)
        elif isinstance(node, LambdaNode):
            if hasattr(node, 'body') and node.body:
                self._analyze_expression(node.body)

    def get_single_use_functions(self) -> set[str]:
        return {name for name in self.function_definitions.keys() 
                if self.function_calls.get(name, 0) == 1}

    def get_unused_functions(self) -> set[str]:
        return {name for name in self.function_definitions.keys() 
                if self.function_calls.get(name, 0) == 0}