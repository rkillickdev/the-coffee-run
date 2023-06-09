import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from tabulate import tabulate

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('the_coffee_run')

order_list = []

def get_menu_choice(ingredient):
    """
    Pulls data from whatever sheet name is passed as an argument to the function.
    Assigns values to the variable data.
    Assigns index 0 of the variable data to the variable header_names.
    Assigns remaining indexes of variable data to the variable menu_content.  
    """

    menu = SHEET.worksheet(f"{ingredient}")
    data = menu.get_all_values()
    
    # Set first row of specified sheet as header names.
    header_names = data[0]

    # Assign rows from data to variable menu_content. 
    menu_content = data[1:]

    # Generate a list of code options to validate input against.
    code_options = []
    for row in menu_content:
        code = row[0]
        code_options.append(code)
    
    # Print menu as a table
    print(tabulate(menu_content, headers=header_names, tablefmt='fancy_grid')
     + "\n")
    # Assign user input to variable selected_code and check if valid.
    while True:
        print(f"Please select your {ingredient} by entering the code (1-4)\n")

        selected_code = input("Enter your choice here:\n")

        if validate_data(selected_code, code_options):
            break

    item = (data[int(selected_code)][1])
    unit_cost = (data[int(selected_code)][2])
    if ingredient == "coffee":
        print("Great, now let's get your coffee just how you like it!\n")
    return item, float(unit_cost)

def get_quantity():
    """
    Takes quantity input from user and returns as an integer.
    """

    # Assign user input to variable selected_quantity and check if valid.
    while True:

        print("Please select a quantity between 1 and 10\n")

        selected_quantity = input("Enter your choice here:\n")
        
        # Create a list of integers to pass as the expected_values argument.
        quantity_options = range(1, 11)

        if validate_data(selected_quantity, list(map(str, quantity_options))):
            break

    return int(selected_quantity)

def validate_data(user_input, expected_values):
    """
    Raises ValueError if user_input is not found in list of expected_values.
    """

    try:
        if user_input not in expected_values:
            raise ValueError(
                "This code is not valid"
            )
    except ValueError as e:
            print(f"Something went wrong. {e}. Please try again.")
            return False

    return True

def view_order():
    """
    Iterates over each dictionary stored in order_list and uses f string to
    print items currently in the order.
    """

    print("You're order currently contains the following:\n")
    for order in order_list:
        print(f"1 X {order.get('Coffee')} with {order.get('Milk')} milk: £{order.get('Price')}")

    while True:
        print(f"Would you like to add any more drinks to your order?\n")

        selected_code = input("Enter y/n here:\n")

        if validate_data(selected_code, ["y", "n"]):
            break

    if selected_code == 'y':
        main()
    else:
        return False
    
        
def display_final_order(order):
    """
    Accepts an instance of the class CompleteOrder as an argument.

    """

    # header_names = ["Coffee", "Milk", "Price"]
    # menu_content = order.items

    df = pd.DataFrame(order.items)

    print("Here is a summary of your order:\n")

    # print(menu_content)

    # Print final order as a table
    print(tabulate(df.T, headers="keys", tablefmt='fancy_grid')
     + "\n")
    
def main():
    """
    Run all program functions.
    """

    class CompleteOrder:
        """
        Defines the class CompleteOrder.
        """

        def __init__(self, items):
            self.items = items
    
    order_list.append(order)
    view_order()

    if view_order() == False:
       

        # Create an instance of the class CompleteOrder
        user_order = CompleteOrder(order_dict)

        display_final_order(user_order)

# main()

print("So you need some coffee... and fast?! Here's what we offer:\n")
user_choices = [get_menu_choice("coffee"), get_menu_choice("milk"), get_quantity()]

print(user_choices)

#     sum = 0
#     elements = []
#     for i in user_selection:
#         elements.append(i[0])
#         sum = sum + i[1]

#     item = {
#         "Coffee" : elements[0],
#         "Milk" : elements[1],
#         "Quantity" : elements[2],
#         "Price" : sum
#     }

    # Create a dictionary of all ordered items
        # keys = []
        # for i in range(len(order_list)):
        #     i = i + 1
        #     keys.append(i)
        # order_dict = dict(zip(keys, order_list))



