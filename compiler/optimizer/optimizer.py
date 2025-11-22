#!/usr/bin/env python3
from .unused_variable_remover import UnusedVariableRemover
from ..node.program_node import ProgramNode
from .function_inliner import FunctionInliner
from .unused_function_remover import UnusedFunctionRemover

class Optimizer:
    def __init__(self):
        self.variable_remover = UnusedVariableRemover()
        self.function_inliner = FunctionInliner()
        self.function_remover = UnusedFunctionRemover()

    def optimize(self, ast: ProgramNode) -> dict[str, int]:
        while self.variable_remover.remove_unused(ast):
            pass
        
        self.function_inliner.inline_single_use(ast)
        self.function_remover.remove_unused(ast)
        
        return {
            'variables_removed': self.variable_remover.removed_count,
            'functions_inlined': self.function_inliner.inlined_count,
            'functions_removed': self.function_remover.removed_count
        }
