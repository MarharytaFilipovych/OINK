#!/usr/bin/env python3
from typing import TYPE_CHECKING
from ...constants import UNDERLINE
from ...node.decl_node import DeclNode
from ...node.assign_node import AssignNode
from ...node.id_node import IDNode

if TYPE_CHECKING:
    from .semantic_analyzer import SemanticAnalyzer


class VariableAnalyzer:
    def __init__(self, context, semantic_analyzer: 'SemanticAnalyzer'):
        self.context = context
        self.semantic_analyzer = semantic_analyzer

    def visit_declaration(self, node: DeclNode):
        if isinstance(node.data_type, str) and node.data_type != "lambda":
            self._validate_struct_type_exists(node.data_type, node.line)

        if self.context.is_variable_declared(node.variable):
            raise ValueError(f"Variable \"{node.variable}\" has already been declared at line {node.line}!!!!!!!!!!")
        
        
        if not self.context.declare_variable(node.variable, node.data_type, node.mutable):
             raise ValueError(f"Variable \"{node.variable}\" has already been declared at line {node.line}!!!!!!!!!!")

        self.context.currently_initializing = node.variable
        expr_type = node.expr_node.accept(self.semantic_analyzer)
        
        if node.data_type != "lambda":
            self.semantic_analyzer.check_type_match(expr_type, node.data_type, node.line)
        
        self.context.currently_initializing = None

    def _validate_struct_type_exists(self, type_name: str, line: int):
        if not self.context.is_struct_defined(type_name):
            raise ValueError(f"Type \"{type_name}\" is not defined at line {line}! "
                f"Did you forget to declare the struct?")

    def visit_assign(self, node: AssignNode):
        if UNDERLINE in node.variable:
            self.__handle_struct_assignment(node)
        else:
            self.__handle_simple_assignment(node)

    def __handle_struct_assignment(self, node: AssignNode):
        object_name, member_name = node.variable.split(UNDERLINE, 1)

        self.semantic_analyzer.check_variable_declared(object_name, node.line)

        base_type = self.context.get_variable_type(object_name)
        self.__check_struct_type(base_type, member_name, node.line)

        struct_fields = self.context.get_struct_definition(base_type)
        field_info = self.__get_struct_field(struct_fields, member_name, node.line)

        self.__check_struct_mutability(object_name, field_info, node.line)

        data_type = field_info.field_type
        expr_type = node.expr_node.accept(self.semantic_analyzer)
        self.semantic_analyzer.check_type_match(expr_type, data_type, node.line)

    @staticmethod
    def __check_struct_type(base_type, member_name, line):
        if isinstance(base_type, str):
            return
        raise ValueError(f"Cannot assign member \"{member_name}\" on primitive type \"{base_type}\" at line {line}!")

    @staticmethod
    def __get_struct_field(struct_fields, member_name, line):
        field_info = next((f for f in struct_fields if f.name == member_name), None)
        if not field_info:
            raise ValueError(f"Struct has no field \"{member_name}\" at line {line}!")
        return field_info

    def __check_struct_mutability(self, object_name, field_info, line):
        if not self.context.is_variable_mutable(object_name):
            raise ValueError(
                f"Cannot assign to a field of an immutable struct variable \"{object_name}\" at line {line}!")
        if not field_info.mutable:
            raise ValueError(f"Cannot assign to immutable field \"{field_info.name}\" at line {line}!")

    def __handle_simple_assignment(self, node: AssignNode):
        self.semantic_analyzer.check_variable_declared(node.variable, node.line)
        self.semantic_analyzer.check_variable_mutable(node.variable, node.line)

        if isinstance(node.expr_node, IDNode) and node.expr_node.value == node.variable:
            raise ValueError(f"Self-assignment like \"{node.variable} = {node.variable}\" "
                             f"is not allowed at line {node.line}!")

        data_type = self.context.get_variable_type(node.variable)
        expr_type = node.expr_node.accept(self.semantic_analyzer)
        self.semantic_analyzer.check_type_match(expr_type, data_type, node.line)

    def visit_id(self, node: IDNode):
        if self.context.currently_initializing == node.value:
            raise ValueError(f"Self-assignment like \"{node.value} = {node.value}\" "
                f"is not allowed at line {node.line}!")
        self.semantic_analyzer.check_variable_declared(node.value, node.line)
        return self.context.get_variable_type(node.value)