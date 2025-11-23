#!/usr/bin/env python3
from ..node.program_node import ProgramNode
from ..node.decl_node import DeclNode
from ..node.stmt_node import StmtNode
from .variable_usage_analyzer import VariableUsageAnalyzer

class UnusedVariableRemover:
    def __init__(self):
        self.removed_count = 0

    def remove_unused(self, node: ProgramNode) -> bool:
        analyzer = VariableUsageAnalyzer()
        analyzer.analyze_program(node)
        unused = analyzer.get_unused_variables()
        
        if not unused:
            return False
        
        node.statement_nodes = [
            stmt for stmt in node.statement_nodes
            if not self._should_remove_statement(stmt, unused)
        ]
        
        self.removed_count += len(unused)
        return True

    def _should_remove_statement(self, stmt: StmtNode, unused: set[str]) -> bool:
        if isinstance(stmt, DeclNode) and stmt.variable in unused:
            if stmt.data_type == "lambda":
                return False
            return True
        return False