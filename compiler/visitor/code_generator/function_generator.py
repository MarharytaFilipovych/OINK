#!/usr/bin/env python3
from typing import Optional, Union

from ...constants import VARIABLE_ALLOWED_SIGN, UNDERLINE
from ...llvm_specifics.data_type import DataType
from ...context.function_info import FunctionInfo


class FunctionGenerator:
    def __init__(self, emitter, variable_registry, type_converter, struct_ops):
        self.emitter = emitter
        self.variable_registry = variable_registry
        self.type_converter = type_converter
        self.struct_ops = struct_ops
        self.function_return_types = {}
        self.function_signatures: dict[str, FunctionInfo] = {}
        self.current_struct_context: Optional[str] = None
        self.in_function = False

    @staticmethod
    def _type_to_string(type_obj: Union[DataType, str]) -> str:
        return type_obj.keyword if isinstance(type_obj, DataType) else type_obj

    @staticmethod
    def _string_to_type(type_str: str) -> Union[DataType, str]:
        try:
            return DataType.from_string(type_str)
        except ValueError:
            return type_str

    def generate_standalone_function(self, node, visitor):
        self._prepare_function_context(node.variable, node.return_type, node.params)
        func_signature = self._build_function_signature(node)
        self._initialize_function_body(node, visitor, func_signature)
        self._finalize_function()

    def generate_member_function(self, struct_name: str, node, visitor):
        mangled_name = f"{struct_name}_{node.variable}"
        self._prepare_function_context(mangled_name, node.return_type, node.params, is_member=True, struct_name=struct_name)

        func_signature = self._build_member_function_signature(struct_name, node, mangled_name)
        self._setup_this_context(struct_name)
        self._initialize_function_body(node, visitor, func_signature)

        self.current_struct_context = None
        self._finalize_function()

    def generate_regular_function_call(self, node, visitor) -> str:
        if hasattr(self.variable_registry, 'lambda_functions') and \
           node.value in self.variable_registry.lambda_functions:
            lambda_func_name = self.variable_registry.lambda_functions[node.value].strip('@')
            
            return_type = self.type_converter.get_node_type(node)
            return_llvm_type = self._get_llvm_type(return_type)
            
            signatures = self.variable_registry.lambda_signatures.get(node.value, [])
            
            args = []
            for i, arg in enumerate(node.arguments):
                arg_value = arg.accept(visitor)
                
                expected_type = signatures[i] if i < len(signatures) else DataType.I32
                expected_llvm_type = self._get_llvm_type(expected_type)
                
                arg_type = self.type_converter.get_node_type(arg)
                arg_llvm_type = self._get_llvm_type(arg_type)
                
                if arg_llvm_type != expected_llvm_type:
                    arg_value = self.struct_ops.widen_value(arg_value, arg_llvm_type, expected_llvm_type)
                
                args.append(f"{expected_llvm_type} {arg_value}")
            
            if return_type == DataType.VOID:
                self.emitter.emit_line(f"  call {return_llvm_type} @{lambda_func_name}({', '.join(args)})")
                return ""
            else:
                result_reg = self.emitter.get_temp_register()
                self.emitter.emit_line(f"  {result_reg} = call {return_llvm_type} @{lambda_func_name}({', '.join(args)})")
                return result_reg
        
        if self.current_struct_context and self._is_member_function(node.value):
            return self._generate_member_to_member_call(node, visitor)
        
        return_type = self.type_converter.get_node_type(node)
        return_llvm_type = self._get_llvm_type(return_type)
        func_name = node.value.replace(VARIABLE_ALLOWED_SIGN, UNDERLINE)

        func_info = self.function_signatures.get(func_name)
        
        if not func_info:
            expected_types = [DataType.I32] * len(node.arguments)
        else:
            expected_types = [self._string_to_type(t) for t in func_info.param_types]
        
        args = [self._build_call_argument(arg, visitor, expected_type)
                for arg, expected_type in zip(node.arguments, expected_types)]

        if return_type == DataType.VOID:
            self.emitter.emit_line(f"  call {return_llvm_type} @{func_name}({', '.join(args)})")
            return ""
        else:
            result_reg = self.emitter.get_temp_register()
            self.emitter.emit_line(f"  {result_reg} = call {return_llvm_type} @{func_name}({', '.join(args)})")
            return result_reg

    def generate_member_function_call(self, node, visitor) -> str:
        obj_type = self.variable_registry.get_variable_type(node.object_name)
        if not isinstance(obj_type, str):
            raise ValueError(f"Cannot call member function on primitive type")
        
        object_ptr = self.struct_ops.get_object_pointer(node.object_name)
        mangled_name = f"{obj_type}_{node.value}"

        return_type = self.type_converter.get_node_type(node)
        return_llvm_type = self._get_llvm_type(return_type)

        func_info = self.function_signatures.get(mangled_name)
        if not func_info:
            expected_types = [DataType.I32] * len(node.arguments)
        else:
            expected_types = [self._string_to_type(t) for t in func_info.param_types[1:]]
        
        arg_strs = [f"%struct.{obj_type}* {object_ptr}"] + [
            self._build_call_argument(arg, visitor, expected_type) 
            for arg, expected_type in zip(node.arguments, expected_types)]
        
        if return_type == DataType.VOID:
            self.emitter.emit_line(f"  call {return_llvm_type} @{mangled_name}({', '.join(arg_strs)})")
            return ""
        else:
            result_reg = self.emitter.get_temp_register()
            self.emitter.emit_line(f"  {result_reg} = call {return_llvm_type} @{mangled_name}({', '.join(arg_strs)})")
            return result_reg

    def load_field_from_this(self, field_name: str) -> str:
        field_ptr, field_llvm_type = self._get_this_field_pointer(field_name)
        field_value = self.emitter.get_temp_register()
        self.emitter.emit_line(f"  {field_value} = load {field_llvm_type}, {field_llvm_type}* {field_ptr}")
        return field_value

    def store_field_to_this(self, field_name: str, value: str):
        field_ptr, field_llvm_type = self._get_this_field_pointer(field_name)
        self.emitter.emit_line(f"  store {field_llvm_type} {value}, {field_llvm_type}* {field_ptr}")

    def _is_member_function(self, func_name: str) -> bool:
        if not self.current_struct_context:
            return False
        
        struct_name = self.current_struct_context
        if struct_name not in self.struct_ops.struct_definitions:
            return False
        
        mangled_name = f"{struct_name}_{func_name}"
        return mangled_name in self.function_return_types

    def _generate_member_to_member_call(self, node, visitor) -> str:
        struct_name = self.current_struct_context
        mangled_name = f"{struct_name}_{node.value}"
        
        return_type = self.type_converter.get_node_type(node)
        return_llvm_type = self._get_llvm_type(return_type)
        
        func_info = self.function_signatures.get(mangled_name)
        if not func_info:
            expected_types = [DataType.I32] * len(node.arguments)
        else:
            expected_types = [self._string_to_type(t) for t in func_info.param_types[1:]]
            
        arg_strs = [f"%struct.{struct_name}* %this"] + [
            self._build_call_argument(arg, visitor, expected_type) 
            for arg, expected_type in zip(node.arguments, expected_types)]
        
        if return_type == DataType.VOID:
            self.emitter.emit_line(f"  call {return_llvm_type} @{mangled_name}({', '.join(arg_strs)})")
            return ""
        else:
            result_reg = self.emitter.get_temp_register()
            self.emitter.emit_line(f"  {result_reg} = call {return_llvm_type} @{mangled_name}({', '.join(arg_strs)})")
            return result_reg

    @staticmethod
    def _get_llvm_type(data_type) -> str:
        if isinstance(data_type, DataType):
            return data_type.to_llvm()
        try:
            if isinstance(data_type, str) and data_type in ["i16", "i32", "i64", "i1", "void"]:
                return data_type
            return DataType.from_string(data_type).to_llvm()
        except (ValueError, AttributeError):
            return f"%struct.{data_type}*" if isinstance(data_type, str) else "i32"
        
    def _get_this_field_pointer(self, field_name: str) -> tuple[str, str]:
        struct_name = self.current_struct_context
        fields = self.struct_ops.struct_definitions[struct_name]
        field_index = next(i for i, (name, _, _) in enumerate(fields) if name == field_name)
        field_llvm_type = fields[field_index][1]

        field_ptr = self.emitter.get_temp_register()
        self.emitter.emit_line(f"  {field_ptr} = getelementptr inbounds %struct.{struct_name}, "
            f"%struct.{struct_name}* %this, i32 0, i32 {field_index}")
        return field_ptr, field_llvm_type

    def _prepare_function_context(self, func_name: str, return_type, params, is_member: bool = False, struct_name: Optional[str] = None):
        sanitized_name = func_name.replace('&', '_')
        type_str = self._type_to_string(return_type)
        self.function_return_types[sanitized_name] = type_str
        
        param_types = [self._type_to_string(p.param_type) for p in params]
        
        if is_member and struct_name:
            param_types.insert(0, struct_name)
            
        self.function_signatures[sanitized_name] = FunctionInfo(param_types, type_str)

        self._saved_state = self._save_state()
        self._reset_for_function()
        self.in_function = True

    def _initialize_function_body(self, node, visitor, func_signature: str):
        self._declare_function_params(node)
        node.body.accept(visitor)
        self._store_function_definition(func_signature)

    def _finalize_function(self):
        self._restore_state(self._saved_state)
        self.in_function = False

    def _build_function_signature(self, node) -> str:
        param_strs = [self._build_param_string(p) for p in node.params]
        return_llvm_type = self._get_llvm_type(node.return_type)
        func_name = node.variable.replace('&', '_')
        return f"define {return_llvm_type} @{func_name}({', '.join(param_strs)}) {{"

    def _build_member_function_signature(self, struct_name: str, node, mangled_name: str) -> str:
        return_llvm_type = self._get_llvm_type(node.return_type)
        param_strs = [f"%struct.{struct_name}* %this"] + [
            self._build_param_string(p) for p in node.params]
        return f"define {return_llvm_type} @{mangled_name}({', '.join(param_strs)}) {{"

    def _build_param_string(self, param) -> str:
        llvm_type = self._get_llvm_type(param.param_type)
        return f"{llvm_type} %{param.name}"

    def _declare_function_params(self, node):
        for param in node.params:
            param_type = param.param_type
            self.variable_registry.set_variable_type(param.name, param_type)
            self.variable_registry.max_versions[param.name] = 0
            self.variable_registry.variable_versions[param.name] = 0
            param_reg = self.variable_registry.get_variable_register(param.name)
            param_llvm_type = self._get_llvm_type(param_type)
            self.emitter.emit_line(f"  {param_reg} = alloca {param_llvm_type}")
            self.emitter.emit_line(f"  store {param_llvm_type} %{param.name}, {param_llvm_type}* {param_reg}")

    def _store_function_definition(self, signature: str):
        lines = [signature] + self.emitter.translated_lines + ["}", ""]
        self.emitter.add_function_definition(lines)

    def _setup_this_context(self, struct_name: str):
        self.current_struct_context = struct_name
        for field_name, field_llvm_type, field_data_type in self.struct_ops.struct_definitions[struct_name]:
            try:
                field_type = DataType.from_string(field_data_type)
            except ValueError:
                field_type = field_data_type
            
            self.variable_registry.set_variable_type(field_name, field_type)
            self.variable_registry.set_variable_version(field_name, -1)

    def _build_call_argument(self, arg, visitor, expected_type: Union[DataType, str]) -> str:
        arg_value = arg.accept(visitor)
        arg_type = self.type_converter.get_node_type(arg)
        
        expected_llvm_type = self._get_llvm_type(expected_type)
        
        if isinstance(arg_type, DataType) and isinstance(expected_type, DataType):
            arg_llvm_type = arg_type.to_llvm()
            if arg_type != expected_type:
                arg_value = self.struct_ops.widen_value(arg_value, arg_llvm_type, expected_llvm_type)
            arg_llvm_type = expected_llvm_type
        elif isinstance(arg_type, str) and isinstance(expected_type, str) and arg_type == expected_type:
            arg_llvm_type = expected_llvm_type
        else:
            arg_llvm_type = expected_llvm_type
            
        return f"{arg_llvm_type} {arg_value}"

    def _save_state(self) -> dict:
        return {
            "emitter": self.emitter.copy_state(),
            "variable_registry": self.variable_registry.copy_state(),
            "in_function": self.in_function
        }

    def _restore_state(self, state: dict):
        self.emitter.restore_state(state["emitter"])
        self.variable_registry.restore_state(state["variable_registry"])
        self.in_function = state["in_function"]

    def _reset_for_function(self):
        self.emitter.reset_for_function()
        self.variable_registry.reset()