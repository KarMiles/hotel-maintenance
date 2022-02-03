import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
from tabulate import tabulate
from collections import Counter

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


def get_is_new_ticket():
    """
    Ask if user wants to enter new ticket.
    """
    while True:
        is_new_ticket = input("Do you wish to enter new ticket?\nAnswer Y for yes, or N for no: ")
        
        if validate_is_new_ticket(is_new_ticket):
            print("Y/N answer correct.")
            break
    
    return is_new_ticket


def validate_is_new_ticket(value):
    """
    Checks validity of Y/N anser about new ticket.
    Returns ValueError if entered value 
    is not Y or N.
    """
    try:
        value = value.lower()
        if str(value) != "y" and str(value) != "n":
            raise ValueError(
                "Please answer Y for yes or N for no!"
            )

    except ValueError as e:
        print(f"Invalid data: {e}")
        return False
    
    return True
    

def get_room_number():
    """
    Get room number from user.
    Run a while loop to collect a valid room number from the user
    via the terminal, which must be a number built of 3 digits:
    1st between 1-6, 2nd equal 0, 3rd between 1-8.
    The loop will repeatedly request data, until it is valid.
    """

    while True:
        print("Please enter room number.")
        print("Room number should be 3 digits, e.g. 102.")
        print("First digit representing floor (1-6),")
        print("followed by 0,")
        print("followed by digit 1-8.")
        room_number = input("\nEnter room number here: ")

        if validate_room_number(room_number):
            print(f"\nYou entered room number {room_number}.")
            break
    
    return room_number


def validate_room_number(value):
    """
    Checks validity of room number entered by user.
    Returns ValueError if entered value 
    is not a correct room number.
    """
    try:
        if len(value) != 3 or int(value) > 608 or (int(value) == 0) or int(value[0]) > 6 or (value[0] == "0") or (value[1] != "0") or (value[2] == "0") or (int(value[2]) > 8):
            raise ValueError(
                f"Room number should be 3 digits in the given format.\nTry again!"
            )

    except ValueError as e:
        print(f"Invalid data: {e}")
        return False
    
    return True


# def room_enquiry(room_number):


def display_last_ticket(room_number):
    """
    Shows most recent room ticket.
    """
    print(f"Receiving information about room {room_number}...")
    tickets = SHEET.worksheet("tickets").get_all_values()
    last_ticket = tickets[-1]
    print(last_ticket)
    

def display_summary():
    """
    Displays summary of maintenance tickets for all rooms in the hotel. 
    """
    tickets = SHEET.worksheet("tickets").get_all_values()
    number_of_tickets = len(tickets) - 1

    tickets_summary = SHEET.worksheet("tickets")
    urgency_column = tickets_summary.col_values(2)
    
    urgency = Counter(urgency_column)
    critical = urgency["critical"]
    urgent = urgency["urgent"]
    normal = urgency["normal"]
    print(f"Total number of tickets: {number_of_tickets}, of which:\nCritical: {critical}, Urgent: {urgent}, Normal: {normal}.")

    
def display_all_tickets():
    """
    Display tickets for all rooms 
    with maintenance tickets
    """
    print("Dislaying all maintenance tickets:")
    tickets = SHEET.worksheet("tickets").get_all_values()
    # pprint(tickets)
    tickets_headers = tickets[0]
    del tickets[0]
    # print(tickets_headers)
    print (tabulate(tickets, tickets_headers))

        
def main():
    """
    Run all program functions
    """
    print("\nWelcome to Hotel Maintenance System!\n")
    room = get_room_number()
    get_is_new_ticket()
    display_last_ticket(room)
    display_all_tickets()

# main()
display_summary()