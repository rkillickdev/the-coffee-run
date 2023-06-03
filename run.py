import gspread
from google.oauth2.service_account import Credentials
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

def get_coffee_type():
    """
    Pulls data from the sheet "coffee" and assigns to variable "coffee_data".
    Assigns index 0 of the list "coffee_data" to the variable "header_names.
    Assigns remaining indexes of list to the variable menu_content  
    """

    print("So you need some coffee... and fast?! Here's what we offer:\n")
    coffee_menu = SHEET.worksheet("coffee")
    coffee_data = coffee_menu.get_all_values()

    # Set first row of 'coffee' sheet as header names
    header_names = coffee_data[0]

    # Assign rows from coffe_data to variable menu_content 
    menu_content = coffee_data[-4:]
    
    # Print coffee menu as a table
    print(tabulate(menu_content, headers=header_names, tablefmt='fancy_grid')
     + "\n")
    # Assign user input to variable coffee_code and check if valid
    while True:
        print("Please select you coffee by entering the code (1-4)\n")

        coffee_code = input("Enter your choice here: ")

        if validate_data(coffee_code, ["1", "2", "3", "4"]):
            print("Great, now let's get your coffee just how you like it!")
            break

    return coffee_code

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

get_coffee_type()