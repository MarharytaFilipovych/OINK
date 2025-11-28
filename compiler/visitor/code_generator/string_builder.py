#!/usr/bin/env python3
from ...llvm_specifics.data_type import DataType
from ...constants import I1, I16, I32, I64


class StringBuilder:
    def __init__(self, emitter):
        self.emitter = emitter
        self.next_string_id = 0
        self.string_constants = []

    def build_string_constant(self, text: str) -> str:
        if not text:
            return self.__create_empty_string()
        
        string_id = self.next_string_id
        self.next_string_id += 1
        
        escaped_text = self.__escape_for_llvm(text)
        length = len(text) + 1
        
        global_name = f"@.str.{string_id}"
        constant_def = f"{global_name} = private unnamed_addr constant [{length} x i8] c\"{escaped_text}\\00\", align 1"
        self.string_constants.append(constant_def)
        
        ptr_reg = self.emitter.get_temp_register()
        self.emitter.emit_line(f"  {ptr_reg} = getelementptr inbounds [{length} x i8], [{length} x i8]* {global_name}, i32 0, i32 0")
        self.emitter.emit_line(f"  call i32 (i8*, ...) @printf(i8* {ptr_reg})")
        
        return ptr_reg

    def __create_empty_string(self):
        ptr_reg = self.emitter.get_temp_register()
        self.emitter.emit_line(f"  {ptr_reg} = getelementptr inbounds [1 x i8], [1 x i8]* @.str.empty, i32 0, i32 0")
        return ptr_reg

    def build_interpolated_string(self, segments: list) -> str:
        for i, (seg_type, content) in enumerate(segments):
            if seg_type == 'text':
                self.__print_text_segment(content)
            else:
                value_reg, expr_type = content
                self.__print_expr_segment(value_reg, expr_type)
        
        self.__print_newline()
        return ""

    def __print_text_segment(self, text: str):
        if text:
            string_id = self.next_string_id
            self.next_string_id += 1
            
            escaped_text = self.__escape_for_llvm(text)
            length = len(text) + 1
            
            global_name = f"@.str.{string_id}"
            constant_def = f"{global_name} = private unnamed_addr constant [{length} x i8] c\"{escaped_text}\\00\", align 1"
            self.string_constants.append(constant_def)
            
            ptr_reg = self.emitter.get_temp_register()
            self.emitter.emit_line(f"  {ptr_reg} = getelementptr inbounds [{length} x i8], [{length} x i8]* {global_name}, i32 0, i32 0")
            self.emitter.emit_line(f"  call i32 (i8*, ...) @printf(i8* {ptr_reg})")

    def __print_expr_segment(self, value_reg: str, expr_type: DataType):
        llvm_type = expr_type.to_llvm()
        
        if llvm_type == I1:
            value_reg = self.__extend_bool_to_i32(value_reg)
            llvm_type = I32
        
        format_str = self.__get_format_string(llvm_type)
        ptr_reg = self.emitter.get_temp_register()
        self.emitter.emit_line(f"  {ptr_reg} = getelementptr inbounds {format_str}")
        self.emitter.emit_line(f"  call i32 (i8*, ...) @printf(i8* {ptr_reg}, {llvm_type} {value_reg})")

    def __print_newline(self):
        newline_reg = self.emitter.get_temp_register()
        self.emitter.emit_line(f"  {newline_reg} = getelementptr inbounds [2 x i8], [2 x i8]* @.str.newline, i32 0, i32 0")
        self.emitter.emit_line(f"  call i32 (i8*, ...) @printf(i8* {newline_reg})")

    def __extend_bool_to_i32(self, bool_reg: str) -> str:
        result_reg = self.emitter.get_temp_register()
        self.emitter.emit_line(f"  {result_reg} = zext i1 {bool_reg} to i32")
        return result_reg

    @staticmethod
    def __get_format_string(llvm_type: str) -> str:
        if llvm_type == I16:
            return "[4 x i8], [4 x i8]* @.fmt.i16, i32 0, i32 0"
        elif llvm_type == I32:
            return "[3 x i8], [3 x i8]* @.fmt.i32, i32 0, i32 0"
        elif llvm_type == I64:
            return "[5 x i8], [5 x i8]* @.fmt.i64, i32 0, i32 0"
        else:
            raise ValueError(f"Unsupported type for interpolation: {llvm_type}")

    @staticmethod
    def __escape_for_llvm(text: str) -> str:
        result = []
        for char in text:
            if char == '\n':
                result.append('\\0A')
            elif char == '\t':
                result.append('\\09')
            elif char == '\\':
                result.append('\\\\')
            elif char == '"':
                result.append('\\"')
            else:
                result.append(char)
        return ''.join(result)

    def get_string_constant_definitions(self) -> list[str]:
        constants = [
            "@.str.empty = private unnamed_addr constant [1 x i8] zeroinitializer, align 1",
            "@.str.newline = private unnamed_addr constant [2 x i8] c\"\\0A\\00\", align 1",
            "@.fmt.i16 = private unnamed_addr constant [4 x i8] c\"%hd\\00\", align 1",
            "@.fmt.i32 = private unnamed_addr constant [3 x i8] c\"%d\\00\", align 1",
            "@.fmt.i64 = private unnamed_addr constant [5 x i8] c\"%lld\\00\", align 1"
        ]
        return constants + self.string_constants