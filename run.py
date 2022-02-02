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
SHEET = GSPREAD_CLIENT.open('hotel_maintenance')

# check if connections are working:
# tickets = SHEET.worksheet('tickets')
# data = tickets.get_all_values()
# print(data)


    

def get_room_number():
    """
    Get room number from user.
    Run a while loop to collect a valid room number from the user
    via the terminal, which must be a number built of 3 digits:
    1st between 1-6, 2nd equal 0, 3rd between 1-8.
    The loop will repeatedly request data, until it is valid.
    """

    while True:
        print("\nPlease enter room number.")
        print("Room number should be 3 digits, e.g. 102.")
        print("First digit representing floor (1-6),")
        print("followed by 0,")
        print("followed by digit 1-8.")
        room_number = input("\nEnter room number here: ")

        if validate_room_number(room_number):
            print(f"You entered room number {room_number}.")
            break

    return room_number


def validate_room_number(value):
    """
    Checks validity of room number entered by user.
    Returns ValueError if entered value 
    is not a correct room number.
    """
    try:
        # [int(value)]
        # value = int(value)
        if int(value) > 608 or (int(value) == 0) or (int(value[0]) > 6) or (value[0] == "0") or (value[1] != "0") or (value[2] == "0") or (int(value[2]) > 8):
            raise ValueError(
                f"Room number should be 3 digits in the given format.\nTry again!"
            )

    except ValueError as e:
        print(f"Invalid data: {e}")
        return False
    
    return True

        

welcome()
get_room_number()