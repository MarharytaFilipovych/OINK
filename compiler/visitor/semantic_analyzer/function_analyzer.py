#!/usr/bin/env python3
from pickle import GLOBAL
from typing import Optional, TYPE_CHECKING
from ...llvm_specifics.data_type import DataType
from ...node.function_decl_node import FunctionDeclNode
from ...node.function_call_node import FunctionCallNode

if TYPE_CHECKING:
    from .semantic_analyzer import SemanticAnalyzer


class FunctionAnalyzer:
    def __init__(self, context, semantic_analyzer: 'SemanticAnalyzer'):
        self.context = context
        self.semantic_analyzer = semantic_analyzer

    def register_function(self, node: FunctionDeclNode):
        param_types = [self.semantic_analyzer.type_to_string(p.param_type) for p in node.params]
        return_type = self.semantic_analyzer.type_to_string(node.return_type)
        self.context.define_function(GLOBAL, node.variable, param_types, return_type)

    def visit_function_declaration(self, node: FunctionDeclNode):
        self.context.enter_scope()
        self._declare_function_parameters(node)

        if node.return_type != DataType.VOID and not node.body.return_node:
            raise ValueError(f"Function \"{node.variable}\" must have a return statement!")

        self.semantic_analyzer._expected_return_type = node.return_type
        self.semantic_analyzer._function_name = node.variable

        node.body.accept(self.semantic_analyzer)

        self.semantic_analyzer._expected_return_type = None
        self.semantic_analyzer._function_name = None
        self.context.exit_scope()

    def _declare_function_parameters(self, node: FunctionDeclNode):
        for param in node.params:
            if not self.context.declare_variable(param.name, param.param_type, mutable=False):
                raise ValueError(f"Duplicate parameter \"{param.name}\" in function \"{node.variable}\"!")

    def visit_function_call(self, node: FunctionCallNode):
        if self.context.is_variable_declared(node.value):
            var_type = self.context.get_variable_type(node.value)
            if var_type == "lambda":
                return self._validate_lambda_call(node)
        
        function_scope = self._identify_function_scope(node.object_name)
        
        if not self.context.is_function_defined(function_scope, node.value):
            if self.semantic_analyzer.current_struct_context and function_scope != GLOBAL:
                function_scope = GLOBAL
            
            if not self.context.is_function_defined(function_scope, node.value):
                raise ValueError(f"Function \"{node.value}\" not defined at line {node.line}!")
        
        func_info = self.context.get_function_info(function_scope, node.value)
        self._validate_argument_count(node, func_info)
        self._validate_argument_types(node, func_info)
        return self.semantic_analyzer.string_to_type(func_info.return_type)

    def _validate_lambda_call(self, node: FunctionCallNode):
        for arg in node.arguments:
            arg.accept(self.semantic_analyzer)
        return DataType.I32

    @staticmethod
    def _validate_argument_count(node: FunctionCallNode, func_info):
        if len(node.arguments) != len(func_info.param_types):
            raise ValueError(f"Function \"{node.value}\" expects {len(func_info.param_types)} arguments "
                f"but got {len(node.arguments)} at line {node.line}!")

    def _validate_argument_types(self, node: FunctionCallNode, func_info):
        for i, (arg, expected_type_str) in enumerate(zip(node.arguments, func_info.param_types)):
            arg_type = arg.accept(self.semantic_analyzer)
            expected_type = self.semantic_analyzer.string_to_type(expected_type_str)
            if not self.semantic_analyzer.types_match(arg_type, expected_type):
                raise ValueError(f"Argument {i + 1} to function \"{node.value}\" has type "
                    f"\"{self.semantic_analyzer.type_to_string(arg_type)}\" but expected \"{expected_type_str}\" "
                    f"at line {node.line}!")

    def _identify_function_scope(self, object_name: Optional[str]) -> str:
        if not object_name:
            return self.semantic_analyzer.current_struct_context if self.semantic_analyzer.current_struct_context else GLOBAL

        var_type = self.context.get_variable_type(object_name)
        return var_type if isinstance(var_type, str) else GLOBAL