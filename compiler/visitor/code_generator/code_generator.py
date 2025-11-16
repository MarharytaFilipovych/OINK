#!/usr/bin/env python3
from ...llvm_specifics.boolean import Boolean
from ...llvm_specifics.data_type import DataType
from ...visitor.ast_visitor import ASTVisitor
from ...node.code_block_node import CodeBlockNode
from ...node.if_node import IfNode
from ...node.elif_node import ElifNode
from ...node.while_node import WhileNode
from ...constants import NOT
from .variable_registry import VariableRegistry
from .llvm_emitter import LLVMEmitter
from .type_converter import TypeConverter
from .struct_operations import StructOperations
from .function_generator import FunctionGenerator


class CodeGenerator(ASTVisitor):

    def __init__(self):
        self.variable_registry = VariableRegistry()
        self.emitter = LLVMEmitter()
        self.type_converter = None
        self.struct_ops = None
        self.func_gen = None
        self._initialize_helpers()

    def _initialize_helpers(self):
        self.type_converter = TypeConverter(self.variable_registry, None, {})
        self.struct_ops = StructOperations(self.emitter, self.variable_registry, self.type_converter)
        self.func_gen = FunctionGenerator(self.emitter, self.variable_registry,
                                          self.type_converter, self.struct_ops)
        self.type_converter.struct_ops = self.struct_ops
        self.type_converter.function_return_types = self.func_gen.function_return_types

    def visit_program(self, node):
        self._reset_state()
        [decl.accept(self) for decl in node.struct_declarations]
        [decl.accept(self) for decl in node.function_declarations]
        [stmt.accept(self) for stmt in node.statement_nodes]
        node.return_node.accept(self)
        return self.emitter.build_final_output()

    def _reset_state(self):
        self.emitter.translated_lines = []
        self.emitter.struct_type_lines = []
        self.emitter.function_definitions = []

    def visit_struct_declaration(self, node):
        fields = self.struct_ops.build_struct_fields(node)
        self.struct_ops.register_struct(node.variable, fields)
        [self.func_gen.generate_member_function(node.variable, func, self)
         for func in node.member_functions]

    def visit_struct_initialization(self, node):
        struct_reg = self.struct_ops.allocate_struct(node.value)
        self.struct_ops.initialize_struct_fields(node, struct_reg, self)
        return struct_reg

    def visit_member_access(self, node):
        object_reg = self.variable_registry.get_current_register(node.value)
        object_type = self.variable_registry.get_variable_type(node.value)
        return self.struct_ops.load_field_value(object_type, object_reg, node.member_name)

    def visit_function_declaration(self, node):
        self.func_gen.generate_standalone_function(node, self)

    def visit_function_call(self, node):
        return (self.func_gen.generate_member_function_call(node, self) 
                if node.object_name else self.func_gen.generate_regular_function_call(node, self))

    def visit_declaration(self, node):
        self._declare_struct_variable(node) if isinstance(node.data_type, str)\
            else self._declare_primitive_variable(node)


    def _declare_struct_variable(self, node):
        struct_value = node.expr_node.accept(self)
        reg = self.variable_registry.get_variable_register(node.variable)
        self.variable_registry.set_variable_type(node.variable, node.data_type)
        self.emitter.emit_line(f"  {reg} = alloca %struct.{node.data_type}")
        self.struct_ops.copy_struct_fields(node.data_type, struct_value, reg)

    def _declare_primitive_variable(self, node):
        llvm_type = node.data_type.to_llvm()
        value = node.expr_node.accept(self)
        reg = self.variable_registry.get_variable_register(node.variable)
        self.variable_registry.set_variable_type(node.variable, node.data_type)
        value = self._widen_value_if_needed(value, node.expr_node, node.data_type)
        
        self.emitter.emit_line(f"  {reg} = alloca {llvm_type}")
        self.emitter.emit_line(f"  store {llvm_type} {value}, {llvm_type}* {reg}")

    def visit_assign(self, node):
        if self.variable_registry.is_field_access_from_this(node.variable):
            expr_value = node.expr_node.accept(self)
            self.func_gen.store_field_to_this(node.variable, expr_value)
            return

        var_type = self._get_assignable_variable_type(node)
        self._emit_assignment_code(node, var_type)

    def _get_assignable_variable_type(self, node):
        var_type = self.variable_registry.get_variable_type(node.variable)
        if not isinstance(var_type, DataType):
            raise ValueError(f"Cannot reassign entire struct variable '{node.variable}' at line {node.line}! "
                f"Use field assignment instead: {node.variable}_field @ value")
        return var_type

    def _emit_assignment_code(self, node, var_type):
        llvm_type = var_type.to_llvm()
        value = node.expr_node.accept(self)
        reg = self.variable_registry.get_current_register(node.variable) 
        value = self._widen_value_if_needed(value, node.expr_node, var_type)
        self.emitter.emit_line(f"  store {llvm_type} {value}, {llvm_type}* {reg}")

    def visit_return(self, node):
        if node.expr_node is None:
            if self.func_gen.in_function:
                self.emitter.emit_line("  ret void")
            else:
                self.emitter.emit_line("  call void @printResult(i32 0)")
                self.emitter.emit_line("  ret i32 0")
            return
        
        value = node.expr_node.accept(self)
        return_type = self.type_converter.get_node_type(node.expr_node)
        self._generate_function_return(value, return_type) if self.func_gen.in_function \
        else self._generate_main_return(value, return_type)

    def _generate_function_return(self, value: str, return_type):
        llvm_type = self._get_llvm_type_string(return_type)
        self.emitter.emit_line(f"  ret {llvm_type} {value}")

    def _generate_main_return(self, value: str, return_type):
        if not isinstance(return_type, DataType):
            raise NotImplementedError( f"Cannot return struct types from main. "
                f"Attempted to return value of type '{return_type}'" )
        value = self._cast_to_i32(value, return_type)
        self.emitter.emit_line(f"  call void @printResult(i32 {value})")
        self.emitter.emit_line(f"  ret i32 {value}")

    def _cast_to_i32(self, value: str, value_type: DataType) -> str:
        if value_type == DataType.I32:
            return value
        cast_reg = self.emitter.get_temp_register()
        if value_type == DataType.BOOL:
            self.emitter.emit_line(f"  {cast_reg} = zext i1 {value} to i32")
        elif value_type == DataType.I16:
            self.emitter.emit_line(f"  {cast_reg} = sext i16 {value} to i32")
        elif value_type == DataType.I64:
            self.emitter.emit_line(f"  {cast_reg} = trunc i64 {value} to i32")
        else:
            return value
        return cast_reg

    def visit_binary_operation(self, node):
        left_value = node.left.accept(self)
        right_value = node.right.accept(self)
        left_type = self.type_converter.get_node_type(node.left)
        right_type = self.type_converter.get_node_type(node.right)
        temp_reg = self.emitter.get_temp_register()
        if node.operator.is_for_comparison():
            self._generate_comparison(node, left_value, right_value, left_type, right_type, temp_reg)
        elif node.operator.is_logical():
            self._generate_logical_operation(node, left_value, right_value, temp_reg)
        else:
            self._generate_arithmetic(node, left_value, right_value, left_type, right_type, temp_reg)
        return temp_reg

    def _generate_comparison(self, node, left_value, right_value, left_type, right_type, temp_reg):
        operand_type = self.type_converter.infer_operand_type(node.left, node.right)
        left_value = self._widen_to_type(left_value, left_type, operand_type)
        right_value = self._widen_to_type(right_value, right_type, operand_type)
        llvm_op = node.operator.to_llvm()
        self.emitter.emit_line(f"  {temp_reg} = {llvm_op} {operand_type} {left_value}, {right_value}")

    def _generate_logical_operation(self, node, left_value, right_value, temp_reg):
        llvm_op = node.operator.to_llvm()
        self.emitter.emit_line(f"  {temp_reg} = {llvm_op} i1 {left_value}, {right_value}")

    def _generate_arithmetic(self, node, left_value, right_value, left_type, right_type, temp_reg):
        result_type = node.result_type if node.result_type else DataType.I32
        llvm_type = result_type.to_llvm()
        left_value = self._widen_to_type(left_value, left_type, llvm_type)
        right_value = self._widen_to_type(right_value, right_type, llvm_type)
        llvm_op = node.operator.to_llvm()
        self.emitter.emit_line(f"  {temp_reg} = {llvm_op} {llvm_type} {left_value}, {right_value}")

    def _widen_to_type(self, value: str, current_type: DataType, target_llvm_type: str) -> str:
        if not isinstance(current_type, DataType):
            return value

        current_llvm = current_type.to_llvm()
        return value if current_llvm == target_llvm_type \
            else self.struct_ops.widen_value(value, current_llvm, target_llvm_type)

    def _widen_value_if_needed(self, value: str, expr_node, target_type: DataType) -> str:
        expr_type = self.type_converter.get_node_type(expr_node)
        return value if not isinstance(expr_type, DataType) \
                else self.struct_ops._convert_type_if_needed(value, expr_type, target_type.keyword)

    def _get_llvm_type_string(self, return_type) -> str:
        return self.type_converter.get_llvm_type(return_type) if isinstance(return_type, str) \
            else return_type.to_llvm()

    def visit_id(self, node):
        if self.variable_registry.is_field_access_from_this(node.value):
            return self.func_gen.load_field_from_this(node.value)
        else:
            reg = self.variable_registry.get_current_register(node.value)
            var_type = self.variable_registry.get_variable_type(node.value)
            if isinstance(var_type, DataType):
                llvm_type = var_type.to_llvm()
                temp_reg = self.emitter.get_temp_register()
                self.emitter.emit_line(f"  {temp_reg} = load {llvm_type}, {llvm_type}* {reg}")
                return temp_reg
            return reg

    def visit_number(self, node):
        return node.value

    def visit_boolean(self, node):
        return Boolean.from_string(node.value).to_llvm()

    def visit_if_statement(self, node: IfNode):
        label_id = self.emitter.get_next_label_id()
        condition_value = node.condition.accept(self)
        then_label = f"if_then_{label_id}"
        end_label = f"if_end_{label_id}"
        
        elif_start_label = f"if_next_{label_id}"
        next_label = elif_start_label if node.elif_blocks or node.else_block else end_label
        
        self.emitter.emit_line(f"  br i1 {condition_value}, label %{then_label}, label %{next_label}")
        self._emit_then_block(node.block, then_label, label_id)
        
        current_fallthrough_label = next_label 
        if node.elif_blocks:
            current_fallthrough_label = self._emit_elif_blocks(
                node.elif_blocks, 
                elif_start_label, 
                label_id, 
                end_label, 
                node.else_block is not None)
        
        if node.else_block:
            self._emit_else_block(node.else_block, current_fallthrough_label, end_label)
        
        self.emitter.emit_label(end_label)

    def visit_elif_statement(self, node: ElifNode):
        pass

    def _emit_then_block(self, block: CodeBlockNode, label: str, label_id: int) -> str:
        end_label = f"if_end_{label_id}"
        self.emitter.emit_label(label)
        block.accept(self)
        if not block.return_node:
            self.emitter.emit_line(f"  br label %{end_label}")
        return end_label

    def _emit_elif_blocks(self, elif_blocks, start_label: str, label_id: int, end_label: str, has_else: bool) -> str:
        current_label = start_label
        
        for i, elif_block in enumerate(elif_blocks):
            self.emitter.emit_label(current_label)
            condition_value = elif_block.condition.accept(self)
            elif_then_label = f"elif_then_{label_id}_{i}"
            is_last_elif = i == len(elif_blocks) - 1
            next_label = (f"if_else_{label_id}" if has_else else end_label) \
            if is_last_elif else f"elif_next_{label_id}_{i + 1}"
            self.emitter.emit_line(f"  br i1 {condition_value}, label %{elif_then_label}, label %{next_label}")
            self.emitter.emit_label(elif_then_label)
            elif_block.block.accept(self)
            if not elif_block.block.return_node:
                self.emitter.emit_line(f"  br label %{end_label}")
            current_label = next_label
        return current_label

    def _emit_else_block(self, block: CodeBlockNode, label: str, end_label: str) -> str:
        self.emitter.emit_label(label)
        block.accept(self)
        if not block.return_node:
            self.emitter.emit_line(f"  br label %{end_label}")
        return end_label

    def visit_while_loop(self, node: WhileNode):
        label_id = self.emitter.get_next_label_id()
        cond_label = f"while_cond_{label_id}"
        body_label = f"while_body_{label_id}"
        end_label = f"while_end_{label_id}"

        self.emitter.emit_line(f"  br label %{cond_label}")
        self.emitter.emit_label(cond_label)
        
        condition_value = node.condition.accept(self) 
        
        self.emitter.emit_line(f"  br i1 {condition_value}, label %{body_label}, label %{end_label}")
        
        self.emitter.emit_label(body_label)
        node.block.accept(self)
        if not node.block.return_node:
            self.emitter.emit_line(f"  br label %{cond_label}")
        
        self.emitter.emit_label(end_label)

    def visit_code_block(self, node: CodeBlockNode):
        saved_state = self.variable_registry.copy_state()
        [stmt.accept(self) for stmt in node.statements]
        if node.return_node:
            node.return_node.accept(self)
        self.variable_registry.restore_state(saved_state)

    def visit_unary_operation(self, node):
        if node.operator == NOT:
            operand = node.operand.accept(self)
            temp_reg = self.emitter.get_temp_register()
            self.emitter.emit_line(f"  {temp_reg} = xor i1 {operand}, 1")
            return temp_reg
        raise ValueError(f"We do not support this unary operator: {node.operator}!")

    @staticmethod
    def _get_scanf_format_len(data_type: DataType) -> int:
        if data_type == DataType.I16:
            return 4 
        if data_type == DataType.I32:
            return 3 
        if data_type == DataType.I64:
            return 5
        return 0

    def visit_read(self, node):
        var_type = self.variable_registry.get_variable_type(node.variable)
        scanf_format_len = self._get_scanf_format_len(var_type)
        
        temp_ptr = self.emitter.get_temp_register() 
        
        llvm_type_name = var_type.to_llvm().replace('%', '')
        if llvm_type_name == 'i16':
            format_string_name = "@read_i16_format"
        elif llvm_type_name == 'i32':
            format_string_name = "@read_i32_format"
        elif llvm_type_name == 'i64':
            format_string_name = "@read_i64_format"
        else:
            raise ValueError(f"Unsupported read type: {llvm_type_name}")

        self.emitter.emit_line(f"  {temp_ptr} = alloca {var_type.to_llvm()}")
        self.emitter.emit_line(f"  call i32 (i8*, ...) @scanf(i8* getelementptr inbounds "
                              f"([{scanf_format_len} x i8], [{scanf_format_len} x i8]* "
                              f"{format_string_name}, i32 0, i32 0), "
                              f"{var_type.to_llvm()}* {temp_ptr})")
        
        temp_val = self.emitter.get_temp_register()
        self.emitter.emit_line(f"  {temp_val} = load {var_type.to_llvm()}, {var_type.to_llvm()}* {temp_ptr}")
        current_ptr = self.variable_registry.get_current_register(node.variable) 
        self.emitter.emit_line(f"  store {var_type.to_llvm()} {temp_val}, {var_type.to_llvm()}* {current_ptr}")
        
    def visit_print(self, node):
        value = node.expr_node.accept(self)
        expr_type = self.type_converter.get_node_type(node.expr_node)
        if expr_type == DataType.BOOL:
            value = self.struct_ops.widen_value(value, DataType.BOOL.to_llvm(), DataType.I32.to_llvm())
            print_func_name = "@printValue_i32"
            llvm_type = DataType.I32.to_llvm()
        else: 
            llvm_type = expr_type.to_llvm()
            print_func_name = f"@printValue_{llvm_type}"
        self.emitter.emit_line(f"  call void {print_func_name}({llvm_type} {value})")

    @staticmethod
    def _get_scanf_format(data_type: DataType) -> str:
        formats = {
            DataType.I16: "%hd\\00",
            DataType.I32: "%d\\00",
            DataType.I64: "%lld\\00"
        }
        return formats.get(data_type, "%d\\00")

    @staticmethod
    def _get_printf_format(data_type: DataType) -> str:
        formats = {
            DataType.I16: "%d\\n\\00",
            DataType.I32: "%d\\n\\00",
            DataType.I64: "%lld\\n\\00",
            DataType.BOOL: "%d\\n\\00"
        }
        return formats.get(data_type, "%d\\n\\00")

    def _prepare_print_value(self, value: str, expr_type: DataType) -> str:
        if expr_type in (DataType.I32, DataType.I64):
            return value
        
        cast_reg = self.emitter.get_temp_register()
        if expr_type == DataType.BOOL:
            self.emitter.emit_line(f"  {cast_reg} = zext i1 {value} to i32")
        elif expr_type == DataType.I16:
            self.emitter.emit_line(f"  {cast_reg} = sext i16 {value} to i32")
        
        return cast_reg