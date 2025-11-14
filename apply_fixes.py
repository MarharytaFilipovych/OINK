#!/usr/bin/env python3
"""
Automated fix script for PigLang compiler bugs
Run this script from your project root directory
"""
import os
import sys

def apply_fix_1_lexer():
    """Fix lexer.py - emoji token length checking"""
    filepath = "compiler/lexer/lexer.py"
    
    if not os.path.exists(filepath):
        print(f"ERROR: {filepath} not found!")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the for loop in __try_emoji_token
    old_line = "for length in [9, 6, 3, 2, 1]:"
    new_line = "for length in [9, 7, 6, 5, 4, 3, 2, 1]:"
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed {filepath}")
        return True
    else:
        print(f"⚠ Already fixed or pattern not found in {filepath}")
        return True

def apply_fix_2_expression_parser():
    """Fix expression_parser.py - struct type parsing"""
    filepath = "compiler/syntax_parser/expression_parser.py"
    
    if not os.path.exists(filepath):
        print(f"ERROR: {filepath} not found!")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find and replace the _parse_type method
    in_parse_type = False
    method_start = -1
    
    for i, line in enumerate(lines):
        if 'def _parse_type(self)' in line:
            in_parse_type = True
            method_start = i
            break
    
    if method_start == -1:
        print(f"ERROR: _parse_type method not found in {filepath}")
        return False
    
    # Replace the method implementation
    new_method = '''    def _parse_type(self) -> Union[DataType, str]:
        token = self._peek()
        
        if not token:
            raise ValueError("Expected type declaration but reached end of input")
        
        type_map = {
            TokenType.I16_TYPE: DataType.I16,
            TokenType.I32_TYPE: DataType.I32,
            TokenType.I64_TYPE: DataType.I64,
            TokenType.BOOL: DataType.BOOL,
            TokenType.VOID: DataType.VOID
        }
        
        if token.token_type in type_map:
            self._eat()
            return type_map[token.token_type]
        
        # Check if it's a struct type (variable name)
        if token.token_type == TokenType.VARIABLE:
            struct_name = token.value
            self._eat()
            return struct_name
        
        raise ValueError(f"Expected type declaration at line {token.line}")
'''
    
    # Find the end of the method
    method_end = method_start + 1
    indent_level = len(lines[method_start]) - len(lines[method_start].lstrip())
    
    for i in range(method_start + 1, len(lines)):
        line = lines[i]
        if line.strip() and not line.startswith(' ' * (indent_level + 1)):
            method_end = i
            break
    
    # Replace
    lines[method_start:method_end] = [new_method + '\n']
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"✓ Fixed {filepath}")
    return True

def apply_fix_3_statement_parser():
    """Fix statement_parser.py - add VARIABLE case and fix _parse_declaration"""
    filepath = "compiler/syntax_parser/statement_parser.py"
    
    if not os.path.exists(filepath):
        print(f"ERROR: {filepath} not found!")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Add VARIABLE case in _parse_statement
    old_pattern1 = '''        elif token.token_type == TokenType.BLOCK_BORDER:
            self._eat()
        else:
            raise ValueError(f"Unexpected token at line {token.line}: {token.token_type}")'''
    
    new_pattern1 = '''        elif token.token_type == TokenType.BLOCK_BORDER:
            self._eat()
        elif token.token_type == TokenType.VARIABLE:
            stmt = self._parse_declaration()
        else:
            raise ValueError(f"Unexpected token at line {token.line}: {token.token_type}")'''
    
    if old_pattern1 in content:
        content = content.replace(old_pattern1, new_pattern1)
    
    # Fix 2: Make mutability optional in _parse_declaration
    old_pattern2 = '''    def _parse_declaration(self) -> DeclNode:
        can_mutate = self._peek().token_type == TokenType.MUT
        self._eat()
        var_type = self._parse_type()'''
    
    new_pattern2 = '''    def _parse_declaration(self) -> DeclNode:
        token = self._peek()
        
        if token.token_type in [TokenType.MUT, TokenType.CONST]:
            can_mutate = token.token_type == TokenType.MUT
            self._eat()
        else:
            can_mutate = True
        
        var_type = self._parse_type()'''
    
    if old_pattern2 in content:
        content = content.replace(old_pattern2, new_pattern2)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Fixed {filepath}")
    return True

def apply_fix_4_declaration_parser():
    """Fix declaration_parser.py - struct types in member functions"""
    filepath = "compiler/syntax_parser/declaration_parser.py"
    
    if not os.path.exists(filepath):
        print(f"ERROR: {filepath} not found!")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the condition in _is_member_function_declaration
    old_line = "if not self._peek() or not self._peek().token_type.is_data_type():"
    new_line = "if not self._peek() or not (self._peek().token_type.is_data_type() or self._peek().token_type == TokenType.VARIABLE):"
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed {filepath}")
        return True
    else:
        print(f"⚠ Already fixed or pattern not found in {filepath}")
        return True

def main():
    print("=" * 60)
    print("PigLang Compiler Auto-Fix Script")
    print("=" * 60)
    print()
    
    # Check we're in the right directory
    if not os.path.exists("compiler"):
        print("ERROR: Please run this script from the project root directory")
        print("(The directory containing the 'compiler' folder)")
        sys.exit(1)
    
    success = True
    
    print("Applying fixes...")
    print()
    
    success &= apply_fix_1_lexer()
    success &= apply_fix_2_expression_parser()
    success &= apply_fix_3_statement_parser()
    success &= apply_fix_4_declaration_parser()
    
    print()
    if success:
        print("=" * 60)
        print("✓ All fixes applied successfully!")
        print("=" * 60)
        print()
        print("Now run: ./tests.sh")
    else:
        print("=" * 60)
        print("✗ Some fixes failed. Please check the errors above.")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
