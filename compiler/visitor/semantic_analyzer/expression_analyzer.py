#!/usr/bin/env python3
from typing import TYPE_CHECKING
from ...constants import I32_MAX, I32_MIN, I16_MAX, I16_MIN, NOT
from ...llvm_specifics.data_type import DataType
from ...node.binary_op_node import BinaryOpNode
from ...node.number_node import NumberNode
from ...node.bool_node import BooleanNode
from ...node.unary_op_node import UnaryOpNode

if TYPE_CHECKING:
    from .semantic_analyzer import SemanticAnalyzer


class ExpressionAnalyzer:
    def __init__(self, context, semantic_analyzer: 'SemanticAnalyzer'):
        self.context = context
        self.semantic_analyzer = semantic_analyzer

    def visit_binary_operation(self, node: BinaryOpNode):
        left_type = node.left.accept(self.semantic_analyzer)
        right_type = node.right.accept(self.semantic_analyzer)
        self._validate_primitive_types(left_type, right_type, node.operator)
        if node.operator.is_for_comparison():
            return self._validate_comparison(left_type, right_type, node.operator)
        if node.operator.is_for_arithmetic():
            return self._validate_arithmetic(left_type, right_type, node.operator, node)
        if node.operator.is_logical():
            return self._validate_logical(left_type, right_type, node.operator)
        raise ValueError(f"Where did you take this operator from?: {node.operator}")

    @staticmethod
    def _validate_primitive_types(left_type, right_type, operator):
        if not isinstance(left_type, DataType) or not isinstance(right_type, DataType):
            raise ValueError(f"Cannot use operator \"{operator}\" on struct types! "
                f"Operators only work with primitive types (i16, i32, i64, bool).")

    @staticmethod
    def _validate_comparison(left_type: DataType, right_type: DataType, operator) -> DataType:
        if (left_type == DataType.BOOL) != (right_type == DataType.BOOL):
            raise ValueError(f"You cannot compare using \"{operator}\" boolean with non-boolean!")
        return DataType.BOOL

    def _validate_arithmetic(self, left_type: DataType, right_type: DataType,
                             operator, node) -> DataType:
        if left_type == DataType.BOOL or right_type == DataType.BOOL:
            raise ValueError(f"You cannot play math using \"{operator}\" on booleans!!!")
        result_type = self._infer_arithmetic_result_type(left_type, right_type)
        node.result_type = result_type
        return result_type

    @staticmethod
    def _validate_logical(left_type: DataType, right_type: DataType, operator) -> DataType:
        if left_type != DataType.BOOL or right_type != DataType.BOOL:
             raise ValueError(f"Logical operator \"{operator}\" requires boolean operands, "
                 f"but got \"{left_type}\" and \"{right_type}\"!")
    
        return DataType.BOOL

    @staticmethod
    def _infer_arithmetic_result_type(left_type: DataType, right_type: DataType) -> DataType:
        if left_type == DataType.I64 or right_type == DataType.I64:
            return DataType.I64
        if left_type == DataType.I32 or right_type == DataType.I32:
            return DataType.I32
        return DataType.I16

    @staticmethod
    def visit_number(node: NumberNode) -> DataType:
        value = int(node.value)
        if I16_MIN <= value <= I16_MAX:
            return DataType.I16
        if I32_MIN <= value <= I32_MAX:
            return DataType.I32
        return DataType.I64

    @staticmethod
    def visit_boolean(node: BooleanNode) -> DataType:
        return DataType.BOOL

    def visit_unary_operation(self, node: UnaryOpNode) -> DataType:
        operand_type = node.operand.accept(self.semantic_analyzer)
        if node.operator == NOT:
            if operand_type != DataType.BOOL:
                raise ValueError(f"The NOT operator (💩) can only be applied to boolean values, dummy, "
                    f"but you applied it to \"{operand_type}\"! Do you think it is okay?")
            return DataType.BOOL
        raise ValueError(f"Unknown unary operator: \"{node.operator}\"")