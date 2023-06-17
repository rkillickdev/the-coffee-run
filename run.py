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
            self.name = ""
            self.items = []
            self.total_drinks = 0
            self.date = ""
            self.time = ""
            self.total_price = 0
            self.prep_time = 0
            self.pickup = ""
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

        def get_quantity(self, ingredient, type, keys):
            """
            Iterates over the class attribute items and checks the quantity
            of the 'type' argument that has been passed, in each dictionary
            in the list.  The total of items of this 'type' is then calculated
            and returned as the variable total_quantity
            """

            quantities_list = []
            
            for k, item in zip(keys, self.items):
                if item [k][f"{ingredient}"] == type:
                    quantity = item[k]['Quantity']
                else:
                    quantity = 0
                quantities_list.append(quantity)
            total_quantity = sum(quantities_list)
            return total_quantity
                        
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
            """
            Returns current date
            """ 
            now = datetime.now()
            date = now.strftime("%d/%m/%Y")
            self.date = date

        def get_time(self):
            """
            Returns current time
            """
            now = datetime.now()
            time = now.strftime("%H:%M:%S") 
            self.time = time

        def calculate_pickup(self):
            """
            Creates a datetime object for the current time and a timedelta
            object using the value stored in the order attribute 'prep_time'.
            These objects are added and then converted to a string which is
            assigned to the orderattribute 'pickup'. 
            """
            # I read the following article for adding minutes to datetime:
            # https://thispointer.com/how-to-add-minutes-to-datetime-in-python/

            time_now = datetime.strptime(self.time, "%H:%M:%S")
            duration = timedelta(minutes=self.prep_time)
            pickup_time = time_now + duration
            pickup_string = pickup_time.strftime("%H:%M:%S")
            self.pickup = pickup_string

        def complete_order(self):
            self.is_complete = True


user_options = {
    1: {
        "Action" : "Order Coffee"
    },
    2: {
        "Action" : "View Existing Order"
    },
    3: {
        "Action" : "Admin Login"
    }
}

action_options = {
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
    },
    5: {
        "Action" : "Cancel Order"
    }
}

def options_complete(status):
    """
    """

    if status == "current":
        options_complete = {
            1: {
                "Action" : "Return To Main Menu"
            }, 
            2: {
                "Action" : "View Order"
            },
            3: {
                "Action" : "Quit App"     
            }
        }
    elif status == "completed" :
        options_complete = {
            1: {
                "Action" : "Return To Main Menu"
            }, 
            2: {
                "Action" : "Quit App"     
            }
        }

    return options_complete   


def user_menu(options, menu):
    """
    Create a data frame from the options dictionary.
    Display user options using tabulate.
    Accept user input, validate and pass this as an argument 
    to the function next_step.
    """

    # Generate a list of code options to validate input against.
    code_options = list(options.keys())
    first = code_options[0]
    last = code_options[-1]

    if menu == "main":
        print("Welcome to The Coffee Run, what would you like to do today?\n")
    else:
        print("What would you like to do next?\n")

    df = pd.DataFrame(options)
    print(tabulate(df.T, headers="keys", tablefmt='fancy_grid')
     + "\n")

    while True:
        print(f"Please choose your next step by entering the code " 
              f"({first} - {last})\n")

        selected_code = int(input("Enter your choice here:\n"))

        if validate_data(selected_code, code_options, "options"):
            break

    
    if menu == "main":
        main_menu_steps(selected_code)
    elif menu == "order_options":
        next_step(selected_code)
    elif menu == "order_complete":
        completed_steps(selected_code, code_options)

def main_menu_steps(user_choice):
    """
    """

    if user_choice == 1:
        assemble_order()
    elif user_choice == 2:
        view_completed(pull_menu("orders"))
    elif user_choice == 3:
        print("Welcome admin")

def assemble_order():
    """
    """

    os.system('cls' if os.name == 'nt' else 'clear')

    if user_order.name == "":
        get_user_name()

    os.system('cls' if os.name == 'nt' else 'clear')

    if not user_order.items:
        print(f"Hi {user_order.name}, so you need some coffee..." 
               "and fast?! Here's what we offer:\n")
    else:
        print(f"Hello again {user_order.name}, so you want to add "
               "some more items?  Go ahead:\n")

    item = create_item_dict()
    user_order.update_item(item)
    view_order("choices")

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

    user_order.name = user_name

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

def create_item_dict():
    """
    Stores user_choices by calling the get_menu_choice and get_quantity functions"
    """

    user_choices = [get_menu_choice(pull_menu("coffee")), get_menu_choice(pull_menu("milk")), get_quantity()]

    # calculate unit price
    unit = user_choices[0][1] + user_choices[1][1] 

    # user_choices converted from a list to a dictionary
    item = [{
        "Coffee" : user_choices[0][0],
        "Milk" : user_choices[1][0],
        "Unit Price" : unit,
        "Quantity" : user_choices[2],
        "Price" : unit * user_choices[2]
    }]

    # Generates a key based on the number of items already in the order
    key = [len(user_order.items) + 1]

    # Creates a dictionary using the item dictionary as the value.
    item_dict = dict(zip(key, item))

    return item_dict

def pull_menu(ingredient):
    """
    Pulls data from whatever sheet name is passed as an argument to the function.
    Assigns values to the variable data.
    """

    menu = SHEET.worksheet(f"{ingredient}")
    data = menu.get_all_values()
    return [data, ingredient]

def get_menu_choice(data):
    """
    Assigns index 0 of the variable data to the variable header_names.
    Assigns remaining indexes of variable data to the variable menu_content.  
    """
    
    menu = data[0]
    ingredient = data[1]

    # Set first row of specified sheet as header names.
    header_names = menu[0]

    # Assign rows from data to variable menu_content. 
    menu_content = menu[1:]

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
    
    item = (menu[int(selected_code)][1])
    unit_cost = (menu[int(selected_code)][2])
    if ingredient == "coffee":
        print("Great, now let's get your coffee just how you like it!\n")
    return item, float(unit_cost)

def validate_data(user_input, expected_values, selection = ""):
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
            elif selection == "options":
                raise ValueError(
                    "This code is not valid.  Please select a number from the menu"
                )
            elif selection == "reference":
                raise ValueError(
                    "This order reference does not exist.  Please try again"
                )                                       
    except ValueError as e:
            print(f"Something went wrong. {e}. Please try again.")
            return False

    return True

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

        if validate_data(selected_quantity, list(map(str, quantity_options)),
                        "coffee_quantity"):
            break

    if not validate_drinks(selected_quantity):
        print("here are your options")
        view_order_options()

    os.system('cls' if os.name == 'nt' else 'clear')

    return int(selected_quantity)

def validate_drinks(user_input):
    """
    Checks sum of user input and total number of drinks currently in the order.
    If sum is greater than 10 return False.
    """
    try:
        if int(user_input) + user_order.total_drinks >10:
            raise ValueError(
                "You can only order a maximum of 10 drinks per order" 
            )

    except ValueError as e:
        print(f"Something went wrong. {e}. Please try again.")
        return False

    return True


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

    # I used the following article to learn about manipulating datetime:
    # https://www.dataquest.io/blog/python-datetime-tutorial/
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
    return total_recent
        
def view_order(selection=""):
    """
    Iterates over each dictionary stored in user_order items list and uses f string to
    print items currently in the order.
    """

    os.system('cls' if os.name == 'nt' else 'clear')

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

    # Updates user_order total_drinks attribute.
    user_order.get_drinks_total()

    
    if selection == "choices":
        user_menu(action_options, "order_options")
    elif selection == "completed":
        user_menu(options_complete("completed"), "order_complete")      
        

def next_step(user_choice):
    """
    Check value of the parameter user_choice and run 
    associated function based on this value.
    """

    if user_choice == 1:
        assemble_order()
    elif user_choice == 2:
        if not user_order.items:
            print("I'm sorry there are no more items to remove")
            main()
        else:
            input_options(get_keys(), "remove")
    elif user_choice == 3:
        input_options(get_keys(), "edit")
    elif user_choice == 4:
        complete_order()
    elif user_choice == 5:
        clear_order()
        main()

def get_keys():
    """
    Finds the length of the user_order.items list and iterates over this
    to generate a list of integers to be used as dictionary keys.
    """

    options = list(range(len(user_order.items)))
    keys = [i + 1 for i in options]
    return keys

def input_options(keys, option):
    """
    Accepts a code form the user.  If valid, this code is used to generate the
    necessary index for the item being removed, which is then passed as an 
    argument to the remove_item method on the class instance user_order.
    """

    os.system('cls' if os.name == 'nt' else 'clear')
    view_order()

    while True:

        print(f"Which item of your order you would like to {option}?")

        selected_code = int(input("Enter a number here:\n"))

        if validate_data(selected_code, keys, "options"):
            break

    index = selected_code - 1
    if option == "remove":
        user_order.remove_item(index)
        update_order_dict()
        if not user_order.items:
            main()
        else:
            view_order("choices")

    elif option == "edit":
        updated_quantity = get_quantity()
        item = user_order.items[index]
        item[index + 1]['Quantity'] = updated_quantity
        item[index + 1]['Price'] = item[index + 1]['Unit Price'] * updated_quantity
        view_order("choices")

def update_order_dict():
    """
    """

    options = list(range(len(user_order.items)))
    keys = [i + 1 for i in options]
    updated_order_list = [] 

    for k, item in zip(keys, user_order.items):
        dict_key = list(item.keys())
        value = dict_key[0]
        new_dict = {k : item[value]}
        updated_order_list.append(new_dict)
    
    user_order.items = updated_order_list

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
            summary = f"{item[3]} X {item[0]} with {item[1]} milk"
            details_list.append(summary)
    
    details_string = '\n'.join(details_list)
    return details_string

def complete_order():
    """
    """

    os.system('cls' if os.name == 'nt' else 'clear')

    user_order.get_order_total()
    user_order.get_date()
    user_order.get_time()
    user_order.calculate_prep()
    user_order.calculate_pickup()
    user_order.complete_order()

    order_details = [user_order.order_ref, user_order.name, items_to_string(),
                    user_order.total_price, user_order.total_drinks, user_order.date, user_order.time, user_order.pickup]

    send_data(order_details, "orders")

    print("Thank you, your order has been submitted!\n")
    print(f"Your order reference is {user_order.order_ref}\n")
    print(f"The total cost of your order is £{user_order.total_price}\n")
    print(f"Your coffee will be ready to pickup at {user_order.pickup}\n")

    user_menu(options_complete("current"), "order_complete")
    
    send_data(sales_data(), "sales")

def completed_steps(user_choice, codes):
    """
    """
    last = codes[-1]
    if user_choice == codes[0]:
        clear_order()
        main()
    elif user_choice == 2 and user_choice != last:
        view_order("completed")
    elif user_choice == last:
        print(f"Thanks fo ordering your Coffee with us {user_order.name}")

def clear_order():
    """
    """
    user_order.items = []
    user_order.name = ""    

def view_completed(sheet_data):
    """
    Collates a list of existing order references from the "orders" sheet.
    Validates input of user input by checking if their order ref exists.
    If order ref valid, use data from this order to display details to user.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

    data = sheet_data[0]
    header_names = data[0] 
    completed_orders = data[1:]
    order_refs = []

    for order in completed_orders:
        ref = order[0]
        order_refs.append(ref)

    while True:

        print("To view an existing order, please enter your " 
              "reference number:\n")

        selected_code = (input("Enter a reference here:\n"))

        if validate_data(selected_code, order_refs, "reference"):
            break

    os.system('cls' if os.name == 'nt' else 'clear')

    for order in completed_orders:
        if order[0] == selected_code:
            print(f"Hi {order[1]},\n")
            print(f"Details for order ref {order[0]} are as follows:\n")
            print(f"{order[2]}")
            print("\n")
            print(f"The total cost of your order is £{order[3]}\n")

    user_menu(options_complete("completed"), "order_complete")

def sales_data():
    """
    Compile a sales list with the quantity of each type of coffe and milk
    in the order.
    """

    fw_sales = user_order.get_quantity("Coffee", "flat white", get_keys())
    la_sales = user_order.get_quantity("Coffee", "latte", get_keys())
    ca_sales = user_order.get_quantity("Coffee", "cappuccino", get_keys())
    am_sales = user_order.get_quantity("Coffee", "americano", get_keys())   
    reg_sales = user_order.get_quantity("Milk", "regular", get_keys())
    ski_sales = user_order.get_quantity("Milk", "skinny", get_keys())
    oat_sales = user_order.get_quantity("Milk", "oat", get_keys())
    soy_sales = user_order.get_quantity("Milk", "soy", get_keys())

    sales = [fw_sales, la_sales, ca_sales, am_sales, reg_sales, ski_sales,
            oat_sales, soy_sales]
    sales.append(user_order.time)
    sales.append(user_order.date)

    return sales 

def send_data(data, sheet_name):
    """
    Receives a list to be inserted into a worksheet.
    Update the relevant worksheet with the data provided.
    """
    worksheet_to_update = SHEET.worksheet(sheet_name)
    worksheet_to_update.append_row(data)
    
def main():
    """
    Run all program functions.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    user_menu(user_options, "main")
   
       
# Create an instance of the class Order
user_order = Order()

main()






