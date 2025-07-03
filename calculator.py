# Main file for the professional calculator
import math

def display_menu():
    """Displays the calculator menu to the user."""
    print("\n--- ماشین حساب حرفه‌ای ---")
    print("عملیات مورد نظر را انتخاب کنید:")
    print("1. جمع (+)")
    print("2. تفریق (-)")
    print("3. ضرب (*)")
    print("4. تقسیم (/)")
    print("5. توان (^)")
    print("6. جذر (sqrt)")
    print("7. لگاریتم مبنای 10 (log10)")
    print("8. سینوس (sin)")
    print("9. کسینوس (cos)")
    print("10. تانژانت (tan)")
    print("0. خروج")

def get_user_choice():
    """Gets the user's choice for an operation."""
    while True:
        try:
            choice = input("انتخاب شما (0-10): ")
            if choice.strip() == "": # Handle empty input
                print("ورودی نمی‌تواند خالی باشد. لطفاً یک عدد وارد کنید.")
                continue
            choice = int(choice)
            if 0 <= choice <= 10:
                return choice
            else:
                print("انتخاب نامعتبر است. لطفاً عددی بین 0 تا 10 وارد کنید.")
        except ValueError:
            print("ورودی نامعتبر است. لطفاً یک عدد وارد کنید.")

def get_number_input(prompt):
    """Gets a number input from the user."""
    while True:
        try:
            num_str = input(prompt)
            if num_str.strip() == "": # Handle empty input
                print("ورودی نمی‌تواند خالی باشد. لطفاً یک عدد وارد کنید.")
                continue
            return float(num_str)
        except ValueError:
            print("ورودی نامعتبر است. لطفاً یک عدد معتبر وارد کنید.")

# --- Basic Arithmetic Functions ---
def add(x, y):
    """Adds two numbers."""
    return x + y

def subtract(x, y):
    """Subtracts the second number from the first."""
    return x - y

def multiply(x, y):
    """Multiplies two numbers."""
    return x * y

def divide(x, y):
    """Divides the first number by the second.
    Handles division by zero.
    """
    if y == 0:
        return "خطا: تقسیم بر صفر امکان‌پذیر نیست."
    return x / y

# --- Advanced Functions ---
def power(x, y):
    """Calculates x raised to the power of y."""
    return x ** y

def square_root(x):
    """Calculates the square root of x.
    Handles negative input.
    """
    if x < 0:
        return "خطا: جذر عدد منفی تعریف نشده است (در اعداد حقیقی)."
    return math.sqrt(x)

def log10(x):
    """Calculates the base-10 logarithm of x.
    Handles non-positive input.
    """
    if x <= 0:
        return "خطا: لگاریتم برای اعداد غیر مثبت تعریف نشده است."
    return math.log10(x)

def sine(x_degrees):
    """Calculates the sine of x in degrees."""
    return math.sin(math.radians(x_degrees))

def cosine(x_degrees):
    """Calculates the cosine of x in degrees."""
    return math.cos(math.radians(x_degrees))

def tangent(x_degrees):
    """Calculates the tangent of x in degrees.
    Handles angles where tangent is undefined (e.g., 90, 270 degrees).
    """
    if x_degrees % 180 == 90: # Check for 90, 270, etc.
        return "خطا: تانژانت برای این زاویه تعریف نشده است."
    return math.tan(math.radians(x_degrees))


def calculator():
    """Main function to run the calculator."""
    while True:
        display_menu()
        choice = get_user_choice()

        if choice == 0:
            print("از ماشین حساب خارج شدید. خدانگهدار!")
            break

        result = None

        if choice in [1, 2, 3, 4, 5]: # Operations requiring two numbers
            num1 = get_number_input("عدد اول را وارد کنید: ")
            num2 = get_number_input("عدد دوم را وارد کنید: ")
            if choice == 1:
                result = add(num1, num2)
            elif choice == 2:
                result = subtract(num1, num2)
            elif choice == 3:
                result = multiply(num1, num2)
            elif choice == 4:
                result = divide(num1, num2)
            elif choice == 5:
                result = power(num1, num2)
        elif choice in [6, 7, 8, 9, 10]: # Operations requiring one number
            num = get_number_input("عدد را وارد کنید (برای توابع مثلثاتی، زاویه به درجه): ")
            if choice == 6:
                result = square_root(num)
            elif choice == 7:
                result = log10(num)
            elif choice == 8:
                result = sine(num)
            elif choice == 9:
                result = cosine(num)
            elif choice == 10:
                result = tangent(num)

        if result is not None:
            print("نتیجه: ", result)

        # Ask if user wants to continue
        # continue_choice = input("\nآیا می‌خواهید محاسبه دیگری انجام دهید؟ (بله/خیر): ").lower()
        # if continue_choice not in ['بله', 'bale', 'yes', 'y']:
        #     print("از ماشین حساب خارج شدید. خدانگهدار!")
        #     break

if __name__ == "__main__":
    calculator()
