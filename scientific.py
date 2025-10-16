import math

def main_menu():
    """
        Displays the Scientific Mode menu and handles user input for mathematical operations.

        Offers the following functions:
            1. sin(x): Calculates the sine of an angle in degrees.
            2. cos(x): Calculates the cosine of an angle in degrees.
            3. log10(x): Computes the base-10 logarithm of a positive number.
            4. exp(x): Calculates the exponential value e^x.
            5. Exit: Returns to the main menu.

        The function prompts the user to select an operation, validates input,
        performs the calculation using the math module, and displays the result.
        Handles invalid numeric input and domain errors gracefully.
        """

    while True:
        print("\n----- Scientific Mode Menu -----")
        print("1. sin(x)  (Angle in Degrees)")
        print("2. cos(x)  (Angle in Degrees)")
        print("3. log10(x)")
        print("4. exp(x) ")
        print("5. Exit Scientific Mode")
        print("-" * 32)

        choice = input("Enter your choice: ")

        print("-" * 32,'\n')

        if choice == '5':

            print("Exiting Scientific Mode. Returning to Main Menu.")

            break

        try:

            if choice == '1':

                x = float(input("Enter angle in degrees: "))

                result = math.sin(math.radians(x))

                print(f"Result: {round(result, 4)}\n")

            elif choice == '2':

                x = float(input("Enter angle in degrees: "))

                result = math.cos(math.radians(x))

                print(f"Result: {round(result, 4)}\n")

            elif choice == '3':

                x = float(input("Enter x: "))
                if x <= 0:
                    print("Error: Logarithm is undefined for non-positive numbers.\n")
                else:
                    result = math.log10(x)
                    print(f"Result: {round(result, 4)}\n")
            elif choice == '4':
                x = float(input("Enter x: "))
                result = math.exp(x)
                print(f"Result: {round(result, 4)}\n")
            else:
                print("Invalid choice. Please choose a number from 1 to 5.\n")
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")


