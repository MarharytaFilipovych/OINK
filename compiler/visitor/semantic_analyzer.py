#!/usr/bin/env python3
from pickle import GLOBAL
from typing import Optional
from ..constants import I32_MAX, I32_MIN, I16_MAX, I16_MIN, NOT
from ..visitor.ast_visitor import ASTVisitor
from ..context.context import Context
from ..llvm_specifics.data_type import DataType
from ..node.assign_node import AssignNode
from ..node.binary_op_node import BinaryOpNode
from ..node.bool_node import BooleanNode
from ..node.code_block_node import CodeBlockNode
from ..node.decl_node import DeclNode
from ..node.function_call_node import FunctionCallNode
from ..node.function_decl_node import FunctionDeclNode
from ..node.id_node import IDNode
from ..node.if_node import IfNode
from ..node.elif_node import ElifNode
from ..node.number_node import NumberNode
from ..node.program_node import ProgramNode
from ..node.return_node import ReturnNode
from ..node.member_access_node import MemberAccessNode
from ..node.unary_op_node import UnaryOpNode
from ..node.struct_decl_node import StructDeclNode
from ..node.struct_init_node import StructInitNode
from ..node.while_node import WhileNode
from ..node.io_nodes import ReadNode, PrintNode


class SemanticAnalyzer(ASTVisitor):
    def __init__(self):
        self.context = Context()
        self._expected_return_type: Optional[DataType] = None
        self._function_name: Optional[str] = None
        self._current_struct_context: Optional[str] = None

    def visit_program(self, node: ProgramNode):
        [struct_decl.accept(self) for struct_decl in node.struct_declarations]
        [self._register_function(func_decl) for func_decl in node.function_declarations]
        [func_decl.accept(self) for func_decl in node.function_declarations]
        [stmt.accept(self) for stmt in node.statement_nodes]
        node.return_node.accept(self)

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
            param_types = [self._type_to_string(p.param_type) for p in member_function.params]
            return_type = self._type_to_string(member_function.return_type)
            self.context.define_function(struct_name, member_function.variable,
                                         param_types, return_type)

    @staticmethod
    def _type_to_string(type_obj) -> str:
        return type_obj.keyword if isinstance(type_obj, DataType) else type_obj

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
            expr_type = node.init_expressions[i].accept(self)
            expected_type = field.field_type
            if not self._types_match(expr_type, expected_type):
                raise ValueError(f"Type mismatch for field \"{field.name}\" in struct \"{node.value}\": "
                    f"expected \"{expected_type}\", but you typed \"{expr_type}\" at line {node.line}!")

    def visit_member_access(self, node: MemberAccessNode):
        self._check_variable_declared(node.value, node.line)
        base_type = self.context.get_variable_type(node.value)
        if not isinstance(base_type, str):
            raise ValueError(f"Cannot access member \"{node.member_name}\" on primitive type "
                f"\"{base_type}\" at line {node.line}!")
        struct_fields = self.context.get_struct_definition(base_type)
        field_info = next((f for f in struct_fields if f.name == node.member_name), None)
        if not field_info:
            raise ValueError(f"Struct \"{base_type}\" has no field \"{node.member_name}\" at line {node.line}!")
        return field_info.field_type

    def visit_declaration(self, node: DeclNode):
        if isinstance(node.data_type, str):
            self._validate_struct_type_exists(node.data_type, node.line)
        if not self.context.declare_variable(node.variable, node.data_type, node.mutable):
            raise ValueError(f"Variable \"{node.variable}\" has already been declared at line {node.line}!!!!!!!!!!")
        self.context.currently_initializing = node.variable
        expr_type = node.expr_node.accept(self)
        self._check_type_match(expr_type, node.data_type, node.line)
        self.context.currently_initializing = None

    def _validate_struct_type_exists(self, type_name: str, line: int):
        if not self.context.is_struct_defined(type_name):
            raise ValueError(f"Type \"{type_name}\" is not defined at line {line}! "
                f"Did you forget to declare the struct?")

    def _check_variable_declared(self, var_name: str, line: int):
        if not self.context.is_variable_declared(var_name):
            raise ValueError(f"Variable \"{var_name}\" not declared at line {line}!")

    def _check_variable_mutable(self, var_name: str, line: int):
        if not self.context.is_variable_mutable(var_name):
            raise ValueError(f"Sorry, but you cannot assign something new to an immutable variable!!! "
                f"Remove \"{var_name}\" from line {line}!")

    def _check_type_match(self, expr_type, expected_type, line: int):
        if not self._types_match(expr_type, expected_type):
            raise ValueError(f"Types do not match at line {line}: "
                f"you cannot assign \"{expr_type}\" to \"{expected_type}\"! Be careful!")

    def visit_assign(self, node: AssignNode):
        self._check_variable_declared(node.variable, node.line)
        self._check_variable_mutable(node.variable, node.line)

        if isinstance(node.expr_node, IDNode) and node.expr_node.value == node.variable:
            raise ValueError(f"Self-assignment like \"{node.variable} = {node.variable}\" "
                f"is not allowed at line {node.line}!")
        data_type = self.context.get_variable_type(node.variable)
        expr_type = node.expr_node.accept(self)
        self._check_type_match(expr_type, data_type, node.line)


    def visit_return(self, node: ReturnNode):
        returned_type = node.expr_node.accept(self) if node.expr_node else DataType.VOID 
            
        if self._expected_return_type is not None:
            expected_str = self._type_to_string(self._expected_return_type)
            returned_str = self._type_to_string(returned_type)
            if not self._types_match(returned_type, self._expected_return_type):
                raise ValueError(f"Function \"{self._function_name}\" returns \"{returned_str}\" "
                    f"but declared as \"{expected_str}\"!")
        return returned_type

    def visit_binary_operation(self, node: BinaryOpNode):
        left_type = node.left.accept(self)
        right_type = node.right.accept(self)
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

    def visit_id(self, node: IDNode):
        if self.context.currently_initializing == node.value:
            raise ValueError(f"Self-assignment like \"{node.value} = {node.value}\" "
                f"is not allowed at line {node.line}!")
        self._check_variable_declared(node.value, node.line)
        return self.context.get_variable_type(node.value)

    def visit_number(self, node: NumberNode) -> DataType:
        value = int(node.value)
        if I16_MIN <= value <= I16_MAX:
            return DataType.I16
        if I32_MIN <= value <= I32_MAX:
            return DataType.I32
        return DataType.I64

    def visit_boolean(self, node: BooleanNode) -> DataType:
        return DataType.BOOL

    def visit_if_statement(self, node: IfNode):
        condition_type = node.condition.accept(self)
        if condition_type != DataType.BOOL:
            raise ValueError(f"If condition must be of type bool, but you placed \"{condition_type}\" "
                f"at line {node.line}! How could you????????")
        node.block.accept(self)
        [elif_block.accept(self) for elif_block in node.elif_blocks]
        if node.else_block:
            node.else_block.accept(self)

    def visit_elif_statement(self, node: ElifNode):
        condition_type = node.condition.accept(self)
        if condition_type != DataType.BOOL:
            raise ValueError(f"Elif condition must be of type bool, but you placed \"{condition_type}\" "
                f"at line {node.line}!")
        node.block.accept(self)

    def visit_while_loop(self, node: WhileNode):
        condition_type = node.condition.accept(self)
        if condition_type != DataType.BOOL:
            raise ValueError(f"While condition must be of type bool, but you placed \"{condition_type}\" "
                f"at line {node.line}!")
        node.block.accept(self)

    def visit_code_block(self, node: CodeBlockNode):
        self.context.enter_scope()
        [stmt.accept(self) for stmt in node.statements]
        if node.return_node:
            node.return_node.accept(self)
        self.context.exit_scope()

    def visit_unary_operation(self, node: UnaryOpNode) -> DataType:
        operand_type = node.operand.accept(self)
        if node.operator == NOT:
            if operand_type != DataType.BOOL:
                raise ValueError(f"The NOT operator (💩) can only be applied to boolean values, dummy, "
                    f"but you applied it to \"{operand_type}\"! Do you think it is okay?")
            return DataType.BOOL
        raise ValueError(f"Unknown unary operator: \"{node.operator}\"")

    def _register_function(self, node: FunctionDeclNode):
        param_types = [self._type_to_string(p.param_type) for p in node.params]
        return_type = self._type_to_string(node.return_type)
        self.context.define_function(GLOBAL, node.variable, param_types, return_type)

    def visit_function_declaration(self, node: FunctionDeclNode):
        self.context.enter_scope()
        self._declare_function_parameters(node)

        if node.return_type != DataType.VOID and not node.body.return_node:
            raise ValueError(f"Function \"{node.variable}\" must have a return statement!")

        self._expected_return_type = node.return_type
        self._function_name = node.variable

        node.body.accept(self)

        self._expected_return_type = None
        self._function_name = None
        self.context.exit_scope()

    def _declare_function_parameters(self, node: FunctionDeclNode):
        for param in node.params:
            if not self.context.declare_variable(param.name, param.param_type, mutable=False):
                raise ValueError(f"Duplicate parameter \"{param.name}\" in function \"{node.variable}\"!")

    def visit_function_call(self, node: FunctionCallNode):
        function_scope = self._identify_function_scope(node.object_name)
        if not self.context.is_function_defined(function_scope, node.value):
            raise ValueError(f"Function \"{node.value}\" not defined at line {node.line}!")
        func_info = self.context.get_function_info(function_scope, node.value)
        self._validate_argument_count(node, func_info)
        self._validate_argument_types(node, func_info)
        return self._string_to_type(func_info.return_type)

    @staticmethod
    def _string_to_type(type_str: str):
        try:
            return DataType.from_string(type_str)
        except ValueError:
            return type_str

    @staticmethod
    def _validate_argument_count(node: FunctionCallNode, func_info):
        if len(node.arguments) != len(func_info.param_types):
            raise ValueError(f"Function \"{node.value}\" expects {len(func_info.param_types)} arguments "
                f"but got {len(node.arguments)} at line {node.line}!")

    def _validate_argument_types(self, node: FunctionCallNode, func_info):
        for i, (arg, expected_type_str) in enumerate(zip(node.arguments, func_info.param_types)):
            arg_type = arg.accept(self)
            expected_type = self._string_to_type(expected_type_str)
            if not self._types_match(arg_type, expected_type):
                raise ValueError(f"Argument {i + 1} to function \"{node.value}\" has type "
                    f"\"{self._type_to_string(arg_type)}\" but expected \"{expected_type_str}\" "
                    f"at line {node.line}!")

    def _types_match(self, expr_type, expected_type) -> bool:
        if isinstance(expected_type, DataType) and isinstance(expr_type, DataType):
            return self._is_type_compatible(expr_type, expected_type)
        if isinstance(expected_type, str) and isinstance(expr_type, str):
            return expr_type == expected_type
        return False

    @staticmethod
    def _is_type_compatible(source_type: DataType, target_type: DataType) -> bool:
        if source_type == target_type:
            return True
        if source_type == DataType.I16 and target_type in (DataType.I32, DataType.I64):
            return True
        if source_type == DataType.I32 and target_type == DataType.I64:
            return True
        return False

    def _identify_function_scope(self, object_name: Optional[str]) -> str:
        if not object_name:
            return self._current_struct_context if self._current_struct_context else GLOBAL

        var_type = self.context.get_variable_type(object_name)
        return var_type if isinstance(var_type, str) else GLOBAL

    def _analyze_member_function(self, struct_name: str, node: FunctionDeclNode):
        self.context.enter_scope()
        self._current_struct_context = struct_name

        struct_fields = self.context.get_struct_definition(struct_name)
        for field in struct_fields:
            self.context.declare_variable(field.name, field.field_type, field.mutable)

        self._declare_function_parameters(node)

        if node.return_type != DataType.VOID and not node.body.return_node:
            raise ValueError(f"Member function \"{node.variable}\" in struct \"{struct_name}\" "
                f"must have a return statement!")

        self._expected_return_type = node.return_type
        self._function_name = f"{struct_name}::{node.variable}"

        node.body.accept(self)

        self._expected_return_type = None
        self._function_name = None
        self._current_struct_context = None
        self.context.exit_scope()

    def visit_read(self, node: ReadNode):
        self._check_variable_declared(node.variable, node.line)
        self._check_variable_mutable(node.variable, node.line)

        var_type = self.context.get_variable_type(node.variable)
        if not isinstance(var_type, DataType) or var_type == DataType.BOOL:
            raise ValueError(f"Cannot read into variable \"{node.variable}\" at line {node.line}! "
                f"Read only supports numeric types (i16, i32, i64).")

    def visit_print(self, node: PrintNode):
        expr_type = node.expr_node.accept(self)
        if not isinstance(expr_type, DataType):
            raise ValueError(f"Cannot print struct type at line {node.line}! "
                f"Only primitive types can be printed.")
