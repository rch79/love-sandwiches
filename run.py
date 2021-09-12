import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')  # opens spreadsheet on gdrive

sales = SHEET.worksheet('sales')  # access tab sales on our worksheet


def get_sales_data():
    """
    Get sales figures input from the user
    Function will loop indefinitely until the data entered
    by the user passes validation
    """
    while True:
        print('Please enter sales data from last market.')
        print('Data should be six numbers, separated by commas.')
        print('Example: 2,10,40,5,8,12\n')

        data_str = input('Enter your data here: ')

        sales_data = data_str.split(",")    # breaks up data at the commas

        if validate_data(sales_data):
            print("Data is valid\n")
            break    # breaks out of while True loop

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        if len(values) != 6:
            raise ValueError(f'Exactly 6 values are required, you provided {len(values)}')
        else:
            [int(value)for value in values]
    except ValueError as e:
        print(f"Invalid data: {e}. Please try again.\n")
        return False

    return True


def update_sales_worksheet(data):
    """
    Updates sales worksheet; adds new row with the list data provided
    """
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each type

    The surplus is defined as the sales figure subtracted from the stock:
     - Positive surplus indicates waste
     - Negative surplus indicates extra sandwiches were made when stock
      ran out
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]   # assigns last row on stock worksheet to variable

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):  # zip iterates through two lists at the same time
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)


print("Welcome to Love Sandwiches\n")
main()
