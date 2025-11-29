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
- **String interpolation** with drumstick emoji 🍗 for embedding expressions
- **Powerful optimizations** including dead code elimination, function inlining, and unused function removal

## ✨ Key Features

### 🥓 String Literals
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

### 🍗 String Interpolation
Embed expressions directly into strings using the drumstick emoji for dynamic, formatted output:

```piglang
# 😀 🐷 🐖x🐖 @ 10 #
# print🤮 🥓Value: 🍗🐖x🐖🍗🥓 #
```

**Interpolation Syntax:**
- Wrap expressions in `🍗` (drumstick emoji) markers
- Can embed variables, arithmetic expressions, and any valid expression
- Format: `🥓text 🍗expression🍗 more text🥓`
- Expressions are automatically evaluated and converted to strings

**Interpolation Examples:**
```piglang
# Simple variable interpolation
# 😀 🐷 🐖age🐖 @ 25 #
# print🤮 🥓Your age is: 🍗🐖age🐖🍗\n🥓 #

# Multiple values in one string
# 😀 🐷 🐖a🐖 @ 5 #
# 😀 🐷 🐖b🐖 @ 3 #
# print🤮 🥓Sum: 🍗🐖a🐖🍗 + 🍗🐖b🐖🍗 = 🍗🐖a🐖 ❤️ 🐖b🐖🍗\n🥓 #

# Expression interpolation
# 😀 🐷 🐖x🐖 @ 7 #
# 😀 🐷 🐖y🐖 @ 2 #
# print🤮 🥓Result: 🍗🐖x🐖 💞 🐖y🐖🍗\n🥓 #

# Complex expressions with labels
# print🤮 🥓Temperature: 🍗🐖celsius🐖🍗 C = 🍗🐖fahrenheit🐖🍗 F\n🥓 #
```

**Supported Types in Interpolation:**
- `🐽` (i16) - 16-bit integers
- `🐷` (i32) - 32-bit integers  
- `🐗` (i64) - 64-bit integers
- `wow` (Boolean) - Automatically converted to integers (1 for LOVE, 0 for HATE)
- Arithmetic expressions (e.g., `🍗🐖a🐖 ❤️ 🐖b🐖🍗`)
- Variable references

**Interpolation Features:**
- Multiple interpolations in a single string
- Automatic type conversion for output
- Escape sequences work alongside interpolation
- Clean, readable output formatting

**Important Notes:**
- Avoid non-ASCII special characters (like °, €, etc.) in string literals as they may cause compilation issues
- Use basic ASCII characters and standard escape sequences for best compatibility
- Interpolated strings are designed for `print🤮` output

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
- `print🤮` - Print output to console (supports integers, strings, and interpolated strings)

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
| `🍗` | String Interpolation | Expression marker within strings                | N/A            |

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
🥩 ** type 🐖param🐖 ** ** type 🐖param🐖 ** 🥩 expression 🥩
```

**Features:**
- Declared with `😀 🥩` mutability marker and type
- Parameters wrapped in `** **` brackets
- Body is a single expression
- Must be initialized at declaration

**Usage:**
```piglang
# Lambda declaration
# 😀 🥩 🐖double🐖 @ 🥩 ** 🐷 🐖x🐖 ** 🥩 🐖x🐖 💞 2 🥩 #

# Lambda call
# 😀 🐷 🐖result🐖 @ 🐖double🐖 ** 10 ** #
# ... 🐖result🐖 ... #  # Returns 20
```

### Input/Output

#### Read Input: `eat😋`
Reads numeric input from the user.

**Supported types:** i16 (🐽), i32 (🐷), i64 (🐗)

```piglang
# 😀 🐷 🐖input_value🐖 #
# eat😋 🐖input_value🐖 #
```

#### Print Output: `print🤮`
Prints values to console (supports integers, string literals, and interpolated strings).

**Supported types:** i16 (🐽), i32 (🐷), i64 (🐗), string literals (🥓), interpolated strings (🥓...🍗...🥓)

```piglang
# Print integer value
# print🤮 🐖value🐖 #

# Print expression result
# print🤮 ** 🐖x🐖 ❤️ 🐖y🐖 ** #

# Print string literal
# print🤮 🥓Hello, World!🥓 #

# Print interpolated string
# print🤮 🥓Result: 🍗🐖value🐖🍗\n🥓 #
```

### Operator Precedence (High to Low)

1. `🌳` ... `🌳` (grouping)
2. `💩` (unary NOT)
3. `💞`, `💕` (multiplication, division)
4. `❤️`, `💔` (addition, subtraction)
5. `>`, `<`, `🌸>`, `🌸<`, `🌸🌸`, `💩🌸` (comparison)
6. `hru` (logical AND)
7. `bruh` (logical OR)

---

## 🚀 Compiler Pipeline

The OINK compiler processes your code through multiple stages:

1. **Lexer**: Tokenizes source code into tokens
2. **Parser**: Builds an Abstract Syntax Tree (AST) from tokens
3. **Semantic Analyzer**: Validates types, scopes, and semantics
4. **Optimizer**: Applies multiple optimization passes
5. **Code Generator**: Produces LLVM IR code

### Optimization Passes

The optimizer performs three main optimizations:

#### 1. Dead Variable Elimination
Removes unused variables iteratively until no more can be removed (max 100 iterations):
- Identifies variables that are declared but never used
- Removes their declarations from the AST
- Reports number of variables removed

#### 2. Function Inlining
Inlines functions that are called exactly once:
- Identifies single-use functions
- Replaces function calls with function body
- Handles parameter substitution
- Reports number of functions inlined

#### 3. Unused Function Removal
Removes functions that are never called:
- Identifies functions with zero call sites
- Removes function declarations from AST
- Reports number of functions removed

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
print_stmt ::= "print🤮" ( expr | string_literal | interpolated_string )
string_literal ::= "🥓" STRING_CONTENT "🥓"
interpolated_string ::= "🥓" ( STRING_CONTENT | interpolation )* "🥓"
interpolation ::= "🍗" expr "🍗"

Statements are either declarations, assignments, conditionals, loops, or function calls:
stmt ::= decl | assign | if_stmt | while_stmt | function_call | struct_init

Structure initialization:
struct_init ::= "😀" "🐖" ID "🐖" "🐖" ID "🐖" "@" "🐖" ID "🐖" "**" expr_list "**"
expr_list ::= expr { "**" "**" expr }*

Declaration: mutability, type, identifier wrapped in 🐖, and initializer expression.
Variables are immutable by default unless 😀 is present:
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

Factor: the base units of expressions—numeric literals (NUMBER, e.g., "10"), identifiers (ID, e.g., "x"), booleans (LOVE/HATE), string literals, interpolated strings, function calls, member access, lambda expressions, or parenthesized sub-expressions for grouping and overriding precedence:
factor ::= NUMBER | "🐖" ID "🐖" [ "_" "🐖" ID "🐖" ]* | "🌳" expr "🌳" | ...
 "**" | boolean | string_literal | interpolated_string | function_call | lambda
boolean ::= "LOVE" | "HATE"
ID ::= LETTER { LETTER | "&" }*
NUMBER ::= [ "-" ] DIGIT { DIGIT }*
STRING_CONTENT ::= any characters except "🥓", "🍗", or NEWLINE, with escape sequences \n, \t, \\

NEWLINE ::= "\n" | "\r\n"

```

## Key Syntax Notes

All examples above demonstrate:
- **Expression grouping** with `🌳` (e.g., `🌳 🐖x🐖 ❤️ 🐖y🐖 🌳`)
- **Function arguments** with `**` (e.g., `** 🐷 🐖param🐖 **`)
- **String literals** with `🥓` and escape sequences (`\n`, `\t`)
- **String interpolation** with `🍗` for embedding expressions
- **Structures** with member functions
- **Lambda expressions** as first-class values

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
- Interpolation markers must be properly paired within strings

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
- Use string interpolation for dynamic values and formatted output
- Avoid non-ASCII special characters in strings (use ASCII equivalents)

### Block Formatting
```piglang
# SAVE condition #
# 🐖🐖🐖 #
# statement1 #
# statement2 #
# 🐖🐖🐖 #
```

---

## 📝 Example Programs

Complete example programs demonstrating all OINK features can be found in the `programs/` directory:

- **user_greeting.txt** - Simple user input/output with string interpolation
- **calculator.txt** - Basic arithmetic with formatted output
- **factorial.txt** - Recursive function example
- **lambda_math.txt** - Lambda expressions for math operations
- **lambda_square_cube.txt** - Multiple lambda functions
- **point_struct.txt** - Structure with member functions
- **temperature_converter.txt** - Full-featured app with validation, structures, lambdas, and string interpolation
- **bmi_calculator.txt** - BMI calculation with input validation and categorization
- **garden_calculator.txt** - Complex calculations with structures and pricing

All programs include:
- Input validation where applicable
- String interpolation for clear output
- Functions and/or lambdas for logic
- Structures for data organization
- Professional formatting

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

... and then you can launch already ready-for-use programs (note some of them require interaction -> your input):
* you can launch them all at once -> they will go one after another:
```bash
    chmod +x programs.sh
    ./programs.sh
```
* or launch only one (some) of your free choice:
```bash
    python3 -m compiler ./programs/<YOUR_CHOICE_PROGRAM_TXT> ./programs/llm/<YOUR_CHOICE_PROGRAM_TXT>.ll
    llc -filetype=obj -relocation-model=pic ./programs/llm/<YOUR_CHOICE_PROGRAM_TXT>.ll -o ./programs/obj/<YOUR_CHOICE_PROGRAM_TXT>.o
    clang -fPIE ./programs/obj/<YOUR_CHOICE_PROGRAM_TXT>.o -o ./programs/exe/<YOUR_CHOICE_PROGRAM_TXT>
    ./exe/<YOUR_CHOICE_PROGRAM_TXT>
```
NOTE: this checks the overall compiler work with optimizations:)

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

The compiler will output optimization statistics:
- Variables removed: Number of unused variables eliminated
- Functions inlined: Number of single-use functions inlined
- Functions removed: Number of unused functions eliminated

---

## 🤔 FAQ

**Why pig emojis?**  
*Answer*: BECAUSE I DECIDED TO CHOOSE PIGS AS A SOURCE OF INSPIRATION

**What's the bacon emoji (🥓) for?**  
*Answer*: Bacon comes from pigs! It's the perfect delimiter for string literals in our pig-themed language.

**What's the drumstick emoji (🍗) for?**  
*Answer*: String interpolation! It lets you embed expressions directly into strings for dynamic, formatted output. Just like how a drumstick is meaty and flavorful, interpolation adds substance to your strings!

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
*Answer*: No! Variable shadowing is strictly forbidden in OINK. Every variable must have a unique name within the entire program scope.

**What optimizations does the compiler perform?**  
*Answer*: The OINK compiler performs dead variable elimination, function inlining for single-use functions, and unused function removal. These optimizations run automatically during compilation.

**How does function inlining work?**  
*Answer*: Functions that are called exactly once are automatically inlined - their body replaces the call site. This reduces function call overhead and can enable further optimizations.

**Can I disable optimizations?**  
*Answer*: No, optimizations are always enabled and are an integral part of the compilation process.

**Can I use special characters (like °, €, etc.) in strings?**  
*Answer*: It's recommended to avoid non-ASCII special characters in string literals as they may cause compilation issues. Use ASCII equivalents or describe them in words instead (e.g., "degrees C" instead of "°C").

**How many expressions can I interpolate in one string?**  
*Answer*: You can interpolate as many expressions as you need! Each expression is wrapped in `🍗` markers and evaluated independently.

**Can I interpolate structure values?**  
*Answer*: No, string interpolation only supports primitive types (i16, i32, i64) and boolean values. For structures, access their fields first and then interpolate those values.

---

## 🐷 Quick Reference

- Use `🥓` for string literals - bacon delimiters!
- Use `🍗` for string interpolation - embed expressions in strings!
- Use `🥩` for lambda expressions - meaty functions!
- Every program must return something!
- No variable shadowing allowed!
- Use `hru` for AND and `bruh` for OR
- Declare functions with `PIG`, member functions with `PIGLET`
- Create structures with `BOAR`
- Use `_` for member access (pig tail!)
- Chain function calls with `_`
- Read with `eat😋`, print with `print🤮`
- Strings support escape sequences: `\n`, `\t`, `\\`
- Interpolation works with all primitive numeric types and booleans
- Avoid non-ASCII characters in strings for best compatibility
- Compiler optimizations automatically improve your code!

Happy *OINK* coding! 🐷🥩🥓🍗✨

# ENJOY🐖🐖🐖