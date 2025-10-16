def main_menu() :
    """
       Displays the Converter Mode menu and handles user input for unit conversions.

       Available conversion categories:
           1. Length: Converts between meters (m), centimeters (cm), feet (ft), and inches (in).
           2. Weight: Converts between kilograms (kg), grams (g), pounds (lb), and ounces (oz).
           3. Temperature: Converts between Celsius (C), Fahrenheit (F), and Kelvin (K).
           4. Exit: Returns to the main menu.

       The function prompts the user to select a conversion category, then requests
       source and target units along with a numeric value. It validates input, performs
       the conversion using predefined formulas, and displays the result.

       Handles invalid unit selections, negative values (where not allowed), and
       non-numeric input gracefully.
       """


while True:
    print("--- Converter Mode ---")
    print("1. Length (m, cm, ft, in)")
    print("2. Weight (kg, g, lb, oz)")
    print("3. Temperature (C, F, K)")
    print("4. Exit Converter Mode")
    print("-"*22)
    choice = input("Select (1 to 4): ")
    print("-" * 22,"\n")
    if choice == "1":
        print("\n"
              "----------------- Length -----------------\n")
        from_unit = input(""
              "Select your value unit from (m/cm/ft/in): ").lower()# use [.lower()] helps To avoid input errors ##ALSHOBAKI##
        value = float(input("Enter the value: "))
        to_unit = input("Select the unit you want to convert the value to (m/cm/ft/in): ").lower()

        if from_unit not in ["m", "cm", "ft", "in"] or to_unit not in ["m", "cm", "ft", "in"]:
            print(" Units must be one of: m, cm, ft, in")
            continue

        if value < 0:
            print(" Length can't be negative.")
            continue

        if from_unit == "m":
            meter = value * 1
        elif from_unit == "cm":
            meter = value * 0.01
        elif from_unit == "ft":
            meter = value * 0.3048
        elif from_unit == "in":
            meter = value * 0.0254

        if to_unit == "m":
            result = meter * 1
        elif to_unit == "cm":
            result = meter * 100
        elif to_unit == "ft":
            result = meter * 3.28084
        elif to_unit == "in":
            result = meter * 39.3701

        print(f" {value} {from_unit} = {result:.2f} {to_unit}")

    elif choice == "2":
        print("\n\n"
              "----------------- Weight -----------------\n")
        from_unit = input(""
              "Select your value unit from (kg/g/lb/oz): ").lower()# use [.lower()] helps To avoid input errors ##ALSHOBAKI##
        value = float(input("Enter the value: "))
        to_unit = input("Select the unit you want to convert the value to (kg/g/lb/oz): ").lower()

        if from_unit not in ["kg", "g", "lb", "oz"] or to_unit not in ["kg", "g", "lb", "oz"]:
            print(" Units must be one of: kg, g, lb, oz")
            continue

        if value < 0:
            print(" Weight can't be negative.")
            continue

        if from_unit == "kg":
            kg = value * 1
        elif from_unit == "g":
            kg = value * 0.001
        elif from_unit == "lb":
            kg = value * 0.453592
        elif from_unit == "oz":
            kg = value * 0.0283495

        if to_unit == "kg":
            result = kg * 1
        elif to_unit == "g":
            result = kg * 1000
        elif to_unit == "lb":
            result = kg * 2.20462
        elif to_unit == "oz":
            result = kg * 35.274

        print(f" {value} {from_unit} = {result:.2f} {to_unit}")

    elif choice == "3":
        print("\n\n"
              "-------------- Temperature --------------\n")

        from_unit = input(""
              "Select your value unit from (C , F or K): ").upper()# # use [.upper()] helps To avoid input errors ##ALSHOBAKI##
        value = float(input("Enter the value: "))
        to_unit = input("\n Select the unit you want to convert the value to w (C , F or K): ").upper()

        if from_unit not in ["C", "F", "K"] or to_unit not in ["C", "F", "K"]:
            print(" Units must be one of: C, F, K")
            continue

        if from_unit == "C":
            celsius = value
        elif from_unit == "F":
            celsius = (value - 32) * 5 / 9
        elif from_unit == "K":
            celsius = value - 273.15

        if to_unit == "C":
            result = celsius
        elif to_unit == "F":
            result = (celsius * 9 / 5) + 32
        elif to_unit == "K":
            result = celsius + 273.15

        print(f"{value} {from_unit} = {result:.2f} {to_unit}")

    elif choice == "4":
        print("Exiting Converter Mode. Returning to Main Menu. ")
        break

    else:
        print(" Invalid choice. Please select from 1 to 4.")
