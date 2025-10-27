# 🐷 OINK Programming Language

## THE BEST LANGUAGE IN YOUR LIFE EVER*

---

## 🎯 Overview

**OINK* is a unique programming language that combines:
- **Emoji-based operators** for visual expressiveness
- **Pig-themed syntax** with 🐽 variable wrapping and 🐖🐖🐖 blocks, and funny piggy numeric data types(🐽,🐷, 🐗)
- **Mood Lines** - innovative inverted logic execution
- **Strict line structure** for clean, and for some people, readable code
- **Type-safe arithmetic** with overflow checking

## ✨ Key Features

### 🐽 Pig-Wrapped Variables
All variables are wrapped ina 🐽 snout emoji:

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

## 📋 Language Specification

### Type System

*! If you do not declare a varible, it will get a relevant default value !*

| Type | Description        | Range                                             | Default value |
|------|--------------------|---------------------------------------------------|----------------|
| `🐽` | 16-bit integer (i16) | -32,768 to 32,767                                | 0              |
| `🐷` | 32-bit integer (i32) | -2,147,483,648 to 2,147,483,647                 | 0              |
| `🐗` | 64-bit integer (i64) | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 | 0      |
| `wow` | Boolean             | `LOVE` (true) or `HATE` (false)                 | `HATE`         |

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
- `SAVE` If
- `HURT` Elif
- `KILL` Else

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
- `OINK` While

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
A program is zero or more statement wrappers followed by a return statement:

program ::= statement_wrapper* return_statement

Statements are wrapped in delimiters and can be normal or mood (inverted logic):

statement_wrapper ::= normal_statement | mood_statement
normal_statement ::= "#" statement_content "#" NEWLINE
mood_statement ::= "#" "~" statement_content "~" "#" NEWLINE
statement_content ::= stmt | block_delimiter
return_statement ::= "#" "..." expr "..." "#"

Statements are either declarations, assignments, conditionals, or loops:
stmt ::= decl | assign | if_stmt | while_stmt

Declaration: mutability, type, identifier wrapped in 🐽, and initializer expression. Variables are immutable by default unless 😀 is present:
decl ::= mutability type "🐽" ID "🐽" "@" expr
mutability ::= "😀" | "😭"
type ::= "🐽" | "🐷" | "🐗" | "wow"

Assignment: identifier wrapped in 🐽, assignment operator, expression:
assign ::= "🐽" ID "🐽" "@" expr

Conditional statements: if block with optional elif blocks and else block:
if_stmt ::= if_block elif_block* else_block?

if_block ::= "#" "SAVE" expr "#" NEWLINE "#" "🐖🐖🐖" "#" NEWLINE statement_wrapper* "#" "🐖🐖🐖" "#" NEWLINE
elif_block ::= "#" "HURT" expr "#" NEWLINE "#" "🐖🐖🐖" "#" NEWLINE statement_wrapper* "#" "🐖🐖🐖" "#" NEWLINE
else_block ::= "#" "KILL" "#" NEWLINE "#" "🐖🐖🐖" "#" NEWLINE statement_wrapper* "#" "🐖🐖🐖" "#" NEWLINE

While loop: condition followed by body block:
while_stmt ::= "#" "OINK" expr "#" NEWLINE "#" "🐖🐖🐖" "#" NEWLINE statement_wrapper* "#" "🐖🐖🐖" "#" NEWLINE

block_delimiter ::= "🐖🐖🐖"

Expression: handles logical OR operations with lower precedence; chains terms with bruh (left-associative):
expr ::= logical_and_expr { "bruh" logical_and_expr }*

Logical AND: handles logical AND operations; chains comparison expressions with hru (left-associative):
logical_and_expr ::= comparison_expr { "hru" comparison_expr }*

Comparison: handles equality and relational operations:
comparison_expr ::= additive_expr [ comparison_op additive_expr ]
comparison_op ::= "🌸🌸" | "💩🌸" | "🌸>" | "🌸<" | ">" | "<"

Additive expression: handles addition and subtraction with lower precedence; chains terms with ❤️ or 💔 (left-associative):
additive_expr ::= multiplicative_expr { ("❤️" | "💔") multiplicative_expr }*

Multiplicative expression: handles multiplication and division with higher precedence than expr; chains factors with 💞 or 💕 (left-associative):
multiplicative_expr ::= unary_expr { ("💞" | "💕") unary_expr }*

Unary expression: handles logical NOT operator:
unary_expr ::= [ "💩" ] factor

Factor: the base units of expressions—numeric literals (NUMBER, e.g., "10"), identifiers (ID, e.g., "x"), booleans (LOVE/HATE), or parenthesized sub-expressions for grouping and overriding precedence:
factor ::= NUMBER | "🐽" ID "🐽" | "" expr "" | boolean
boolean ::= "LOVE" | "HATE"
ID ::= LETTER { LETTER | "&" }*
NUMBER ::= [ "-" ] DIGIT { DIGIT }*

NEWLINE ::= "\n" | "\r\n"
```

---

## 🔒 Safety Features

### Type overflow checking
All arithmetic operations automatically check for overflow/underflow:
```piglang
# 😀 🐽 🐽small🐽 @ 32767 #
# 🐽small🐽 @ 🐽small🐽 ❤️ 1 #  # Runtime error: i16 overflow!
```

### Immutability enforcement
Constants cannot be reassigned:
```piglang
# 😭 🐷 🐽constant🐽 @ 100 #
# 🐽constant🐽 @ 200 #  # Compile error: cannot assign to constant!
```

### No variable shadowing
Variables cannot be redeclared in any scope:
```piglang
# 😀 🐷 🐽x🐽 @ 10 #
# SAVE LOVE #
# 🐖🐖🐖 #
# 😀 🐷 🐽x🐽 @ 20 #  # Compile error: variable 'x' already declared!
# 🐖🐖🐖 #
```

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
# 😀 🐷 🐽x🐽 @ 10 #
```
---

## 🎨 Style Guide

### Line Structure
- Each statement must be on its own line
- Lines start with `#` and end with `#`
- Mood lines are warpped  in `#~` and `~#` (instead of usual `#`)

### Variable Naming
- Use descriptive names: `🐽counter🐽`, `🐽total&sum🐽`
- Only letteters and `&` in variable names can be used!
- Always wrap your variable name in `🐽`

### Block Formatting
```piglang
# SAVE condition #
# 🐖🐖🐖 #
# statement1 #
# statement2 #
# 🐖🐖🐖 #
```
---

## 🚀 Getting Started

### Fibonacci Calculator

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

### Another program
```piglang
# 😀 🐷 🐽x🐽 @ 42 #

# 😀 wow 🐽is&valid🐽 @ HATE #

# SAVE 🐽x🐽 > 0 hru 🐽x🐽 < 100 #
# 🐖🐖🐖 #
# 🐽is&valid🐽 @ LOVE #
# 🐖🐖🐖 #
# HURT 🐽x🐽 🌸🌸 0 #
# 🐖🐖🐖 #
# 🐽is&valid🐽 @ HATE #
# 🐖🐖🐖 #
# KILL #
# 🐖🐖🐖 #
# 🐽is&valid🐽 @ HATE #
# 🐖🐖🐖 #

# ... 🐽is&valid🐽 ... #
```
---

## 🤔 FAQ

**Why pig emojis?**  
*Answer*: BEACAUSE I DECIDED TO CHOOSE PIGS AS A SOURCE OF INSPIRATION

**What's the purpose of Mood Lines?**  
*Answer*: Mood Lines provide a unique way to write inverse logic without explicit negation operators, making certain patterns more concise.

**Can I nest conditionals?**  
*Answer*: Yes! You can nest any control structures, but do not forget about placing them within 🐖🐖🐖 blocks.

**Is PigLang case-sensitive?**  
*Answer*: Yes, identifiers are case-sensitive. `🐽myVar🐽` and `🐽MyVar🐽` are different variables.

**Why `**` instead of `()`?**  
*Answer*: To maintain PigLang's unique visual identity!!!!!!!!!!!!!!!!!!!!!!

**Can I shadow variables?**
*Answer*: No! PigLang does not allow variable shadowing. Once a variable is declared, it cannot be redeclared in any scope.

**Can I use numbers within a varible name?**
*Answer*: No! Your variable name must start with a letter (alpha) and then can be followed either by a letter or a `&` sign!

---

## 🎉 HAVE FUN CODING (OR NOT), MY LOVELY FRIENDS!

**Remember:**
- Wrap your variables in 🐽
- Enclose blocks with 🐖🐖🐖
- Use `LOVE` and `HATE` for booleans
- Try *Mood Lines* for inverted logic
- Every program must return something!
- No variable shadowing allowed!
- Use `hru` for AND and `bruh` for OR

Happy *OINK* coding! 🐷✨

---

## 📦HOW TO RUN IT???

Unfortunatly, as for now, you cannot directly code in this amazing and superb language((
That is because the compiler is not implemented yet. However, do not worry, cutie, because it will be eventually:)
So, the time will come when you will use only this language on your daily basis and forget about other sacry languages at once:)

## ✨ WHAT SHOULD I DO NOW?

As I stated above -> WAIT.
Nevertheless, you can run some tests and verify that it is working. 
You can run these commands.... (but verify that you are not inside the *compiler* directory, you must be at the root level)

```bash

chmod +x tests.sh
./tests.sh

```

# ENJOY🐽🐽🐽
