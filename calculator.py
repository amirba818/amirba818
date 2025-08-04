#!/usr/bin/env python3
"""
Professional Calculator
A comprehensive calculator with GUI and CLI interfaces
Supports basic arithmetic, scientific functions, and advanced operations
"""

import math
import sys
import re
from typing import Union, Optional

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    tk = None
    ttk = None
    messagebox = None


class Calculator:
    """Professional Calculator Engine"""
    
    def __init__(self):
        self.memory = 0
        self.history = []
        self.angle_mode = "degrees"  # degrees or radians
    
    def add(self, a: float, b: float) -> float:
        """Addition"""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Subtraction"""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiplication"""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Division"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, base: float, exponent: float) -> float:
        """Power operation"""
        return base ** exponent
    
    def square_root(self, x: float) -> float:
        """Square root"""
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(x)
    
    def cube_root(self, x: float) -> float:
        """Cube root"""
        return math.copysign(math.pow(abs(x), 1/3), x)
    
    def factorial(self, n: int) -> int:
        """Factorial"""
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if n > 170:  # Prevent overflow
            raise ValueError("Number too large for factorial calculation")
        return math.factorial(int(n))
    
    def sin(self, x: float) -> float:
        """Sine function"""
        if self.angle_mode == "degrees":
            x = math.radians(x)
        return math.sin(x)
    
    def cos(self, x: float) -> float:
        """Cosine function"""
        if self.angle_mode == "degrees":
            x = math.radians(x)
        return math.cos(x)
    
    def tan(self, x: float) -> float:
        """Tangent function"""
        if self.angle_mode == "degrees":
            x = math.radians(x)
        return math.tan(x)
    
    def asin(self, x: float) -> float:
        """Arcsine function"""
        if abs(x) > 1:
            raise ValueError("Input must be between -1 and 1")
        result = math.asin(x)
        if self.angle_mode == "degrees":
            result = math.degrees(result)
        return result
    
    def acos(self, x: float) -> float:
        """Arccosine function"""
        if abs(x) > 1:
            raise ValueError("Input must be between -1 and 1")
        result = math.acos(x)
        if self.angle_mode == "degrees":
            result = math.degrees(result)
        return result
    
    def atan(self, x: float) -> float:
        """Arctangent function"""
        result = math.atan(x)
        if self.angle_mode == "degrees":
            result = math.degrees(result)
        return result
    
    def log(self, x: float, base: Optional[float] = None) -> float:
        """Logarithm"""
        if x <= 0:
            raise ValueError("Logarithm input must be positive")
        if base is None:
            return math.log10(x)  # Common logarithm
        elif base <= 0 or base == 1:
            raise ValueError("Logarithm base must be positive and not equal to 1")
        return math.log(x, base)
    
    def ln(self, x: float) -> float:
        """Natural logarithm"""
        if x <= 0:
            raise ValueError("Natural logarithm input must be positive")
        return math.log(x)
    
    def evaluate_expression(self, expression: str) -> float:
        """Evaluate mathematical expression safely"""
        # Replace common mathematical functions
        expression = expression.replace("π", str(math.pi))
        expression = expression.replace("e", str(math.e))
        expression = expression.replace("^", "**")
        
        # Safe evaluation using eval with restricted namespace
        allowed_names = {
            "sin": self.sin, "cos": self.cos, "tan": self.tan,
            "asin": self.asin, "acos": self.acos, "atan": self.atan,
            "sqrt": self.square_root, "log": self.log, "ln": self.ln,
            "abs": abs, "round": round, "floor": math.floor, "ceil": math.ceil,
            "pi": math.pi, "e": math.e, "inf": math.inf,
            "factorial": self.factorial,
            "__builtins__": {}
        }
        
        try:
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            self.history.append(f"{expression} = {result}")
            return float(result)
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def memory_store(self, value: float):
        """Store value in memory"""
        self.memory = value
    
    def memory_recall(self) -> float:
        """Recall value from memory"""
        return self.memory
    
    def memory_add(self, value: float):
        """Add value to memory"""
        self.memory += value
    
    def memory_subtract(self, value: float):
        """Subtract value from memory"""
        self.memory -= value
    
    def memory_clear(self):
        """Clear memory"""
        self.memory = 0
    
    def get_history(self) -> list:
        """Get calculation history"""
        return self.history.copy()
    
    def clear_history(self):
        """Clear calculation history"""
        self.history.clear()


class CalculatorGUI:
    """Professional Calculator GUI using tkinter"""
    
    def __init__(self):
        self.calc = Calculator()
        self.root = tk.Tk()
        self.root.title("Professional Calculator")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        
        # Variables
        self.display_var = tk.StringVar(value="0")
        self.current_input = ""
        self.result_displayed = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Display frame
        display_frame = ttk.Frame(main_frame)
        display_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Display entry
        self.display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 20, "bold"),
            justify="right",
            state="readonly",
            bg="#34495e",
            fg="white",
            bd=0,
            highlightthickness=2,
            highlightcolor="#3498db"
        )
        self.display.pack(fill=tk.X, ipady=15)
        
        # History frame
        history_frame = ttk.LabelFrame(main_frame, text="History", padding=5)
        history_frame.pack(fill=tk.X, pady=(0, 10))
        
        # History listbox with scrollbar
        history_scroll_frame = ttk.Frame(history_frame)
        history_scroll_frame.pack(fill=tk.X)
        
        self.history_listbox = tk.Listbox(
            history_scroll_frame,
            height=3,
            font=("Arial", 10),
            bg="#ecf0f1",
            selectbackground="#3498db"
        )
        history_scrollbar = ttk.Scrollbar(history_scroll_frame, orient=tk.VERTICAL)
        
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox.config(yscrollcommand=history_scrollbar.set)
        history_scrollbar.config(command=self.history_listbox.yview)
        
        # Mode frame
        mode_frame = ttk.Frame(main_frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(mode_frame, text="Angle Mode:").pack(side=tk.LEFT, padx=(0, 5))
        self.angle_mode_var = tk.StringVar(value="degrees")
        angle_combo = ttk.Combobox(
            mode_frame,
            textvariable=self.angle_mode_var,
            values=["degrees", "radians"],
            state="readonly",
            width=10
        )
        angle_combo.pack(side=tk.LEFT)
        angle_combo.bind("<<ComboboxSelected>>", self.change_angle_mode)
        
        # Memory indicator
        self.memory_label = ttk.Label(mode_frame, text="M: 0", font=("Arial", 10, "bold"))
        self.memory_label.pack(side=tk.RIGHT)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_buttons(buttons_frame)
        
        # Bind keyboard events
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
    
    def create_buttons(self, parent):
        """Create calculator buttons"""
        # Button style configuration
        style = ttk.Style()
        style.configure("Calc.TButton", font=("Arial", 12, "bold"))
        style.configure("Scientific.TButton", font=("Arial", 10))
        style.configure("Operator.TButton", font=("Arial", 12, "bold"))
        
        # Button definitions
        buttons = [
            # Row 1: Memory and Clear functions
            [("MC", "memory_clear", "Scientific.TButton"), ("MR", "memory_recall", "Scientific.TButton"), 
             ("MS", "memory_store", "Scientific.TButton"), ("M+", "memory_add", "Scientific.TButton"),
             ("M-", "memory_subtract", "Scientific.TButton")],
            
            # Row 2: Scientific functions
            [("sin", "sin", "Scientific.TButton"), ("cos", "cos", "Scientific.TButton"), 
             ("tan", "tan", "Scientific.TButton"), ("ln", "ln", "Scientific.TButton"),
             ("log", "log", "Scientific.TButton")],
            
            # Row 3: More functions
            [("√", "sqrt", "Scientific.TButton"), ("x²", "square", "Scientific.TButton"),
             ("xʸ", "power", "Scientific.TButton"), ("x!", "factorial", "Scientific.TButton"),
             ("π", "pi", "Scientific.TButton")],
            
            # Row 4: Clear and operations
            [("C", "clear", "Operator.TButton"), ("CE", "clear_entry", "Operator.TButton"),
             ("⌫", "backspace", "Operator.TButton"), ("÷", "/", "Operator.TButton"),
             ("(", "(", "Calc.TButton")],
            
            # Row 5: Numbers and operations
            [("7", "7", "Calc.TButton"), ("8", "8", "Calc.TButton"),
             ("9", "9", "Calc.TButton"), ("×", "*", "Operator.TButton"),
             (")", ")", "Calc.TButton")],
            
            # Row 6
            [("4", "4", "Calc.TButton"), ("5", "5", "Calc.TButton"),
             ("6", "6", "Calc.TButton"), ("−", "-", "Operator.TButton"),
             ("e", "e", "Scientific.TButton")],
            
            # Row 7
            [("1", "1", "Calc.TButton"), ("2", "2", "Calc.TButton"),
             ("3", "3", "Calc.TButton"), ("+", "+", "Operator.TButton"),
             ("±", "negate", "Operator.TButton")],
            
            # Row 8
            [("0", "0", "Calc.TButton"), (".", ".", "Calc.TButton"),
             ("=", "equals", "Operator.TButton"), ("", "", ""), ("", "", "")]
        ]
        
        for i, row in enumerate(buttons):
            for j, (text, command, style_name) in enumerate(row):
                if text:  # Skip empty cells
                    if text == "0":
                        colspan = 2
                    elif text == "=":
                        rowspan = 2
                        button = ttk.Button(
                            parent,
                            text=text,
                            style=style_name,
                            command=lambda cmd=command: self.button_click(cmd)
                        )
                        button.grid(row=i, column=j, rowspan=rowspan, sticky="nsew", padx=2, pady=2)
                        continue
                    else:
                        colspan = 1
                    
                    button = ttk.Button(
                        parent,
                        text=text,
                        style=style_name,
                        command=lambda cmd=command: self.button_click(cmd)
                    )
                    button.grid(row=i, column=j, columnspan=colspan, sticky="nsew", padx=2, pady=2)
        
        # Configure grid weights
        for i in range(8):
            parent.rowconfigure(i, weight=1)
        for j in range(5):
            parent.columnconfigure(j, weight=1)
    
    def button_click(self, command):
        """Handle button clicks"""
        try:
            if command.isdigit() or command == ".":
                self.input_number(command)
            elif command in ["+", "-", "*", "/", "(", ")"]:
                self.input_operator(command)
            elif command == "equals":
                self.calculate()
            elif command == "clear":
                self.clear_all()
            elif command == "clear_entry":
                self.clear_entry()
            elif command == "backspace":
                self.backspace()
            elif command == "negate":
                self.negate()
            elif command == "pi":
                self.input_constant("π")
            elif command == "e":
                self.input_constant("e")
            elif command in ["sin", "cos", "tan", "ln", "log", "sqrt"]:
                self.input_function(command)
            elif command == "square":
                self.input_operator("^2")
            elif command == "power":
                self.input_operator("^")
            elif command == "factorial":
                self.input_function("factorial")
            elif command.startswith("memory"):
                self.handle_memory(command)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def input_number(self, num):
        """Input numbers and decimal point"""
        if self.result_displayed:
            self.current_input = num
            self.result_displayed = False
        else:
            if num == "." and "." in self.current_input.split()[-1]:
                return  # Prevent multiple decimal points
            self.current_input += num
        
        self.update_display()
    
    def input_operator(self, op):
        """Input operators"""
        if self.result_displayed:
            self.result_displayed = False
        
        if op == "^2":
            self.current_input += "^2"
        else:
            self.current_input += f" {op} "
        
        self.update_display()
    
    def input_function(self, func):
        """Input mathematical functions"""
        if self.result_displayed:
            self.current_input = f"{func}("
            self.result_displayed = False
        else:
            self.current_input += f"{func}("
        
        self.update_display()
    
    def input_constant(self, const):
        """Input mathematical constants"""
        if self.result_displayed:
            self.current_input = const
            self.result_displayed = False
        else:
            self.current_input += const
        
        self.update_display()
    
    def calculate(self):
        """Perform calculation"""
        if not self.current_input:
            return
        
        try:
            # Clean up the expression
            expression = self.current_input.replace("×", "*").replace("÷", "/").replace("−", "-")
            
            result = self.calc.evaluate_expression(expression)
            
            # Format result
            if abs(result) < 1e-10:
                result = 0
            
            if result == int(result):
                formatted_result = str(int(result))
            else:
                formatted_result = f"{result:.10g}"
            
            self.current_input = formatted_result
            self.result_displayed = True
            self.update_display()
            self.update_history()
            
        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))
            self.clear_all()
    
    def clear_all(self):
        """Clear all input"""
        self.current_input = ""
        self.display_var.set("0")
        self.result_displayed = False
    
    def clear_entry(self):
        """Clear current entry"""
        self.current_input = ""
        self.display_var.set("0")
    
    def backspace(self):
        """Remove last character"""
        if self.current_input:
            self.current_input = self.current_input[:-1]
            self.update_display()
    
    def negate(self):
        """Change sign of current number"""
        if self.current_input:
            try:
                value = float(self.current_input)
                self.current_input = str(-value)
                self.update_display()
            except ValueError:
                pass
    
    def handle_memory(self, command):
        """Handle memory operations"""
        if command == "memory_clear":
            self.calc.memory_clear()
        elif command == "memory_recall":
            self.current_input = str(self.calc.memory_recall())
            self.update_display()
        elif command == "memory_store":
            if self.current_input:
                try:
                    value = float(self.current_input)
                    self.calc.memory_store(value)
                except ValueError:
                    pass
        elif command == "memory_add":
            if self.current_input:
                try:
                    value = float(self.current_input)
                    self.calc.memory_add(value)
                except ValueError:
                    pass
        elif command == "memory_subtract":
            if self.current_input:
                try:
                    value = float(self.current_input)
                    self.calc.memory_subtract(value)
                except ValueError:
                    pass
        
        self.update_memory_display()
    
    def change_angle_mode(self, event=None):
        """Change angle mode between degrees and radians"""
        self.calc.angle_mode = self.angle_mode_var.get()
    
    def update_display(self):
        """Update the display"""
        if self.current_input:
            self.display_var.set(self.current_input)
        else:
            self.display_var.set("0")
    
    def update_memory_display(self):
        """Update memory indicator"""
        memory_value = self.calc.memory_recall()
        if memory_value == 0:
            self.memory_label.config(text="M: 0")
        else:
            self.memory_label.config(text=f"M: {memory_value:.6g}")
    
    def update_history(self):
        """Update history display"""
        self.history_listbox.delete(0, tk.END)
        history = self.calc.get_history()
        for item in history[-10:]:  # Show last 10 items
            self.history_listbox.insert(tk.END, item)
        self.history_listbox.see(tk.END)
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.keysym
        char = event.char
        
        if char.isdigit() or char == ".":
            self.button_click(char)
        elif char in "+-*/()":
            self.button_click(char)
        elif key == "Return" or key == "KP_Enter":
            self.button_click("equals")
        elif key == "BackSpace":
            self.button_click("backspace")
        elif key == "Delete" or key == "Escape":
            self.button_click("clear")
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()


class CalculatorCLI:
    """Command Line Interface for the calculator"""
    
    def __init__(self):
        self.calc = Calculator()
    
    def print_menu(self):
        """Print the main menu"""
        print("\n" + "="*50)
        print("      PROFESSIONAL CALCULATOR")
        print("="*50)
        print("1. Basic Calculator")
        print("2. Scientific Calculator")
        print("3. Expression Evaluator")
        print("4. Memory Operations")
        print("5. View History")
        print("6. Settings")
        print("7. Help")
        print("8. Exit")
        print("="*50)
    
    def basic_calculator(self):
        """Basic calculator operations"""
        print("\nBasic Calculator Mode")
        print("Available operations: +, -, *, /, ^, sqrt")
        
        while True:
            try:
                print("\nEnter 'back' to return to main menu")
                a = input("Enter first number: ")
                if a.lower() == 'back':
                    break
                a = float(a)
                
                operation = input("Enter operation (+, -, *, /, ^, sqrt): ").strip()
                
                if operation == "sqrt":
                    result = self.calc.square_root(a)
                    print(f"√{a} = {result}")
                else:
                    b = float(input("Enter second number: "))
                    
                    if operation == "+":
                        result = self.calc.add(a, b)
                    elif operation == "-":
                        result = self.calc.subtract(a, b)
                    elif operation == "*":
                        result = self.calc.multiply(a, b)
                    elif operation == "/":
                        result = self.calc.divide(a, b)
                    elif operation == "^":
                        result = self.calc.power(a, b)
                    else:
                        print("Invalid operation!")
                        continue
                    
                    print(f"{a} {operation} {b} = {result}")
                
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
    
    def scientific_calculator(self):
        """Scientific calculator operations"""
        print("\nScientific Calculator Mode")
        print("Available functions: sin, cos, tan, asin, acos, atan, log, ln, factorial")
        
        while True:
            try:
                print("\nEnter 'back' to return to main menu")
                func = input("Enter function: ").strip().lower()
                if func == 'back':
                    break
                
                if func in ['sin', 'cos', 'tan']:
                    x = float(input("Enter angle: "))
                    result = getattr(self.calc, func)(x)
                    print(f"{func}({x}) = {result}")
                
                elif func in ['asin', 'acos', 'atan']:
                    x = float(input("Enter value: "))
                    result = getattr(self.calc, func)(x)
                    print(f"{func}({x}) = {result}")
                
                elif func == 'log':
                    x = float(input("Enter number: "))
                    base_input = input("Enter base (press Enter for base 10): ").strip()
                    base = float(base_input) if base_input else None
                    result = self.calc.log(x, base)
                    base_str = base if base else 10
                    print(f"log_{base_str}({x}) = {result}")
                
                elif func == 'ln':
                    x = float(input("Enter number: "))
                    result = self.calc.ln(x)
                    print(f"ln({x}) = {result}")
                
                elif func == 'factorial':
                    x = int(input("Enter integer: "))
                    result = self.calc.factorial(x)
                    print(f"{x}! = {result}")
                
                else:
                    print("Invalid function!")
                
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
    
    def expression_evaluator(self):
        """Evaluate mathematical expressions"""
        print("\nExpression Evaluator Mode")
        print("You can use: +, -, *, /, ^, sqrt(), sin(), cos(), tan(), ln(), log(), π, e")
        print("Example: sin(30) + cos(60) * π")
        
        while True:
            try:
                print("\nEnter 'back' to return to main menu")
                expression = input("Enter expression: ").strip()
                if expression.lower() == 'back':
                    break
                
                result = self.calc.evaluate_expression(expression)
                print(f"Result: {result}")
                
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
    
    def memory_operations(self):
        """Memory operations"""
        while True:
            print(f"\nMemory Operations (Current: {self.calc.memory_recall()})")
            print("1. Store (MS)")
            print("2. Recall (MR)")
            print("3. Add (M+)")
            print("4. Subtract (M-)")
            print("5. Clear (MC)")
            print("6. Back to main menu")
            
            choice = input("Choose option: ").strip()
            
            try:
                if choice == "1":
                    value = float(input("Enter value to store: "))
                    self.calc.memory_store(value)
                    print(f"Stored {value} in memory")
                
                elif choice == "2":
                    value = self.calc.memory_recall()
                    print(f"Memory value: {value}")
                
                elif choice == "3":
                    value = float(input("Enter value to add: "))
                    self.calc.memory_add(value)
                    print(f"Added {value} to memory")
                
                elif choice == "4":
                    value = float(input("Enter value to subtract: "))
                    self.calc.memory_subtract(value)
                    print(f"Subtracted {value} from memory")
                
                elif choice == "5":
                    self.calc.memory_clear()
                    print("Memory cleared")
                
                elif choice == "6":
                    break
                
                else:
                    print("Invalid option!")
                    
            except ValueError:
                print("Invalid input!")
    
    def view_history(self):
        """View calculation history"""
        history = self.calc.get_history()
        if not history:
            print("\nNo calculations in history")
        else:
            print("\nCalculation History:")
            print("-" * 30)
            for i, item in enumerate(history, 1):
                print(f"{i}. {item}")
        
        input("\nPress Enter to continue...")
    
    def settings(self):
        """Calculator settings"""
        while True:
            print(f"\nSettings (Current angle mode: {self.calc.angle_mode})")
            print("1. Change angle mode")
            print("2. Clear history")
            print("3. Back to main menu")
            
            choice = input("Choose option: ").strip()
            
            if choice == "1":
                if self.calc.angle_mode == "degrees":
                    self.calc.angle_mode = "radians"
                    print("Angle mode changed to radians")
                else:
                    self.calc.angle_mode = "degrees"
                    print("Angle mode changed to degrees")
            
            elif choice == "2":
                self.calc.clear_history()
                print("History cleared")
            
            elif choice == "3":
                break
            
            else:
                print("Invalid option!")
    
    def show_help(self):
        """Show help information"""
        help_text = """
PROFESSIONAL CALCULATOR HELP
============================

BASIC OPERATIONS:
- Addition: +
- Subtraction: -
- Multiplication: *
- Division: /
- Power: ^
- Square root: sqrt()

SCIENTIFIC FUNCTIONS:
- Trigonometric: sin(), cos(), tan()
- Inverse trig: asin(), acos(), atan()
- Logarithms: log(), ln()
- Factorial: factorial()

CONSTANTS:
- π (pi): 3.14159...
- e (Euler's number): 2.71828...

EXPRESSION EXAMPLES:
- sin(30) + cos(60)
- 2^3 + sqrt(16)
- ln(e) + log(100)
- 5! / (3! * 2!)

MEMORY OPERATIONS:
- MS: Memory Store
- MR: Memory Recall
- M+: Memory Add
- M-: Memory Subtract
- MC: Memory Clear

ANGLE MODE:
- Degrees: Default mode
- Radians: For advanced calculations

Press Enter to continue...
        """
        print(help_text)
        input()
    
    def run(self):
        """Run the CLI calculator"""
        print("Welcome to Professional Calculator!")
        
        while True:
            self.print_menu()
            choice = input("Choose an option (1-8): ").strip()
            
            if choice == "1":
                self.basic_calculator()
            elif choice == "2":
                self.scientific_calculator()
            elif choice == "3":
                self.expression_evaluator()
            elif choice == "4":
                self.memory_operations()
            elif choice == "5":
                self.view_history()
            elif choice == "6":
                self.settings()
            elif choice == "7":
                self.show_help()
            elif choice == "8":
                print("Thank you for using Professional Calculator!")
                break
            else:
                print("Invalid option! Please choose 1-8.")


def main():
    """Main function to choose interface"""
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # Run CLI version
        cli = CalculatorCLI()
        cli.run()
    else:
        # Run GUI version if available
        if GUI_AVAILABLE:
            try:
                gui = CalculatorGUI()
                gui.run()
            except Exception as e:
                print(f"GUI failed to start: {e}")
                print("Running CLI version...")
                cli = CalculatorCLI()
                cli.run()
        else:
            print("GUI not available (tkinter not installed). Running CLI version...")
            cli = CalculatorCLI()
            cli.run()


if __name__ == "__main__":
    main()