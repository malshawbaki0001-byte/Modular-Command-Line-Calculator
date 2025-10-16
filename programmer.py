def to_base(num, base):
    """
     Converts a decimal integer to a string representation in the specified base.

     Parameters:
         num (int): The decimal number to convert.
         base (int): The target base (must be one of 2, 8, 10, or 16).

     Returns:
         str: The number represented in the target base as a string.
              Returns an error message if the base is invalid.
     """

    if base == 2:
        ''' the use of [2:] to remove the type of the new 
        base for example
         bin(2) = '0b10',      
        so we remove '0b' '''
        return bin(num)[2:]

    elif base == 8:
        return oct(num)[2:]
    elif base == 10:
        return str(num)
    elif base == 16:
        return hex(num)[2:].upper()
    else:
        return "Error: Invalid base."

def from_base(num_str, base):
    """
      Converts a number string from a given base to its decimal integer value.

      Parameters:
          num_str (str): The number represented as a string in the given base.
          base (int): The base of the input number (2, 8, 10, or 16).

      Returns:
          int or None: The decimal integer value, or None if the input is invalid.
      """
    try:
        return int(num_str, base)
    except ValueError:
        return None

def input_int(prompt):
    """
    Prompts the user to enter an integer and validates the input.

    Parameters:
        prompt (str): The message displayed to the user.

    Returns:
        int or None: The entered integer, or None if the input is invalid.
    """
    try:
        return int(input(prompt))
    except ValueError:
        print("Error: Please enter a valid integer.")
        return None

def base_conversion():
    """
     Handles base conversion operations in Programmer Mode.

     Options:
         1. Converts a decimal number to binary, octal, or hexadecimal.
         2. Converts a binary, octal, or hexadecimal number to decimal.

     Prompts the user for input, validates base and number formats,
     and displays the conversion result or appropriate error messages.
     """

    print("\nBase Conversion Options:")
    print("1. Decimal to Binary/Octal/Hex")
    print("2. Binary/Octal/Hex to Decimal")
    choice = input("Enter choice (1 or 2 ): ").strip()

    if choice == "1":
        n = input_int("Enter decimal: ")
        if n is None:
            return
        print("Choose target base (2, 8, 16): ", end="")
        try:
            b = int(input().strip())
        except ValueError:
            print("Error: Invalid base.")
            return
        if b not in [2, 8, 16]:
            print("Error: Invalid base.")
            return
        print(f"Result: {to_base(n, b)}")

    elif choice == "2":
        base_str = input("Enter source base (2, 8, 16): ").strip()
        if not base_str.isdigit() or int(base_str) not in [2, 8, 16]:
            print("Error: Invalid base.")
            return
        b = int(base_str)
        num_str = input(f"Enter number in base {b}: ").strip()
        val = from_base(num_str, b)
        if val is None:
            print("Error: Invalid number for this base.")
        else:
            print(f"Decimal: {val}")
    else:
        print("Error: Invalid choice.")

def bitwise_operations():
    """
     Performs bitwise operations between integers.

     Available operations:
         1. AND (&)
         2. OR (|)
         3. XOR (^)
         4. NOT (~)
         5. Left Shift (<<)
         6. Right Shift (>>)

     Prompts the user to select an operation and enter operands.
     Validates input and displays the result or error messages.
     """

    print("\nBitwise Operations:")
    print("1. AND (&)")
    print("2. OR (|)")
    print("3. XOR (^)")
    print("4. NOT (~)")
    print("5. Left Shift (<<)")
    print("6. Right Shift (>>)")
    choice = input("Enter choice: ").strip()

    if choice in ["1", "2", "3"]:
        a = input_int("Enter first integer: ")
        b = input_int("Enter second integer: ")
        if a is None or b is None:
            return
        if choice == "1":
            print(f"Result: {a & b}")
        elif choice == "2":
            print(f"Result: {a | b}")
        elif choice == "3":
            print(f"Result: {a ^ b}")

    elif choice == "4":
        a = input_int("Enter integer: ")
        if a is None:
            return
        print(f"Result: {~a}")

    elif choice in ["5", "6"]:
        a = input_int("Enter integer: ")
        b = input_int("Enter shift amount: ")
        if a is None or b is None:
            return
        if choice == "5":
            print(f"Result: {a << b}")
        elif choice == "6":
            print(f"Result: {a >> b}")
    else:
        print("Error: Invalid choice.")

def main_menu():
    print("=== Programmer Mode ===")
    while True:
        print("\nMenu:")
        print("1. Base Conversion")
        print("2. Bitwise Operations")
        print("3. Exit")
        choice = input("Enter choice (1, 2 or 3): ").strip()
        if choice == "1":
            base_conversion()
        elif choice == "2":
            bitwise_operations()
        elif choice == "3":
            print("Exiting Programmer Mode...")
            break
        else:
            print("Error: Invalid choice.")


