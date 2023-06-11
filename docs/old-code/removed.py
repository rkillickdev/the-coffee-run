# Loops over user_order items list and gets values from each dictionary

for dict in user_order.items:
    for key, value in dict.items():
        print(f"{value.get('Quantity')} X {value.get('Coffee')} with {value.get('Milk')} milk: £{value.get('Price')}")


# Takes yes/ no inputs and validates

 while True:
    print(f"Would you like to add any more drinks to your order?\n")

    selected_code = input("Enter y/n here:\n")

    if validate_data(selected_code, ["y", "n"]):
        break

    if selected_code == 'y':
        main()
    else:
        while True:
            print("Would you like to remove any items from your order?\n")

            selected_code = input("Enter y/n here:\n")

            if validate_data(selected_code, ["y", "n"]):
                break
    if selected_code == 'y':
        edit_order()     
    else:
        return False

# This validation code was causing a bug "selected_code not defined."
# Fixed by adding a third parameter to the function.  See new code

def validate_data(user_input, expected_values):
    """
    Raises ValueError if user_input is not found in list of expected_values.
    """

    try:
        if user_input not in expected_values:
            if user_input == selected_code:
                raise ValueError(
                    "This code is not valid"
                )
            elif user_input == selected_quantity:
                raise ValueError(
                    "This value is not valid, please enter a number between 1 and 10"
                )                                       
    except ValueError as e:
            print(f"Something went wrong. {e}. Please try again.")
            return False

    return True