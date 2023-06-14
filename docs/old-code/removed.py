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


    def remove_options(keys):
    """
    Original workings for this function with much experimentation!
    """

    options = list(range(len(user_order.items)))
    # Generates a key based on the number of items already in the order
    # key = [len(user_order.items) + 1]
    keys = [i + 1 for i in options]
    # print(options)
    # print(keys)

    # Creates a dictionary using the item dictionary as the value.

    # new_dict = {k:v for item in user_order.items for k,v in item.items()}
    # for k, item in zip(keys, user_order.items):
    #     print(k)
    #     print(item)
    #     updated_dict = dict.fromkeys(keys, item.values())
    #     print(updated_dict)
    # new_list = []
    # for i, item in zip(options, user_order.items):
    # for item in user_order.items:
        # key = i+1
        # value = item.values()
        # item = dict.fromkeys(i, item.values())
        # new_list.append(item)
        # print(key)
        # print(value)
        # updated_dict = dict(key, value)
        # print(updated_dict)
    # print(new_list)
        # index = i
        # print(index)
        # key = item[index]
        # print(key)


    # print(options)

    while True:

        print("Which item of your order you would like to remove?")

        selected_code = int(input("Enter a number here:\n"))

        if validate_data(selected_code, keys):
            break

    index = selected_code - 1
    print(index)
    user_order.remove_item(index)
    update_order_dict()
    view_order()