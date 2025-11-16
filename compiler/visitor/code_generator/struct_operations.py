#!/usr/bin/env python3
from ...llvm_specifics.data_type import DataType


class StructOperations:
    def __init__(self, emitter, variable_registry, type_converter):
        self.emitter = emitter
        self.variable_registry = variable_registry
        self.type_converter = type_converter
        self.struct_definitions: dict[str, list[tuple[str, str, str]]] = {}

    def build_struct_fields(self, node) -> list[tuple[str, str, str]]:
        fields = []
        for field in node.fields:
            llvm_type = self.type_converter.get_llvm_type(field.field_type)
            data_type_str = (field.field_type.keyword 
                           if isinstance(field.field_type, DataType) 
                           else field.field_type)
            fields.append((field.name, llvm_type, data_type_str))
        return fields

    def register_struct(self, struct_name: str, fields: list[tuple[str, str, str]]):
        self.struct_definitions[struct_name] = fields
        field_types = [f[1] for f in fields]
        struct_def = f"%struct.{struct_name} = type {{ {', '.join(field_types)} }}"
        self.emitter.add_struct_type_definition(struct_def)

    def allocate_struct(self, struct_name: str) -> str:
        struct_reg = self.emitter.get_temp_register()
        self.emitter.emit_line(f"  {struct_reg} = alloca %struct.{struct_name}")
        return struct_reg

    def initialize_struct_fields(self, node, struct_reg: str, visitor):
        fields = self.struct_definitions[node.value]

        for i, (field_name, field_llvm_type, field_data_type) in enumerate(fields):
            expr_value = node.init_expressions[i].accept(visitor)
            expr_type = self.type_converter.get_node_type(node.init_expressions[i])

            field_ptr = self.get_struct_field_ptr(node.value, struct_reg, i)

            if isinstance(expr_type, str):
                self.copy_struct_fields(field_data_type, expr_value, field_ptr)
            else:
                expr_value = self._convert_type_if_needed(expr_value, expr_type, field_data_type)
                self.emitter.emit_line(f"  store {field_llvm_type} {expr_value}, {field_llvm_type}* {field_ptr}")

    def get_struct_field_ptr(self, struct_name: str, struct_ptr: str, field_index: int) -> str:
        field_ptr = self.emitter.get_temp_register()
        self.emitter.emit_line(
            f"  {field_ptr} = getelementptr inbounds %struct.{struct_name}, "
            f"%struct.{struct_name}* {struct_ptr}, i32 0, i32 {field_index}")
        return field_ptr

    def _convert_type_if_needed(self, value: str, expr_type, target_type_str: str) -> str:
        if not isinstance(expr_type, DataType):
            return value
        try:
            target_type = DataType.from_string(target_type_str)
            if expr_type != target_type:
                return self.widen_value(value, expr_type.to_llvm(), target_type.to_llvm())
        except ValueError:
            pass
        return value

    def widen_value(self, value: str, from_type: str, to_type: str) -> str:
        if from_type == to_type:
            return value

        conversions = {
            ("i16", "i32"): "sext",
            ("i16", "i64"): "sext",
            ("i32", "i64"): "sext",
            ("i64", "i32"): "trunc",
            ("i64", "i16"): "trunc",
            ("i32", "i16"): "trunc",
            ("i1", "i16"): "zext",
            ("i1", "i32"): "zext",
            ("i1", "i64"): "zext",
        }
        
        conv_key = (from_type, to_type)
        if conv_key not in conversions:
            return value
        
        temp_reg = self.emitter.get_temp_register()
        op = conversions[conv_key]
        self.emitter.emit_line(f"  {temp_reg} = {op} {from_type} {value} to {to_type}")
        return temp_reg

    def access_field(self, field_name: str, current_type, current_reg: str, 
                    is_final: bool) -> tuple[str, object]:
        if not isinstance(current_type, str):
            return current_reg, current_type

        field_ptr, field_llvm_type, field_data_type = self._get_field_info(
            current_type, field_name, current_reg)

        if is_final:
            value_reg = self.emitter.get_temp_register()
            self.emitter.emit_line(f"  {value_reg} = load {field_llvm_type}, {field_llvm_type}* {field_ptr}")
            current_reg = value_reg
        else:
            current_reg = field_ptr

        try:
            new_type = DataType.from_string(field_data_type)
        except ValueError:
            new_type = field_data_type
        
        return current_reg, new_type

    def _get_field_info(self, struct_name: str, field_name: str, 
                       base_reg: str) -> tuple[str, str, str]:
        fields = self.struct_definitions[struct_name]
        field_index, field_llvm_type, field_data_type = self._find_field(fields, field_name)
        field_ptr = self.get_struct_field_ptr(struct_name, base_reg, field_index)
        return field_ptr, field_llvm_type, field_data_type

    @staticmethod
    def _find_field(fields: list, field_name: str) -> tuple[int, str, str]:
        for i, (name, field_type, fdata) in enumerate(fields):
            if name == field_name:
                return i, field_type, fdata
        raise ValueError(f"Field \"{field_name}\" not found!")

    def copy_struct_fields(self, struct_name: str, src_ptr: str, dst_ptr: str):
        fields = self.struct_definitions[struct_name]
        for i, (field_name, field_llvm_type, _) in enumerate(fields):
            src_field_ptr = self.get_struct_field_ptr(struct_name, src_ptr, i)
            src_val = self._load_value(field_llvm_type, src_field_ptr)

            dst_field_ptr = self.get_struct_field_ptr(struct_name, dst_ptr, i)
            self.emitter.emit_line(f"  store {field_llvm_type} {src_val}, {field_llvm_type}* {dst_field_ptr}")

    def _load_value(self, llvm_type: str, ptr: str) -> str:
        val_reg = self.emitter.get_temp_register()
        self.emitter.emit_line(f"  {val_reg} = load {llvm_type}, {llvm_type}* {ptr}")
        return val_reg

    def get_object_pointer(self, object_name: str) -> str:
        return self.variable_registry.get_current_register(object_name)
