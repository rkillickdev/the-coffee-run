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
    coffee_menu = SHEET.worksheet("coffee")
    coffee_data = coffee_menu.get_all_values()

    # Set first row of 'coffee' sheet as header names
    header_names = coffee_data[0]

    # Assign rows from coffe_data to variable menu_content 
    menu_content = coffee_data[-4:]
    print(header_names)
    print(menu_content)

get_coffee_type()