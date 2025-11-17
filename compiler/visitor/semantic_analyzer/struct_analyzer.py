#!/usr/bin/env python3
from typing import TYPE_CHECKING
from ...llvm_specifics.data_type import DataType
from ...node.struct_decl_node import StructDeclNode
from ...node.struct_init_node import StructInitNode
from ...node.member_access_node import MemberAccessNode

if TYPE_CHECKING:
    from .semantic_analyzer import SemanticAnalyzer


class StructAnalyzer:
    def __init__(self, context, semantic_analyzer: 'SemanticAnalyzer'):
        self.context = context
        self.semantic_analyzer = semantic_analyzer

    def visit_struct_declaration(self, node: StructDeclNode):
        self._check_duplicate_fields(node)
        self._validate_field_types(node)
        self.context.define_struct(node.variable, node.fields)
        self._register_member_functions(node.variable, node.member_functions)
        [self._analyze_member_function(node.variable, func) for func in node.member_functions]

    def _register_member_functions(self, struct_name: str, member_functions):
        member_func_names = set()
        for member_function in member_functions:
            if member_function.variable in member_func_names:
                raise ValueError(f"Duplicate member function \"{member_function.variable}\" "
                    f"in struct \"{struct_name}\" at line {member_function.line}! "
                    f"Don't you have enough imagination to create sth new???")
            member_func_names.add(member_function.variable)
            param_types = [self.semantic_analyzer._type_to_string(p.param_type) for p in member_function.params]
            return_type = self.semantic_analyzer._type_to_string(member_function.return_type)
            self.context.define_function(struct_name, member_function.variable,
                                         param_types, return_type)

    @staticmethod
    def _check_duplicate_fields(node: StructDeclNode):
        field_names = set()
        for field in node.fields:
            if field.name in field_names:
                raise ValueError(f"Duplicate field name \"{field.name}\" in struct \"{node.variable}\" "
                    f"at line {node.line}! GET RID OF IT!")
            field_names.add(field.name)

    def _validate_field_types(self, node: StructDeclNode):
        for field in node.fields:
            if not self._is_valid_type(field.field_type):
                raise ValueError(f"The type \"{field.field_type}\" for field \"{field.name}\" "
                 f"in struct \"{node.variable}\" at line {node.line} does not exist!")

    def _is_valid_type(self, type_obj) -> bool:
        if isinstance(type_obj, DataType):
            return True
        if isinstance(type_obj, str):
            return self.context.is_struct_defined(type_obj)
        return False

    def visit_struct_initialization(self, node: StructInitNode):
        if not self.context.is_struct_defined(node.value):
            raise ValueError(f"No such struct type \"{node.value}\" at line {node.line}!")
        struct_fields = self.context.get_struct_definition(node.value)
        self._validate_field_count(node, struct_fields)
        self._validate_field_types_in_init(node, struct_fields)
        return node.value

    @staticmethod
    def _validate_field_count(node: StructInitNode, struct_fields):
        if len(node.init_expressions) != len(struct_fields):
            raise ValueError(f"Struct \"{node.value}\" expects {len(struct_fields)} fields "
                f"but you typed {len(node.init_expressions)} at line {node.line}!")

    def _validate_field_types_in_init(self, node: StructInitNode, struct_fields):
        for i, field in enumerate(struct_fields):
            expr_type = node.init_expressions[i].accept(self.semantic_analyzer)
            expected_type = field.field_type
            if not self.semantic_analyzer._types_match(expr_type, expected_type):
                raise ValueError(f"Type mismatch for field \"{field.name}\" in struct \"{node.value}\": "
                    f"expected \"{expected_type}\", but you typed \"{expr_type}\" at line {node.line}!")

    def visit_member_access(self, node: MemberAccessNode):
        self.semantic_analyzer._check_variable_declared(node.value, node.line)
        base_type = self.context.get_variable_type(node.value)
        if not isinstance(base_type, str):
            raise ValueError(f"Cannot access member \"{node.member_name}\" on primitive type "
                f"\"{base_type}\" at line {node.line}!")
        struct_fields = self.context.get_struct_definition(base_type)
        field_info = next((f for f in struct_fields if f.name == node.member_name), None)
        if not field_info:
            raise ValueError(f"Struct \"{base_type}\" has no field \"{node.member_name}\" at line {node.line}!")
        return field_info.field_type

    def _analyze_member_function(self, struct_name: str, node):
        self.context.enter_scope()
        self.semantic_analyzer._current_struct_context = struct_name

        struct_fields = self.context.get_struct_definition(struct_name)
        for field in struct_fields:
            self.context.declare_variable(field.name, field.field_type, field.mutable)

        self._declare_function_parameters(node)

        if node.return_type != DataType.VOID and not node.body.return_node:
            raise ValueError(f"Member function \"{node.variable}\" in struct \"{struct_name}\" "
                f"must have a return statement!")

        self.semantic_analyzer._expected_return_type = node.return_type
        self.semantic_analyzer._function_name = f"{struct_name}::{node.variable}"

        node.body.accept(self.semantic_analyzer)

        self.semantic_analyzer._expected_return_type = None
        self.semantic_analyzer._function_name = None
        self.semantic_analyzer._current_struct_context = None
        self.context.exit_scope()

    def _declare_function_parameters(self, node):
        for param in node.params:
            if not self.context.declare_variable(param.name, param.param_type, mutable=False):
                raise ValueError(f"Duplicate parameter \"{param.name}\" in function \"{node.variable}\"!")