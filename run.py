import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os
from tabulate import tabulate
from datetime import datetime, timedelta, timezone
import pytz
from termcolor import colored, cprint
from pyfiglet import Figlet
from collections import OrderedDict

# Code for implementing Google Sheets API modified from the
# Code Institute Love Sandwiches walk through project.

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("the_coffee_run")


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
        self.pickup_date = ""
        self.order_ref = create_order_ref(get_orders())
        self.is_complete = False

    def update_item(self, item):
        """
        Appends item to the items list.
        """
        self.items.append(item)

    def remove_item(self, item):
        """
        Removes the last item from the items list.
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
                subtotal = value.get("Sub Total")
                order_total += subtotal
        self.total_price = round(order_total, 1)

    def get_drinks_total(self):
        """
        Iterates over items list and for each dictionary sums the value
        of all 'Quantity' keys to get the total number of drinks in the order.
        """

        drinks_total = 0

        for dict in self.items:
            for key, value in dict.items():
                subtotal = value.get("Quantity")
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
            if item[k][f"{ingredient}"] == type:
                quantity = item[k]["Quantity"]
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
        elif 0 < recent_drinks < 10:
            additional_time = 10

        self.prep_time = (self.total_drinks * 2) + additional_time

    def get_date(self):
        """
        Returns current date.
        """
        now = get_datetime()
        date = now.strftime("%d/%m/%Y")
        self.date = date

    def get_time(self):
        """
        Returns current time.
        """
        now = get_datetime()
        time = now.strftime("%H:%M:%S")
        self.time = time

    def calculate_pickup(self):
        """
        Creates a datetime object for the current time and a timedelta
        object using the value stored in the order attribute 'prep_time'.
        These objects are added and then converted to a string which is
        assigned to the order attribute 'pickup'.
        """
        # I read the following article for adding minutes to datetime:
        # https://thispointer.com/how-to-add-minutes-to-datetime-in-python/

        now_string = self.date + self.time
        time_now = datetime.strptime(now_string, "%d/%m/%Y%H:%M:%S")
        duration = timedelta(minutes=self.prep_time)
        pickup_time = time_now + duration
        pickup_time_string = pickup_time.strftime("%H:%M:%S")
        pickup_date_string = pickup_time.strftime("%d/%m/%Y")
        self.pickup = pickup_time_string
        self.pickup_date = pickup_date_string

    def complete_order(self):
        """
        This sets the is_complete attribute of Order to True.
        """
        self.is_complete = True


user_options = {
    1: {"Action": "Order Coffee"},
    2: {"Action": "View Existing Order"},
    3: {"Action": "Admin View"},
    4: {"Action": "Quit App"},
}

action_options = {
    1: {"Action": "Add an item to order"},
    2: {"Action": "Remove an item from order"},
    3: {"Action": "Edit Quantities"},
    4: {"Action": "View Current Order"},
    5: {"Action": "Finalise Order"},
    6: {"Action": "Cancel Order"},
}

options_complete = {
    1: {"Action": "Return To Main Menu"},
    2: {"Action": "View Order"},
}


def get_datetime():
    """
    Uses datetime and pytz modules to return current time and date
    for London timezone as the coffee shop is located in London.
    """

    now = datetime.now(pytz.timezone("Europe/London"))
    return now


def title_screen():
    """
    Use Figlet from pyfiglet library to print title screen.
    Learnt about this library from the following article:
    https://towardsdatascience.com/prettify-your-terminal
    -text-with-termcolor-and-pyfiglet-880de83fda6b
    """

    line_1 = "COFFEE  RUN"
    centered = line_1.center(24)
    f = Figlet(font="big")
    print(f.renderText(centered))


def user_menu(options, menu):
    """
    Create a data frame from the options dictionary.
    Display user options using tabulate.
    Accept user input, validate and pass this as an argument
    to the function next_step.
    """

    if menu == "order_options":
        os.system("cls" if os.name == "nt" else "clear")

    # Generate a list of code options to validate input against.
    code_options = list(options.keys())
    first = code_options[0]
    last = code_options[-1]

    # Turn code options into a list of strings.
    code_string = list(map(str, code_options))

    if menu == "main":
        title_screen()
        message = "Welcome to The Coffee Run. What would you like to do today?"
    else:
        message = "What would you like to do next?\n"

    df = pd.DataFrame(options)
    print(tabulate(df.T, headers="keys", tablefmt="fancy_grid"))

    while True:
        print(f"\n{message}")

        selected_code = input(
            f"{colored(f'Enter {first} - {last} here:', 'green')}\n"
        )

        if validate_data(selected_code, code_string, "options"):
            break

    if menu == "main":
        main_menu_steps(int(selected_code))
    elif menu == "order_options":
        next_step(int(selected_code))
    elif menu == "order_complete":
        completed_steps(int(selected_code), code_options)


def main_menu_steps(user_choice):
    """
    Accepts user_choice as an argument which will be a value between 1 - 4.
    This value then determines the next function that should be run.
    """

    if user_choice == 1:
        assemble_order()
    elif user_choice == 2:
        view_completed(pull_menu("orders"))
    elif user_choice == 3:
        admin_stats(10)
    elif user_choice == 4:
        quit_app()


def assemble_order():
    """
    A dictionary is created based on the user choice of coffee type,
    milk and quantity. This item is then added to the user_order items
    list and the current order displayed by running the view_order function.
    """

    os.system("cls" if os.name == "nt" else "clear")

    if user_order.name == "":
        get_user_name()

    os.system("cls" if os.name == "nt" else "clear")

    if not user_order.items:
        print(
            f"Hi {user_order.name}, so you need some coffee..."
            "and fast?! Here's what we offer:\n"
        )
    else:
        print(
            f"Hello again {user_order.name}, so you want to add "
            "some more items?  Go ahead:\n"
        )

    item = create_item_dict()
    user_order.update_item(item)
    user_order.get_order_total()
    view_order("choices")


def get_user_name():
    """
    Takes user_name input from user and validates.
    """

    while True:
        user_name = input(
            f"{colored('Please enter your name here:', 'green')}\n"
        )

        if validate_name(user_name):
            break

    user_order.name = user_name.capitalize()


def validate_name(user_input):
    """
    Raises ValueError if user_input is not all letters or is greater than
    10 characters.
    """
    os.system("cls" if os.name == "nt" else "clear")

    try:
        if len(user_input) > 10:
            raise ValueError("You cannot enter more than 10 characters")

        elif not user_input.isalpha():
            raise ValueError("You must enter all letters")
    except ValueError as e:
        print(f"{colored(f'{e}. Please try again.', 'red')}")
        return False

    return True


def create_item_dict():
    """
    Stores user_choices by calling the get_menu_choice and
    get_quantity functions"
    """

    user_choices = [
        get_menu_choice(pull_menu("coffee")),
        get_menu_choice(pull_menu("milk")),
        coffee_quantity("add"),
    ]

    # calculates unit price
    unit = user_choices[0][1] + user_choices[1][1]

    # user_choices converted from a list to a dictionary
    item = [
        {
            "Coffee": user_choices[0][0],
            "Milk": user_choices[1][0],
            "Price": unit,
            "Quantity": user_choices[2],
            "Sub Total": unit * user_choices[2],
        }
    ]

    # Generates a key based on the number of items already in the order.
    key = [len(user_order.items) + 1]

    # Creates a dictionary using the item dictionary as the value.
    item_dict = OrderedDict(zip(key, item))

    return item_dict


def pull_menu(ingredient):
    """
    Pulls data from sheet name that is passed as an argument to the function.
    Assigns values to the variable data.
    """

    menu = access_google_sheet(f"{ingredient}")
    data = menu.get_all_values()
    return [data, ingredient]


def access_google_sheet(sheet):
    """
    Accesses the google sheet passed as the argument 'sheet'
    """

    gs_data = SHEET.worksheet(sheet)
    return gs_data


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

    first = code_options[0]
    last = code_options[-1]

    # Prints menu as a table
    print(
        tabulate(menu_content, headers=header_names, tablefmt="fancy_grid")
        + "\n"
    )

    # Assign user input to variable selected_code and check if valid.
    while True:
        selected_code = input(
            colored(
                f"Please select your {ingredient} by entering the code"
                f" {first} - {last}\n",
                "green",
            )
        )
        if validate_data(selected_code, code_options, "coffee_code"):
            break

    os.system("cls" if os.name == "nt" else "clear")

    item = menu[int(selected_code)][1]
    unit_cost = menu[int(selected_code)][2]
    if ingredient == "coffee":
        print("Great, now let's get your coffee just how you like it!\n")
    return item, float(unit_cost)


def validate_data(user_input, expected_values, selection=""):
    """
    Raises ValueError if user_input is not found in list of expected_values.
    The ValueError raised is determined by the string passed as the argument
    'selection'.
    """

    try:
        if user_input not in expected_values:
            if selection == "coffee_code":
                raise ValueError("This code is not valid")
            elif selection == "options":
                raise ValueError(
                    "This code is not valid.  Please select a number from"
                    " the menu"
                )
            elif selection == "reference":
                raise ValueError("This order reference does not exist")

        if selection == "coffee_quantity":
            if not user_input.isdigit() or int(user_input) < 1:
                raise ValueError("Please enter a number between 1 and 5")
    except ValueError as e:
        print(f"{colored(f'{e}. Please try again.', 'red')}")
        return False

    return True


def coffee_quantity(action):
    """
    Takes quantity input from user and returns as an integer.
    """

    # Assign user input to variable selected_quantity and check if valid.
    while True:
        # Create a list of integers to pass as the expected_values argument.
        quantity_options = range(1, 11)

        selected_quantity = input(
            colored("Please select a quantity between 1 and 5\n", "green")
        )
        if validate_data(
            selected_quantity,
            list(map(str, quantity_options)),
            "coffee_quantity",
        ) and validate_drinks(selected_quantity, action):
            break

    return int(selected_quantity)


def validate_drinks(user_input, step):
    """
    Checks sum of user input and total number of drinks currently in the order.
    If sum is greater than 5 return False.
    """

    os.system("cls" if os.name == "nt" else "clear")

    try:
        if step == "add" and int(user_input) + user_order.total_drinks > 5:
            raise ValueError("Sorry, this would take your order over 5 drinks")
        elif (
            step == "edit"
            and int(user_input) > 5
            or int(user_input) + user_order.total_drinks > 5
        ):
            raise ValueError(
                "You can only order a maximum of 5 drinks per order"
            )

    except ValueError as e:
        if user_order.total_drinks == 5:
            alert = f"{colored(f'{e}. Please choose another option:','red')}\n"
            view_order("choices", alert)
        else:
            print(f"{colored(f'{e}. Please choose again:', 'red')}")
        return False

    return True


def get_sales_data(dates):
    """
    Converts sales figures from worksheet to lists of integers.
    Takes a list of dates as an argument and iterates over each
    row, checking whether the date in column J is in the list of
    dates.  If it is, the date is appended to the list of
    requested_data and the function returns this list.
    """

    list_of_dates = dates
    sales = access_google_sheet("sales")
    data = sales.get_all_values()
    headers = data[0]
    sales_data = data[1:]
    requested_data = []
    most_recent = []

    for row in sales_data:
        if row[9] in list_of_dates:
            requested_data.append(row)

    # If there is no sales data available for the specified date
    # range, by default the last 20 entries on the "sales" sheet
    # will be appended to the requested_data list.
    if not requested_data:
        most_recent = sales_data[-20:]
        for row in most_recent:
            requested_data.append(row)

    requested_data.insert(0, headers)

    return requested_data


def date_range(days):
    """
    Generates a list of date strings for the past number of days
    specified in the argument 'days'.  I used the following article
    to find a way to achieve this:
    https://www.pythonprogramming.in/getting-the-date-of-7-days-
    ago-from-current-date-in-python.html
    """
    now = get_datetime()
    dates_list = []

    for x in range(days):
        date = now - timedelta(days=x)
        date_string = date.strftime("%d/%m/%Y")
        dates_list.append(date_string)
    return dates_list


def get_sales_totals(time_span):
    """
    Iterates over each row of sales figures for a range of
    days as specified in the 'time_span' argument.
    The total sales for each column is then calculated.
    """

    data = get_sales_data(date_range(time_span))

    headers = data[0][:8]
    units = data[1:]
    sales_rows = []

    for item in units:
        # convert from a list of strings to integers
        integers = [int(x) for x in item[:8]]
        sales_rows.append(integers)

    totals = [sum(i) for i in zip(*sales_rows)]

    coffee_totals = [headers[:4], totals[:4]]
    milk_totals = [headers[4:], totals[4:]]

    return [coffee_totals, milk_totals]


def most_popular(data):
    """
    Iterates over sales totals provided in the argument 'data'.
    The max() method is used to find the highest total and
    these stats are returned by the function.
    """

    titles = data[0]
    totals = data[1]

    most_popular = []

    for title, total in zip(titles, totals):
        if total == max(totals):
            most_popular.append(title)
            most_popular.append(total)

    return most_popular


def admin_stats(days):
    """
    Gets sales totals for coffee and milk for the past number of days
    specified in the argument 'days' and finds the most popular.
    Tabulates sales for each type of coffee, provides a total figure
    for coffee sold, and also prints information on the most
    popular coffee and milk.
    """
    os.system("cls" if os.name == "nt" else "clear")

    sales_data = get_sales_totals(days)
    coffee = sales_data[0]
    coffee_sales = sum(coffee[1])
    milk = sales_data[1]
    top_coffee = most_popular(coffee)
    top_milk = most_popular(milk)

    print(
        f"Total number of coffees sold in the past {days} days"
        f" : {colored(coffee_sales, 'cyan', attrs=['bold'])}\n"
    )

    print(tabulate(coffee, headers="firstrow", tablefmt="fancy_grid") + "\n")

    print(
        f"Most popular coffee:"
        f" {colored(top_coffee[0],'cyan', attrs=['bold'])}\n"
    )
    print(
        f"Most popular milk:"
        f" {colored(top_milk[0],'cyan', attrs=['bold'])}\n"
    )

    selected_code = return_to_menu("main")

    if selected_code == "m":
        main()


def return_to_menu(menu_type):
    """
    Guides the user back to a menu as specified in the argument 'menu_type'.
    User input must pass validation before the next step runs.
    """

    code_options = ["m"]
    menu_message = ""

    if menu_type == "main":
        menu_message = "press m to get back to the main menu"
    elif menu_type == "order_choices":
        menu_message = "press m to return to the menu options"

    while True:
        selected_code = input(f"{colored(menu_message, 'green')}\n")
        if validate_data(selected_code, code_options, "coffee_code"):
            break

    return selected_code


def get_recent():
    """
    Gets the column data for total drinks and time from "orders" sheet.
    Iterates over the last 15 orders.
    Filters and returns total drinks ordered in the last 15 minutes.
    """
    orders = access_google_sheet("orders")
    total_drinks = orders.col_values(5)
    time = orders.col_values(7)
    drinks = total_drinks[-15:]
    order_times = time[-15:]

    # I used the following article to learn about manipulating datetime:
    # https://www.dataquest.io/blog/python-datetime-tutorial/
    now = get_datetime()
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


def view_order(selection="", message=""):
    """
    Iterates over each dictionary stored in user_order items list and uses
    f string literal to print items currently in the order.
    """

    os.system("cls" if os.name == "nt" else "clear")

    if not user_order.is_complete:
        print(
            "The total cost of your order is currently: £ "
            f"{colored(user_order.total_price,'cyan',attrs=['bold'])}\n"
        )
        print("Your order currently contains the following:\n")
    else:
        print(
            "Here is a summary of order: "
            f"{colored(user_order.order_ref,'cyan',attrs=['bold'])}"
            " The total price will be: £ "
            f"{colored(user_order.total_price,'cyan',attrs=['bold'])}\n"
        )

    # Turn the user_order items list into a single dictionary.
    # Used the following article to learn about this:
    # https://blog.finxter.com/merge-dictionaries/
    item_dictionary = OrderedDict(
        {k: v for item in user_order.items for k, v in item.items()}
    )

    # Print order summary as a table using pandas data frames.
    # I used the following article to learn about data frames:
    # https://tutorial.eyehunts.com/python/python-tabulate-
    # dictionary-example-code/
    df = pd.DataFrame(item_dictionary)

    print(tabulate(df.T, headers="keys", tablefmt="fancy_grid") + "\n")

    if message:
        print(message)

    # Updates user_order total_drinks attribute.
    user_order.get_drinks_total()

    if selection == "choices":
        selected_code = return_to_menu("order_choices")
        if selected_code == "m":
            user_menu(action_options, "order_options")

    if selection == "completed":
        selected_code = return_to_menu("main")
        if selected_code == "m":
            clear_order()
            main()


def next_step(user_choice):
    """
    Checks value of the parameter user_choice and runs
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
        view_order("choices")
    elif user_choice == 5:
        submit_order()
    elif user_choice == 6:
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
    Accepts a code from the user.  If valid, this code is used to generate the
    necessary index to manipulate the item being removed or edited.
    If removing an item, the index is passed as an argument to the remove_item
    method of the Class Order. The view_order function is then called to
    display the new order summary with the item removed.
    If editing the quantity of an item, the quantity value is set to zero,
    before re-entering the desired quantity.  The quantity and price values are
    then updated in the item dictionary.  The view_order function is then
    called displaying a summary of the order with ammended quantity and price.
    """

    os.system("cls" if os.name == "nt" else "clear")
    view_order()

    keys_as_strings = [str(x) for x in keys]

    while True:
        print(f"Which item of your order you would like to {option}?\n")

        selected_code = input(colored("Enter a number here:\n", "green"))

        if validate_data(selected_code, keys_as_strings, "options"):
            break

    index = int(selected_code) - 1

    if option == "remove":
        user_order.remove_item(index)
        update_order_dict()
        user_order.get_order_total()
        if not user_order.items:
            main()
        else:
            view_order("choices")

    elif option == "edit":
        item = user_order.items[index]
        item[index + 1]["Quantity"] = 0
        user_order.get_drinks_total()
        updated_quantity = coffee_quantity("edit")
        item[index + 1]["Quantity"] = updated_quantity
        item[index + 1]["Sub Total"] = (
            item[index + 1]["Price"] * updated_quantity
        )
        user_order.get_order_total()
        view_order("choices")


def update_order_dict():
    """
    Updates keys for dictionaries in user_order.items when an item
    is removed from the list, so the keys are always sequential
    when displayed in a table format.
    """

    options = list(range(len(user_order.items)))
    keys = [i + 1 for i in options]
    updated_order_list = []

    for k, item in zip(keys, user_order.items):
        dict_key = list(item.keys())
        value = dict_key[0]
        new_dict = {k: item[value]}
        updated_order_list.append(new_dict)

    user_order.items = updated_order_list


def get_orders():
    """
    Pulls data from "orders" sheet and returns the data without the headers
    as orders_list.
    """

    orders = access_google_sheet("orders")
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

    details_string = "\n".join(details_list)
    return details_string


def submit_order():
    """
    Class methods called on the instance of Order 'user_order'.
    A list of order details collated  from the user_order attributes which
    are then sent to the google sheet called "orders".
    Print statements using f string literals are used to communicate key
    information from the order to the user.
    The sales_data function is also called and this data is sent to the
    google sheet called "sales".
    Next step options are then displayed to the user in tabular form.
    """

    os.system("cls" if os.name == "nt" else "clear")

    user_order.get_order_total()
    user_order.get_date()
    user_order.get_time()
    user_order.calculate_prep()
    user_order.calculate_pickup()
    user_order.complete_order()

    order_details = [
        user_order.order_ref,
        user_order.name,
        items_to_string(),
        user_order.total_price,
        user_order.total_drinks,
        user_order.date,
        user_order.time,
        user_order.pickup,
        user_order.pickup_date,
    ]

    send_data(order_details, "orders")

    print(
        f"Thanks {colored(user_order.name, 'cyan',attrs=['bold'])}."
        " Your order has been submitted!\n"
    )
    print(
        f"Your order reference is:"
        f" {colored(f'{user_order.order_ref}','cyan',attrs=['bold'])}\n"
    )
    print(
        f"The total cost of your order is:"
        f" £ {colored(f'{user_order.total_price}','cyan',attrs=['bold'])}\n"
    )
    print(
        f"Your coffee will be ready to pickup at:"
        f" {colored(f'{user_order.pickup}','cyan',attrs=['bold'])}"
        f" on {colored(f'{user_order.pickup_date}','cyan',attrs=['bold'])}\n"
    )

    sales = sales_data()
    send_data(sales, "sales")

    user_menu(options_complete, "order_complete")


def completed_steps(user_choice, codes):
    """
    This either returns the user to the main menu or displays a
    summary of their sumitted order, depending on the value passed
    as the argument 'user_choice'.
    """
    last = codes[-1]
    if user_choice == codes[0]:
        clear_order()
        main()
    elif user_choice == codes[1]:
        view_order("completed")


def quit_app():
    """
    Prints a thank you message and runs the title_screen function to
    display "Coffee Run".
    """
    os.system("cls" if os.name == "nt" else "clear")
    title_screen()
    print(
        colored("Thanks for stopping by, see you again soon!\n", "cyan"),
        end="\r",
    )


def clear_order():
    """
    Updates the attributes items, total_drinks, name and ordedr_ref for the
    class instance of Order called user_order.
    """
    user_order.items = []
    user_order.total_drinks = 0
    user_order.name = ""
    user_order.order_ref = create_order_ref(get_orders())


def view_completed(sheet_data):
    """
    Collates a list of existing order references from the "orders" sheet.
    Validates input of user input by checking if their order ref exists.
    If order ref valid, use data from this order to display details to user.
    """
    os.system("cls" if os.name == "nt" else "clear")

    data = sheet_data[0]
    header_names = data[0]
    completed_orders = data[1:]
    order_refs = []

    for order in completed_orders:
        ref = order[0]
        order_refs.append(ref)

    while True:
        print(
            "To view an existing order, please enter your "
            "reference number:\n"
        )

        selected_code = input(colored("Enter a reference here:\n", "green"))

        if validate_data(selected_code, order_refs, "reference"):
            break

    os.system("cls" if os.name == "nt" else "clear")

    pickup_time = []

    for order in completed_orders:
        if order[0] == selected_code:
            pickup_time.append(order[8])
            pickup_time.append(order[7])
            string_pickup = " ".join(pickup_time)
            date_format = "%d/%m/%Y %H:%M:%S"
            present = get_datetime()
            current_string = datetime.strftime(present, date_format)
            present_datetime = datetime.strptime(current_string, date_format)
            pickup_datetime = datetime.strptime(string_pickup, date_format)

            print(f"Hi {colored(order[1],'cyan',attrs=['bold'])}\n")
            print(
                "Details for order ref "
                f"{colored(order[0],'cyan',attrs=['bold'])}"
                " are as follows:\n"
            )
            print(f"{colored(order[2],'cyan',attrs=['bold'])}\n")
            print(
                f"The total cost of your order is"
                f" £ {colored(order[3], 'cyan',attrs=['bold'])}\n"
            )
            if present_datetime < pickup_datetime:
                print(
                    f"Your coffee will be ready to pickup at"
                    f" {colored(order[7],'cyan',attrs=['bold'])}"
                    f" on {colored(order[8],'cyan',attrs=['bold'])}\n"
                )
            else:
                print(
                    f"Your coffee is"
                    f"{colored(' READY','cyan',attrs=['bold'])} to pickup\n"
                )

    selected_code = return_to_menu("main")
    if selected_code == "m":
        main()


def sales_data():
    """
    Compile and return a sales list with the quantity of each type of
    coffe and milk in the order.
    """

    fw_sales = user_order.get_quantity("Coffee", "Flat White", get_keys())
    la_sales = user_order.get_quantity("Coffee", "Latte", get_keys())
    ca_sales = user_order.get_quantity("Coffee", "Cappuccino", get_keys())
    am_sales = user_order.get_quantity("Coffee", "Americano", get_keys())
    reg_sales = user_order.get_quantity("Milk", "Regular", get_keys())
    ski_sales = user_order.get_quantity("Milk", "Skinny", get_keys())
    oat_sales = user_order.get_quantity("Milk", "Oat", get_keys())
    soy_sales = user_order.get_quantity("Milk", "Almond", get_keys())

    sales = [
        fw_sales,
        la_sales,
        ca_sales,
        am_sales,
        reg_sales,
        ski_sales,
        oat_sales,
        soy_sales,
    ]
    sales.append(user_order.time)
    sales.append(user_order.date)

    return sales


def send_data(data, sheet_name):
    """
    Receives a list to be inserted into a worksheet.
    Updates the specified worksheet with the data provided.
    """
    worksheet_to_update = SHEET.worksheet(sheet_name)
    worksheet_to_update.append_row(data)


def main():
    """
    Displays the main user menu.
    """
    os.system("cls" if os.name == "nt" else "clear")
    user_menu(user_options, "main")


# Create an instance of the class Order
user_order = Order()

main()
