#!/usr/bin/env python3
from typing import Optional
from ...node.intr_string_node import InterpolatedStringNode
from ...constants import LAMBDA, get_token_display_name
from ...node.print_node import PrintNode
from ...visitor.ast_visitor import ASTVisitor
from ...context.context import Context
from ...llvm_specifics.data_type import DataType
from ...node.assign_node import AssignNode
from ...node.binary_op_node import BinaryOpNode
from ...node.bool_node import BooleanNode
from ...node.code_block_node import CodeBlockNode
from ...node.decl_node import DeclNode
from ...node.function_call_node import FunctionCallNode
from ...node.function_decl_node import FunctionDeclNode
from ...node.id_node import IDNode
from ...node.if_node import IfNode
from ...node.elif_node import ElifNode
from ...node.number_node import NumberNode
from ...node.program_node import ProgramNode
from ...node.return_node import ReturnNode
from ...node.member_access_node import MemberAccessNode
from ...node.unary_op_node import UnaryOpNode
from ...node.struct_decl_node import StructDeclNode
from ...node.struct_init_node import StructInitNode
from ...node.while_node import WhileNode
from ...node.read_node import ReadNode
from .struct_analyzer import StructAnalyzer
from .function_analyzer import FunctionAnalyzer
from .variable_analyzer import VariableAnalyzer
from .expression_analyzer import ExpressionAnalyzer


class SemanticAnalyzer(ASTVisitor):
    def __init__(self):
        self.context = Context()
        self._expected_return_type: Optional[DataType] = None
        self._function_name: Optional[str] = None
        self.current_struct_context: Optional[str] = None
        self.inside_lambda = False
        
        self.struct_analyzer = StructAnalyzer(self.context, self)
        self.function_analyzer = FunctionAnalyzer(self.context, self)
        self.variable_analyzer = VariableAnalyzer(self.context, self)
        self.expression_analyzer = ExpressionAnalyzer(self.context, self)

    def visit_program(self, node: ProgramNode):
        [self._register_function(func_decl) for func_decl in node.function_declarations] 
        [struct_decl.accept(self) for struct_decl in node.struct_declarations] 
        [func_decl.accept(self) for func_decl in node.function_declarations]
        [stmt.accept(self) for stmt in node.statement_nodes]
        node.return_node.accept(self)

    def visit_struct_declaration(self, node: StructDeclNode):
        self.struct_analyzer.visit_struct_declaration(node)

    def visit_struct_initialization(self, node: StructInitNode):
        return self.struct_analyzer.visit_struct_initialization(node)

    def visit_member_access(self, node: MemberAccessNode):
        return self.struct_analyzer.visit_member_access(node)

    def visit_declaration(self, node: DeclNode):
        self.variable_analyzer.visit_declaration(node)

    def visit_assign(self, node: AssignNode):
        self.variable_analyzer.visit_assign(node)

    def visit_id(self, node: IDNode):
        return self.variable_analyzer.visit_id(node)

    def visit_return(self, node: ReturnNode):
        returned_type = node.expr_node.accept(self) if node.expr_node else DataType.VOID 
            
        if self._expected_return_type is not None:
            expected_str = self._format_type(self._expected_return_type)
            returned_str = self._format_type(returned_type)
            if not self.types_match(returned_type, self._expected_return_type):
                raise ValueError(f"Function 🐖{self._function_name}🐖 returns {returned_str} "
                    f"but declared as {expected_str}!")
        return returned_type

    def visit_binary_operation(self, node: BinaryOpNode):
        return self.expression_analyzer.visit_binary_operation(node)

    def visit_number(self, node: NumberNode) -> DataType:
        return self.expression_analyzer.visit_number(node)

    def visit_boolean(self, node: BooleanNode) -> DataType:
        return self.expression_analyzer.visit_boolean(node)

    def visit_unary_operation(self, node: UnaryOpNode) -> DataType:
        return self.expression_analyzer.visit_unary_operation(node)

    def visit_if_statement(self, node: IfNode):
        condition_type = node.condition.accept(self)
        if condition_type != DataType.BOOL:
            raise ValueError(f"SAVE (if statement) condition must be of type wow (bool), but you placed "
                f"{self._format_type(condition_type)} at line {node.line}! How could you????????")
        node.block.accept(self)
        [elif_block.accept(self) for elif_block in node.elif_blocks]
        if node.else_block:
            node.else_block.accept(self)

    def visit_elif_statement(self, node: ElifNode):
        condition_type = node.condition.accept(self)
        if condition_type != DataType.BOOL:
            raise ValueError(f"HURT (else-if statement) condition must be of type wow (bool), but you placed "
                f"{self._format_type(condition_type)} at line {node.line}!")
        node.block.accept(self)

    def visit_while_loop(self, node: WhileNode):
        condition_type = node.condition.accept(self)
        if condition_type != DataType.BOOL:
            raise ValueError(f"OINK (while loop) condition must be of type wow (bool), but you placed "
                f"{self._format_type(condition_type)} at line {node.line}!")
        node.block.accept(self)

    def visit_code_block(self, node: CodeBlockNode):
        self.context.enter_scope()
        [stmt.accept(self) for stmt in node.statements]
        if node.return_node:
            node.return_node.accept(self)
        self.context.exit_scope()

    def _register_function(self, node: FunctionDeclNode):
        self.function_analyzer.register_function(node)

    def visit_function_declaration(self, node: FunctionDeclNode):
        self.function_analyzer.visit_function_declaration(node)

    def visit_function_call(self, node: FunctionCallNode):
        return self.function_analyzer.visit_function_call(node)

    def visit_read(self, node):
        from ...llvm_specifics.data_type import DataType
        self.check_variable_declared(node.variable, node.line)
        self.check_variable_mutable(node.variable, node.line)
        var_type = self.context.get_variable_type(node.variable)
        if (not isinstance(var_type, DataType) and var_type != LAMBDA) or var_type == DataType.BOOL or var_type == DataType.VOID:
            raise ValueError(f"Cannot read into variable \"{node.variable}\" at line {node.line}! "
                f"Read only supports numeric types (i16, i32, i64) and string (i8*).")

    def visit_print(self, node: PrintNode):
        expr_type = node.expr_node.accept(self)
        if not isinstance(expr_type, DataType):
            raise ValueError(f"Cannot print struct type at line {node.line}! "
                f"Only primitive types can be printed with print🤮 (output).")

    def check_variable_declared(self, var_name: str, line: int):
        if not self.context.is_variable_declared(var_name):
            raise ValueError(f"Variable 🐖{var_name}🐖 not declared at line {line}!")

    def check_variable_mutable(self, var_name: str, line: int):
        if not self.context.is_variable_mutable(var_name):
            raise ValueError(f"Sorry, but you cannot assign something new to an immutable variable (😭 const)!!! "
                f"Remove 🐖{var_name}🐖 from line {line}!")

    def check_type_match(self, expr_type, expected_type, line: int):
        if not self.types_match(expr_type, expected_type):
            raise ValueError(f"Types do not match at line {line}: "
                f"you cannot assign {self._format_type(expr_type)} to {self._format_type(expected_type)}! Be careful!")

    def types_match(self, expr_type, expected_type) -> bool:
        if isinstance(expected_type, DataType) and isinstance(expr_type, DataType):
            return self._is_type_compatible(expr_type, expected_type)
        if isinstance(expected_type, str) and isinstance(expr_type, str): # For struct type matching
            return expected_type == expr_type
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

    @staticmethod
    def type_to_string(type_obj) -> str:
        return type_obj.keyword if isinstance(type_obj, DataType) else type_obj

    @staticmethod
    def string_to_type(type_str: str):
        try:
            return DataType.from_string(type_str)
        except ValueError:
            return type_str

    @staticmethod
    def _format_type(type_obj):
        """Format type for display in error messages"""
        if isinstance(type_obj, DataType):
            type_map = {
                DataType.I16: "🐽 (i16)",
                DataType.I32: "🐷 (i32)",
                DataType.I64: "🐗 (i64)",
                DataType.BOOL: "wow (bool)",
                DataType.VOID: "😑 (void)",
            }
            return type_map.get(type_obj, str(type_obj))
        elif type_obj == DataType.STRING:
            return "👺 (string)"
        elif type_obj == LAMBDA:
            return "🥩 (lambda)"
        return str(type_obj)

    def visit_lambda(self, node):
        for param in node.params:
            if isinstance(param.param_type, str):
                if not self.context.is_struct_defined(param.param_type):
                    raise ValueError(f"Type 🐖{param.param_type}🐖 is not defined for lambda parameter at line {node.line}!")
        self.context.enter_scope()
        for param in node.params:
            if not self.context.declare_variable(param.name, param.param_type, mutable=False):
                raise ValueError(f"Duplicate parameter 🐖{param.name}🐖 in lambda at line {node.line}!")
        
        was_inside_lambda = self.inside_lambda
        self.inside_lambda = True
        body_type = node.body.accept(self)
        node.inferred_return_type = body_type
        self.inside_lambda = was_inside_lambda
        self.context.exit_scope()
        return LAMBDA
    
    def visit_string(self, node):
        return DataType.STRING

    def visit_interpolated_string(self, node: InterpolatedStringNode):
        for part_type, content in node.parts:
            if part_type == 'expr':
                expr_type = content.accept(self)
                if not isinstance(expr_type, DataType):
                    raise ValueError(f"Cannot interpolate struct type in string at line {node.line}! "
                        f"Only primitive types can be interpolated with 🍗.")
        return DataType.STRING