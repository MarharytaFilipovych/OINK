#!/usr/bin/env python3
from ..node.program_node import ProgramNode
from .function_usage_analyzer import FunctionUsageAnalyzer

class UnusedFunctionRemover:
    def __init__(self):
        self.removed_count = 0

    def remove_unused(self, node: ProgramNode) -> bool:
        analyzer = FunctionUsageAnalyzer()
        analyzer.analyze_program(node)
        unused = analyzer.get_unused_functions()
        
        if not unused:
            return False
        
        node.function_declarations = [
            f for f in node.function_declarations
            if f.variable not in unused
        ]
        
        self.removed_count += len(unused)
        return True
