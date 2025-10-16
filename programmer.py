def to_base(num, base):
    """Convert integer to string in given base (2, 8, 10, 16)."""
    if base == 2:
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
    """Convert string from given base to decimal integer."""
    try:
        return int(num_str, base)
    except ValueError:
        return None

def input_int(prompt):
    """Safely get an integer input."""
    try:
        return int(input(prompt))
    except ValueError:
        print("Error: Please enter a valid integer.")
        return None

def base_conversion():
    print("\nBase Conversion Options:")
    print("1. Decimal to Binary/Octal/Hex")
    print("2. Binary/Octal/Hex to Decimal")
    choice = input("Enter choice: ").strip()

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

def main():
    print("=== Programmer Mode ===")
    while True:
        print("\nMenu:")
        print("1. Base Conversion")
        print("2. Bitwise Operations")
        print("3. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            base_conversion()
        elif choice == "2":
            bitwise_operations()
        elif choice == "3":
            print("Exiting Programmer Mode...")
            break
        else:
            print("Error: Invalid choice.")

if __name__ == "__main__":
    main()

