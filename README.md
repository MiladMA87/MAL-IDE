# MAL IDE

### A lightweight IDE and interpreter for the MAL programming language

**MAL IDE** is a Python-based development environment built for the **MAL programming language**.

It brings together a custom interpreter, code editor, debugger, syntax highlighting, file management, built-in APIs, and Python integration in a single desktop application.

The project was created as an exploration of **programming language design, interpreter development, debugging systems, and desktop application development**.

---

## ✨ Features

### 🧠 MAL Interpreter

MAL includes a custom interpreter implemented in Python.

The language supports:

* Variables
* Expressions and operators
* Functions
* Return values
* `if / elif / else`
* `while` loops
* `for` loops
* `break` and `continue`
* Lists
* Dictionaries
* Tuples
* Sets
* User input
* Built-in functions
* Comments

Example:

```mal
let numbers = list(1, 2, 3, 4, 5)
let total = 0

for number from numbers {
    total = total + number
}

print total
```

---

## 🛠️ Integrated Development Environment

MAL IDE provides a desktop editor for writing and running MAL programs.

### Editor

* Syntax highlighting
* Line numbers
* Automatic indentation
* Undo / Redo
* Clipboard operations
* Current line and column indicator
* Font customization
* Light and dark themes
* File creation and editing
* Save and open functionality

The editor is designed to keep the development workflow inside a single application instead of requiring a separate editor and interpreter.

---

## 🐞 Debugger

MAL IDE includes an integrated debugger for inspecting program execution.

### Debugging capabilities

* Breakpoints
* Step Over
* Step Into
* Step Out
* Continue execution
* Stop execution
* Current-line highlighting
* Variable inspection
* Call stack inspection
* Debug status information
* Interactive input handling

Breakpoints can also be managed directly from the editor.

### Debug Commands

MAL provides debugging commands such as:

```mal
debug breakpoint 10
debug step
debug continue
debug stop
debug vars
debug stack
```

This allows debugging to be controlled both through the IDE interface and from the MAL runtime.

---

# 🧩 Built-in APIs

MAL provides several built-in APIs that extend the language beyond basic computation.

## System API

The `sys` API exposes information about the environment in which MAL is running.

Example:

```mal
print sys.os
print sys.cpu
print sys.python
print sys.path
print sys.time()
print sys.memory()
```

It provides access to information such as:

* Operating system
* OS version
* Platform
* CPU information
* Current working directory
* Home directory
* Python version
* Current time
* Memory information

---

## File API

The `file` API provides file-system operations directly from MAL.

Example:

```mal
file.create("example.txt", "Hello MAL")

file.append("example.txt", "\nWelcome!")

let content = file.read("example.txt")

print content
```

Supported operations include:

* Create
* Read
* Read lines
* Write
* Append
* Copy
* Move
* Rename
* Delete
* Existence checking
* File size
* File information
* JSON reading
* JSON writing

---

## Directory API

The `dir` API provides directory-management functionality.

```mal
dir.create("data")

let files = dir.list(".")
print files

dir.change("data")
```

Operations include:

* Create directories
* Delete directories
* List directory contents
* Change working directory
* Check existence
* Copy directories
* Move directories
* Generate directory trees

---

## Random API

MAL also includes utilities for generating random values.

```mal
let number = random.number(1, 100)
let item = random.choice(list("A", "B", "C"))
let flag = random.boolean()

print number
print item
print flag
```

Additional functionality includes:

* Random numbers
* Random choices
* Boolean values
* List shuffling
* RGB generation

---

# 🐍 Python Integration

One of the features of MAL IDE is the ability to combine **MAL and Python code inside the same source file**.

A source file can switch between the two environments using:

```text
using MAL
```

and:

```text
using PYTHON
```

Example:

```text
using MAL

let x = 10
print x

using PYTHON

print("Hello from Python")

using MAL

let y = 20
print y
```

This allows Python to be used alongside MAL when functionality is easier to implement or access directly through Python.

Python sections are executed through Python's runtime and their output is integrated into the IDE's output system.

---

# 📚 MAL Language Examples

## Variables

MAL supports multiple variable-assignment forms:

```mal
let name = "MAL"
let version = 2
var counter = 0
set result = version + counter
```

---

## Conditions

```mal
let score = 85

if score >= 90 {
    print "Excellent"
} elif score >= 60 {
    print "Passed"
} else {
    print "Failed"
}
```

---

## Functions

```mal
function greet(name) {
    print "Hello"
    print name
}

greet("MAL")
```

---

## Loops

### While

```mal
let i = 0

while i < 5 {
    print i
    i = i + 1
}
```

### For

```mal
for i from 1 to 5 {
    print i
}
```

### Iterating over collections

```mal
let languages = list("MAL", "Python", "C++")

for language from languages {
    print language
}
```

---

# ⌨️ Keyboard Shortcuts

| Shortcut   | Action            |
| ---------- | ----------------- |
| `F5`       | Run               |
| `F6`       | Stop              |
| `F9`       | Toggle breakpoint |
| `F1`       | Open MAL help     |
| `Ctrl + N` | New file          |
| `Ctrl + O` | Open file         |
| `Ctrl + S` | Save              |
| `Ctrl + Z` | Undo              |
| `Ctrl + Y` | Redo              |
| `Ctrl + C` | Copy              |
| `Ctrl + V` | Paste             |
| `Ctrl + A` | Select all        |

---

# 🚀 Installation

## Requirements

* Python **3.7+**
* Tkinter
* NumPy

Tkinter is included with most standard Python installations.
On some Linux distributions, it may need to be installed separately.

### Install NumPy

```bash
pip install numpy
```

---

## Running MAL IDE

Clone the repository:

```bash
git clone https://github.com/MiladMA87/MAL-IDE.git
```

Enter the project directory:

```bash
cd MAL-IDE
```

Run the IDE:

```bash
python MAL.py
```

---

# 📁 Project Structure

```text
MAL-IDE/
│
├── MAL.py
├── Note.txt
├── README.md
├── LICENSE
└── .gitignore
```

The main implementation is currently contained in:

```text
MAL.py
```

This file contains the core components of the project, including the interpreter, IDE interface, debugger, APIs, editor functionality, and Python integration.

---

# 🧱 Technology Stack

MAL IDE is primarily built using:

| Technology                  | Purpose                           |
| --------------------------- | --------------------------------- |
| **Python**                  | Core implementation               |
| **Tkinter**                 | Desktop user interface            |
| **NumPy**                   | Numerical functionality           |
| **AST**                     | Expression parsing and evaluation |
| **Python Standard Library** | Runtime and system functionality  |

---

# 🎯 Project Goals

MAL IDE is primarily an experimental and educational project focused on exploring how a programming language and its development environment can be designed from the ground up.

The project explores several areas:

* Programming language design
* Lexing and parsing
* Expression evaluation
* Interpreter architecture
* Runtime APIs
* Debugger implementation
* Source-code editing
* Python integration
* Desktop GUI development

Rather than attempting to replace established development environments, MAL IDE focuses on understanding and experimenting with the components that make a programming language and its IDE work together.

---

# 📌 Current Status

MAL IDE is an actively evolving personal project.

The current implementation already provides a functional environment for writing, executing, and debugging MAL programs, while several parts of the language and IDE architecture remain open to further development.

Potential future improvements include:

* Expanded language syntax
* More advanced debugging capabilities
* Improved error reporting
* Additional standard libraries
* Better code completion
* Improved project management
* More extensive documentation
* A more modular interpreter architecture

---

# 🤝 Contributing

MAL IDE is currently maintained as a personal project.

Ideas, bug reports, and technical discussions are welcome through the repository's GitHub issues and discussions.

---

# 📄 License

This project is distributed under the **MIT License**.

See [`LICENSE`](LICENSE) for the complete license text.

---

# 👤 Author

**Milad Moradpour**

GitHub: [@MiladMA87](https://github.com/MiladMA87)

---

<div align="center">

### MAL IDE

*A programming language experiment evolving into a development environment.*

</div>
