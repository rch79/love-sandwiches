import gspread
from google.oauth2.service_account import Credentials
# from pprint import pprint (better print layout)

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


def update_worksheet(worksheet, data):
    """
    Update worksheet with data provided
    """
    print(f"Updating {worksheet.capitalize()} worksheet\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet.capitalize()} updated successfuly\n")


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


def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet,
    collecting the last 5 entries for each sandwich
    and returns the data as a list of lists.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])     # grabs everything from -5 through rest of array

    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1   # adds 10% to the average
        new_stock_data.append(round(stock_num))  # rounds the new stock

    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    new_sales_data = [int(num) for num in data]
    update_worksheet("sales", new_sales_data)
    new_surplus_data = calculate_surplus_data(new_sales_data)
    update_worksheet("surplus", new_surplus_data)
    get_last_5_entries_sales()
    sales_columns = get_last_5_entries_sales()
    new_stock_data = calculate_stock_data(sales_columns)
    update_worksheet("stock", new_stock_data)


print("Welcome to Love Sandwiches\n")
main()
