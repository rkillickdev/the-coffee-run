import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os
from tabulate import tabulate
from datetime import datetime, timedelta

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
            self.total_drinks = 0
            self.date = ""
            self.time = ""
            self.total_price = 0
            self.prep_time = 0
            self.order_ref = create_order_ref(get_orders())
            self.is_complete = False

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
            of all 'Price' keys.
            """

            order_total = 0

            for dict in self.items:
                for key, value in dict.items():
                    subtotal = value.get('Price')
                    order_total += subtotal
            self.total_price = order_total

        def get_drinks_total(self):
            """
            Iterates over items list and for each dictionary sums the value 
            of all 'Quantity' keys.
            """

            drinks_total = 0

            for dict in self.items:
                for key, value in dict.items():
                    subtotal = value.get('Quantity')
                    drinks_total += subtotal
            self.total_drinks = drinks_total
        
        def calculate_prep(self):
            """
            Takes the total number of drinks for the order and calculates
            prep time based on the estimation that each coffee will take
            2 minutes to prepare.  The number of recent drinks orders is
            also used to estimate the additional time required to prepare.
            """
            recent_drinks = get_recent()
            additional_time = 0
            if recent_drinks >= 10:
                additional_time = 15
            elif 0< recent_drinks <10:
                additional_time = 10   

            self.prep_time = (self.total_drinks * 2) + additional_time   

        def get_date(self):
            # Returns current date 
            now = datetime.now()
            date = now.strftime("%d/%m/%Y")
            self.date = date

        def get_time(self):
            # Returns current time
            now = datetime.now()
            time = now.strftime("%H:%M:%S") 
            self.time = time

        def complete_order(self):
            self.is_complete = True  

def get_recent():
    """
    Gets the column data for total drink and time from "orders" sheet.
    Filters and returns total drinks ordered in the last 15 minutes. 
    """
    orders = SHEET.worksheet("orders")
    total_drinks = orders.col_values(5)
    time = orders.col_values(7)
    drinks = total_drinks[1:]
    order_times = time[1:]

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current = datetime.strptime(current_time, "%H:%M:%S")
    recent = []
    total_recent = 0

    # Iterates over order times and calculates difference between current time.
    for order, time in zip(drinks, order_times):
        max_time = timedelta(minutes=15) 
        past = datetime.strptime(time, "%H:%M:%S") 
        difference = current - past
        
        # Appends total drinks placed in last 15 minutes to recent list
        if difference <= max_time:
            recent.append(order)

    # Calculates total number of recent drinks ordered
    for num in recent:
        total_recent += int(num)
    print(f"Recent Orders: {recent}")
    print(f"Total number of recent drinks is {total_recent}")
    return total_recent

def get_orders():
    """
    Pulls data from "orders" sheet and returns the data without the headers
    as orders_list.
    """

    orders = SHEET.worksheet("orders")
    data = orders.get_all_values()
    orders_list = data[1:]
    return orders_list

def create_order_ref(orders_list):
    """
    Filters only order references from the orders_list, finds the next 
    avaialable number based on the length of the order_refs list, and 
    assigns this to new_order_ref.  The function then returns this value.
    """
    order_refs = []
    for order in orders_list:
        order_refs.append(order[0])
    new_order_ref = len(order_refs) + 1
    return new_order_ref
        
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

        if validate_data(selected_code, code_options, "coffee_code"):
            break

    os.system('cls' if os.name == 'nt' else 'clear')
    
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

        if validate_data(selected_quantity, list(map(str, quantity_options)), "coffee_quantity"):
            break
    os.system('cls' if os.name == 'nt' else 'clear')

    return int(selected_quantity)

def validate_data(user_input, expected_values, selection):
    """
    Raises ValueError if user_input is not found in list of expected_values.
    """

    try:
        if user_input not in expected_values:
            if selection == "coffee_code":
                raise ValueError(
                    "This code is not valid"
                )
            elif selection == "coffee_quantity":
                raise ValueError(
                    "This value is not valid, please enter a number between 1 and 10"
                )
            elif selection == "next_step":
                raise ValueError(
                    "This code is not valid.  Please select a number from the menu"
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

    if not user_order.is_complete:
        print("You're order currently contains the following:\n")
    else:
        print("Here is a summary of your order:\n") 

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

    if not user_order.is_complete:
        view_order_options()
    else:
        print(f"Your order total is £{user_order.total_price}\n"  
              f"Your reference number is {user_order.order_ref}")

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

        if validate_data(selected_code, code_options, "next_step"):
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
        complete_order()
        
def remove_options():
    """
    """

    options = list(range(len(user_order.items)))
    print(options)

    while True:

        print("Which item of your order you would like to remove?")

        selected_code = int(input("Enter a number here:\n"))

        if validate_data(selected_code, options):
            break

    index = selected_code - 1
    print(index)
    user_order.remove_item(index)
    view_order()

def edit_order():
    """
    """

def complete_order():
    """
    """

    os.system('cls' if os.name == 'nt' else 'clear')

    user_order.get_order_total()
    user_order.get_date()
    user_order.get_time()
    user_order.get_drinks_total()
    user_order.calculate_prep()
    user_order.complete_order()

    order_details = [user_order.order_ref, user_order.name, items_to_string(),
                    user_order.total_price, user_order.total_drinks, user_order.date, user_order.time]

    send_data(order_details, "orders")
    items_to_string()

    view_order()

def send_data(data, worksheet):
    """
    Receives a list to be inserted into a worksheet.
    Update the relevant worksheet with the data provided.
    """
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print("Your order has been submitted!")

def items_to_string():
    """
    Iterates over items in instance of the Class Order.
    Nested loop used to get the values of each dictionary.
    A summary string is created for each item and appended
    to the details_list.
    The summary strings are joined and saved as details_string. 
    """
    details_list = []
    
    for dict in user_order.items:
        item = []    
        for key, value in dict.items():
            details = value
            for key, value in details.items():
                item.append(value)
            summary = f"{item[2]} X {item[0]} with {item[1]} milk"
            details_list.append(summary)
    
    details_string = '\n'.join(details_list)
    return details_string
    
def main():
    """
    Run all program functions.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Hi {user_order.name} So you need some coffee... and fast?! Here's what we offer:\n")
    item = create_item_dict()
    os.system('cls' if os.name == 'nt' else 'clear')
    user_order.update_item(item)
    view_order()
       

# Create an instance of the class Order
user_order = Order()
main()
print(user_order.prep_time)





