# imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# external libraries imports
import gspread
import pwinput
from google.oauth2.service_account import Credentials

# internal imports
# import google_config
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hotel_maintenance')


def login() -> bool:
    """
    Allow for user login by getting login credentials from user
    and comparing them to data from worksheet.
    Function will loop until login credentials are correct.
    Returns True or False.
    """
    # receive information from Google Sheets
    logins_ws = SHEET.worksheet("logins")

    # get login credentials from user
    id = input("Enter your username:\n")
    # get password, mask entered characters with asterisks
    pwd = pwinput.pwinput(prompt='Enter password:\n', mask='*')

    try:
        # get index of user id in logins worksheet
        id_column = logins_ws.col_values(1)
        id_column.pop(0)
        id_index = id_column.index(id)

        # pull corresponding password in logins worksheet
        psw_column = logins_ws.col_values(2)
        psw_column.pop(0)
        correct_pwd = psw_column[id_index]

    except:
        result = False
        print("\nLogin failed.\nPlease check and try again.\n")
        login()

    else:
        # check login credentials
        if pwd == correct_pwd:
            result = True
            print("\nLogin correct.")

        else:
            result = False
            print("\nLogin failed.\nPlease check and try again.\n")
            login()

    return result
