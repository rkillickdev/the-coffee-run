import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from tabulate import tabulate
from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('the_coffee_run')

class Order:
        """
        Defines the class Order.
        """

        def __init__(self):
            self.name = get_user_name()
            self.items = [] 
            self.date = get_date()
            self.time = get_time()

        def update_item(self, item):
            """
            Appends item to the items list.
            """
            self.items.append(item)

        def remove_item(self, item):
            """
            """

            self.items.pop(item)

        def get_order_total(self):
            """
            Iterates over items list and for each dictionary sums the value 
            of all 'price' keys.
            """

            order_total = 0

            for dict in self.items:
                for key, value in dict.items():
                    subtotal = value.get('Price')
                    order_total += subtotal
            print(f"The total cost of your order is: £{order_total}") 

def get_user_name():
    """
    Takes user_name input from user and validates.
    """

    # Assign user input to variable selected_quantity and check if valid.
    while True:

        print("Please enter your name\n")

        user_name = input("Enter your choice here:\n")

        if validate_name(user_name):
            break

    return user_name

def validate_name(user_input):
    """
    Raises ValueError if user_input is not all letters or is greater than 10 characters.
    """

    try:
        if len(user_input) > 10:
            raise ValueError(
                "You cannot enter more than 10 characters"
            )

        elif not user_input.isalpha():
            raise ValueError(
                "You must enter all letters"
            )
    except ValueError as e:
            print(f"Something went wrong. {e}. Please try again.")
            return False

    return True


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

def create_item_dict():
    """
    Stores user_choices by calling the get_menu_choice and get_quantity functions"
    """

    user_choices = [get_menu_choice("coffee"), get_menu_choice("milk"), get_quantity()]

    # user_choices converted from a list to a dictionary
    item = [{
        "Coffee" : user_choices[0][0],
        "Milk" : user_choices[1][0],
        "Quantity" : user_choices[2],
        "Price" : (user_choices[0][1] + user_choices[1][1]) * user_choices[2]
    }]

    # Generates a key based on the number of items already in the order
    key = [len(user_order.items) + 1]

    # Creates a dictionary using the item dictionary as the value.
    item_dict = dict(zip(key, item))

    return item_dict

def view_order():
    """
    Iterates over each dictionary stored in user_order items list and uses f string to
    print items currently in the order.
    """

    print("You're order currently contains the following:\n")

    # Turn the user_order items list into a single dictionary.
    # Used the following article to learn about this:
    # https://blog.finxter.com/merge-dictionaries/
    order_dict = {k:v for item in user_order.items for k,v in item.items()}
    
    # Print order summary as a table using pandas data frames.
    # I used the following article to learn about data frames:
    # https://tutorial.eyehunts.com/python/python-tabulate-dictionary-example-code/
    df = pd.DataFrame(order_dict)

    print(tabulate(df.T, headers="keys", tablefmt='fancy_grid')
     + "\n")

    view_order_options()

def view_order_options():
    """
    Create a data frame from the options dictionary.
    Display user options using tabulate.
    Accept user input, validate and pass this as an argument 
    to the function next_step.
    """

    options = {
        1 : {
            "Action" : "Add an item to order"
        },
        2 : {
            "Action" : "Remove an item from order"
        },
        3 : {
            "Action" : "Edit Quantities" 
        },
        4 : {
            "Action" : "Finalise Order"
        }
    }

    # Generate a list of code options to validate input against.
    code_options = list(options.keys())

    print("What would you like to do next?\n")

    df = pd.DataFrame(options)
    print(tabulate(df.T, headers="keys", tablefmt='fancy_grid')
     + "\n")

    while True:
        print("Please choose your next step by entering the code (1-4)\n")

        selected_code = int(input("Enter your choice here:\n"))

        if validate_data(selected_code, code_options):
            break

    next_step(selected_code)

def next_step(user_choice):
    """
    Check value of the parameter user_choice and run 
    associated function based on this value.
    """

    if user_choice == 1:
        main()
    elif user_choice == 2:
        remove_options()
    elif user_choice == 3:
        edit_options()
    elif user_choice == 4:
        view_final()

def edit_order():
    """
    """
    
def get_date():
    # Returns current date 
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    return date

def get_time():
    # Returns current time
    now = datetime.now()
    time = now.strftime("%H:%M:%S") 
    return time

def main():
    """
    Run all program functions.
    """
    
    print(f"Hi {user_order.name} So you need some coffee... and fast?! Here's what we offer:\n")
    item = create_item_dict()
    user_order.update_item(item)
    view_order()
       

# Create an instance of the class Order
user_order = Order()
main()
user_order.get_order_total()



