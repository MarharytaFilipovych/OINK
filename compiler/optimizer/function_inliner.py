#!/usr/bin/env python3
from ..node.program_node import ProgramNode
from ..node.decl_node import DeclNode
from ..node.assign_node import AssignNode
from ..node.function_decl_node import FunctionDeclNode
from ..node.function_call_node import FunctionCallNode
from ..node.id_node import IDNode
from ..node.code_block_node import CodeBlockNode
from ..node.stmt_node import StmtNode
from ..node.if_node import IfNode
from ..node.elif_node import ElifNode
from ..node.while_node import WhileNode
from ..node.expr_node import ExprNode
from ..node.binary_op_node import BinaryOpNode
from ..node.unary_op_node import UnaryOpNode
from ..node.struct_init_node import StructInitNode
from ..node.print_node import PrintNode
from .function_usage_analyzer import FunctionUsageAnalyzer

class FunctionInliner:
    def __init__(self):
        self.inlined_count = 0
        self.param_mapping: dict[str, ExprNode] = {}
        self.inlined_functions: set[str] = set()

    def inline_single_use(self, node: ProgramNode) -> bool:
        analyzer = FunctionUsageAnalyzer()
        analyzer.analyze_program(node)
        single_use = analyzer.get_single_use_functions()
        
        if not single_use:
            return False
        
        inlined_any = False
        for func_name in list(single_use):
            func_def = analyzer.function_definitions.get(func_name)
            if func_def and self._can_inline(func_def):
                self._inline_function(node, func_name, func_def)
                self.inlined_functions.add(func_name)
                self.inlined_count += 1
                inlined_any = True
        
        if inlined_any:
            node.function_declarations = [
                f for f in node.function_declarations 
                if f.variable not in self.inlined_functions or not self._can_inline(f)
            ]
        
        return inlined_any

    def _can_inline(self, func_def: FunctionDeclNode) -> bool:
        from ..llvm_specifics.data_type import DataType
        if func_def.return_type == DataType.VOID:
            return False
        if not func_def.body.return_node:
            return False
        if func_def.body.statements:
            return False
        return True

    def _inline_function(self, program: ProgramNode, func_name: str, func_def: FunctionDeclNode):
        program.statement_nodes = [
            self._inline_in_statement(stmt, func_name, func_def)
            for stmt in program.statement_nodes
        ]
        
        if program.return_node and program.return_node.expr_node:
            program.return_node.expr_node = self._inline_in_expression(
                program.return_node.expr_node, func_name, func_def
            )

        for struct in program.struct_declarations:
            for member_func in struct.member_functions:
                self._inline_in_code_block(member_func.body, func_name, func_def)

    def _inline_in_statement(self, stmt: StmtNode, func_name: str, func_def: FunctionDeclNode) -> StmtNode:
        if isinstance(stmt, DeclNode):
            if stmt.expr_node:
                stmt.expr_node = self._inline_in_expression(stmt.expr_node, func_name, func_def)
        elif isinstance(stmt, AssignNode):
            stmt.expr_node = self._inline_in_expression(stmt.expr_node, func_name, func_def)
        elif isinstance(stmt, IfNode):
            stmt.condition = self._inline_in_expression(stmt.condition, func_name, func_def)
            self._inline_in_code_block(stmt.block, func_name, func_def)
            for elif_node in stmt.elif_blocks:
                elif_node.condition = self._inline_in_expression(elif_node.condition, func_name, func_def)
                self._inline_in_code_block(elif_node.block, func_name, func_def)
            if stmt.else_block:
                self._inline_in_code_block(stmt.else_block, func_name, func_def)
        elif isinstance(stmt, WhileNode):
            stmt.condition = self._inline_in_expression(stmt.condition, func_name, func_def)
            self._inline_in_code_block(stmt.block, func_name, func_def)
        elif isinstance(stmt, PrintNode):
            stmt.expr_node = self._inline_in_expression(stmt.expr_node, func_name, func_def)
        return stmt

    def _inline_in_code_block(self, block: CodeBlockNode, func_name: str, func_def: FunctionDeclNode):
        block.statements = [
            self._inline_in_statement(stmt, func_name, func_def)
            for stmt in block.statements
        ]
        if block.return_node and block.return_node.expr_node:
            block.return_node.expr_node = self._inline_in_expression(
                block.return_node.expr_node, func_name, func_def
            )

    def _inline_in_expression(self, expr: ExprNode, func_name: str, func_def: FunctionDeclNode) -> ExprNode:
        if isinstance(expr, FunctionCallNode) and expr.value == func_name and expr.object_name is None:
            return self._create_inlined_expression(expr, func_def)
        elif isinstance(expr, BinaryOpNode):
            expr.left = self._inline_in_expression(expr.left, func_name, func_def)
            expr.right = self._inline_in_expression(expr.right, func_name, func_def)
        elif isinstance(expr, UnaryOpNode):
            expr.operand = self._inline_in_expression(expr.operand, func_name, func_def)
        elif isinstance(expr, FunctionCallNode):
            expr.arguments = [
                self._inline_in_expression(arg, func_name, func_def)
                for arg in expr.arguments
            ]
        elif isinstance(expr, StructInitNode):
            expr.init_expressions = [
                self._inline_in_expression(e, func_name, func_def)
                for e in expr.init_expressions
            ]
        return expr

    def _create_inlined_expression(self, call: FunctionCallNode, func_def: FunctionDeclNode) -> ExprNode:
        self.param_mapping = {
            param.name: arg
            for param, arg in zip(func_def.params, call.arguments)
        }
        
        if func_def.body.return_node and func_def.body.return_node.expr_node:
            return self._substitute_parameters(func_def.body.return_node.expr_node)
        
        return call

    def _substitute_parameters(self, expr: ExprNode) -> ExprNode:
        if isinstance(expr, IDNode) and expr.value in self.param_mapping:
            return self.param_mapping[expr.value]
        elif isinstance(expr, BinaryOpNode):
            expr.left = self._substitute_parameters(expr.left)
            expr.right = self._substitute_parameters(expr.right)
        elif isinstance(expr, UnaryOpNode):
            expr.operand = self._substitute_parameters(expr.operand)
        elif isinstance(expr, FunctionCallNode):
            expr.arguments = [
                self._substitute_parameters(arg) for arg in expr.arguments
            ]
        return expr