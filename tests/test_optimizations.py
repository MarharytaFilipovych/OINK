#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler.lexer.lexer import Lexer
from compiler.syntax_parser.syntax_parser import SyntaxParser
from compiler.visitor.semantic_analyzer.semantic_analyzer import SemanticAnalyzer
from compiler.optimizer.optimizer import Optimizer


def test_unused_variable_removal():
    print("Test 1: Unused Variable Removal")
    
    code = """# 😀 🐷 🐖used🐖 @ 10 #
# 😀 🐷 🐖unused1🐖 @ 20 #
# 😀 🐷 🐖unused2🐖 @ 30 #
# 😀 🐷 🐖result🐖 @ 🐖used🐖 ❤️ 5 #
# ... 🐖result🐖 ... #
"""
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = SyntaxParser(tokens)
    ast = parser.parse_program()
    semantic_analyzer = SemanticAnalyzer()
    ast.accept(semantic_analyzer)
    
    initial_count = len(ast.statement_nodes)
    
    optimizer = Optimizer()
    stats = optimizer.optimize(ast)
    
    final_count = len(ast.statement_nodes)
    
    print(f"  Initial statements: {initial_count}")
    print(f"  Final statements: {final_count}")
    print(f"  Variables removed: {stats['variables_removed']}")
    assert stats['variables_removed'] == 2, "Should remove 2 unused variables"
    print("  ✓ PASSED\n")


def test_iterative_variable_removal():
    print("Test 2: Iterative Variable Removal")
    
    code = """# 😀 🐷 🐖used🐖 @ 10 #
# 😀 🐷 🐖chain1🐖 @ 🐖used🐖 ❤️ 5 #
# 😀 🐷 🐖chain2🐖 @ 🐖chain1🐖 💞 2 #
# 😀 🐷 🐖unused🐖 @ 🐖chain2🐖 💔 1 #
# ... 🐖used🐖 ... #
"""
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = SyntaxParser(tokens)
    ast = parser.parse_program()
    semantic_analyzer = SemanticAnalyzer()
    ast.accept(semantic_analyzer)
    
    optimizer = Optimizer()
    stats = optimizer.optimize(ast)
    
    print(f"  Variables removed: {stats['variables_removed']}")
    assert stats['variables_removed'] >= 3, "Should remove chain of unused variables"
    print("  ✓ PASSED\n")


def test_function_inlining():
    print("Test 3: Function Inlining (Single Use)")
    
    code = """# 🐷 PIG 🐖helper🐖 ** 🐷 🐖x🐖 ** #
# 🐖🐖🐖 #
# ... 🐖x🐖 💞 2 ... #
# 🐖🐖🐖 #
# 😀 🐷 🐖result🐖 @ 🐖helper🐖 ** 10 ** #
# ... 🐖result🐖 ... #
"""
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = SyntaxParser(tokens)
    ast = parser.parse_program()
    semantic_analyzer = SemanticAnalyzer()
    ast.accept(semantic_analyzer)
    
    initial_funcs = len(ast.function_declarations)
    
    optimizer = Optimizer()
    stats = optimizer.optimize(ast)
    
    final_funcs = len(ast.function_declarations)
    
    print(f"  Initial functions: {initial_funcs}")
    print(f"  Final functions: {final_funcs}")
    print(f"  Functions inlined: {stats['functions_inlined']}")
    assert stats['functions_inlined'] == 1, "Should inline single-use function"
    print("  ✓ PASSED\n")


def test_unused_function_removal():
    print("Test 4: Unused Function Removal")
    
    code = """# 🐷 PIG 🐖used_func🐖 ** 🐷 🐖x🐖 ** #
# 🐖🐖🐖 #
# ... 🐖x🐖 ❤️ 1 ... #
# 🐖🐖🐖 #
# 🐷 PIG 🐖unused_func🐖 ** 🐷 🐖y🐖 ** #
# 🐖🐖🐖 #
# ... 🐖y🐖 💞 2 ... #
# 🐖🐖🐖 #
# 😀 🐷 🐖a🐖 @ 🐖used_func🐖 ** 5 ** #
# 😀 🐷 🐖b🐖 @ 🐖used_func🐖 ** 10 ** #
# ... 🐖a🐖 ❤️ 🐖b🐖 ... #
"""
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = SyntaxParser(tokens)
    ast = parser.parse_program()
    semantic_analyzer = SemanticAnalyzer()
    ast.accept(semantic_analyzer)
    
    initial_funcs = len(ast.function_declarations)
    
    optimizer = Optimizer()
    stats = optimizer.optimize(ast)
    
    final_funcs = len(ast.function_declarations)
    
    print(f"  Initial functions: {initial_funcs}")
    print(f"  Final functions: {final_funcs}")
    print(f"  Functions removed: {stats['functions_removed']}")
    assert stats['functions_removed'] == 1, "Should remove unused function"
    print("  ✓ PASSED\n")


def test_combined_optimizations():
    print("Test 5: Combined Optimizations")
    
    code = """# 🐷 PIG 🐖single_use🐖 ** 🐷 🐖x🐖 ** #
# 🐖🐖🐖 #
# ... 🐖x🐖 💞 3 ... #
# 🐖🐖🐖 #
# 🐷 PIG 🐖never_used🐖 ** 🐷 🐖y🐖 ** #
# 🐖🐖🐖 #
# ... 🐖y🐖 💔 5 ... #
# 🐖🐖🐖 #
# 😀 🐷 🐖unused_var🐖 @ 100 #
# 😀 🐷 🐖result🐖 @ 🐖single_use🐖 ** 7 ** #
# ... 🐖result🐖 ... #
"""
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = SyntaxParser(tokens)
    ast = parser.parse_program()
    semantic_analyzer = SemanticAnalyzer()
    ast.accept(semantic_analyzer)
    
    optimizer = Optimizer()
    stats = optimizer.optimize(ast)
    
    print(f"  Variables removed: {stats['variables_removed']}")
    print(f"  Functions inlined: {stats['functions_inlined']}")
    print(f"  Functions removed: {stats['functions_removed']}")
    
    assert stats['variables_removed'] >= 1, "Should remove unused variables"
    assert stats['functions_inlined'] == 1, "Should inline single-use function"
    assert stats['functions_removed'] == 1, "Should remove unused function"
    print("  ✓ PASSED\n")


if __name__ == "__main__":
    print("=" * 60)
    print("OINK Compiler Optimization Tests")
    print("=" * 60)
    print()
    
    try:
        test_unused_variable_removal()
        test_iterative_variable_removal()
        test_function_inlining()
        test_unused_function_removal()
        test_combined_optimizations()
        
        print("=" * 60)
        print("All optimization tests PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)