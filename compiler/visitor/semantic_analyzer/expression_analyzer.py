#!/usr/bin/env python3
from typing import TYPE_CHECKING
from ...constants import I32_MAX, I32_MIN, I16_MAX, I16_MIN, NOT
from ...llvm_specifics.data_type import DataType
from ...node.binary_op_node import BinaryOpNode
from ...node.number_node import NumberNode
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
        self.__validate_primitive_types(left_type, right_type, node.operator)
        if node.operator.is_for_comparison():
            return self.__validate_comparison(left_type, right_type, node.operator)
        if node.operator.is_for_arithmetic():
            return self.__validate_arithmetic(left_type, right_type, node.operator, node)
        if node.operator.is_logical():
            return self.__validate_logical(left_type, right_type, node.operator)
        raise ValueError(f"Where did you take this operator from?: {self._format_operator(node.operator)}")

    @staticmethod
    def _format_operator(operator):
        op_map = {
            '+': '❤️ (addition)',
            '-': '💔 (subtraction)',
            '*': '💞 (multiplication)',
            '/': '💕 (division)',
            '==': '🌸🌸 (equals)',
            '!=': '💩🌸 (not equals)',
            '>': '> (greater than)',
            '<': '< (less than)',
            '>=': '🌸> (greater or equal)',
            '<=': '🌸< (less or equal)',
            'and': 'hru (logical AND)',
            'or': 'bruh (logical OR)',
        }
        return op_map.get(str(operator), str(operator))

    def __validate_primitive_types(self, left_type, right_type, operator):
        if not isinstance(left_type, DataType) or not isinstance(right_type, DataType):
            raise ValueError(f"Cannot use operator {self._format_operator(operator)} on struct types! "
                f"Operators only work with primitive types (🐽 i16, 🐷 i32, 🐗 i64, wow bool).")

    def __validate_comparison(self, left_type: DataType, right_type: DataType, operator) -> DataType:
        if (left_type == DataType.BOOL) != (right_type == DataType.BOOL):
            raise ValueError(f"You cannot compare using {self._format_operator(operator)} boolean with non-boolean!")
        return DataType.BOOL

    def __validate_arithmetic(self, left_type: DataType, right_type: DataType,
                              operator, node) -> DataType:
        if left_type in (DataType.BOOL, DataType.STRING) or right_type in (DataType.BOOL, DataType.STRING):
            op_name = self._format_operator(operator)
            left_str = self._format_type(left_type)
            right_str = self._format_type(right_type)
            line = node.left.line if hasattr(node.left, 'line') else node.right.line
            raise ValueError(f"You cannot use operator {op_name} for arithmetic on incompatible types: "
                             f"'{left_str}' and '{right_str}' at line {line}! "
                             f"Only integer types (🐽, 🐷, 🐗) are supported.")
        result_type = self.__infer_arithmetic_result_type(left_type, right_type)
        node.result_type = result_type
        return result_type

    def __validate_logical(self, left_type: DataType, right_type: DataType, operator) -> DataType:
        if left_type != DataType.BOOL or right_type != DataType.BOOL:
             raise ValueError(f"Logical operator {self._format_operator(operator)} requires boolean operands, "
                 f"but got {self._format_type(left_type)} and {self._format_type(right_type)}!")
    
        return DataType.BOOL

    @staticmethod
    def _format_type(data_type):
        type_map = {
            DataType.I16: "🐽 (i16)",
            DataType.I32: "🐷 (i32)",
            DataType.I64: "🐗 (i64)",
            DataType.BOOL: "wow (bool)",
            DataType.VOID: "😑 (void)",
            DataType.STRING: "👺 (string)",
        }
        return type_map.get(data_type, str(data_type))

    @staticmethod
    def __infer_arithmetic_result_type(left_type: DataType, right_type: DataType) -> DataType:
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
    def visit_boolean(node) -> DataType:
        return DataType.BOOL
    
    @staticmethod
    def visit_string(node) -> DataType:
        return DataType.STRING

    def visit_unary_operation(self, node: UnaryOpNode) -> DataType:
        operand_type = node.operand.accept(self.semantic_analyzer)
        if node.operator == NOT:
            if operand_type != DataType.BOOL:
                raise ValueError(f"The NOT operator (💩) can only be applied to boolean values, dummy, "
                    f"but you applied it to {self._format_type(operand_type)}! Do you think it is okay?")
            return DataType.BOOL
        raise ValueError(f"Unknown unary operator: {self._format_operator(node.operator)}")