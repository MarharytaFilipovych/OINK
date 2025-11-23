#!/usr/bin/env python3
from ...constants import I16, I32, I64, I1


class LLVMEmitter:
    def __init__(self):
        self.translated_lines: list[str] = []
        self.struct_type_lines: list[str] = []
        self.function_definitions: list[str] = []
        self.temp_counter = 0
        self.label_counter = 0

    def emit_line(self, line: str):
        self.translated_lines.append(line)

    def get_temp_register(self) -> str:
        reg = f"%_temp_{self.temp_counter}"
        self.temp_counter += 1
        return reg

    def get_next_label_id(self) -> int:
        label_id = self.label_counter
        self.label_counter += 1
        return label_id

    def emit_label(self, label: str):
        self.translated_lines.append(f"{label}:")

    def add_struct_type_definition(self, struct_def: str):
        self.struct_type_lines.append(struct_def)

    def add_function_definition(self, lines: list[str]):
        self.function_definitions.extend(lines)

    def build_final_output(self) -> str:
        result = [self.__get_io_functions_llvm()]
        if self.struct_type_lines:
            result.extend(self.struct_type_lines)
            result.append("")
        if self.function_definitions:
            result.extend(self.function_definitions)
            result.append("")
        result.append("define i32 @main() {")
        result.extend(self.translated_lines)
        result.append("}")
        return "\n".join(result)

    @staticmethod
    def __get_io_functions_llvm() -> str:
        return """declare i32 @printf(i8*, ...)
declare i32 @scanf(i8*, ...)

@exit_format = private unnamed_addr constant [29 x i8] c"Program exit with result %d\\0A\\00", align 1
@print_i16_format = private unnamed_addr constant [5 x i8] c"%hd\\0A\\00", align 1
@print_i32_format = private unnamed_addr constant [4 x i8] c"%d\\0A\\00", align 1
@print_i64_format = private unnamed_addr constant [6 x i8] c"%lld\\0A\\00", align 1
@read_i16_format = private unnamed_addr constant [4 x i8] c"%hd\\00", align 1
@read_i32_format = private unnamed_addr constant [3 x i8] c"%d\\00", align 1
@read_i64_format = private unnamed_addr constant [5 x i8] c"%lld\\00", align 1

define void @printResult(i32 %val) {
  %fmt_ptr = getelementptr inbounds [29 x i8], [29 x i8]* @exit_format, i32 0, i32 0
  call i32 (i8*, ...) @printf(i8* %fmt_ptr, i32 %val)
  ret void
}

define void @printValue_i16(i16 %val) {
  %fmt_ptr = getelementptr inbounds [5 x i8], [5 x i8]* @print_i16_format, i32 0, i32 0
  call i32 (i8*, ...) @printf(i8* %fmt_ptr, i16 %val)
  ret void
}

define void @printValue_i32(i32 %val) {
  %fmt_ptr = getelementptr inbounds [4 x i8], [4 x i8]* @print_i32_format, i32 0, i32 0
  call i32 (i8*, ...) @printf(i8* %fmt_ptr, i32 %val)
  ret void
}

define void @printValue_i64(i64 %val) {
  %fmt_ptr = getelementptr inbounds [6 x i8], [6 x i8]* @print_i64_format, i32 0, i32 0
  call i32 (i8*, ...) @printf(i8* %fmt_ptr, i64 %val)
  ret void
}

define i16 @readInput_i16() {
  %val_ptr = alloca i16
  %fmt_ptr = getelementptr inbounds [4 x i8], [4 x i8]* @read_i16_format, i32 0, i32 0
  call i32 (i8*, ...) @scanf(i8* %fmt_ptr, i16* %val_ptr)
  %val = load i16, i16* %val_ptr
  ret i16 %val
}

define i32 @readInput_i32() {
  %val_ptr = alloca i32
  %fmt_ptr = getelementptr inbounds [3 x i8], [3 x i8]* @read_i32_format, i32 0, i32 0
  call i32 (i8*, ...) @scanf(i8* %fmt_ptr, i32* %val_ptr)
  %val = load i32, i32* %val_ptr
  ret i32 %val
}

define i64 @readInput_i64() {
  %val_ptr = alloca i64
  %fmt_ptr = getelementptr inbounds [5 x i8], [5 x i8]* @read_i64_format, i32 0, i32 0
  call i32 (i8*, ...) @scanf(i8* %fmt_ptr, i64* %val_ptr)
  %val = load i64, i64* %val_ptr
  ret i64 %val
}

"""

    def reset_for_function(self):
        self.translated_lines = []
        self.temp_counter = 0
        self.label_counter = 0

    def copy_state(self) -> dict:
        return {
            'translated_lines': self.translated_lines.copy(),
            'temp_counter': self.temp_counter,
            'label_counter': self.label_counter
        }

    def restore_state(self, state: dict):
        self.translated_lines = state['translated_lines']
        self.temp_counter = state['temp_counter']
        self.label_counter = state['label_counter']

    @staticmethod
    def get_print_function(llvm_type: str) -> str:
        if llvm_type == I16:
            return "@printValue_i16"
        elif llvm_type == I32 or llvm_type == I1:
            return "@printValue_i32"
        elif llvm_type == I64:
            return "@printValue_i64"
        else:
            raise ValueError(f"Unsupported print type: {llvm_type}")

    @staticmethod
    def get_scanf_format_string(var_type) -> str:
        llvm_type_name = var_type.to_llvm().replace('%', '')
        if llvm_type_name == I16:
            return "@read_i16_format"
        elif llvm_type_name == I32:
            return "@read_i32_format"
        elif llvm_type_name == I64:
            return "@read_i64_format"
        else:
            raise ValueError(f"Unsupported read type: {llvm_type_name}")
