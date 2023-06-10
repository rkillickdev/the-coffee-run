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