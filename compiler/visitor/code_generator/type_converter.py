#!/usr/bin/env python3
from typing import Union
from ...llvm_specifics.data_type import DataType
from ...node.id_node import IDNode
from ...node.number_node import NumberNode
from ...node.bool_node import BooleanNode
from ...node.binary_op_node import BinaryOpNode
from ...node.unary_op_node import UnaryOpNode
from ...node.struct_init_node import StructInitNode
from ...node.member_access_node import MemberAccessNode
from ...node.function_call_node import FunctionCallNode
from ...constants import I16_MAX, I16_MIN, I32_MAX, I32_MIN


def _get_binary_op_type(node: BinaryOpNode) -> DataType:
    if node.operator.is_for_comparison() or node.operator.is_logical():
        return DataType.BOOL
    return node.result_type if node.result_type else DataType.I32


def _parse_return_type(type_str: str) -> Union[DataType, str]:
    try:
        return DataType.from_string(type_str)
    except (ValueError, AttributeError):
        return type_str


class TypeConverter:
    def __init__(self, variable_registry, struct_ops, function_return_types: dict):
        self.variable_registry = variable_registry
        self.struct_ops = struct_ops
        self.function_return_types = function_return_types

    def get_llvm_type(self, type_obj) -> str:
        if isinstance(type_obj, DataType):
            return type_obj.to_llvm()
        
        # FIX: Check for primitive LLVM type strings and return them directly (Test 39)
        if isinstance(type_obj, str) and type_obj in ['i16', 'i32', 'i64', 'i1', 'void']:
            return type_obj
            
        if isinstance(type_obj, str):
            try:
                return DataType.from_string(type_obj).to_llvm()
            except ValueError:
                return f"%struct.{type_obj}*"
        return "i32"

    def get_node_type(self, node) -> Union[DataType, str]:
        if isinstance(node, IDNode):
            return self.variable_registry.get_variable_type(node.value)
        if isinstance(node, NumberNode):
            return self._infer_number_type(int(node.value))
        if isinstance(node, BooleanNode):
            return DataType.BOOL
        if isinstance(node, BinaryOpNode):
            return _get_binary_op_type(node)
        if isinstance(node, UnaryOpNode):
            return DataType.BOOL
        if isinstance(node, StructInitNode):
            return node.value
        if isinstance(node, MemberAccessNode):
            return self._get_member_access_type(node)
        if isinstance(node, FunctionCallNode):
            return self._get_function_return_type(node)
        return DataType.I32

    @staticmethod
    def _infer_number_type(value: int) -> DataType:
        if I16_MIN <= value <= I16_MAX:
            return DataType.I16
        if I32_MIN <= value <= I32_MAX:
            return DataType.I32
        return DataType.I64

    def _get_member_access_type(self, node: MemberAccessNode) -> Union[DataType, str]:
        obj_type = self.variable_registry.get_variable_type(node.value)
        
        if not isinstance(obj_type, str):
            return obj_type
        
        fields = self.struct_ops.struct_definitions[obj_type]
        field_info = next((f for f in fields if f[0] == node.member_name), None)
        
        if not field_info:
            return DataType.I32
        
        try:
            return DataType.from_string(field_info[2])
        except ValueError:
            return field_info[2]

    def _get_function_return_type(self, node: FunctionCallNode) -> Union[DataType, str]:
        if node.object_name:
            obj_type = self.variable_registry.get_variable_type(node.object_name)
            if isinstance(obj_type, str):
                mangled_name = f"{obj_type}_{node.value}".replace('&', '_')
                type_str = self.function_return_types.get(mangled_name, "i32")
                return _parse_return_type(type_str)
        
        func_name = node.value.replace('&', '_')
        type_str = self.function_return_types.get(func_name, "i32")
        return _parse_return_type(type_str)

    def infer_operand_type(self, left_node, right_node) -> str:
        left_type = self.get_node_type(left_node)
        right_type = self.get_node_type(right_node)

        if not isinstance(left_type, DataType) or not isinstance(right_type, DataType):
            return "i32"

        if left_type == DataType.I64 or right_type == DataType.I64:
            return "i64"
        if left_type == DataType.I32 or right_type == DataType.I32:
            return "i32"
        if left_type == DataType.I16 or right_type == DataType.I16:
            return "i16"
        return "i1"