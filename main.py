# import standard
# import programmer
# import scientific
# import converter


while True:

    print("Welcome to Multi-Mode Calculator "
          "\n1. Standard Mode "
          "\n2. Programmer Mode "
          "\n3. Scientific Mode "
          "\n4. Converter Mode "
          "\n5. Exit ")

    model=eval(input("Enter your choice number: "))


    if model ==1:
        # import standard

        #standard.

        '''This mode handles basic arithmetic operations
        , similar to a simple calculator.
        '''
    elif model ==2:
        #import programmer

        #programmer

        '''This mode focuses on operations useful for
         programmers, including base conversions and 
        bitwise operations.
        '''
    elif model ==3:
        #import scientific

        #scientific

        '''This mode includes advanced mathematical 
        functions, leveraging Python's math module.
        '''
    elif model ==4:
        #import converter

        #converter

        '''This mode handles unit conversions
         across categories.
         '''
    elif model ==5:

        break

    else:
        print("invalid input")



