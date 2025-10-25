# 🐷 PigLang Programming Language

## THE BEST LANGUAGE IN YOUR LIFE EVER*

---

## 🎯 Overview

PigLang is a unique programming language that combines:
- **Emoji-based operators** for visual expressiveness
- **Pig-themed syntax** with 🐽 variable wrapping and 🐖🐖🐖 blocks
- **Mood Lines** - innovative inverted logic execution
- **Strict line structure** for clean, readable code
- **Type-safe arithmetic** with overflow checking

## ✨ Key Features

### 🐽 Pig-Wrapped Variables
All variables are wrapped in pig, poop, heart or flower emojis:
```piglang
# 😀 🐷 🐽my_variable🐽 @ 42 #
```

### 💖 Emotional Operators
- `❤️` Addition
- `💔` Subtraction  
- `💞` Multiplication
- `💕` Division
- `🌸🌸` Equals
- `💩🌸` Not equals
- `💩` Logical NOT

### 🌙 Mood Lines (Inverted Logic)
Lines wrapped in `#~ ... ~#` execute with inverted logic:
```piglang
# 🐽x🐽 @ 10 ❤️ 5 #        # Normal: x = 15
#~ 🐽x🐽 @ 10 ❤️ 5 ~#      # Mood: x = 5 (❤️ → 💔)

# SAVE 🐽x🐽 > 10 #         # Normal: if x > 10
#~ SAVE 🐽x🐽 > 10 ~#       # Mood: if x <= 10
```

### 🐖 Block Delimiters
All code blocks are wrapped in `🐖🐖🐖`:
```piglang
# SAVE condition #
# 🐖🐖🐖 #
# statements #
# 🐖🐖🐖 #
```

---

### Comments
There are two types of comments:
* Single-line comments:
```piglang
👀 This is a single-line comment
# 😀 🐷 🐽x🐽 @ 10 #  👀 Comment at end of line
```
* Multi-line comments:
```piglang
👀👀👀
This is a multi-line comment
It can span multiple lines
👀👀👀
```
# 😀 🐷 🐽x🐽 @ 10 #

---

## 📋 Language Specification

### Variable naming

The variable name must contain only *letters* or *&*, but the first symbol must be a letter

### Type System

| Type | Description | Range |
|------|-------------|-------|
| `🐽` | 16-bit integer (i16) | -32,768 to 32,767 |
| `🐷` | 32-bit integer (i32) | -2,147,483,648 to 2,147,483,647 |
| `🐗` | 64-bit integer (i64) | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 |
| `wow` | Boolean | `LOVE` (true) or `HATE` (false) |

### Mutability

- `😀` - Mutable variable
- `😭` - Constant (immutable) variable

### Operators

#### Arithmetic
- `❤️` Addition
- `💔` Subtraction
- `💞` Multiplication
- `💕` Division

#### Comparison
- `🌸🌸` Equals
- `💩🌸` Not equals
- `>` Greater than
- `<` Less than
- `🌸>` Greater or equal
- `🌸<` Less or equal

#### Logical
- `💩` NOT (unary)
- `hru` AND
- `bruh` OR

#### Other
- `@` Assignment
- `**` ... `**` Expression grouping

### Control Flow

#### If-Elif-Else
```piglang
# SAVE condition #
# 🐖🐖🐖 #
# statements #
# 🐖🐖🐖 #
# HURT another_condition #
# 🐖🐖🐖 #
# statements #
# 🐖🐖🐖 #
# KILL #
# 🐖🐖🐖 #
# statements #
# 🐖🐖🐖 #
```

#### While Loop
```piglang
# OINK condition #
# 🐖🐖🐖 #
# statements #
# 🐖🐖🐖 #
```

### Operator Precedence (High to Low)

1. `**` ... `**` (grouping)
2. `💩` (unary NOT)
3. `💞`, `💕` (multiplication, division)
4. `❤️`, `💔` (addition, subtraction)
5. `>`, `<`, `🌸>`, `🌸<`, `🌸🌸`, `💩🌸` (comparison)
6. `hru` (logical AND)
7. `bruh` (logical OR)

---

## 📝 Example Programs

### Hello Counter
```piglang
# 😀 🐷 🐽counter🐽 @ 0 #
# 😭 🐷 🐽max🐽 @ 10 #

# OINK 🐽counter🐽 < 🐽max🐽 #
# 🐖🐖🐖 #
# 🐽counter🐽 @ 🐽counter🐽 ❤️ 1 #
# 🐖🐖🐖 #

# ... 🐽counter🐽 ... #
```

### Conditional Logic
```piglang
# 😀 🐷 🐽x🐽 @ 42 #
# 😀 wow 🐽is_valid🐽 @ HATE #

# SAVE 🐽x🐽 > 0 hru 🐽x🐽 < 100 #
# 🐖🐖🐖 #
# 🐽is_valid🐽 @ LOVE #
# 🐖🐖🐖 #
# HURT 🐽x🐽 🌸🌸 0 #
# 🐖🐖🐖 #
# 🐽is_valid🐽 @ HATE #
# 🐖🐖🐖 #
# KILL #
# 🐖🐖🐖 #
# 🐽is_valid🐽 @ HATE #
# 🐖🐖🐖 #

# ... 🐽is_valid🐽 ... #
```

### Using Mood Lines
```piglang
# 😀 🐷 🐽value🐽 @ 20 #

# 🐽value🐽 @ 🐽value🐽 ❤️ 10 #
#~ 🐽value🐽 @ 🐽value🐽 ❤️ 5 ~#

# SAVE 🐽value🐽 🌸🌸 25 #
# 🐖🐖🐖 #
# ... LOVE ... #
# 🐖🐖🐖 #

# ... HATE ... #
```
**Explanation:** 
- Line 3: `value = 20 + 10 = 30`
- Line 4 (Mood): `value = 30 - 5 = 25` (❤️ inverted to 💔)
- Line 6: Condition evaluates to true, returns `LOVE`

### Complex Expression
```piglang
# 😀 🐷 🐽a🐽 @ 5 #
# 😀 🐷 🐽b🐽 @ 3 #
# 😀 🐷 🐽c🐽 @ 2 #

# 😀 🐷 🐽result🐽 @ ** 🐽a🐽 ❤️ 🐽b🐽 ** 💞 🐽c🐽 #

# ... 🐽result🐽 ... #
```
**Result:** `(5 + 3) * 2 = 16`

---

## 🎭 Mood Lines Explained

Mood lines (`#~ ... ~#`) invert the logic of the enclosed statement:

### Arithmetic Inversion
| Normal | Mood Inverted |
|--------|---------------|
| `❤️` (add) | `💔` (sub) |
| `💔` (sub) | `❤️` (add) |
| `💞` (mul) | `💕` (div) |
| `💕` (div) | `💞` (mul) |

### Comparison Inversion
| Normal | Mood Inverted |
|--------|---------------|
| `>` | `🌸<` |
| `<` | `🌸>` |
| `🌸>` | `<` |
| `🌸<` | `>` |
| `🌸🌸` | `💩🌸` |
| `💩🌸` | `🌸🌸` |

### Boolean Inversion
| Normal | Mood Inverted |
|--------|---------------|
| `LOVE` | `HATE` |
| `HATE` | `LOVE` |

### Conditional Inversion
Mood lines negate the entire boolean condition:
```piglang
# SAVE 🐽x🐽 > 5 hru 🐽y🐽 < 10 #     # if (x > 5 && y < 10)
#~ SAVE 🐽x🐽 > 5 hru 🐽y🐽 < 10 ~#   # if !(x > 5 && y < 10)
```

---

## 📐 EBNF Grammar

```ebnf
program ::= line* return_line

line ::= normal_line | mood_line
normal_line ::= "#" line_content "#"
mood_line ::= "#" "~" line_content "~" "#"

line_content ::= stmt | block_delimiter | control_start
return_line ::= "#" "..." expr "..." "#"

stmt ::= decl | assign
decl ::= mutability type "🐽" ID "🐽" [ "@" expr ]
assign ::= "🐽" ID "🐽" "@" expr

mutability ::= "😀" | "😭"
type ::= "🐽" | "🐷" | "🐗" | "wow"

control_start ::= if_start | elif_start | else_start | loop_start
if_start ::= "SAVE" expr
elif_start ::= "HURT" expr
else_start ::= "KILL"
loop_start ::= "OINK" expr

block_delimiter ::= "🐖🐖🐖"

expr ::= logical_or_expr
logical_or_expr ::= logical_and_expr { "bruh" logical_and_expr }*
logical_and_expr ::= comparison_expr { "hru" comparison_expr }*
comparison_expr ::= additive_expr [ comparison_op additive_expr ]
comparison_op ::= "🌸🌸" | "💩🌸" | "🌸>" | "🌸<" | ">" | "<"

additive_expr ::= multiplicative_expr { ("❤️" | "💔") multiplicative_expr }*
multiplicative_expr ::= unary_expr { ("💞" | "💕") unary_expr }*
unary_expr ::= [ "💩" ] factor

factor ::= NUMBER | "🐽" ID "🐽" | "**" expr "**" | boolean
boolean ::= "LOVE" | "HATE"

ID ::= LETTER { LETTER | DIGIT | "_" }*
NUMBER ::= [ "-" ] DIGIT { DIGIT }*
```

---

## 🔒 Safety Features

### Type Overflow Checking
All arithmetic operations automatically check for overflow/underflow:
```piglang
# 😀 🐽 🐽small🐽 @ 32767 #
# 🐽small🐽 @ 🐽small🐽 ❤️ 1 #  # Runtime error: i16 overflow!
```

### Immutability Enforcement
Constants cannot be reassigned:
```piglang
# 😭 🐷 🐽constant🐽 @ 100 #
# 🐽constant🐽 @ 200 #  # Compile error: cannot assign to constant!
```

### No Variable Shadowing
Variables cannot be redeclared in any scope:
```piglang
# 😀 🐷 🐽x🐽 @ 10 #
# SAVE LOVE #
# 🐖🐖🐖 #
# 😀 🐷 🐽x🐽 @ 20 #  # Compile error: variable 'x' already declared!
# 🐖🐖🐖 #
```

---

## 🎨 Style Guide

### Line Structure
- Each statement on its own line
- Lines start with `#` and end with `#`
- Mood lines use `#~` and `~#`

### Variable Naming
- Use descriptive names: `🐽counter🐽`, `🐽total_sum🐽`
- Snake_case recommended
- Always wrap in 🐽 emojis

### Block Formatting
```piglang
# SAVE condition #
# 🐖🐖🐖 #
# statement1 #
# statement2 #
# 🐖🐖🐖 #
```

### Comments
PigLang does not support comments in the current specification. Use descriptive variable names instead.

---

## 🚀 Getting Started

### Example: Fibonacci Calculator
```piglang
# 😀 🐷 🐽a🐽 @ 0 #
# 😀 🐷 🐽b🐽 @ 1 #
# 😀 🐷 🐽counter🐽 @ 0 #
# 😭 🐷 🐽n🐽 @ 10 #

# OINK 🐽counter🐽 < 🐽n🐽 #
# 🐖🐖🐖 #
# 😀 🐷 🐽temp🐽 @ 🐽a🐽 ❤️ 🐽b🐽 #
# 🐽a🐽 @ 🐽b🐽 #
# 🐽b🐽 @ 🐽temp🐽 #
# 🐽counter🐽 @ 🐽counter🐽 ❤️ 1 #
# 🐖🐖🐖 #

# ... 🐽a🐽 ... #
```

---

## 🤔 FAQ

**Why pig emojis?**  
*Answer*: BEACAUSE I DECIDED TO CHOOSE PUGS AS ANA SOURCE OF INSPIRATION

**What's the purpose of Mood Lines?**  
*Answer*: Mood Lines provide a unique way to write inverse logic without explicit negation operators, making certain patterns more concise.

**Can I nest conditionals?**  
*Answer*: Yes! You can nest any control structures within 🐖🐖🐖 blocks.

**Is PigLang case-sensitive?**  
*Answer*: Yes, identifiers are case-sensitive. `🐽myVar🐽` and `🐽MyVar🐽` are different variables.

**Why `**` instead of `()`?**  
*Answer*: To maintain PigLang's unique visual identity and distinguish it from traditional languages.

**Can I shadow variables?**
*Answer*: No! PigLang does not allow variable shadowing. Once a variable is declared, it cannot be redeclared in any scope.

---

## 🎉 Have Fun Coding!

**Remember:**
- Wrap your variables in 🐽
- Enclose blocks with 🐖🐖🐖
- Use LOVE and HATE for booleans
- Try Mood Lines for inverted logic
- Every program must return something!
- No variable shadowing allowed!
- Use `hru` for AND and `bruh` for OR

Happy PigLang coding! 🐷✨

---

## 📦 Implementation Notes

### Modified Files
The following files have been updated to support PigLang:

1. **lexer_state.py** - Added EMOJI and MOOD_LINE states
2. **token_type.py** - Complete rewrite with PigLang tokens (emoji operators, pig types, control flow keywords)
3. **data_type.py** - Updated with pig emoji types (🐽 for i16, 🐷 for i32, 🐗 for i64, wow for bool)
4. **operator.py** - Updated with emoji operators (❤️💔💞💕🌸💩) and logical operators (hru, bruh)
5. **lexer.py** - Complete rewrite to handle emoji tokenization and PigLang syntax
6. **context.py** - Modified to restrict variable shadowing across all scopes

### Logical Operator Changes
- `aaNdd` → `hru` (AND operator)
- `oorr` → `bruh` (OR operator)