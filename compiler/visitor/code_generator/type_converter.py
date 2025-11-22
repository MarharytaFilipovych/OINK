#!/usr/bin/env python3
from typing import Union
from ...llvm_specifics.data_type import DataType
from ...node.id_node import IDNode
from ...node.lambda_node import LambdaNode
from ...node.number_node import NumberNode
from ...node.bool_node import BooleanNode
from ...node.binary_op_node import BinaryOpNode
from ...node.unary_op_node import UnaryOpNode
from ...node.struct_init_node import StructInitNode
from ...node.member_access_node import MemberAccessNode
from ...node.function_call_node import FunctionCallNode
from ...constants import I16_MAX, I16_MIN, I32_MAX, I32_MIN, UNDERLINE, VARIABLE_ALLOWED_SIGN


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

    @staticmethod
    def get_llvm_type(type_obj) -> str:
        llvm_types = {
            DataType.I16.to_llvm(),
            DataType.I32.to_llvm(),
            DataType.I64.to_llvm(),
            DataType.BOOL.to_llvm(),
            DataType.VOID.to_llvm()
        }

        if isinstance(type_obj, DataType):
            return type_obj.to_llvm()
        if isinstance(type_obj, str):
            if type_obj in llvm_types:
                return type_obj
            try:
                return DataType.from_string(type_obj).to_llvm()
            except ValueError:
                return f"%struct.{type_obj}*"
        return DataType.I32.to_llvm()

    def get_node_type(self, node) -> Union[DataType, str]:
        if isinstance(node, IDNode):
            var_type = self.variable_registry.get_variable_type(node.value)
            return var_type if var_type is not None else DataType.I32
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
        if isinstance(node, LambdaNode):
            return f"lambda_{id(node)}"
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
        if obj_type is None:
            return DataType.I32
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
                mangled_name = f"{obj_type}_{node.value}".replace(VARIABLE_ALLOWED_SIGN, UNDERLINE)
                type_str = self.function_return_types.get(mangled_name, DataType.I32.to_llvm())
                return _parse_return_type(type_str)

        func_name = node.value.replace(VARIABLE_ALLOWED_SIGN, UNDERLINE)
        type_str = self.function_return_types.get(func_name, DataType.I32.to_llvm())
        return _parse_return_type(type_str)

    def infer_operand_type(self, left_node, right_node) -> str:
        left_type = self.get_node_type(left_node)
        right_type = self.get_node_type(right_node)

        if not isinstance(left_type, DataType) or not isinstance(right_type, DataType):
            return DataType.I32.to_llvm()

        if left_type == DataType.I64 or right_type == DataType.I64:
            return DataType.I64.to_llvm()
        if left_type == DataType.I32 or right_type == DataType.I32:
            return DataType.I32.to_llvm()
        if left_type == DataType.I16 or right_type == DataType.I16:
            return DataType.I16.to_llvm()
        return DataType.BOOL.to_llvm()