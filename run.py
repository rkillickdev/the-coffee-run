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

        selected_code = input("Enter your choice here: ")

        if validate_data(selected_code, code_options):
            break

    return selected_code

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

print("So you need some coffee... and fast?! Here's what we offer:\n")
get_menu_choice("coffee")
print("Great, now let's get your coffee just how you like it!\n")
get_menu_choice("milk")
