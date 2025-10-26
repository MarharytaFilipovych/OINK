#!/usr/bin/env python3
from ..llvm_specifics.boolean import Boolean
from ..llvm_specifics.data_type import DataType
from .ast_visitor import ASTVisitor
from ..node.code_block_node import CodeBlockNode
from ..node.id_node import IDNode
from ..node.if_node import IfNode
from ..node.elif_node import ElifNode
from ..node.while_node import WhileNode
from ..node.number_node import NumberNode
from ..node.bool_node import BooleanNode
from ..node.binary_op_node import BinaryOpNode
from ..constants import I32_MAX, I32_MIN
from ..node.unary_op_node import UnaryOpNode
from ..constants import NOT
from ..node.factor_node import FactorNode
from ..node.expr_node import ExprNode
from ..node.program_node import ProgramNode
from ..node.decl_node import DeclNode
from ..node.assign_node import AssignNode
from ..node.return_node import ReturnNode

class CodeGenerator(ASTVisitor):

    def __init__(self):
        self.variable_versions: dict[str, int] = {}
        self.variable_types: dict[str, DataType] = {}
        self.translated_lines: list[str] = []
        self.temp_counter = 0
        self.label_counter = 0

    @staticmethod
    def get_print_function_llvm() -> str:
        return """declare i32 @printf(i8*, ...)

@exit_format = private unnamed_addr constant [29 x i8] c"Program exit with result %d\\0A\\00", align 1

define void @printResult(i32 %val) {
  %fmt_ptr = getelementptr inbounds [29 x i8], [29 x i8]* @exit_format, i32 0, i32 0
  call i32 (i8*, ...) @printf(i8* %fmt_ptr, i32 %val)
  ret void
}
"""

    def visit_program(self, node: ProgramNode) -> str:
        self.translated_lines = []

        for stmt in node.statement_nodes:
            stmt.accept(self)

        node.return_node.accept(self)

        return "\n".join([
            self.get_print_function_llvm(),
            "define i32 @main() {",
            *self.translated_lines,
            "}"])

    def visit_declaration(self, node: DeclNode) -> None:  
        llvm_type = node.data_type.to_llvm()
        value = node.expr_node.accept(self)
        reg = self.__get_variable_register(node.variable)

        self.variable_types[node.variable] = node.data_type

        expr_type = self.__get_node_type(node.expr_node)
        
        value = self.__promote_type(value, expr_type, node.data_type)

        self.translated_lines.append(f"  {reg} = add {llvm_type} 0, {value}")

    def visit_assign(self, node: AssignNode) -> None:
        var_type = self.variable_types[node.variable]
        llvm_type = var_type.to_llvm()
        value = node.expr_node.accept(self)
        reg = self.__get_variable_register(node.variable)
        expr_type = self.__get_node_type(node.expr_node)
        
        value = self.__promote_type(value, expr_type, var_type)

        self.translated_lines.append(f"  {reg} = add {llvm_type} 0, {value}")

    def visit_return(self, node: ReturnNode) -> None:
        value = node.expr_node.accept(self)
        return_type = self.__get_node_type(node.expr_node)
        cast_reg = self.__get_temp_register()
        llvm_type_return = return_type.to_llvm()

        match return_type:
            case DataType.BOOL:
                self.translated_lines.append(f"  {cast_reg} = zext {llvm_type_return} {value} to i32")
            case DataType.I64:
                self.translated_lines.append(f"  {cast_reg} = trunc {llvm_type_return} {value} to i32")
            case DataType.I16:
                self.translated_lines.append(f"  {cast_reg} = sext {llvm_type_return} {value} to i32")
            case DataType.I32:
                cast_reg = value
        
        value = cast_reg

        self.translated_lines.append(f"  call void @printResult(i32 {value})")
        self.translated_lines.append(f"  ret i32 {value}")

    def visit_binary_operation(self, node: BinaryOpNode) -> str:
        left_value = node.left.accept(self)
        right_value = node.right.accept(self)
        
        left_type = self.__get_node_type(node.left)
        right_type = self.__get_node_type(node.right)
        
        temp_reg = self.__get_temp_register()

        if node.operator.is_for_comparison():
            self.__generate_comparison(node, left_value, right_value, left_type, right_type, temp_reg)
        elif node.operator.is_logical():
            self.__generate_logical(node, left_value, right_value, temp_reg)
        else:
            self.__generate_arithmetic(node, left_value, right_value, left_type, right_type, temp_reg)

        return temp_reg

    def __generate_comparison(self, node: BinaryOpNode, left_value: str, right_value: str, 
                              left_type: DataType, right_type: DataType, temp_reg: str):
        operand_type = self.__infer_operand_type(node.left, node.right)
        
        left_value = self.__promote_type(left_value, left_type, operand_type)
        right_value = self.__promote_type(right_value, right_type, operand_type)
    
        llvm_op = node.operator.to_llvm()
        self.translated_lines.append(
            f"  {temp_reg} = {llvm_op} {operand_type} {left_value}, {right_value}")

    def __generate_logical(self, node: BinaryOpNode, left_value: str, 
                           right_value: str, temp_reg: str) -> None:
        llvm_op = node.operator.to_llvm()
        self.translated_lines.append(
            f"  {temp_reg} = {llvm_op} i1 {left_value}, {right_value}")

    def __generate_arithmetic(self, node: BinaryOpNode, left_value: str, right_value: str, 
                              left_type: DataType, right_type: DataType, temp_reg: str):
        result_type = node.result_type if node.result_type else DataType.I32
        llvm_type = result_type.to_llvm()
        
        left_value = self.__promote_type(left_value, left_type, result_type)
        right_value = self.__promote_type(right_value, right_type, result_type)
        
        llvm_op = node.operator.to_llvm()
        self.translated_lines.append( f"  {temp_reg} = {llvm_op} {llvm_type} {left_value}, {right_value}")

    def __promote_type(self, value: str, from_type: DataType, to_type: DataType):
        if from_type == to_type:
            return value
        
        ext_reg = self.__get_temp_register()
        llvm_type_from = DataType.to_llvm(from_type)
        llvm_type_to = DataType.to_llvm(to_type)

        if (from_type == DataType.I16 and to_type in [DataType.I32, DataType.I64]) or \
              (from_type == DataType.I32 and to_type == DataType.I64):
            self.translated_lines.append(f"  {ext_reg} = sext {llvm_type_from} {value} to {llvm_type_to}")
            return ext_reg
        
        return value
    
    def visit_id(self, node: IDNode) -> str:
        return self.__get_current_register(node.value)

    def visit_number(self, node: NumberNode) -> str:
        return node.value

    def visit_boolean(self, node: BooleanNode) -> str:
        return Boolean.from_string(node.value).to_llvm()

    def __get_variable_register(self, variable: str) -> str:
        if variable not in self.variable_versions:
            self.variable_versions[variable] = 0
            return f"%{variable}"
        else:
            self.variable_versions[variable] += 1
            return f"%{variable}.{self.variable_versions[variable]}"

    def __get_current_register(self, variable: str) -> str:
        if variable not in self.variable_versions or self.variable_versions[variable] == 0:
            return f"%{variable}"
        return f"%{variable}.{self.variable_versions[variable]}"

    def __get_temp_register(self) -> str:
        reg = f"%_temp_{self.temp_counter}"
        self.temp_counter += 1
        return reg
    
    def __infer_operand_type(self, left_node: FactorNode, right_node: FactorNode) -> DataType:
        left_type = self.__get_node_type(left_node)
        right_type = self.__get_node_type(right_node)
        
        if left_type == DataType.I64 or right_type == DataType.I64:
            return DataType.I64
        elif left_type == DataType.I32 or right_type == DataType.I32:
            return DataType.I32
        elif left_type == DataType.I16 or right_type == DataType.I16:
            return DataType.I16
        else:
            return DataType.BOOL

    def __get_node_type(self, node: ExprNode) -> DataType:
        if isinstance(node, IDNode):
            return self.variable_types[node.value]
        if isinstance(node, NumberNode):
            value = int(node.value)
            if -32768 <= value <= 32767:
                return DataType.I16
            elif I32_MIN <= value <= I32_MAX:
                return DataType.I32
            else:
                return DataType.I64
        if isinstance(node, BooleanNode):
            return DataType.BOOL
        if isinstance(node, BinaryOpNode):
            if node.operator.is_for_comparison() or node.operator.is_logical():
                return DataType.BOOL
            return node.result_type if node.result_type else DataType.I32
        if isinstance(node, UnaryOpNode):
            return DataType.BOOL
        return DataType.I32

    def visit_if_statement(self, node: IfNode):
        label_id = self.__get_next_label_id()
        
        then_label = f"then_{label_id}"
        elif_labels = [f"elif_{label_id}_{i}" for i in range(len(node.elif_blocks))]
        else_label = f"else_{label_id}" if node.else_block else f"end_{label_id}"
        end_label = f"end_{label_id}"
        
        condition_value = node.condition.accept(self)
        next_label = elif_labels[0] if elif_labels else else_label
        self.translated_lines.append(
            f"  br i1 {condition_value}, label %{then_label}, label %{next_label}")
        
        self.__emit_block_with_label(node.block, then_label, end_label)
        
        for i, elif_node in enumerate(node.elif_blocks):
            self._emit_label(elif_labels[i])
            condition_value = elif_node.condition.accept(self)
            next_label = elif_labels[i + 1] if i + 1 < len(elif_labels) else else_label
            self.translated_lines.append(
                f"  br i1 {condition_value}, label %{elif_labels[i]}_body, label %{next_label}")
            
            self.__emit_block_with_label(elif_node.block, f"{elif_labels[i]}_body", end_label)
        
        if node.else_block:
            self.__emit_block_with_label(node.else_block, else_label, end_label)
        
        self._emit_label(end_label)

    def visit_elif_statement(self, node: ElifNode):
        pass

    def visit_while_loop(self, node: WhileNode):
        label_id = self.__get_next_label_id()
        cond_label = f"while_cond_{label_id}"
        body_label = f"while_body_{label_id}"
        end_label = f"while_end_{label_id}"
        
        self.translated_lines.append(f"  br label %{cond_label}")
        
        self._emit_label(cond_label)
        condition_value = node.condition.accept(self)
        self.translated_lines.append(f"  br i1 {condition_value}, label %{body_label}, label %{end_label}")
        
        self._emit_label(body_label)
        node.block.accept(self)
        if not node.block.return_node:
            self.translated_lines.append(f"  br label %{cond_label}")
        
        self._emit_label(end_label)

    def __get_next_label_id(self) -> int:
        label_id = self.label_counter
        self.label_counter += 1
        return label_id

    def __emit_block_with_label(self, block: CodeBlockNode, label: str, end_label: str):
        self._emit_label(label)
        block.accept(self)
        if not block.return_node:
            self.translated_lines.append(f"  br label %{end_label}")

    def _emit_label(self, label: str):
        self.translated_lines.append(f"{label}:")

    def visit_code_block(self, node: CodeBlockNode):
        for n in node.statements:
            n.accept(self)
        if node.return_node:
            node.return_node.accept(self)

    def visit_unary_operation(self, node: UnaryOpNode) -> str:
        if node.operator == NOT:
            operand = node.operand.accept(self)
            temp_reg = self.__get_temp_register()
            self.translated_lines.append(f"  {temp_reg} = xor i1 {operand}, 1")
            return temp_reg

        raise ValueError(f"Unsupported unary operator: {node.operator}")