MAL IDE v2.0

An Integrated Development Environment (IDE) for the MAL programming language with advanced debugging support


Introduction

MAL IDE is a code editor + interpreter + debugger for the MAL language. With this tool, you can write, execute, and debug MAL code line by line.


Features

- Syntax highlighting (keywords, strings, comments, and numbers)
- Full debugging (breakpoints, step over/into/out)
- Real-time variable display during execution
- Call stack viewer
- Mix MAL and Python code in one file
- Light and dark themes
- File management (open, save, new)
- Built-in APIs for file, system, directory, and random operations


Installation and Execution

Prerequisites:
- Python 3.7 or higher

Run:
python MAL2.py

Note: No additional libraries are needed. Python is all you need.


Quick Start

1. Run the program
2. Write the following code in the editor:

using MAL
let name = "World"

function sayHello(person) {
    print "Hello " + person
}

sayHello(name)

3. Press F5 or click the Run button
4. View the result in the output panel


MAL Language Guide

Variables:
let x = 10
let name = "Ali"
let numbers = list(1, 2, 3)
let isOk = true

Functions:
function add(a, b) {
    return a + b
}

let result = add(5, 3)
print result

Conditionals:
let age = 20

if (age < 18) {
    print "Child"
} elif (age < 60) {
    print "Adult"
} else {
    print "Senior"
}

Loops:
# Numeric for loop
for i from 1 to 5 {
    print i
}

# Iterable for loop
let items = list("a", "b", "c")
for item from items {
    print item
}



Built-in APIs

sys - System information:
print sys.os        # Operating system information
print sys.cpu       # CPU information
print sys.time      # Date and time
print sys.memory()  # Memory status

file - File operations:
file.write("test.txt", "My content")
let content = file.read("test.txt")
file.append("test.txt", "More content")
file.copy("src.txt", "dst.txt")
file.delete("test.txt")

dir - Directory operations:
dir.create("myfolder")
dir.list(".")        # List files
dir.tree(".", 2)     # Directory tree
dir.change("/home")  # Change path

random - Random operations:
random.number(1, 100)        # Random number
random.choice(list(1,2,3))   # Random choice
random.boolean()             # True or False
random.rgb()                 # Random RGB color


Debugging Tools

Buttons:
🐛 Debug        : Toggle debug mode
🔴 Breakpoint   : Set breakpoint at current line (or press F9)
⏭ Step Over    : Execute next line (without entering functions)
⏬ Step Into    : Enter function
⏫ Step Out     : Exit function
▶ Continue      : Continue until next breakpoint
⏹ Stop         : Stop execution

Debug commands in code:
debug breakpoint 10   # Breakpoint at line 10
debug step            # Activate step mode
debug continue        # Continue execution
debug vars            # Show variables
debug stack           # Show call stack


Keyboard Shortcuts

F5          : Run code
F9          : Toggle breakpoint
F6          : Stop execution
F1          : Help
Ctrl+N      : New file
Ctrl+O      : Open file
Ctrl+S      : Save file
Ctrl+Z      : Undo
Ctrl+Y      : Redo
Ctrl+C      : Copy
Ctrl+V      : Paste
Ctrl+A      : Select all


File Structure

mal-ide/
│
├── MAL2.py          # Main program file
└── README.md        # This file (documentation)


License

This project is released under the MIT License.

MIT License

Copyright (c) 2024 Milad Moradpour

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Developer

Milad Moradpour
GitHub: @yourusername
Email: your-email@example.com


Happy Coding!!