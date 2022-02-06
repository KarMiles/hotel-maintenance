import gspread
import pwinput
from google.oauth2.service_account import Credentials
from pprint import pprint
from tabulate import tabulate
from collections import Counter
from operator import itemgetter

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


# User login:

def login():
    """
    Allow for user login by getting login credentials from user
    and comparing them to data from worksheet.
    """
    # receive information from Google Sheets
    logins = SHEET.worksheet("logins").get_all_values()
    logins_ws = SHEET.worksheet("logins")

    # get login credentials from user
    id = input("Enter your username:\n")
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


# Get data from user:

def main_menu():
    """
    Get information on user's choice of action in the system.
    """
    while True:
        breaker()
        print("This is Main Menu for *** Hotel Maintenance System ***")
        print("\nPlease choose one of the following options:\n")
        print("1 - Report new issue.")
        print("2 - Enquire about a room.")
        print("3 - See all maintenance tickets.\n")
        choice = input("Enter your choice here:\n")

        if validate_main_menu(choice):
            # change short into full word
            choice_long = {
                '1': '1 - Report new issue.',
                '2': '2 - Enquire about a room.',
                '3': '3 - See all maintenance tickets.'
            }
            selection = choice_long[choice]
            print(f"\nYou selected option: {selection}")
            break

    return choice


def validate_main_menu(value):
    """
    Checks validity of action choice entered by user.
    Returns ValueError if entered value 
    is not in correct format.
    """
    try:
        allowed = ['1', '2' ,'3']
        if not (value in allowed):
            raise ValueError(
                f"Issue type must be one digit: 1, 2 or 3.\nTry again!\n"
            )

    except ValueError as e:
        print(f"Invalid data: {e}")
        return False
    
    return True


def is_new_ticket():
    """
    Ask if user wants to enter new ticket.
    """
    while True:
        is_new_ticket = input(f"Do you wish to register new issue?\nAnswer Y for yes, or N for no: \n")
        
        if validate_yes_no_question(is_new_ticket):

            if is_new_ticket.lower() == "y":
                result = True
            elif is_new_ticket.lower() == "n":
                result = False

            break
    
    return result


def to_main_menu():
    """
    Ask if user wants to go to main menu.
    """
    while True:
        is_new_ticket = input(f"Do you wish to return to main menu?\nAnswer Y for yes, or N for no: \n")
        
        if validate_yes_no_question(is_new_ticket):

            if is_new_ticket.lower() == "y":
                result = True
            elif is_new_ticket.lower() == "n":
                result = False

            break
    
    return result


def get_room_number():
    """
    Get room number from user.
    Run a while loop to collect a valid room number from the user
    via the terminal, which must be a number built of 3 digits:
    1st between 1-6, 2nd equal 0, 3rd between 1-8.
    User may enter a - for all, to have all tickets displayed.
    The loop will repeatedly request data, until it is valid.
    """

    while True:
        print("Please enter room number.")
        print("Room number should be 3 digits, e.g. 102.")
        print("First digit representing floor (1-6),")
        print("followed by 0,")
        print("followed by digit 1-8.")
        print("For all other areas enter 000.")

        room_number = input("\nEnter room number here: \n")
        # normalize zero value to three character format
        if room_number == "0" : room_number = str('000')

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
        if (len(value) != 3 or int(value) > 608 or (int(value) == 0) or int(value[0]) > 6 or (value[0] == "0") or (value[1] != "0") or (value[2] == "0") or (int(value[2]) > 8) ) and int(value) != 0:
            raise ValueError(
                f"Room number should be 3 digits in the given format.\nTry again!"
            )

    except ValueError as e:
        print(f"\nInvalid data: {e}")
        return False
    
    return True


def get_urgency():
    """
    Get new issue urgency from user.
    Run a while loop to collect a valid urgency for the new ticket from the user via the terminal, 
    whic must be a letter:
    c - for critical,
    u - for urgent,
    n - for normal.
    Capital letters are accepted.
    The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("\nPlease enter issue urgency.")
        print("Urgency should be one letter:")
        print("c - for critical, u - for urgent, or n - for normal.")
        urgency = input("\nEnter urgency here: \n")
        urgency = urgency.lower()

        if validate_urgency(urgency):
            # change short into full word
            urgency_library = {
                'c': 'critical',
                'u': 'urgent',
                'n': 'normal'
            }
            urgency = urgency_library[urgency]
            print(f"\nYou entered that issue urgency is: {urgency}.")
            break

    return urgency

def validate_urgency(value):
    """
    Checks validity of urgency entered by user.
    Returns ValueError if entered value 
    is not in correct format.
    """
    try:
        urgency = value.lower()
        if str(urgency) != "c" and str(urgency) != "u" and str(urgency) != "n":
            raise ValueError(
                f"Urgency must be: \nc - for critical, u - for urgent or n - for normal.\nTry again!"
            )

    except ValueError as e:
        print(f"Invalid data: {e}")
        return False
    
    return True


def get_description():
    """
    Get room description of the issue from user.
    Run a while loop to collect a valid description from the user
    via the terminal, which must be a number built of at least 3 characters.
    The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter brief description of issue.")
        description = input("\nEnter description here: \n")

        if validate_description(description):
            print(f"\nDescription entered.")
            break
    
    return description

def validate_description(value):
    """
    Checks validity of issue description entered by user.
    Returns ValueError if entered value 
    is shorter than 3 characters.
    """
    try:
        if len(value) < 3:
            raise ValueError(
                f"Description too short.\nTry again!"
            )

    except ValueError as e:
        print(f"Invalid data: {e}")
        return False
    
    return True


def get_issue_type():
    """
    Get type of issue from user.
    Run a while loop to collect a valid type for the new ticket from the user via the terminal, which must be a letter:
    m - for mechanical,
    e - for electrical,
    h - for hydraulic.
    Capital letters are accepted.
    The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter issue type.")
        print("Type should be one letter:")
        print("m - for mechanical, e - for electrical, h - for hydraulic.")
        issue_type = input("\nEnter issue type here: \n")
        issue_type = issue_type.lower()

        
        if validate_issue_type(issue_type):
            # change short into full word
            issue_library = {
                'm': 'mechanical',
                'e': 'electrical',
                'h': 'hydraulic'
            }
            issue_type = issue_library[issue_type]
            print(f"\nYou entered type of issue: {issue_type}.")
            break

    return issue_type

def validate_issue_type(value):
    """
    Checks validity of issue type entered by user.
    Returns ValueError if entered value 
    is not in correct format.
    """
    try:
        # issue_type = value.lower()
        if str(value) != "m" and str(value) != "e" and str(value) != "h":
            raise ValueError(
                f"Issue type must be: \nm - for mechanical, e - for electrical, h - for hydraulic.\nTry again!"
            )

    except ValueError as e:
        print(f"Invalid data: {e}")
        return False
    
    return True


def should_send_ticket():
    """
    Ask if user wants to send new ticket.
    """
    while True:
        should_send_ticket = input(f"Do you wish to send the ticket?\nAnswer Y for yes, or N for no: \n")
        should_send_ticket = should_send_ticket.lower()
        
        if validate_should_send_ticket(should_send_ticket):

            if should_send_ticket == "y":
                result = True
            elif should_send_ticket == "n":
                result = False

            break
    
    return result

def validate_should_send_ticket(value):
    """
    Checks validity of Y/N answer about sending ticket.
    Returns ValueError if entered value 
    is not Y or N.
    Both lower case and capital letters are accepted.
    """
    try:
        # value = value.lower()
        if str(value) != "y" and str(value) != "n":
            raise ValueError(
                "Please answer Y for yes or N for no!"
            )

    except ValueError as e:
        print(f"Invalid data: {e}")
        return False
    
    return True


# Data manipulation

def create_ticket(room_number, urgency, issue_type, description):
    """
    Put together data for new maintenance ticket.
    """
    ticket = [room_number, urgency, issue_type, description]

    return ticket


def update_worksheet(ticket, worksheet):
    """
    Receives data for new ticket.
    Updates relevant worksheet with the new ticket.
    """
    print(f"\nUpdating '{worksheet}' worksheet...")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(ticket)
    print(f"Worksheet '{worksheet}' updated succesfully.")
    # information about email which is sent by Zapier
    print("Ticket emailed to Maintenance Team member.\n")


def display_ticket(value):
    """
    Shows maintenance ticket(s) for enquired room.
    """
    print(f"\nRetrieving information about room {value}...")
    
    # receive information from Google Sheets
    tickets = SHEET.worksheet("tickets").get_all_values()
    tickets_summary = SHEET.worksheet("tickets")
    
    # display number of tickets related to enquired room
    room_number_column = tickets_summary.col_values(1)
    room = Counter(room_number_column)
    occurencies = room[value]
    if occurencies == 1:
        print(f"There is currently {occurencies} ticket for this room.\n")
    else:
        if occurencies == 0: occurencies = "no"
        print(f"There are currently {occurencies} tickets for this room.\n")
    
    # Display tickets on enquired room if available
    try: 
        searched = value # searched can be a list
        room_indices = []
        for i in range(len(room_number_column)):
            if room_number_column[i] in searched:
                room_indices.append(i)

        # make list of details on rooms enquired only
        rooms_enquired_details = []
        for i in room_indices:
            rooms_enquired_details.append(tickets[i])

        # Show table containing rooms with tickets
        if occurencies != 'no':
            tickets_headers = tickets[0]
            print(tabulate(rooms_enquired_details, tickets_headers))
            print("")

    except:
        pass
    

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
    print(f"Total number of tickets: {number_of_tickets}, of which:\nCritical: {critical}, Urgent: {urgent}, Normal: {normal}.\n")

    
def display_all_tickets():
    """
    Display tickets for all rooms 
    with maintenance tickets.
    Tickets are sorted by room number and displayed as a table. 
    """
    print("Displaying tickets:\n")
    tickets = SHEET.worksheet("tickets").get_all_values()
    tickets_headers = tickets[0]
    del tickets[0]
    all_tickets_sorted = sorted(tickets, key=itemgetter(0))
    print(tabulate(all_tickets_sorted, tickets_headers))
    print("")


def validate_yes_no_question(value):
    """
    Checks validity of Y/N answer.
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


# Messages to show on screen:

def welcome_message():
    message = """ Welcome to Hotel Maintenance System! """
    table = [[message]]
    welcome_message = tabulate(table, tablefmt='fancy_grid')
    print(f"\n{welcome_message}\n")


def end_message():
    print("\nThank you for using *** Hotel Maintenance System! ***\n")


def breaker():
    """
    Provides visual break in the page 
    to distinguish different parts of application.
    """
    print("_" * 79 +"\n")


# Function sequences:

def make_choice():
    """
    Redirect user according to their choice of action.
    """
    choice = main_menu()
    if choice == '1':
        new_ticket_sequence()
        ending_sequence()
    elif choice == '2':
        room_number = get_room_number()
        display_ticket(room_number)
        ending_sequence()
    elif choice == '3':
        display_all_tickets()
        display_summary()
        ending_sequence()


def new_ticket_sequence():
    room_number = get_room_number()
    urgency = get_urgency()
    description = get_description()
    issue_type = get_issue_type()
    if should_send_ticket():
        ticket = create_ticket(room_number, urgency, issue_type, description)
        update_worksheet(ticket, "tickets")
        print("Getting summary for chosen room...")
        display_ticket(room_number)
    else:
        print("\nAction aborted. Ticket was not sent.")


def ending_sequence():
    if to_main_menu():
        make_choice()
    else:
        end_message()


# Main function

def main():
    """
    Run all program functions
    """
    welcome_message()

    login()

    make_choice()
    

main()

