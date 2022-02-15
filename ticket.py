# imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python imports
import datetime

# external libraries imports
# import gspread
# from google.oauth2.service_account import Credentials
from tabulate import tabulate

# internal imports
import google_config
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# SCOPE = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive.file",
#     "https://www.googleapis.com/auth/drive"
#     ]

# CREDS = Credentials.from_service_account_file('creds.json')
# SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# SHEET = GSPREAD_CLIENT.open('hotel_maintenance')


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
    which must be a letter:
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
                "Urgency must be: \n")
            print("c - for critical, u - for urgent or n - for normal.")
            print("Try again!")

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
                "Issue type must be:")
            print("m - for mechanical, e - for electrical, h - for hydraulic.")
            print("Try again!")

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


def display_ticket(room: int):
    """
    Pulls tickets for enquired room from Google sheets.
    Shows open tickets to the user in a table.
    @param room(int): Room number.
    """
    print(f"\nRetrieving information about room {room}...")

    # receive information from Google Sheets
    tickets = google_config.SHEET.worksheet("tickets").get_all_values()
    tickets_all = google_config.SHEET.worksheet("tickets")

    # Display ticket(s) for enquired room if existent
    room_column = tickets_all.col_values(1)
    try:
        room_indices = []
        for i in range(len(room_column)):
            if room_column[i] in room:
                room_indices.append(i)

        # make list of tickets on room enquired
        room_enq_dets = []
        for i in room_indices:
            room_enq_dets.append(tickets[i])

        # make list of open tickets only
        open_tickets = []
        for i in range(len(room_enq_dets)):
            if room_enq_dets[i][4] == "open":
                open_tickets.append(room_enq_dets[i])

        # show summary on open tickets for the room
        open_num = len(open_tickets)
        if open_num == 1:
            print(f"There is now {open_num} open ticket for this room.\n")
        else:
            if open_num == 0:
                open_num = "no"
            print(f"There are now {open_num} open tickets for this room.\n")

        # Show table containing rooms with tickets
        if open_num != 'no':
            tickets_headers = tickets[0]
            # remove status column from view
            [col.pop(4) for col in open_tickets]
            tickets_headers.pop(4)
            # show table
            print(tabulate(open_tickets, tickets_headers))
            print("")

    except ValueError as e:
        print(f"Invalid data: {e}")


def close_ticket() -> bool:
    """
    Get ticket number from user and
    change status of the ticket from open to close.
    """
    # receive information from Google Sheets
    worksheet_to_update = google_config.SHEET.worksheet("tickets")

    # get login credentials from user
    while True:
        print("Please enter ticket id.")
        print(
            "Correct ticket id format is: 6 digits, hyphen (-) and 4 digits.")
        print("Ticket id can be found in room enquiry")
        print("by choosing Option 2 in the Main Menu.\n")
        ticket_id_entered = input("Enter ticket id:\n")

        try:
            # get index of ticket entered in the tickets worksheet
            column = worksheet_to_update.col_values(6)
            ticket_id_index = column.index(ticket_id_entered)

            # update cell
            print("\nUpdating ticket status...")
            col = 5
            worksheet_to_update.update_cell(ticket_id_index + 1, col, "closed")

        except ValueError as e:
            result = False
            print(f"\nUpdate failed. {e}.")
            print("\nPlease check ticket id and try again.")

        else:
            show_ticket_by_id(ticket_id_entered)
            print(f"Ticket {ticket_id_entered} closed successfully.\n")
            result = True
            break

    return result


def show_ticket_by_id(ticket_id_entered: str):
    """
    Pulls ticket from Google sheets.
    Shows open ticket to the user in a table.
    @param ticket_id_entered(str): Unique ticket id.
    """
    print(f"\nRetrieving ticket {ticket_id_entered}...")

    # receive information from Google Sheets
    tickets = google_config.SHEET.worksheet("tickets").get_all_values()

    # get data for ticket to be closed
    ticket_closed = []
    for i in range(len(tickets)):
        if tickets[i][5] == ticket_id_entered:
            ticket_closed = tickets[i]

    # get header for ticket to be closed
    tickets_headers = tickets[0]

    # remove status column from view
    ticket_closed.pop(4)
    tickets_headers.pop(4)

    # build and show table
    print("")
    print(tabulate([ticket_closed], tickets_headers))
    print("")


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
