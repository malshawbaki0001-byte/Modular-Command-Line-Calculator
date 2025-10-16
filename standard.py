
import math
def get_number(message):
    """
        Prompts the user to enter a numeric value and validates the input.

        Parameters:
            message (str): The prompt message displayed to the user.

        Returns:
            float or None: The numeric value entered by the user, or None if invalid.
        """

    n = input(message)
    if not is_number(n):
        print("Error: Please enter a valid number.")
        return None
    return float(n)
def main_menu():
    """
       Displays the Standard Mode menu and handles user input for basic arithmetic operations.

       Available operations:
           1. Addition:       Adds two numbers.
           2. Subtraction:    Subtracts the second number from the first.
           3. Multiplication: Multiplies two numbers.
           4. Division:       Divides the first number by the second (non-zero).
           5. Modulus:        Computes the remainder of division (non-zero).
           6. Exponent:       Raises the first number to the power of the second.
           7. Square Root:    Computes the square root of a non-negative number.
           8. Reciprocal:     Computes 1 divided by the number (non-zero).
           9. Percentage:     Calculates (a × b%) as a percentage of a number.
          10. Exit:           Returns to the main menu.

       The function prompts the user to select an operation, validates input,
       performs the calculation using Python's math module, and displays the result.
       Handles invalid numeric input and domain errors gracefully.
       """
    while True:
        print("\n"
              "================== Standard Mode ===================")

        print(" 1. Addition (+)         |    6. Exponent (**)\n"
              " 2. Subtraction (-)      |    7. Square Root (√)\n"
              " 3. Multiplication (*)   |    8. Reciprocal (1/x)\n"
              " 4. Division (/)         |    9. Percentage (%)\n"
              " 5. Modulus (%)          |   10.Return to Main Menu"

)
        print("_"*52,"\n")
        choice = input("Enter your choice (1-10): ")
        print("-"*29,'\n')
        if choice == "10":

            print("Exiting Standard Mode . Returning to Main Menu...")
            print("-" * 52, )

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
                    print("\nError: Cannot divide by zero.\n"
                           ,"-----------------------------\n")

                    continue
                result = num1 / num2
            elif choice == "5":
                if num2 == 0:
                    print("\nError: Cannot divide by zero.\n"
                           ,"-----------------------------\n")
                    continue
                result = num1 % num2
            elif choice == "6":
                result = num1 ** num2
            print("Result:", result)

        elif choice == "7":
            num = get_number("Enter a number: ")
            if num is None:
                continue
            if num < 0:
                print(
                "\nError: Cannot take square root of a negative number in Standard Mode.\n"
                 ,"---------------------------------------------------------------------\n")

            else:
                print(f"Result: {math.sqrt(num)}"
            )

        elif choice == "8":
            num = get_number("Enter a number: ")
            if num is None:
                continue
            if num == 0
                print(
                "\nError: Cannot divide by zero.\n"
               ,"-------------------------------\n")
            else:
                print(f"Result: {1 / num}"
            )

        elif choice == "9":
            a = get_number("Enter the number: ")
            b = get_number("Enter percentage (%): ")
            if a is None or b is None:
                continue
            print("Result:", (a * b) / 100)
        else:
            print("\nInvalid choice. Please enter a number from 1 to 10.\n"
                    ,"--------------------------------------------------\n")


def is_number(value):
    """Returns True if value can be converted to a number."""
    try:
        float(value)
        return True
    except:
        return False
