# Python imports
from collections import Counter
from operator import itemgetter

# external libraries imports
import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate

# internal imports
import authorization
import ticket
import messages

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hotel_maintenance')


def main_menu() -> int:
    """
    Get information on user's choice of action in the system.
    Returns 1, 2, or 3 for further functions to be called.
    """
    while True:
        messages.Encapsulate(
            " This is Main Menu for *** Hotel Maintenance System *** ", "rst")
        print("Please choose one of the following options:\n")
        print("1 - Report new issue.")
        print("2 - Enquire about a room.")
        print("3 - Close ticket.")
        print("4 - See all maintenance tickets.\n")
        choice = input("Enter your choice here:\n")

        if validate_main_menu(choice):
            # confirm choice on screen
            choice_long = {
                '1': '1 - Report new issue.',
                '2': '2 - Enquire about a room.',
                '3': '3 - Close ticket.',
                '4': '4 - See all maintenance tickets.'
            }
            selection = choice_long[choice]
            messages.Encapsulate(f"You selected option: {selection}", "simple")
            break

    return choice


def validate_main_menu(choice: int) -> bool:
    """
    Checks validity of action choice entered by user.
    Returns ValueError if entered value
    is not in correct format.
    @param option(int): Choice of menu item entered by user.
    """
    try:
        allowed = ['1', '2', '3', '4']
        if not (choice in allowed):
            raise ValueError(
                "Issue type must be one digit: 1, 2, 3, or 4.\nTry again!\n")

    except ValueError as e:
        print(f"Invalid data: {e}")
        return False

    return True


def get_room() -> int:
    """
    Get room number from user.
    Run a while loop to collect a valid room number from the user
    via the terminal.
    Room number must be built of 3 digits:
    1st between 1-6, 2nd equal 0, 3rd between 1-8.
    Number 000 means all other areas of the hotel.
    The loop will repeatedly request data, until it is valid.
    Returns room number in 3 - character format.
    """

    while True:
        print("Please enter room number.")
        print("Room number should be 3 digits, e.g. 102.")
        print("First digit representing floor (1-6),")
        print("followed by 0,")
        print("followed by digit 1-8.")
        print("For all other areas enter 000.")

        room = input("\nEnter room number here: \n")
        # normalize zero value to three character format
        if room == "0":
            room = str('000')

        if validate_room(room):
            print(f"\nYou entered room number {room}.")
            break

    return room


def validate_room(room: int) -> bool:
    """
    Checks validity of room number entered by user.
    Returns ValueError if entered room
    is not a correct room number.
    @param room(int): Room number entered by user.
    """
    try:
        if ((
            len(room) != 3 or
            int(room) > 608 or
            (int(room) == 0) or
            int(room[0]) > 6 or
            (room[0] == "0") or
            (room[1] != "0") or
            (room[2] == "0") or
            (int(room[2]) > 8)) and
                (int(room) != 0)):
                raise ValueError(
                    "\nRoom number is 3 digits in given format.\nTry again!\n")

    except ValueError:
        print(
            "Room number is 3 digits in given format.\nTry again!\n")
        return False

    return True


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
    print(f"Total number of tickets: {number_of_tickets}, of which:")
    print(f"Critical: {critical}, Urgent: {urgent}, Normal: {normal}.\n")


def display_all_tickets():
    """
    Display tickets for all rooms
    with maintenance tickets.
    Tickets are sorted by room number and displayed as a table.
    """
    print("Displaying tickets:\n")

    # get data from worksheet
    tickets = SHEET.worksheet("tickets").get_all_values()

    # prepare headers
    tickets_headers = tickets[0]

    # prepare data
    del tickets[0]
    all_tickets_sorted = sorted(tickets, key=itemgetter(0))

    # remove id column from view - data
    [col.pop(5) for col in all_tickets_sorted]

    # remove status column from view - headers
    tickets_headers.pop(5)

    # show table with all tickets
    print(tabulate(all_tickets_sorted, tickets_headers))
    print("_" * 79)
    print("")


def update_worksheet(ticket: list, worksheet: str):
    """
    Receives data for new ticket.
    Updates relevant Google worksheet with the new ticket.
    @param: ticket(list): List containing data creating a ticket
    (room, urgency, issue_type, description, status).
    @param: worksheet(str): Tab name in Google worksheet
    containing tickets.

    """
    print(f"\nUpdating '{worksheet}' worksheet...")

    # update ticket worksheet with new ticket
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(ticket)

    # show information that worksheet is updated
    print("Worksheet updated succesfully.")

    # show information about email which is sent by Zapier
    print("Ticket emailed to Maintenance Team member.\n")


def new_ticket_sequence():
    """
    Sequence of functions to be started
    when user choses to enter a new ticket.
    """
    room = get_room()
    urgency = ticket.get_urgency()
    description = ticket.get_description()
    issue_type = ticket.get_issue_type()
    if ticket.should_send_ticket():
        new_ticket = ticket.create_ticket(
            room,
            urgency,
            issue_type,
            description)
        update_worksheet(new_ticket, "tickets")
        print("Getting summary for the affected room...")
        ticket.display_ticket(room)
    else:
        print("\nAction aborted. Ticket was not sent.\n")


def make_choice():
    """
    Redirect user to appropriate functions
    according to their choice of action.
    Placed outside main function
    for convenient referencing back from other functions.
    """
    choice = main_menu()
    if choice == '1':
        new_ticket_sequence()
        ending_sequence()
    elif choice == '2':
        room = get_room()
        ticket.display_ticket(room)
        ending_sequence()
    elif choice == '3':
        ticket.close_ticket()
        ending_sequence()
    elif choice == '4':
        display_all_tickets()
        display_summary()
        ending_sequence()


def ending_sequence():
    """
    Asks user whether to return to Main Menu.
    If not an ending message is shown and application ends.
    """
    if ticket.to_main_menu():
        make_choice()
    else:
        messages.end_message()


def main():
    """
    Run all program functions
    """
    messages.welcome_message()

    authorization.login()

    make_choice()


main()
