# 🐷 OINK Programming Language

## THE BEST LANGUAGE IN YOUR LIFE EVER

## 🎯 Overview

**OINK** is a unique programming language that combines:
- **Emoji-based operators** for visual expressiveness
- **Pig-themed syntax** with 🐖 variable wrapping and 🐖🐖🐖 blocks, and funny piggy numeric data types (🐽, 🐷, 🐗)
- **Lambda expressions** with 🥩 meat emoji for anonymous functions
- **Mood Lines** - innovative inverted logic execution
- **Strict line structure** for clean, readable code
- **Type-safe arithmetic** with overflow checking
- **Functions and structures** with member functions
- **Built-in I/O operations** for input and output
- **String literals** with bacon emoji 🥓 delimiters

## ✨ Key Features

### 🥓 String Literals (NEW!)
Create string literals using the bacon emoji as delimiters:

```piglang
# print🤮 🥓Hello, World!🥓 #
# print🤮 🥓Welcome to OINK Programming Language!🥓 #
```

**String Syntax:**
- Start and end with `🥓` (bacon emoji)
- Support escape sequences: `\n` (newline), `\t` (tab), `\\` (backslash)
- Can be used with `print🤮` for output
- Strings must be on a single line

**String Examples:**
```piglang
# Simple string output
# print🤮 🥓Hello, World!🥓 #

# String with escape sequences
# print🤮 🥓Line 1\nLine 2\tTabbed🥓 #

# Multiple string prints
# print🤮 🥓Enter your name:🥓 #
# print🤮 🥓Thank you!🥓 #
```

### 🥩 Lambda Expressions
Create anonymous functions inline using the meat emoji:

```piglang
# 😀 🥩 🐖square🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 💞 🐖x🐖 🥩 #
# 😀 🐷 🐖result🐖 @ 🐖square🐖 ** 5 ** #
# ... 25 ... #
```

**Lambda Syntax:**
- Start and end with `🥩` (meat emoji)
- Parameters: `** type 🐖param🐖 **` (same as regular functions)
- Body: Single expression between `🥩` markers
- Format: `🥩 ** params ** 🥩 expression 🥩`

**Lambda Examples:**
```piglang
# Simple lambda with one parameter
# 😀 🥩 🐖double🐖 @ 🥩 ** 🐷 🐖n🐖 ** 🥩 🐖n🐖 💞 2 🥩 #

# Lambda with multiple parameters
# 😀 🥩 🐖add🐖 @ 🥩 ** 🐷 🐖a🐖 ** ** 🐷 🐖b🐖 ** 🥩 🐖a🐖 ❤️ 🐖b🐖 🥩 #

# Lambda with boolean result
# 😀 🥩 🐖is&positive🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 > 0 🥩 #
```

### 🐖 Pig-Wrapped Variables
All variables are wrapped in 🐖 pig emoji:

```piglang
# 😀 🐷 🐖my&variable🐖 @ 42 #
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
# 🐖x🐖 @ 10 ❤️ 5 #        # Normal: x = 15
#~ 🐖x🐖 @ 10 ❤️ 5 ~#      # Mood: x = 5 (❤️ → 💔)

# SAVE 🐖x🐖 > 10 #         # Normal: if x > 10
#~ SAVE 🐖x🐖 > 10 ~#       # Mood: if x <= 10
```

### 🐖 Block Delimiters
All code blocks are wrapped in `🐖🐖🐖`:

```piglang
# SAVE condition #
# 🐖🐖🐖 #
# statements #
# 🐖🐖🐖 #
```

### 🐷 Functions
Functions are declared using the `PIG` keyword with return type specified before:

```piglang
# 🐷 PIG 🐖add🐖 ** 🐷 🐖a🐖 ** ** 🐷 🐖b🐖 ** #
# 🐖🐖🐖 #
# ... 🐖a🐖 ❤️ 🐖b🐖 ... #
# 🐖🐖🐖 #
```

### 🐗 Structures with Member Functions
Structures are declared using the `BOAR` keyword and can contain both fields and member functions (using `PIGLET`):

```piglang
# BOAR 🐖Point🐖 #
# 🐖🐖🐖 #
# 😀 🐷 🐖x🐖 #
# 😀 🐷 🐖y🐖 #
# 🐷 PIGLET 🐖getX🐖 #
# 🐖🐖🐖 #
# ... 🐖x🐖 ... #
# 🐖🐖🐖 #
# 🐖🐖🐖 #
```

### 📥📤 Input/Output Functions
- `eat😋` - Read input from user (supports i16, i32, i64)
- `print🤮` - Print output to console (supports integers and strings)

## 📋 Language Specification

### Type System

*! If you do not declare a variable, it will get a relevant default value !*

| Type | Description        | Range                                             | Default value |
|------|--------------------|---------------------------------------------------|----------------|
| `🐽` | 16-bit integer (i16) | -32,768 to 32,767                                | 0              |
| `🐷` | 32-bit integer (i32) | -2,147,483,648 to 2,147,483,647                 | 0              |
| `🐗` | 64-bit integer (i64) | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 | 0      |
| `wow` | Boolean             | `LOVE` (true) or `HATE` (false)                 | `HATE`         |
| `😑` | Void                | No return value (for functions only)             | N/A            |
| `🥩` | Lambda              | Anonymous function                               | N/A            |
| `🥓` | String Literal      | Text enclosed in bacon emojis                    | N/A            |

### String Literals

Strings are text literals enclosed in bacon emojis (`🥓`).

**Syntax:**
```
🥓text content🥓
```

**Features:**
- Single-line strings only (no multi-line support)
- Escape sequences supported: `\n`, `\t`, `\\`
- Used primarily with `print🤮` for output
- Cannot be stored in variables (literals only)

**Usage:**
```piglang
# Print a simple message
# print🤮 🥓Hello, World!🥓 #

# Print with escape sequences
# print🤮 🥓Name:\tJohn\nAge:\t25🥓 #

# Create user-friendly prompts
# print🤮 🥓Enter your age:🥓 #
# 😀 🐷 🐖age🐖 #
# eat😋 🐖age🐖 #
# print🤮 🥓Your age is:🥓 #
# print🤮 🐖age🐖 #
```

**Escape Sequences:**
| Sequence | Description |
|----------|-------------|
| `\n`     | Newline     |
| `\t`     | Tab         |
| `\\`     | Backslash   |

### Lambda Expressions

Lambdas are anonymous functions that can be stored in variables and called like regular functions.

**Syntax:**
```
🥩 ** type 🐖param1🐖 ** ** type 🐖param2🐖 ** ... 🥩 expression 🥩
```

**Features:**
- Single expression body (no statements)
- Type-checked parameters
- Can capture outer scope (limited to parameters)
- Stored in lambda type variables (🥩)

**Usage:**
```piglang
# Declare lambda
# 😀 🥩 🐖increment🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 ❤️ 1 🥩 #

# Call lambda
# 😀 🐷 🐖value🐖 @ 10 #
# 😀 🐷 🐖result🐖 @ 🐖increment🐖 ** 🐖value🐖 ** #
# ... 11 ... #
```

**Complex Lambda Example:**
```piglang
# Lambda that operates on other values
# 😀 🥩 🐖compute🐖 @ 🥩 ** 🐷 🐖x🐖 ** ** 🐷 🐖y🐖 ** 🥩 ** 🐖x🐖 💞 🐖x🐖 ** ❤️ ** 🐖y🐖 💞 🐖y🐖 ** 🥩 #
# 😀 🐷 🐖sum&of&squares🐖 @ 🐖compute🐖 ** 3 ** ** 4 ** #
# ... 25 ... #
```

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

### Functions

Functions are declared with return type, `PIG` keyword, function name, and parameters:

```piglang
# return_type PIG 🐖function_name🐖 ** type 🐖param1🐖 ** ** type 🐖param2🐖 ** #
# 🐖🐖🐖 #
# function body #
# ... return_value ... #
# 🐖🐖🐖 #
```

**Function Features:**
- Parameters are wrapped in `** type 🐖param🐖 **`
- Multiple parameters separated by space
- Return statement required: `# ... expr ... #`
- Void functions use `😑` as return type and return nothing

**Function Call:**
```piglang
# 😀 🐷 🐖result🐖 @ 🐖add🐖 ** 🐖a🐖 ** ** 🐖b🐖 ** #
```

**Function Chaining:**
Functions can be chained using `_` (pig tail) operator:
```piglang
# 😀 🐷 🐖result🐖 @ 🐖getValue🐖 _ 🐖double🐖 _ 🐖increment🐖 #
```
Each function in the chain receives the result of the previous function as its first implicit parameter.

### Structures

Structures group data fields and member functions together:

```piglang
# BOAR 🐖StructName🐖 #
# 🐖🐖🐖 #
# field declarations #
# member function declarations #
# 🐖🐖🐖 #
```

**Structure Features:**
- Fields declared like variables: `# mutability type 🐖field_name🐖 #`
- Member functions use `PIGLET` keyword instead of `PIG`
- Member functions can access structure fields directly
- Structure instances created with initialization: `# 😀 🐖StructName🐖 🐖instance🐖 @ 🐖StructName🐖 ** value1 ** ** value2 ** #`

**Member Function Access:**
```piglang
# 😀 🐷 🐖value🐖 @ 🐖instance🐖 _ 🐖getX🐖 #
```
Note: `_` is the member access operator (pig tail!)

### Input/Output

#### Read Input: `eat😋`
Reads numeric input from the user.

**Supported types:** i16 (🐽), i32 (🐷), i64 (🐗)

```piglang
# 😀 🐷 🐖input_value🐖 #
# eat😋 🐖input_value🐖 #
```

#### Print Output: `print🤮`
Prints values to console (supports integers and string literals).

**Supported types:** i16 (🐽), i32 (🐷), i64 (🐗), string literals (🥓)

```piglang
# Print integer value
# print🤮 🐖value🐖 #

# Print expression result
# print🤮 ** 🐖x🐖 ❤️ 🐖y🐖 ** #

# Print string literal
# print🤮 🥓Hello, World!🥓 #
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

## 📐 EBNF Grammar

```ebnf
A program consists of optional structure declarations, function declarations, statements, and a return statement:

program ::= (function_decl | struct_decl)* statement_wrapper* return_statement

Structure declaration: BOAR keyword, structure name, fields, and optional member functions:
struct_decl ::= "#" "BOAR" "🐖" ID "🐖" "#" NEWLINE "#" "🐖🐖🐖" "#" NEWLINE struct_body "#" "🐖🐖🐖" "#" NEWLINE
struct_body ::= field_decl* member_function_decl*
field_decl ::= "#" mutability type "🐖" ID "🐖" "#" NEWLINE

Member function declaration within structure:
member_function_decl ::= "#" return_type "PIGLET" "🐖" ID "🐖" param_list "#" NEWLINE "#" "🐖🐖🐖" "#" NEWLINE statement_wrapper* return_statement? "#" "🐖🐖🐖" "#" NEWLINE

Function declaration: return type, PIG keyword, name, parameters, and body:
function_decl ::= "#" return_type "PIG" "🐖" ID "🐖" param_list "#" NEWLINE "#" "🐖🐖🐖" "#" NEWLINE statement_wrapper* return_statement? "#" "🐖🐖🐖" "#" NEWLINE

param_list ::= [ "**" type "🐖" ID "🐖" "**" ]*
return_type ::= type | "😑"

Statements are wrapped in delimiters and can be normal or mood (inverted logic):

statement_wrapper ::= normal_statement | mood_statement
normal_statement ::= "#" statement_content "#" NEWLINE
mood_statement ::= "#" "~" statement_content "~" "#" NEWLINE
statement_content ::= stmt | block_delimiter | io_stmt
return_statement ::= "#" "..." expr "..." "#"

Input/Output statements:
io_stmt ::= read_stmt | print_stmt
read_stmt ::= "eat😋" "🐖" ID "🐖"
print_stmt ::= "print🤮" ( expr | string_literal )
string_literal ::= "🥓" STRING_CONTENT "🥓"

Statements are either declarations, assignments, conditionals, loops, or function calls:
stmt ::= decl | assign | if_stmt | while_stmt | function_call | struct_init

Structure initialization:
struct_init ::= "😀" "🐖" ID "🐖" "🐖" ID "🐖" "@" "🐖" ID "🐖" "**" expr_list "**"
expr_list ::= expr { "**" "**" expr }*

Declaration: mutability, type, identifier wrapped in 🐖, and initializer expression. Variables are immutable by default unless 😀 is present:
decl ::= mutability type "🐖" ID "🐖" [ "@" ( expr | struct_init | lambda ) ]
mutability ::= "😀" | "😭"
type ::= "🐽" | "🐷" | "🐗" | "wow" | "🥩" | ID

Lambda expression: anonymous function with parameters and body:
lambda ::= "🥩" "**" lambda_params "**" "🥩" expr "🥩"
lambda_params ::= [ type "🐖" ID "🐖" { "**" "**" type "🐖" ID "🐖" }* ]

Assignment: identifier wrapped in 🐖, assignment operator, expression or member access:
assign ::= "🐖" ID "🐖" [ "_" "🐖" ID "🐖" ]* "@" expr

Function call with optional chaining:
function_call ::= "🐖" ID "🐖" [ "_" "🐖" ID "🐖" ] "**" [ expr { "**" "**" expr }* ] "**" [ "_" function_call ]*

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

Factor: the base units of expressions—numeric literals (NUMBER, e.g., "10"), identifiers (ID, e.g., "x"), booleans (LOVE/HATE), string literals, function calls, member access, lambda expressions, or parenthesized sub-expressions for grouping and overriding precedence:
factor ::= NUMBER | "🐖" ID "🐖" [ "_" "🐖" ID "🐖" ]* | "**" expr "**" | boolean | string_literal | function_call | lambda
boolean ::= "LOVE" | "HATE"
ID ::= LETTER { LETTER | "&" }*
NUMBER ::= [ "-" ] DIGIT { DIGIT }*
STRING_CONTENT ::= any characters except "🥓" or NEWLINE, with escape sequences \n, \t, \\

NEWLINE ::= "\n" | "\r\n"
```

---

## 📝 Example Programs

### String I/O Example: User Greeting

```piglang
# print🤮 🥓=============================🥓 #
# print🤮 🥓  Welcome to OINK Language! 🥓 #
# print🤮 🥓=============================🥓 #

# print🤮 🥓Enter your age:🥓 #
# 😀 🐷 🐖age🐖 #
# eat😋 🐖age🐖 #

# print🤮 🥓Your age is:🥓 #
# print🤮 🐖age🐖 #

# print🤮 🥓Thank you for using OINK!🥓 #

# ... 0 ... #
```

### Lambda Example: Function as First-Class Value

```piglang
# 😀 🥩 🐖square🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 💞 🐖x🐖 🥩 #
# 😀 🥩 🐖cube🐖 @ 🥩 ** 🐷 🐖n🐖 ** 🥩 🐖n🐖 💞 🐖n🐖 💞 🐖n🐖 🥩 #

# 😀 🐷 🐖val🐖 @ 5 #
# 😀 🐷 🐖squared🐖 @ 🐖square🐖 ** 🐖val🐖 ** #
# 😀 🐷 🐖cubed🐖 @ 🐖cube🐖 ** 🐖val🐖 ** #

# ... 🐖squared🐖 ❤️ 🐖cubed🐖 ... #
```

### Lambda Example: Mathematical Operations

```piglang
# 😀 🥩 🐖add🐖 @ 🥩 ** 🐷 🐖a🐖 ** ** 🐷 🐖b🐖 ** 🥩 🐖a🐖 ❤️ 🐖b🐖 🥩 #
# 😀 🥩 🐖multiply🐖 @ 🥩 ** 🐷 🐖x🐖 ** ** 🐷 🐖y🐖 ** 🥩 🐖x🐖 💞 🐖y🐖 🥩 #

# 😀 🐷 🐖sum🐖 @ 🐖add🐖 ** 10 ** ** 20 ** #
# 😀 🐷 🐖product🐖 @ 🐖multiply🐖 ** 🐖sum🐖 ** ** 2 ** #

# ... 🐖product🐖 ... #
```

### Function Example: Factorial Calculator

```piglang
# 🐷 PIG 🐖factorial🐖 ** 🐷 🐖n🐖 ** #
# 🐖🐖🐖 #
# SAVE 🐖n🐖 🌸< 2 #
# 🐖🐖🐖 #
# ... 1 ... #
# 🐖🐖🐖 #
# 😀 🐷 🐖result🐖 @ 🐖factorial🐖 ** ** 🐖n🐖 💔 1 ** ** #
# ... 🐖n🐖 💞 🐖result🐖 ... #
# 🐖🐖🐖 #

# 😀 🐷 🐖num🐖 @ 5 #
# 😀 🐷 🐖fact🐖 @ 🐖factorial🐖 ** 🐖num🐖 ** #

# ... 🐖fact🐖 ... #
```

### Structure Example: Point with Distance Calculation

```piglang
# BOAR 🐖Point🐖 #
# 🐖🐖🐖 #
# 😀 🐷 🐖x🐖 #
# 😀 🐷 🐖y🐖 #
# 🐷 PIGLET 🐖getX🐖 #
# 🐖🐖🐖 #
# ... 🐖x🐖 ... #
# 🐖🐖🐖 #
# 🐷 PIGLET 🐖setX🐖 ** 🐷 🐖newX🐖 ** #
# 🐖🐖🐖 #
# 🐖x🐖 @ 🐖newX🐖 #
# ... 0 ... #
# 🐖🐖🐖 #
# 🐖🐖🐖 #

# 😀 🐖Point🐖 🐖p🐖 @ 🐖Point🐖 ** 10 ** ** 20 ** #
# 😀 🐷 🐖coord🐖 @ 🐖p🐖 _ 🐖getX🐖 #
# print🤮 🐖coord🐖 #

# ... 0 ... #
```

### I/O Example: Interactive Calculator with Strings

```piglang
# print🤮 🥓=== Calculator ===🥓 #

# print🤮 🥓Enter first number:🥓 #
# 😀 🐷 🐖a🐖 #
# eat😋 🐖a🐖 #

# print🤮 🥓Enter second number:🥓 #
# 😀 🐷 🐖b🐖 #
# eat😋 🐖b🐖 #

# 😀 🐷 🐖sum🐖 @ 🐖a🐖 ❤️ 🐖b🐖 #

# print🤮 🥓Result:🥓 #
# print🤮 🐖sum🐖 #

# print🤮 🥓Thank you!🥓 #

# ... 🐖sum🐖 ... #
```

---

## 🔒 Safety Features

### Type overflow checking
All arithmetic operations automatically check for overflow/underflow.

### Immutability enforcement
Constants cannot be reassigned:
```piglang
# 😭 🐷 🐖constant🐖 @ 100 #
# 🐖constant🐖 @ 200 #  # Compile error: cannot assign to constant!
```

### No variable shadowing
Variables cannot be redeclared in any scope.

### Function parameter type checking
All function arguments are type-checked at compile time.

### Lambda type safety
Lambda parameters and return types are checked during compilation.

### Member access validation
Structure member access is validated to ensure fields and methods exist.

### Self-assignment
Self-assignment is explicitly forbidden in the OINK programming language. 
An assignment like `# 🐖x🐖 @ 🐖x🐖 #` (equivalent to x = x) will cause a compilation error.

### String validation
- Strings must be closed on the same line (no multi-line strings)
- Escape sequences are validated during lexing
- Unclosed strings result in compile-time errors

---

## 🎨 Style Guide

### Line Structure
- Each statement must be on its own line
- Lines start with `#` and end with `#`
- Mood lines are wrapped in `#~` and `~#` (instead of usual `#`)

### Variable Naming
- Use descriptive names: `🐖counter🐖`, `🐖total&sum🐖`
- Only letters and `&` in variable names can be used
- Always wrap your variable name in `🐖`

### Lambda Naming
- Use verb-based or descriptive names: `🐖transform🐖`, `🐖filter🐖`
- Lambda variables use `🥩` type marker
- Always wrap lambda names in `🐖`

### Function Naming
- Use verb-based names: `🐖calculate🐖`, `🐖getValue🐖`
- Keep names concise and descriptive
- Always wrap function names in `🐖`

### Structure Naming
- Use PascalCase-style: `🐖Point🐖`, `🐖Counter🐖`
- Keep names singular (not plural)
- Always wrap structure names in `🐖`

### String Usage
- Use strings for user prompts and messages
- Keep strings concise and clear
- Use escape sequences for formatting when needed

### Block Formatting
```piglang
# SAVE condition #
# 🐖🐖🐖 #
# statement1 #
# statement2 #
# 🐖🐖🐖 #
```

---

## 🤔 FAQ

**Why pig emojis?**  
*Answer*: BECAUSE I DECIDED TO CHOOSE PIGS AS A SOURCE OF INSPIRATION

**What's the bacon emoji (🥓) for?**  
*Answer*: Bacon comes from pigs! It's the perfect delimiter for string literals in our pig-themed language.

**What's the meat emoji (🥩) for?**  
*Answer*: It represents lambda expressions - meaty, compact functions! Just like how meat is a concentrated source of nutrition, lambdas are concentrated functions.

**What's the purpose of Mood Lines?**  
*Answer*: Mood Lines provide a unique way to write inverse logic without explicit negation operators, making certain patterns more concise.

**Can lambdas have multiple statements?**  
*Answer*: No! Lambdas in OINK can only have a single expression as their body. Use regular functions with `PIG` for multi-statement logic.

**Can I nest conditionals?**  
*Answer*: Yes! You can nest any control structures, but do not forget about placing them within 🐖🐖🐖 blocks.

**Is PigLang case-sensitive?**  
*Answer*: Yes, identifiers are case-sensitive. `🐖myVar🐖` and `🐖MyVar🐖` are different variables.

**Why `**` instead of `()`?**  
*Answer*: To maintain PigLang's unique visual identity!

**Can I shadow variables?**
*Answer*: No! PigLang does not allow variable shadowing. Once a variable is declared, it cannot be redeclared in any scope.

**Can I use numbers within a variable name?**
*Answer*: No! Your variable name must start with a letter (alpha) and then can be followed either by a letter or a `&` sign!

**Can structures inherit from other structures?**
*Answer*: No, PigLang does not support inheritance. Use composition instead!

**Do member functions have access to structure fields?**
*Answer*: Yes! Member functions declared with `PIGLET` can directly access all fields of the structure.

**What's the difference between `PIG` and `PIGLET`?**
*Answer*: `PIG` declares standalone functions, while `PIGLET` declares member functions within structures (BOAR blocks).

**Can I chain function calls?**
*Answer*: Yes! Use the `_` operator to chain functions. The result of each function becomes the first implicit parameter to the next function in the chain. For example: `🐖getValue🐖 _ 🐖double🐖 _ 🐖addTen🐖`

**Why `_` for member access?**
*Answer*: The underscore represents a pig's tail! It's a simple, clear character that fits our pig theme and makes chaining operations easy to read.

**Can lambdas access outer scope variables?**
*Answer*: Currently, lambdas can only access their parameters. Future versions may support closure.

**Can I store strings in variables?**
*Answer*: Currently, strings are literals only and cannot be stored in variables. They are used directly with `print🤮` for output.

**Can strings span multiple lines?**
*Answer*: No! Strings must be closed on the same line. Use `\n` escape sequence for newlines within strings.

---

## 🎉 HAVE FUN CODING (OR NOT), MY LOVELY FRIENDS!

**Remember:**
- Wrap your variables in 🐖
- Enclose blocks with 🐖🐖🐖
- Use `LOVE` and `HATE` for booleans
- Try *Mood Lines* for inverted logic
- Use `🥩` for lambda expressions - meaty functions!
- Use `🥓` for string literals - bacon delimiters!
- Every program must return something!
- No variable shadowing allowed!
- Use `hru` for AND and `bruh` for OR
- Declare functions with `PIG`, member functions with `PIGLET`
- Create structures with `BOAR`
- Use `_` for member access (pig tail!)
- Chain function calls with `_`
- Read with `eat😋`, print with `print🤮`
- Strings support escape sequences: `\n`, `\t`, `\\`

Happy *OINK* coding! 🐷🥩🥓✨

---

## 📦 HOW TO RUN IT???

First of all, you should run some tests and verify that everything is working. 
In order to do this, you must run these commands... (but verify that you are not inside the *compiler* directory, you must be at the root level)

```bash
chmod +x tests.sh
./tests.sh
```
NOTE: this checks the work of syntax parser and lexer

... and then these:

```bash
chmod +x full_compiler.sh
./full_compiler.sh
```

NOTE: this checks the overall compiler work:)

NOW YOU CAN WRITE YOUR OWN MASTERPIECE WITH OINK LANGUAGE. HOW?

1) Place your perfect **OINK code** in a file with a **txt** extension.
2) Locate it somewhere but keep in mind the location!
3) Go to the folder where **compiler.py** file resides.
4) Ensure that you are in the same location as the **compiler.py**.
5) Run this command, specifying the path to your OINK code file location:

```bash
    python3 -m compiler <YOUR_CODE_LOCATION> ./llm/<YOUR_DESIRED_FILE_NAME>.ll
    llc -filetype=obj -relocation-model=pic ./llm/<YOUR_DESIRED_FILE_NAME>.ll -o ./obj/<YOUR_DESIRED_FILE_NAME>.o
    clang -fPIE ./obj/<YOUR_DESIRED_FILE_NAME>.o -o ./exe/<YOUR_DESIRED_FILE_NAME>
    ./exe/<YOUR_DESIRED_FILE_NAME>
```

# ENJOY🐖🐖🐖