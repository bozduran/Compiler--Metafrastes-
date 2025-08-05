# Compiler (Μετφραστές)
# Simple Compiler for Custom Language (`met.py`)

This project implements a basic compiler front-end for a custom programming language. The compiler performs **lexical analysis**, **syntax parsing**, **semantic checks**, and generates **intermediate code**, **C code**, and **assembly-like pseudocode**.

## 🧠 Features

- **Lexical Analysis**: Tokenizes keywords, identifiers, numbers, operators, and handles comments.
- **Syntax Parsing**: Uses recursive descent parsing for custom language constructs (e.g., `if`, `while`, `function`, `loop`, `forcase`, `incase`, etc.).
- **Semantic Analysis**: 
  - Scope management with nested blocks
  - Symbol table with offset tracking
  - Function return validation
  - Argument type/mode checks
- **Intermediate Code Generation**: Generates 4-tuples (quadruples).
- **C Code Generation**: Converts intermediate code into readable `.c` code.
- **Assembly-like Code Generation**: Translates to MIPS-style pseudocode.

## 🛠 Tech Stack

- Python 3
- Custom language parser and code generator

---

## 📁 Output Files

Given an input file named `example.stl`, the compiler will generate:

| File           | Description                              |
|----------------|------------------------------------------|
| `example.int`  | Intermediate code (quadruples)           |
| `example.c`    | Equivalent C code                        |
| `example.asm`  | Assembly-style pseudocode (MIPS-like)    |

---

## ▶️ How to Use

1. **Install Python** (version 3.x recommended)

2. **Prepare a source file** in the custom language, e.g., `program.stl`.

3. **Run the compiler:**

```bash
python met.py program.stl
```

4. **On success**, you will see:

```
Succesfull compile
```

5. **Check generated files:**
   - `program.int`
   - `program.c`
   - `program.asm`

---

## 🧾 Supported Language Syntax (Partial)

- `program` / `endprogram`
- `declare var1, var2;`
- `function fname (in a, inout b)`
- `if (...) then ... endif`
- `while (...) ... endwhile`
- `dowhile ... enddowhile`
- `loop ... endloop`
- `forcase`, `incase`, `when`, `default`, etc.
- `input x;`, `print x;`
- `return x;`
- Expressions with `+`, `-`, `*`, `/`

---

## ⚙️ Internals

### Main Components:

| File      | Purpose                                        |
|-----------|------------------------------------------------|
| `met.py`  | Main compiler logic (lexer, parser, generator) |

### Classes:

- `Scope`: Handles nested scopes and variable tracking.
- `Entity`: Represents variables and functions.
- `Argument`: Stores function parameter details.
- `NewQuad`: Structure for intermediate code.

## 📜 License

This project is open source and free to use under the MIT License.

---

## 👨‍💻 Author

- **MPOZ NTOYRAN** (cs122310)
- **ALEXANDROPOULOS DIMITRIOS** (cse52928)

---
