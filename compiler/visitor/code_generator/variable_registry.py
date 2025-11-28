#!/usr/bin/env python3
from typing import Union, Optional
from ...constants import UNDERLINE, VARIABLE_ALLOWED_SIGN
from ...llvm_specifics.data_type import DataType


class VariableRegistry:
    def __init__(self):
        self.variable_versions: dict[str, int] = {}
        self.variable_types: dict[str, Union[DataType, str]] = {}
        self.max_versions: dict[str, int] = {}
        self.lambda_functions: dict[str, str] = {}
        self.lambda_signatures: dict[str, list] = {}
        self.lambda_return_types: dict[str, Union[DataType, str]] = {}
        self.variable_mutability: dict[str, bool] = {}

    @staticmethod
    def __sanitize_name(variable: str) -> str:
        return variable.replace(VARIABLE_ALLOWED_SIGN, UNDERLINE)

    def get_variable_register(self, variable: str) -> str:
        sanitized_name = self.__sanitize_name(variable)
        if variable not in self.max_versions:
            self.max_versions[variable] = 0
            self.variable_versions[variable] = 0
            return f"%{sanitized_name}"
        self.max_versions[variable] += 1
        self.variable_versions[variable] = self.max_versions[variable]
        return f"%{sanitized_name}.{self.variable_versions[variable]}"

    def get_current_register(self, variable: str) -> str:
        sanitized_name = self.__sanitize_name(variable)
        return f"%{sanitized_name}" \
               if variable not in self.variable_versions or self.variable_versions[variable] == 0 else \
                f"%{sanitized_name}.{self.variable_versions[variable]}"

    def get_variable_type(self, variable: str) -> Optional[Union[DataType, str]]:
        return self.variable_types.get(variable)

    def set_variable_type(self, variable: str, var_type: Union[DataType, str]):
        self.variable_types[variable] = var_type

    def set_can_mutate(self, variable: str, can_mutate: bool):
        self.variable_mutability[variable] = can_mutate

    def set_variable_version(self, variable: str, version: int):
        self.variable_versions[variable] = version

    def get_variable_version(self, variable: str) -> Optional[int]:
        return self.variable_versions.get(variable)

    def is_field_access_from_this(self, variable: str) -> bool:
        return self.variable_versions.get(variable) == -1

    def copy_state(self) -> dict:
        return {
            'versions': self.variable_versions.copy(),
            'types': self.variable_types.copy(),
            'max_versions': self.max_versions.copy(),
            'mutability': self.variable_mutability.copy(),
            'lambda_functions': self.lambda_functions.copy(),
            'lambda_signatures': self.lambda_signatures.copy(),
            'lambda_return_types': self.lambda_return_types.copy(),
        }

    def restore_state(self, state: dict):
        for var in state['versions']:
            if var in self.max_versions and var in state['max_versions']:
                state['max_versions'][var] = max(self.max_versions[var], state['max_versions'][var])
        
        self.variable_versions = state['versions']
        self.variable_types = state['types']
        self.max_versions = state['max_versions']
        self.variable_mutability = state['mutability']
        self.lambda_functions = state['lambda_functions']
        self.lambda_signatures = state['lambda_signatures']
        self.lambda_return_types = state['lambda_return_types']

    def reset(self):
        self.variable_versions = {}
        self.variable_types = {}
        self.max_versions = {}
        self.lambda_functions = {}
        self.lambda_signatures = {}
        self.lambda_return_types = {}
        self.variable_mutability = {}