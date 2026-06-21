import re
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog, filedialog
import io
import contextlib
import numpy as np
import os
import platform
import ast
import math
from datetime import datetime
import json
import random
import time
from collections import deque

# ==================== Random APIs ====================
class RandomAPI:
    """
    Provides random number generation and selection utilities.
    """
    def number(self, a=None, b=None):
        if a is not None and b is not None:
            return random.randint(a, b)
        elif a is not None and b is None:
            return random.randint(0, a)
        else:
            return random.randint(0, 1000000000)
    
    def choice(self, items):
        return random.choice(items)
    
    def shuffle(self, items):
        random.shuffle(items)
        return items
    
    def boolean(self):
        return random.choice(np.array([True, False]))
    
    def bool(self):
        return random.choice(np.array([True, False]))
    
    def rgb(self, r=None, g=None, b=None):
        def rand():
            return random.randint(0, 255)

        if r is None:
            r = rand()
        if g is None:
            g = rand()
        if b is None:
            b = rand()

        return np.array([r, g, b])
         
    
# ==================== System APIs ====================
class SysAPI:
    """
    Provides system information and utilities.
    """
    @property
    def os(self):
        return {
            "name": platform.system(),
            "version": platform.version(),
            "platform": platform.platform(),
            "release": platform.release(),
            "machine": platform.machine()
        }

    @property
    def cpu(self):
        return {
            "count": os.cpu_count(),
            "arch": platform.architecture()[0],
            "processor": platform.processor()
        }

    @property
    def path(self):
        return {
            "cwd": os.getcwd(),
            "home": os.path.expanduser("~"),
            "sep": os.path.sep
        }
    
    @property
    def python(self):
        return {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "compiler": platform.python_compiler()
        }
    
    def memory(self):
        """
        Returns memory usage statistics.
        """
        try:
            if platform.system() == "Windows":
                import ctypes
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)
                    ]
                
                memory_status = MEMORYSTATUSEX()
                memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status))
                
                return {
                    "total": memory_status.ullTotalPhys,
                    "available": memory_status.ullAvailPhys,
                    "percent": memory_status.dwMemoryLoad
                }
            else:
                try:
                    with open('/proc/meminfo', 'r') as f:
                        meminfo = f.read()
                        total = int(re.search(r'MemTotal:\s+(\d+)', meminfo).group(1)) * 1024
                        free = int(re.search(r'MemFree:\s+(\d+)', meminfo).group(1)) * 1024
                        return {
                            "total": total,
                            "available": free,
                            "percent": ((total - free) / total) * 100
                        }
                except:
                    return {"total": "N/A", "available": "N/A", "percent": "N/A"}
        except:
            return {"total": "N/A", "available": "N/A", "percent": "N/A"}
    
    def time(self):
        """
        Returns current date and time information.
        """
        now = datetime.now()
        return {
            "year": now.year,
            "month": now.month,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute,
            "second": now.second,
            "timestamp": now.timestamp()
        }


# ==================== File API ====================
class FileAPI:
    """
    Provides file operations such as read, write, copy, delete, etc.
    """
    def create(self, path, content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    
    def write(self, path, text, mode="w"):
        with open(path, mode, encoding="utf-8") as f:
            f.write(str(text))
        return True
    
    def append(self, path, text):
        return self.write(path, text, "a")
    
    def read(self, path, mode="r"):
        with open(path, mode, encoding="utf-8") as f:
            return f.read()
    
    def readlines(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    
    def exists(self, path):
        return os.path.exists(path)
    
    def rename(self, old, new):
        os.rename(old, new)
        return True
    
    def delete(self, path):
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
    
    def copy(self, src, dst):
        import shutil
        shutil.copy2(src, dst)
        return True
    
    def move(self, src, dst):
        import shutil
        shutil.move(src, dst)
        return True
    
    def size(self, path):
        return os.path.getsize(path)
    
    def info(self, path):
        if not os.path.exists(path):
            return None
        
        stat = os.stat(path)
        return {
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            "is_dir": os.path.isdir(path),
            "is_file": os.path.isfile(path)
        }
    
    def json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def write_json(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True


# ==================== Directory API ====================
class DirAPI:
    """
    Provides directory operations such as create, delete, list, tree, etc.
    """
    def create(self, path, exist_ok=True):
        os.makedirs(path, exist_ok=exist_ok)
        return True
    
    def delete(self, path, recursive=False):
        if recursive:
            import shutil
            shutil.rmtree(path)
        else:
            os.rmdir(path)
        return True
    
    def list(self, path=".", details=False):
        items = os.listdir(path)
        if not details:
            return items
        
        result = []
        for item in items:
            item_path = os.path.join(path, item)
            stat = os.stat(item_path)
            result.append({
                "name": item,
                "is_dir": os.path.isdir(item_path),
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime)
            })
        return result
    
    def change(self, path):
        os.chdir(path)
        return True
    
    def exists(self, path):
        return os.path.exists(path)
    
    def copy(self, src, dst):
        import shutil
        shutil.copytree(src, dst)
        return True
    
    def move(self, src, dst):
        import shutil
        shutil.move(src, dst)
        return True
    
    def tree(self, path=".", level=0, max_level=3):
        """
        Returns a directory tree structure as a list of strings.
        """
        if level > max_level:
            return []
        
        result = []
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                prefix = "│   " * level + "├── " if level > 0 else ""
                
                if os.path.isdir(item_path):
                    result.append(f"{prefix}{item}/")
                    result.extend(self.tree(item_path, level + 1, max_level))
                else:
                    result.append(f"{prefix}{item}")
        except PermissionError:
            result.append("│   " * level + "└── [Permission Denied]")
        
        return result


# ==================== Debugger Class ====================
class Debugger:
    """
    Manages debugging features: breakpoints, step mode, call stack, and execution pause.
    """
    def __init__(self, mal_instance):
        self.mal = mal_instance
        self.breakpoints = set()
        self.step_mode = False
        self.current_line = 0
        self.call_stack = []
        self.history = deque(maxlen=100)
        self.is_paused = False
        self.pause_callback = None
        self.step_into_function = False
        self.step_out_function = False
        self.function_depth = 0
        
    def add_breakpoint(self, line_number):
        self.breakpoints.add(line_number)
        return True
    
    def remove_breakpoint(self, line_number):
        if line_number in self.breakpoints:
            self.breakpoints.remove(line_number)
            return True
        return False
    
    def toggle_breakpoint(self, line_number):
        if line_number in self.breakpoints:
            self.breakpoints.remove(line_number)
            return False
        else:
            self.breakpoints.add(line_number)
            return True
    
    def should_pause(self, line_number, is_function_call=False):
        if self.step_mode:
            if is_function_call and self.step_into_function:
                return True
            if line_number > self.current_line:
                return True
            return False
        
        if line_number in self.breakpoints:
            return True
        
        return False
    
    def step_into(self):
        self.step_mode = True
        self.step_into_function = True
        self.step_out_function = False
        self.is_paused = False
        
    def step_over(self):
        self.step_mode = True
        self.step_into_function = False
        self.step_out_function = False
        self.is_paused = False
        
    def step_out(self):
        self.step_mode = True
        self.step_into_function = False
        self.step_out_function = True
        self.is_paused = False
        
    def continue_execution(self):
        self.step_mode = False
        self.step_into_function = False
        self.step_out_function = False
        self.is_paused = False
    
    def stop_execution(self):
        self.step_mode = False
        self.is_paused = False
        self.mal.execution_stopped = True
    
    def pause_at_line(self, line_number):
        self.current_line = line_number
        self.is_paused = True
        
        self.history.append({
            'line': line_number,
            'vars': dict(self.mal.vars),
            'stack': list(self.call_stack)
        })
        
        if self.pause_callback:
            self.pause_callback(line_number, self.mal.vars, self.call_stack)
        
        while self.is_paused:
            time.sleep(0.01)
            if self.mal.execution_stopped:
                break
    
    def set_pause_callback(self, callback):
        self.pause_callback = callback
    
    def get_current_vars(self):
        return dict(self.mal.vars)
    
    def get_stack(self):
        return list(self.call_stack)


# ==================== MAL Language Core ====================
class MAL:
    """
    Core interpreter for the MAL scripting language.
    Supports variables, functions, conditionals, loops, file I/O, and debugging.
    """
    def __init__(self, root=None, debug=False):
        self.vars = {}
        self.functions = {}
        self.code_help = ""
        self.root = root
        self.debug = debug
        self.output_buffer = []
        self.current_line = 0
        self.execution_stopped = False
        self.input_queue = deque()
        self.waiting_for_input = False
        self._execution_lines = []
        self._return_value = None
        
        self.debugger = Debugger(self)
        self.debugger.set_pause_callback(self._on_debug_pause)
        
        self.env = {
            "True": True,
            "False": False,
            "None": None,
            "abs": abs,
            "int": int,
            "float": float,
            "str": str,
            "len": len,
            "range": range,
            "sum": sum,
            "min": min,
            "max": max,
            "round": round,
            "pow": pow,
            "math": math,
            "np": np,
            "list": self.make_list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Help": self.help_function,
            "input": self.input_function,
            "print": self._print_to_buffer,
            "type": type,
            "sorted": sorted,
            "reversed": reversed,
            "enumerate": enumerate,
            "zip": zip,
            "map": map,
            "filter": filter,
            "debug": self.debug_command,
        }
        self.env.update({
            "sys": SysAPI(),
            "file": FileAPI(),
            "dir": DirAPI(),
            "random": RandomAPI()
        })
    
    def input_function(self, prompt=""):
        """
        Handles user input. Shows a dialog if running in GUI mode.
        """
        if self.root is None:
            return input(prompt)
        
        if len(self.input_queue) > 0:
            return self.input_queue.popleft()
        
        return self._get_input_from_dialog(prompt)
    
    def _get_input_from_dialog(self, prompt=""):
        dialog = tk.Toplevel(self.root)
        dialog.title("Input")
        dialog.geometry("400x120")
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        ttk.Label(dialog, text=prompt, font=("Consolas", 10)).pack(pady=10)
        
        entry = ttk.Entry(dialog, width=50, font=("Consolas", 11))
        entry.pack(pady=5, padx=20)
        entry.focus()
        entry.select_range(0, tk.END)
        
        result = None
        
        def on_submit():
            nonlocal result
            result = entry.get()
            dialog.destroy()
        
        def on_cancel():
            nonlocal result
            result = ""
            dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="✔ Confirm", command=on_submit, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="✖ Cancel", command=on_cancel, width=10).pack(side=tk.LEFT, padx=5)
        
        entry.bind("<Return>", lambda e: on_submit())
        entry.bind("<Escape>", lambda e: on_cancel())
        
        self.waiting_for_input = True
        dialog.wait_window()
        self.waiting_for_input = False
        
        return result if result is not None else ""
    
    def push_input(self, value):
        self.input_queue.append(str(value))
    
    def debug_command(self, *args):
        """
        Built-in debug command for managing breakpoints and execution flow.
        """
        if not args:
            return "Debug commands: breakpoint, step, continue, stop, vars, stack"
        
        cmd = args[0].lower()
        
        if cmd == "breakpoint" or cmd == "bp":
            if len(args) > 1:
                try:
                    line = int(args[1]) - 1
                    self.debugger.toggle_breakpoint(line)
                    return f"Breakpoint at line {args[1]} {'added' if line in self.debugger.breakpoints else 'removed'}"
                except:
                    return "Error: Invalid line number"
            else:
                return f"Current breakpoints: {sorted([b+1 for b in self.debugger.breakpoints])}"
        
        elif cmd == "step" or cmd == "s":
            self.debugger.step_into()
            self.debugger.is_paused = False
            return "Step mode activated"
        
        elif cmd == "continue" or cmd == "c":
            self.debugger.continue_execution()
            self.debugger.is_paused = False
            return "Execution continued"
        
        elif cmd == "stop":
            self.debugger.stop_execution()
            return "Execution stopped"
        
        elif cmd == "vars" or cmd == "v":
            return str(self.vars)
        
        elif cmd == "stack":
            return str(self.debugger.call_stack)
        
        else:
            return "Debug commands: breakpoint, step, continue, stop, vars, stack"
    
    def toggle_breakpoint(self, line_number):
        return self.debugger.toggle_breakpoint(line_number)
    
    def _on_debug_pause(self, line_number, vars_dict, stack):
        if self.root:
            self.root.update_debug_status(f"⏸ Paused at line {line_number + 1}")
            self.root.highlight_line(line_number)
    
    def _print_to_buffer(self, *args, **kwargs):
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '\n')
        output = sep.join(str(arg) for arg in args) + end
        self.output_buffer.append(output.rstrip('\n'))
        return None
    
    def help_function(self):
        return self.code_help
    
    def make_list(self, *args):
        return list(args)
    
    def safe_eval(self, expr):
        """
        Safely evaluates an expression with restricted environment.
        """
        if not expr or expr.strip() == "":
            return None
        
        expr = expr.strip()
        
        try:
            tree = ast.parse(expr, mode='eval')
        except SyntaxError:
            raise ValueError(f"Invalid expression: {expr}")
        
        allowed_names = set(self.env.keys())
        allowed_names.update(self.vars.keys())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if node.id not in allowed_names:
                    raise NameError(f"Name '{node.id}' is not defined")
        
        local_env = dict(self.env)
        local_env.update(self.vars)
        
        try:
            return eval(expr, {"__builtins__": {}}, local_env)
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {expr}\n{e}")
    
    def extract_block(self, lines, start_index):
        """
        Extracts a code block delimited by curly braces.
        """
        block = []
        depth = 1
        i = start_index
        
        while i < len(lines) and depth > 0:
            line = lines[i]
            depth += line.count('{') - line.count('}')
            if depth > 0:
                block.append(line)
            i += 1
        
        return block, i
    
    def run(self, code, debug_mode=False):
        """
        Main entry point for executing MAL code.
        """
        self.vars = {}
        self.output_buffer = []
        self.current_line = 0
        self.execution_stopped = False
        self._return_value = None
        
        self.code_help += code + "\n"
        
        lines_raw = code.split('\n')
        self._execution_lines = self._preprocess_lines(lines_raw)
        
        try:
            if debug_mode or self.debug:
                result = self._run_lines_with_debug(self._execution_lines)
            else:
                result = self._run_lines(self._execution_lines)
            
            output = '\n'.join(self.output_buffer)
            if result and result != output:
                output += '\n' + result if output else result
            
            return output
            
        except Exception as e:
            line_info = f" (line {self.current_line + 1})" if self.current_line > 0 else ""
            error_msg = f"Error{line_info}:\n{type(e).__name__}: {e}"
            self.output_buffer.append(error_msg)
            return '\n'.join(self.output_buffer)
    
    def _preprocess_lines(self, lines_raw):
        """
        Preprocesses raw lines: removes comments, empty lines, and normalizes syntax.
        """
        lines_processed = []
        
        for line in lines_raw:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith("//"):
                continue
            
            if "} elif " in line:
                line = line.replace("} elif ", "}\nelif ")
            if "} else {" in line:
                line = line.replace("} else {", "}\nelse {")
            
            lines_processed.append(line)
        
        return lines_processed
    
    def _run_lines_with_debug(self, lines):
        """
        Executes lines with debugger support.
        """
        i = 0
        function_depth = 0
        
        while i < len(lines) and not self.execution_stopped:
            self.current_line = i
            line = lines[i]
            
            if self.debugger.should_pause(i, self._is_function_call(line)):
                self.debugger.pause_at_line(i)
                if self.execution_stopped:
                    break
            
            try:
                self._execute_line(line, i)
                
                if "function" in line and "{" in line:
                    function_depth += 1
                    self.debugger.call_stack.append(f"Function {line.split()[1]} (line {i+1})")
                
                if "}" in line and not line.strip().startswith("//"):
                    if function_depth > 0:
                        function_depth -= 1
                        if self.debugger.call_stack:
                            self.debugger.call_stack.pop()
                
                if self.debugger.step_out_function and function_depth < self.debugger.function_depth:
                    self.debugger.function_depth = function_depth
                    if function_depth == 0:
                        self.debugger.step_out_function = False
                        self.debugger.step_mode = False
                
                i += 1
                
            except StopIteration as e:
                if str(e) == "return":
                    return self._return_value
                elif str(e) in ["break", "continue"]:
                    raise
                i += 1
                
            except Exception as e:
                raise RuntimeError(f"Line {i+1}: {line}\n{type(e).__name__}: {e}")
        
        return '\n'.join(self.output_buffer)
    
    def _run_lines(self, lines):
        """
        Executes lines without debugger support.
        """
        i = 0
        function_depth = 0
        
        while i < len(lines) and not self.execution_stopped:
            self.current_line = i
            line = lines[i]
            
            try:
                self._execute_line(line, i)
                
                if "function" in line and "{" in line:
                    function_depth += 1
                
                if "}" in line and not line.strip().startswith("//"):
                    if function_depth > 0:
                        function_depth -= 1
                
                i += 1
                
            except StopIteration as e:
                if str(e) == "return":
                    return self._return_value
                elif str(e) in ["break", "continue"]:
                    raise
                i += 1
                
            except Exception as e:
                raise RuntimeError(f"Line {i+1}: {line}\n{type(e).__name__}: {e}")
        
        return '\n'.join(self.output_buffer)
    
    def _is_function_call(self, line):
        return bool(re.match(r'^(\w+)\s*\(.*\)$', line.strip()))
    
    def _execute_line(self, line, line_number):
        """
        Executes a single line of MAL code.
        """
        # 1. Function definition
        func_match = re.match(r'^function\s+(\w+)\s*\((.*?)\)\s*\{', line)
        if func_match:
            func_name = func_match.group(1)
            params = [p.strip() for p in func_match.group(2).split(',') if p.strip()]
            self.vars[func_name] = self._create_function(func_name, params)
            return None
        
        # 2. Variable definition
        var_keywords = ["let", "var", "set"]
        for keyword in var_keywords:
            pattern = rf'{keyword}\s+(\w+)(?:\s*=\s*(.+))?'
            var_match = re.match(pattern, line)
            if var_match:
                var_name = var_match.group(1)
                expr = var_match.group(2)
                value = self.safe_eval(expr) if expr else 0
                self.vars[var_name] = value
                return None
        
        # 3. Control statements
        if line in ["break", "continue"]:
            raise StopIteration(line)
        
        if line.startswith("return "):
            return_expr = line[7:].strip()
            self._return_value = self.safe_eval(return_expr) if return_expr else None
            raise StopIteration("return")
        
        # 4. Index assignment
        index_assign_match = re.match(r'^(\w+)\s*\[\s*(.+)\s*\]\s*=\s*(.+)', line)
        if index_assign_match:
            var_name = index_assign_match.group(1)
            index_expr = index_assign_match.group(2)
            value_expr = index_assign_match.group(3)
            
            if var_name not in self.vars:
                raise NameError(f"Variable '{var_name}' is not defined")
            
            array = self.vars[var_name]
            index = self.safe_eval(index_expr)
            value = self.safe_eval(value_expr)
            if isinstance(array, (list, dict)):
                array[index] = value
            else:
                raise TypeError(f"Variable '{var_name}' is not indexable")
            
            return None
        
        # 5. Simple assignment
        assign_match = re.match(r'^(\w+)\s*=\s*(.+)', line)
        if assign_match:
            var_name = assign_match.group(1)
            expr = assign_match.group(2)
            
            if var_name not in self.vars and var_name not in self.env:
                raise NameError(f"Variable '{var_name}' is not defined. Use 'let' to declare it.")
            
            self.vars[var_name] = self.safe_eval(expr)
            return None
        
        # 6. Print statements
        if (line.startswith("print ") or line.startswith("print(") or 
            line.startswith("show ") or line.startswith("output ") or line.startswith("say ")):
            
            expr = self._extract_print_expr(line)
            value = self.safe_eval(expr)
            self._print_to_buffer(value)
            return None
        
        # 7. Conditional structures
        if line.startswith("if ") or line.startswith("elif ") or line.startswith("else"):
            blocks = [line]
            j = line_number + 1
            while j < len(self._execution_lines):
                next_line = self._execution_lines[j]
                if next_line.startswith("elif ") or next_line.startswith("else"):
                    blocks.append(next_line)
                    j += 1
                elif next_line == "}":
                    blocks.append(next_line)
                    j += 1
                    if j < len(self._execution_lines):
                        following = self._execution_lines[j]
                        if not (following.startswith("elif ") or following.startswith("else")):
                            break
                    else:
                        break
                else:
                    break
            
            self._process_conditional(blocks)
            return None
        
        # 8. While loop
        while_match = re.match(r'while\s+(.+)\s*\{', line)
        if while_match:
            condition_expr = while_match.group(1)
            body, _ = self.extract_block(self._execution_lines, line_number + 1)
            
            while self.safe_eval(condition_expr) and not self.execution_stopped:
                try:
                    self._run_lines(body.copy())
                except StopIteration as e:
                    if str(e) == "break":
                        break
                    elif str(e) == "continue":
                        continue
                    else:
                        raise
            
            return None
        
        # 9. Numeric for loop
        for_range_match = re.match(r'for\s+(\w+)\s+from\s+(.+)\s+to\s+(.+)\s*\{', line)
        if for_range_match:
            var_name = for_range_match.group(1)
            start_expr = for_range_match.group(2)
            end_expr = for_range_match.group(3)
            
            start = int(self.safe_eval(start_expr))
            end = int(self.safe_eval(end_expr))
            
            body, _ = self.extract_block(self._execution_lines, line_number + 1)
            
            for value in range(start, end + 1):
                if self.execution_stopped:
                    break
                self.vars[var_name] = value
                try:
                    self._run_lines(body.copy())
                except StopIteration as e:
                    if str(e) == "break":
                        break
                    elif str(e) == "continue":
                        continue
            
            return None
        
        # 10. Iterable for loop
        for_iter_match = re.match(r'for\s+(\w+)\s+from\s+(.+?)\s*\{', line)
        if for_iter_match:
            var_name = for_iter_match.group(1)
            iterable_expr = for_iter_match.group(2)
            
            iterable = self.safe_eval(iterable_expr)
            
            if not hasattr(iterable, '__iter__'):
                raise TypeError(f"'{iterable_expr}' is not iterable")
            
            body, _ = self.extract_block(self._execution_lines, line_number + 1)
            
            for value in iterable:
                if self.execution_stopped:
                    break
                self.vars[var_name] = value
                try:
                    self._run_lines(body.copy())
                except StopIteration as e:
                    if str(e) == "break":
                        break
                    elif str(e) == "continue":
                        continue
            
            return None
        
        # 11. Function call
        call_match = re.match(r'^(\w+)\s*\((.*)\)$', line)
        if call_match:
            func_name = call_match.group(1)
            args_str = call_match.group(2)
            
            if func_name not in self.vars or not callable(self.vars[func_name]):
                raise NameError(f"Function '{func_name}' is not defined")
            
            args = []
            if args_str.strip():
                args = [self.safe_eval(arg.strip()) for arg in args_str.split(',')]
            
            if self.debugger.step_into_function:
                self.debugger.function_depth = len(self.debugger.call_stack)
                self.debugger.step_into_function = False
            
            self.vars[func_name](*args)
            return None
        
        # 12. Standalone expression
        if line.strip() and not line.strip() in ["{", "}"]:
            value = self.safe_eval(line)
            if value is not None and self.debug:
                self._print_to_buffer(f"[DEBUG] {value}")
        
        return None
    
    def _extract_print_expr(self, line):
        if line.startswith("print("):
            expr = line[5:]
            if expr.startswith("(") and expr.endswith(")"):
                expr = expr[1:-1].strip()
            else:
                expr = expr.strip()
        elif line.startswith("print "):
            expr = line[6:].strip()
            if expr.startswith("(") and expr.endswith(")"):
                expr = expr[1:-1].strip()
        elif line.startswith("show "):
            expr = line[5:].strip()
        elif line.startswith("output "):
            expr = line[7:].strip()
        else:  # say
            expr = line[4:].strip()
        return expr
    
    def _create_function(self, func_name, params):
        """
        Creates a user-defined function dynamically.
        """
        param_names = params
        func_body = []
        
        def func(*args):
            old_vars = dict(self.vars)
            
            if len(args) != len(param_names):
                raise TypeError(f"{func_name}() expects {len(param_names)} arguments, got {len(args)}")
            
            for name, value in zip(param_names, args):
                self.vars[name] = value
            
            return_value = None
            try:
                self._run_lines(func_body)
            except StopIteration as e:
                if str(e) == "return":
                    return_value = self.vars.get("__return__", None)
            
            self.vars = old_vars
            return return_value
        
        func.__body__ = func_body
        return func
    
    def _process_conditional(self, blocks):
        """
        Processes if/elif/else conditional blocks.
        """
        i = 0
        executed = False
        
        while i < len(blocks):
            line = blocks[i]
            
            if line.startswith("if ") or line.startswith("elif "):
                cond_match = re.match(r'(if|elif)\s+(.+?)\s*\{', line)
                if not cond_match:
                    if line.endswith("{"):
                        cond_match = re.match(r'(if|elif)\s+(.+?)\s*\{', line)
                    else:
                        raise SyntaxError(f"Invalid conditional statement: {line}")
                
                condition = self.safe_eval(cond_match.group(2))
                
                i += 1
                depth = 1
                inner_block = []
                while i < len(blocks) and depth > 0:
                    current_line = blocks[i]
                    if current_line == "}":
                        depth -= 1
                        if depth > 0:
                            inner_block.append(current_line)
                    else:
                        depth += current_line.count('{') - current_line.count('}')
                        if depth > 0:
                            inner_block.append(current_line)
                    i += 1
                
                if condition and not executed:
                    self._run_lines(inner_block)
                    executed = True
            
            elif line.startswith("else"):
                if not line.endswith("{"):
                    raise SyntaxError("else statement must end with {")
                
                i += 1
                depth = 1
                else_block = []
                while i < len(blocks) and depth > 0:
                    current_line = blocks[i]
                    if current_line == "}":
                        depth -= 1
                        if depth > 0:
                            else_block.append(current_line)
                    else:
                        depth += current_line.count('{') - current_line.count('}')
                        if depth > 0:
                            else_block.append(current_line)
                    i += 1
                
                if not executed:
                    self._run_lines(else_block)
                    executed = True
            
            else:
                i += 1
        
        return executed


# ==================== Main Application (GUI) ====================
class App(tk.Tk):
    """
    Main IDE window for MAL language with debugging support.
    """
    def __init__(self):
        super().__init__()
        self.title("MAL IDE - Advanced Debugging")
        self.geometry("1100x750")
        self.mal = MAL(root=self, debug=False)
        self.debug_mode = False
        
        self.current_file = None
        self.syntax_highlighting = True
        self.auto_indent_enabled = True
        self.theme = "light"
        
        self.setup_ui()
        self.setup_menu()
        self.setup_tags()
        self.bind_events()
        
        default_code = 'using MAL\nprint "hello world"'
        self.code_editor.insert(tk.END, default_code)
    
    def setup_ui(self):
        toolbar = ttk.Frame(self)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
        
        buttons = [
            ("📁 Open", self.open_file),
            ("💾 Save", self.save_file),
            ("▶ Run", self.run_code),
            ("🐛 Debug", self.toggle_debug_mode),
            ("🔴 Breakpoint", self.add_breakpoint_at_cursor),
            ("⏹ Stop", self.stop_execution),
            ("🎨 Theme", self.toggle_theme),
            ("📊 Clear Output", self.clear_output),
        ]
        
        for text, command in buttons:
            btn = ttk.Button(toolbar, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        debug_buttons = [
            ("⏭ Step Over", self.debug_step_over),
            ("⏬ Step Into", self.debug_step_into),
            ("⏫ Step Out", self.debug_step_out),
            ("▶ Continue", self.debug_continue),
        ]
        
        for text, command in debug_buttons:
            btn = ttk.Button(toolbar, text=text, command=command, state=tk.DISABLED)
            btn.pack(side=tk.LEFT, padx=2)
            self.__dict__[f"debug_{command.__name__}_btn"] = btn
        
        self.status_label = ttk.Label(toolbar, text="Ready")
        self.status_label.pack(side=tk.RIGHT, padx=5)
        
        main_panel = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_panel.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        code_frame = ttk.Frame(main_panel)
        
        self.line_numbers = tk.Text(code_frame, width=4, padx=3, takefocus=0,
                                   border=0, background='lightgray', state='disabled')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        self.code_editor = scrolledtext.ScrolledText(
            code_frame, 
            font=("Consolas", 12),
            undo=True,
            wrap=tk.WORD
        )
        self.code_editor.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        main_panel.add(code_frame, weight=3)
        
        output_frame = ttk.Frame(main_panel)
        
        self.output_notebook = ttk.Notebook(output_frame)
        self.output_notebook.pack(expand=True, fill=tk.BOTH)
        
        self.output_text = scrolledtext.ScrolledText(
            self.output_notebook,
            font=("Consolas", 11),
            state='disabled'
        )
        self.output_notebook.add(self.output_text, text="Output")
        
        self.error_text = scrolledtext.ScrolledText(
            self.output_notebook,
            font=("Consolas", 11),
            state='disabled',
            background='#ffeeee'
        )
        self.output_notebook.add(self.error_text, text="Errors")
        
        self.vars_text = scrolledtext.ScrolledText(
            self.output_notebook,
            font=("Consolas", 11),
            state='disabled',
            background='#f0f8ff'
        )
        self.output_notebook.add(self.vars_text, text="Variables")
        
        main_panel.add(output_frame, weight=1)
        
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)
        
        self.position_label = ttk.Label(bottom_frame, text="Line: 1, Col: 1")
        self.position_label.pack(side=tk.LEFT)
        
        self.debug_status_label = ttk.Label(bottom_frame, text="🔍 Debug: Disabled")
        self.debug_status_label.pack(side=tk.LEFT, padx=20)
        
        self.file_label = ttk.Label(bottom_frame, text="New File")
        self.file_label.pack(side=tk.RIGHT)
    
    def setup_menu(self):
        menubar = tk.Menu(self)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New File", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit, accelerator="Alt+F4")
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        
        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label="Run Program", command=self.run_code, accelerator="F5")
        run_menu.add_command(label="Stop Execution", command=self.stop_execution, accelerator="F6")
        run_menu.add_separator()
        run_menu.add_command(label="Debug Mode", command=self.toggle_debug_mode)
        run_menu.add_command(label="Toggle Breakpoint", command=self.add_breakpoint_at_cursor, accelerator="F9")
        
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_checkbutton(label="Syntax Highlighting", variable=tk.BooleanVar(value=True), 
                                     command=self.toggle_syntax_highlighting)
        settings_menu.add_checkbutton(label="Auto Indent", variable=tk.BooleanVar(value=True),
                                     command=self.toggle_auto_indent)
        settings_menu.add_separator()
        settings_menu.add_command(label="Change Font...", command=self.change_font)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="MAL Help", command=self.show_help)
        help_menu.add_command(label="Code Examples", command=self.show_examples)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
        
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_cascade(label="Run", menu=run_menu)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.config(menu=menubar)
    
    def setup_tags(self):
        self.code_editor.tag_configure("keyword", foreground="#0000FF", font=("Consolas", 12, "bold"))
        self.code_editor.tag_configure("string", foreground="#008000")
        self.code_editor.tag_configure("comment", foreground="#808080", font=("Consolas", 12, "italic"))
        self.code_editor.tag_configure("number", foreground="#FF4500")
        self.code_editor.tag_configure("function", foreground="#8B008B", font=("Consolas", 12, "bold"))
        self.code_editor.tag_configure("variable", foreground="#000080")
        self.code_editor.tag_configure("error", background="#FFB6C1", underline=True)
        self.code_editor.tag_configure("api", foreground="#0066CC", font=("Consolas", 12, "bold"))
    
    def bind_events(self):
        self.code_editor.bind("<KeyRelease>", self.on_key_release)
        self.code_editor.bind("<Return>", self.on_return)
        self.code_editor.bind("<Tab>", self.on_tab)
        self.code_editor.bind("<Control-n>", lambda e: self.new_file())
        self.code_editor.bind("<Control-o>", lambda e: self.open_file())
        self.code_editor.bind("<Control-s>", lambda e: self.save_file())
        self.code_editor.bind("<F5>", lambda e: self.run_code())
        self.code_editor.bind("<F9>", lambda e: self.add_breakpoint_at_cursor())
        self.code_editor.bind("<F1>", lambda e: self.show_help())
        self.code_editor.bind("<Button-1>", self.update_position)
        self.code_editor.bind("<Key>", self.update_position)
        self.code_editor.bind("<Configure>", self.update_line_numbers)
    
    # ==================== Debugging Methods ====================
    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        if self.debug_mode:
            self.debug_status_label.config(text="🔍 Debug: Active")
            self.status_label.config(text="🐛 Debug mode activated")
            for btn_name in ['debug_step_over_btn', 'debug_step_into_btn', 
                           'debug_step_out_btn', 'debug_continue_btn']:
                if hasattr(self, btn_name):
                    getattr(self, btn_name).config(state=tk.NORMAL)
        else:
            self.debug_status_label.config(text="🔍 Debug: Disabled")
            self.status_label.config(text="🐛 Debug mode deactivated")
            for btn_name in ['debug_step_over_btn', 'debug_step_into_btn', 
                           'debug_step_out_btn', 'debug_continue_btn']:
                if hasattr(self, btn_name):
                    getattr(self, btn_name).config(state=tk.DISABLED)
    
    def add_breakpoint_at_cursor(self):
        cursor_pos = self.code_editor.index(tk.INSERT)
        line_number = int(cursor_pos.split('.')[0]) - 1
        
        if self.mal.toggle_breakpoint(line_number):
            self.mark_breakpoint(line_number)
            self.status_label.config(text=f"🔴 Breakpoint added at line {line_number + 1}")
        else:
            self.unmark_breakpoint(line_number)
            self.status_label.config(text=f"🟢 Breakpoint removed at line {line_number + 1}")
    
    def mark_breakpoint(self, line_number):
        start = f"{line_number + 1}.0"
        end = f"{line_number + 1}.end"
        self.code_editor.tag_add("breakpoint", start, end)
        self.code_editor.tag_configure("breakpoint", background="#FF4444", foreground="white")
    
    def unmark_breakpoint(self, line_number):
        start = f"{line_number + 1}.0"
        end = f"{line_number + 1}.end"
        self.code_editor.tag_remove("breakpoint", start, end)
    
    def update_debug_status(self, message):
        self.debug_status_label.config(text=message)
    
    def highlight_line(self, line_number):
        self.code_editor.tag_remove("debug_line", "1.0", tk.END)
        start = f"{line_number + 1}.0"
        end = f"{line_number + 1}.end"
        self.code_editor.tag_add("debug_line", start, end)
        self.code_editor.tag_configure("debug_line", background="#FFFF00")
        self.code_editor.see(start)
    
    def debug_step_over(self):
        if self.debug_mode:
            self.mal.debugger.step_over()
            self.mal.debugger.is_paused = False
            self.status_label.config(text="⏭ Step over")
    
    def debug_step_into(self):
        if self.debug_mode:
            self.mal.debugger.step_into()
            self.mal.debugger.is_paused = False
            self.status_label.config(text="⏬ Step into")
    
    def debug_step_out(self):
        if self.debug_mode:
            self.mal.debugger.step_out()
            self.mal.debugger.is_paused = False
            self.status_label.config(text="⏫ Step out")
    
    def debug_continue(self):
        if self.debug_mode:
            self.mal.debugger.continue_execution()
            self.mal.debugger.is_paused = False
            self.status_label.config(text="▶ Continue execution")
    
    # ==================== Core Methods ====================
    def run_code(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        
        if not code:
            self.show_output("❌ No code to execute!")
            return
        
        self.code_editor.tag_remove("debug_line", "1.0", tk.END)
        self.status_label.config(text="Running..." if not self.debug_mode else "🐛 Debugging...")
        self.update_idletasks()
        
        try:
            lines = code.split('\n')
            output = ""
            i = 0
            
            while i < len(lines):
                line = lines[i].strip()
                
                if line.startswith("using MAL"):
                    mal_lines = []
                    i += 1
                    while i < len(lines):
                        current = lines[i].strip()
                        if current.startswith("using PYTHON"):
                            break
                        if current and not current.startswith("using"):
                            mal_lines.append(lines[i])
                        i += 1
                    
                    if mal_lines:
                        mal_code = '\n'.join(mal_lines)
                        mal_output = self.mal.run(mal_code, debug_mode=self.debug_mode)
                        if mal_output:
                            output += mal_output + "\n"
                
                elif line.startswith("using PYTHON"):
                    py_lines = []
                    i += 1
                    while i < len(lines):
                        current = lines[i].strip()
                        if current.startswith("using MAL"):
                            break
                        if current and not current.startswith("using"):
                            py_lines.append(lines[i])
                        i += 1
                    
                    if py_lines:
                        py_code = '\n'.join(py_lines)
                        py_output = self.run_python_code(py_code)
                        if py_output:
                            output += py_output + "\n"
                
                else:
                    i += 1
            
            self.show_output(output)
            self.show_variables()
            self.status_label.config(text="✅ Execution completed successfully")
            
        except Exception as e:
            self.show_error(f"Execution error:\n{str(e)}")
            self.status_label.config(text="❌ Execution error")
    
    def run_python_code(self, code):
        f = io.StringIO()
        try:
            with contextlib.redirect_stdout(f):
                exec(code, {"__name__": "__main__"})
            return f.getvalue()
        except Exception as e:
            return f"Python error: {e}"
    
    def show_output(self, text):
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state='disabled')
        self.output_notebook.select(0)
    
    def show_error(self, text):
        self.error_text.config(state='normal')
        self.error_text.delete(1.0, tk.END)
        self.error_text.insert(tk.END, text)
        self.error_text.config(state='disabled')
        self.output_notebook.select(1)
    
    def show_variables(self):
        self.vars_text.config(state='normal')
        self.vars_text.delete(1.0, tk.END)
        
        if self.mal.vars:
            for var_name, var_value in self.mal.vars.items():
                if not callable(var_value) and not var_name.startswith("__"):
                    value_str = str(var_value)
                    if len(value_str) > 100:
                        value_str = value_str[:100] + "..."
                    self.vars_text.insert(tk.END, f"{var_name} = {value_str}\n")
        else:
            self.vars_text.insert(tk.END, "No variables defined.\n")
        
        self.vars_text.config(state='disabled')
    
    def stop_execution(self):
        self.mal.execution_stopped = True
        self.mal.debugger.is_paused = False
        self.status_label.config(text="⏹ Execution stopped")
    
    def clear_output(self):
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')
        
        self.error_text.config(state='normal')
        self.error_text.delete(1.0, tk.END)
        self.error_text.config(state='disabled')
        
        self.status_label.config(text="📊 Output cleared")
    
    # ==================== Edit Methods ====================
    def new_file(self):
        if self.current_file or self.code_editor.get(1.0, "end-1c").strip():
            if not messagebox.askyesno("Save", "Do you want to save the current changes?"):
                return
        
        self.code_editor.delete(1.0, tk.END)
        self.current_file = None
        self.file_label.config(text="New File")
        self.status_label.config(text="New file created")
    
    def open_file(self):
        filename = filedialog.askopenfilename(
            defaultextension=".mal",
            filetypes=[
                ("MAL Files", "*.mal"),
                ("Python Files", "*.py"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.code_editor.delete(1.0, tk.END)
                    self.code_editor.insert(tk.END, content)
                
                self.current_file = filename
                self.file_label.config(text=os.path.basename(filename))
                self.status_label.config(text=f"File opened: {filename}")
                
                if self.syntax_highlighting:
                    self.highlight_syntax()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{str(e)}")
    
    def save_file(self):
        if self.current_file:
            try:
                content = self.code_editor.get(1.0, tk.END)
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.status_label.config(text=f"File saved: {self.current_file}")
                return True
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
                return False
        else:
            return self.save_as_file()
    
    def save_as_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".mal",
            filetypes=[
                ("MAL Files", "*.mal"),
                ("Python Files", "*.py"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )
        
        if filename:
            self.current_file = filename
            saved = self.save_file()
            if saved:
                self.file_label.config(text=os.path.basename(filename))
            return saved
        
        return False
    
    def update_line_numbers(self, event=None):
        lines = self.code_editor.get("1.0", "end-1c").count("\n") + 1
        line_numbers_text = "\n".join(str(i) for i in range(1, lines + 1))
        
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.config(state="disabled")
    
    def update_position(self, event=None):
        try:
            cursor_pos = self.code_editor.index(tk.INSERT)
            line, col = cursor_pos.split('.')
            self.position_label.config(text=f"Line: {line}, Col: {int(col)+1}")
        except:
            pass
    
    def on_key_release(self, event=None):
        if self.syntax_highlighting:
            self.highlight_syntax()
        self.update_line_numbers()
        self.update_position()
    
    def on_return(self, event):
        if self.auto_indent_enabled:
            current_pos = self.code_editor.index("insert")
            line_num = int(current_pos.split('.')[0])
            
            if line_num > 1:
                prev_line = self.code_editor.get(f"{line_num - 1}.0", f"{line_num - 1}.end")
            else:
                prev_line = ""
            
            base_indent = 0
            if prev_line:
                base_indent = len(prev_line) - len(prev_line.lstrip())
                if prev_line.rstrip().endswith("{"):
                    base_indent += 4
            
            self.code_editor.insert("insert", "\n" + " " * base_indent)
            return "break"
        else:
            self.code_editor.insert("insert", "\n")
            return "break"
    
    def on_tab(self, event):
        self.code_editor.insert(tk.INSERT, "    ")
        return "break"
    
    def highlight_syntax(self):
        code = self.code_editor.get("1.0", tk.END)
        
        for tag in ["keyword", "string", "comment", "number", "function", "variable", "error", "api"]:
            self.code_editor.tag_remove(tag, "1.0", tk.END)
        
        keywords = [
            "using", "show", "say", "let", "set", "print", "output", "var", "function", "return",
            "if", "elif", "else", "while", "for", "from",
            "to", "break", "continue", "true", "false", "null"
        ]
        
        apis = ["sys", "file", "dir", "random", "np"]
        
        for keyword in keywords:
            pattern = rf'\b{keyword}\b'
            for match in re.finditer(pattern, code, re.IGNORECASE):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.code_editor.tag_add("keyword", start, end)
        
        for pattern in [r'"[^"\n]*"', r"'[^'\n]*'"]:
            for match in re.finditer(pattern, code):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.code_editor.tag_add("string", start, end)
        
        for pattern in [r'#.*', r'//.*']:
            for match in re.finditer(pattern, code):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.code_editor.tag_add("comment", start, end)
        
        for match in re.finditer(r'\b\d+(\.\d+)?\b', code):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.code_editor.tag_add("number", start, end)
        
        for match in re.finditer(r'\bfunction\s+(\w+)', code):
            func_name = match.group(1)
            func_pattern = rf'\b{func_name}\b\s*\([^)]*\)'
            for func_match in re.finditer(func_pattern, code):
                start = f"1.0+{func_match.start()}c"
                end = f"1.0+{func_match.end()}c"
                self.code_editor.tag_add("function", start, end)
        
        for api in apis:
            pattern = rf'\b{api}\b'
            for match in re.finditer(pattern, code, re.IGNORECASE):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.code_editor.tag_add("api", start, end)
    
    def toggle_syntax_highlighting(self):
        self.syntax_highlighting = not self.syntax_highlighting
        if self.syntax_highlighting:
            self.highlight_syntax()
            self.status_label.config(text="Syntax highlighting enabled")
        else:
            self.status_label.config(text="Syntax highlighting disabled")
    
    def toggle_auto_indent(self):
        self.auto_indent_enabled = not self.auto_indent_enabled
        status = "Enabled" if self.auto_indent_enabled else "Disabled"
        self.status_label.config(text=f"Auto indent: {status}")
    
    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.code_editor.config(bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
            self.output_text.config(bg="#1e1e1e", fg="#d4d4d4")
            self.error_text.config(bg="#2d2d2d", fg="#d4d4d4")
            self.vars_text.config(bg="#2d2d2d", fg="#d4d4d4")
            self.line_numbers.config(bg="#2d2d2d", fg="#858585")
        else:
            self.theme = "light"
            self.code_editor.config(bg="white", fg="black", insertbackground="black")
            self.output_text.config(bg="white", fg="black")
            self.error_text.config(bg="#ffeeee", fg="black")
            self.vars_text.config(bg="#f0f8ff", fg="black")
            self.line_numbers.config(bg="lightgray", fg="black")
    
    def change_font(self):
        font = simpledialog.askstring("Change Font", "Font name (e.g., Consolas, Courier New):", 
                                     initialvalue="Consolas")
        if font:
            try:
                self.code_editor.config(font=(font, 12))
                self.status_label.config(text=f"Font changed to: {font}")
            except:
                messagebox.showerror("Error", "Invalid font name!")
    
    def undo(self):
        try:
            self.code_editor.edit_undo()
        except:
            pass
    
    def redo(self):
        try:
            self.code_editor.edit_redo()
        except:
            pass
    
    def cut(self):
        self.code_editor.event_generate("<<Cut>>")
    
    def copy(self):
        self.code_editor.event_generate("<<Copy>>")
    
    def paste(self):
        self.code_editor.event_generate("<<Paste>>")
    
    def select_all(self):
        self.code_editor.tag_add("sel", "1.0", "end")
    
    def show_help(self):
        help_text = """🔧 MAL Language Guide

General Structure:
  using MAL     // Start MAL block
  using PYTHON  // Start Python block

Variables:
  let x = 5
  let name = "Ali"
  let numbers = list(1, 2, 3)

Functions:
  function greet(name) {
    print "Hello " + name
    return "Welcome"
  }

Control Structures:
  if (condition) { ... } elif (other) { ... } else { ... }

Loops:
  for i from 1 to 10 { print i }
  for item from myList { print item }
  while (condition) { ... }

File Operations:
  file.write("test.txt", "content")
  let content = file.read("test.txt")
  dir.create("new_folder")
  let items = dir.list()

Debugging:
  F9: Add/Remove breakpoint
  F5: Run
  🐛 Debug: Activate debug mode
  ⏭ Step Over: Execute next line
  ⏬ Step Into: Enter function
  ⏫ Step Out: Exit function
  ▶ Continue: Continue until next breakpoint

Tips:
  - Comments start with # or //
  - Use curly braces for blocks
  - Case-insensitive
"""
        
        help_window = tk.Toplevel(self)
        help_window.title("MAL Help")
        help_window.geometry("600x500")
        
        text = scrolledtext.ScrolledText(help_window, font=("Consolas", 11))
        text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        text.insert(tk.END, help_text)
        text.config(state='disabled')
    
    def show_examples(self):
        examples = {
            "Factorial": """function factorial(n) {
    if (n <= 1) {
        return 1
    }
    return n * factorial(n - 1)
}

print factorial(5)""",
            
            "Fibonacci": """function fibonacci(n) {
    if (n <= 1) {
        return n
    }
    return fibonacci(n - 1) + fibonacci(n - 2)
}

print fibonacci(10)""",
            
            "File Management": """# Create a report
let report = ""
report = report + "System Report:\\n"
report = report + str(sys.time())

file.write("report.txt", report)
print 'Report saved'""",
            
            "Debugging Example": """# Debug test
let x = 10
let y = 20

function add(a, b) {
    let result = a + b
    return result
}

let z = add(x, y)
print z
# Press F9 to set breakpoint, then enable 🐛 Debug"""
        }
        
        examples_window = tk.Toplevel(self)
        examples_window.title("Code Examples")
        examples_window.geometry("700x500")
        
        notebook = ttk.Notebook(examples_window)
        notebook.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        for title, code in examples.items():
            frame = ttk.Frame(notebook)
            text = scrolledtext.ScrolledText(frame, font=("Consolas", 11))
            text.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
            text.insert(tk.END, code)
            notebook.add(frame, text=title)
    
    def show_about(self):
        about_text = f"""🧬 MAL IDE v2.0 - Advanced Debugging

An Integrated Development Environment for the MAL programming language

New Features:
  ✓ Line-by-line debugging
  ✓ Breakpoints
  ✓ Step Over/Into/Out
  ✓ Interactive input dialogs
  ✓ Real-time variable display
  ✓ Call stack tracking

Available APIs:
  • sys: System information
  • file: File operations
  • dir: Directory operations
  • random: Random operations

Python: {platform.python_version()}
System: {platform.system()} {platform.release()}

© 2024 - Developed with Python and Tkinter
Developer: Milad Moradpour
"""
        
        messagebox.showinfo("About MAL IDE", about_text)


# ==================== Application Entry Point ====================
if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()