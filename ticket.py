# Python imports
import datetime

# external libraries imports
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


def validate_yes_no_question(answer: str) -> bool:
    """
    Checks validity of Y/N answer.
    Returns ValueError and instruction for user if entered value
    is not Y or N.
    """
    try:
        answer = answer.lower()
        if str(answer) != "y" and str(answer) != "n":
            raise ValueError("Please answer Y for yes or N for no!")

    except ValueError as e:
        print(f"Invalid data: {e}")
        return False

    return True


def get_urgency() -> str:
    """
    Get new issue urgency from user.
    Run a while loop to collect a valid urgency for the new ticket 
    from the user via the terminal, 
    whic must be a letter:
    c - for critical,
    u - for urgent,
    n - for normal.
    Capital letters are accepted.
    The loop will repeatedly request data, until it is valid.
    Returns issue urgency (critical, urgent, or normal).
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


def validate_urgency(urgency: str) -> bool:
    """
    Checks validity of urgency entered by user.
    Returns ValueError if entered value 
    is not in correct format.
    @param urgency(str): Ticket urgency in form of one letter
    c - for critical, u - for urgent, or n - for normal.
    """
    try:
        ur = urgency.lower()
        if str(ur) != "c" and str(ur) != "u" and str(ur) != "n":
            raise ValueError(
                "Urgency must be: \nc - for critical, u - for urgent or n - for normal.\nTry again!")

    except ValueError as e:
        print(f"Invalid data: {e}")
        return False

    return True


def get_description() -> str:
    """
    Get room description of the issue from user.
    Discription must be at least 3 characters long.
    The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("\nPlease enter brief description of issue.")
        description = input("\nEnter description here: \n")

        if validate_description(description):
            print("\nDescription entered.")
            break

    return description


def validate_description(description: str) -> bool:
    """
    Checks validity of issue description entered by user.
    Returns ValueError if entered value
    is shorter than 3 characters.
    @param: description(str): Issue description entered by user.
    """
    try:
        if len(description) < 3:
            raise ValueError("Description too short.\nTry again!")

    except ValueError as e:
        print(f"Invalid data: {e}")
        return False

    return True


def get_issue_type() -> str:
    """
    Get type of issue from user.
    Run a while loop to collect a valid type for the new ticket
    from the user via the terminal, which must be a letter:
    m - for mechanical,
    e - for electrical,
    h - for hydraulic.
    Capital letters are accepted.
    The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("\nPlease enter issue type.")
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


def validate_issue_type(type: str) -> bool:
    """
    Checks validity of issue type entered by user.
    Returns ValueError if entered value
    is not in correct format.
    @param type(str): Issue type entered by user,
    accepted values are: m, e or h.
    """
    try:
        type = type.lower()
        if str(type) != "m" and str(type) != "e" and str(type) != "h":
            raise ValueError(
                "Issue type must be: \nm - for mechanical, e - for electrical, h - for hydraulic.\nTry again!")

    except ValueError as e:
        print(f"Invalid data: {e}")
        return False

    return True


def should_send_ticket() -> bool:
    """
    Ask if user wants to submit new ticket.
    Returns True or False depending on 
    whether user confirms sending ticket to the system.
    """
    while True:
        should_send_ticket = input(
            "\nSubmit the ticket?\nAnswer Y for yes, or N for no: \n")
        should_send_ticket = should_send_ticket.lower()

        if validate_yes_no_question(should_send_ticket):

            if should_send_ticket == "y":
                result = True
            elif should_send_ticket == "n":
                result = False

            break

    return result


def create_ticket(
        room: int,
        urgency: str,
        issue_type: str,
        description: str) -> list:
    """
    Put together data for new maintenance ticket.
    Return full maintenence ticket.
    """
    # set default status as open
    status = "open"
   
    # use timestamp as unique ticket id
    now = datetime.datetime.now()
    ticket_id = now.strftime("%y%m%d-%H%M")

    ticket = [room, urgency, issue_type, description, status, ticket_id]

    return ticket


# DRAFT
def close_ticket():
    """
    Change status of a ticket from open to close.
    """
    # receive information from Google Sheets
    worksheet_to_update = SHEET.worksheet("tickets")

    # get login credentials from user
    ticket_id_entered = input("Enter ticket id:\n")

    try:
        # get index of ticket entered in the tickets worksheet
        column = worksheet_to_update.col_values(6)
        ticket_id_index = column.index(ticket_id_entered)
        print("-" * 79)
        print(ticket_id_index)

        # update cell
        col = 5
        worksheet_to_update.update_cell(ticket_id_index + 1, col, "closed")
        print("Updating ticket status...")
    
    except:
        result = False
        print("\nOperation failed.\nPlease check and try again.\n")
    
    else:
        # check login credentials
        if True: 
            result = True
            print(f"\nTicket {ticket_id_entered} closed successfully.")

        else:
            result = False
            print("\nUpdate failed.\nPlease check and try again.\n")

    return result


# close_ticket()


def to_main_menu() -> bool:
    """
    Ask if user wants to go to main menu.
    """
    while True:
        is_new_ticket = input(
            "Return to the Main Menu?\nAnswer Y for yes, or N for no: \n")

        if validate_yes_no_question(is_new_ticket):

            if is_new_ticket.lower() == "y":
                result = True
            elif is_new_ticket.lower() == "n":
                result = False

            break

    return result
