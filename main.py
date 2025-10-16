


while True:

    print("==== Welcome to Multi-Mode Calculator ===="
          "\n1. Standard Mode "
          "\n2. Programmer Mode "
          "\n3. Scientific Mode "
          "\n4. Converter Mode "
          "\n5. Exit ")
    print("-"*42)

    model=int(input("Enter your choice number: "))

    print("-"*27)


    if model ==1:

        '''This mode handles basic arithmetic operations
         , similar to a simple calculator.
                '''
        import standard
        
        print("\n")
        
        standard.main_menu()

    elif model ==2:

        '''This mode focuses on operations useful for
                 programmers, including base conversions and 
                bitwise operations.
                '''
        import programmer

        print("\n")

        programmer.main_menu()

    elif model ==3:
      
        '''This mode includes advanced mathematical 
               functions, leveraging Python's math module.
               '''
        import scientific
        
        
        scientific.main_menu()
    
        print("\n")

    elif model ==4:

        '''This mode handles unit conversions
                across categories.
                '''
        import converter
       
        print("\n")
       
        converter.main_menu()
       
    elif model ==5:
        print("\n\n\n\n\n")

        print("-"*46,"\n| Thank you for using Multi-Mode Calculator  |\n"+"-"*46)
        break

    else:
        print("Invalid input. Please enter a number between 1 and 5.")
