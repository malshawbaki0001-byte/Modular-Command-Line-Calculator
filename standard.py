
import math
def get_number(message):
    n = input(message)
    if not is_number(n):
        print("Error: Please enter a valid number.")
        return None
    return float(n)
def main_menu():
    print("\n=== Standard Mode ===")
    while True:
        print("""
1. Addition (+)
2. Subtraction (-)
3. Multiplication (*)
4. Division (/)
5. Modulus (%)
6. Exponent (**)
7. Square Root (√)
8. Reciprocal (1/x)
9. Percentage (%)
10. Return to Main Menu
""")
        choice = input("Enter your choice (1-10): ")
        if choice == "10":
            print("Returning to Main Menu...")
            break

        if choice in ["1", "2", "3", "4", "5", "6"]:
            num1 = get_number("Enter first number: ")
            num2 = get_number("Enter second number: ")
            if num1 is None or num2 is None:
                continue

            if choice == "1":
                result = num1 + num2
            elif choice == "2":
                result = num1 - num2
            elif choice == "3":
                result = num1 * num2
            elif choice == "4":
                if num2 == 0:
                    print("Error: Cannot divide by zero.")
                    continue
                result = num1 / num2
            elif choice == "5":
                if num2 == 0:
                    print("Error: Cannot divide by zero.")
                    continue
                result = num1 % num2
            elif choice == "6":
                result = num1 ** num2
            print("Result:", result)

        elif choice == "7":
            num = get_number("Enter a number: ")
            if num is None:
                continue
            print(
                "Error: Cannot take square root of a negative number in Standard Mode."
                if num < 0 else f"Result: {math.sqrt(num)}"
            )

        elif choice == "8":
            num = get_number("Enter a number: ")
            if num is None:
                continue
            print(
                "Error: Cannot divide by zero."
                if num == 0 else f"Result: {1 / num}"
            )

        elif choice == "9":
            a = get_number("Enter the number: ")
            b = get_number("Enter percentage (%): ")
            if a is None or b is None:
                continue
            print("Result:", (a * b) / 100)
        else:
            print("Invalid choice. Please enter a number from 1 to 10.")


def is_number(value):
    """Returns True if value can be converted to a number."""
    try:
        float(value)
        return True
    except:
        return False

