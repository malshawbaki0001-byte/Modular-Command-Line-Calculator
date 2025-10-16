import math

def scientific_main_menu():
    while True:
        print("\n--- Scientific Mode Menu ---")
        print("1. sin(x)  (Angle in Degrees)")
        print("2. cos(x)  (Angle in Degrees)")
        print("3. log10(x)")
        print("4. exp(x) ")
        print("5. Exit Scientific Mode")
        print("-" * 28)

        choice = input("Enter your choice: ")

        if choice == '5':
            print("Exiting scientific mode. Returning to main menu.")
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

