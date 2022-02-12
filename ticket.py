import datetime


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


# def is_new_ticket() -> bool:
#     """
#     Ask if user wants to start the process
#     of entering new ticket.
#     Returns True or False depending on user choice.
#     """
#     while True:
#         start_new_ticket = input(
#             "Register new issue?\nAnswer Y for yes, or N for no:\n")

#         if validate_yes_no_question(start_new_ticket):

#             if start_new_ticket.lower() == "y":
#                 result = True
#             elif start_new_ticket.lower() == "n":
#                 result = False

#             break

#     return result


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
