import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')  #opens spreadsheet on gdrive

sales = SHEET.worksheet('sales')  #access tab sales on our worksheet

def get_sales_data():
    """
    Get sales figures input from the user
    """
    print('Please enter sales data from last market.')
    print('Data should be six numbers, separated by commas.')
    print('Example: 2,10,40,5,8,12\n')

    data_str = input('Enter your data here: ')
    print(f'The data entered is {data_str}')

get_sales_data()