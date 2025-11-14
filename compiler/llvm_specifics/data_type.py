#!/usr/bin/env python3
from enum import Enum


class DataType(Enum):
    I16 = ("🐽", "i16")
    I32 = ("🐷", "i32")
    I64 = ("🐗", "i64")
    BOOL = ("wow", "i1")
    VOID = ("😑", "void")

    def __init__(self, keyword: str, llvm_representation: str):
        self.keyword = keyword
        self.llvm_representation = llvm_representation

    @staticmethod
    def from_string(type_str: str) -> 'DataType':
        for vt in DataType:
            if vt.keyword == type_str:
                return vt
        raise ValueError(f"This type does not exist: {type_str}")

    def to_llvm(self) -> str:
        return self.llvm_representation

    def __str__(self) -> str:
        return self.keyword