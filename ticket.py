import datetime


def validate_yes_no_question(value):
    """
    Checks validity of Y/N answer.
    Returns ValueError if entered value 
    is not Y or N.
    """
    try:
        value = value.lower()
        if str(value) != "y" and str(value) != "n":
            raise ValueError("Please answer Y for yes or N for no!")

    except ValueError as e:
        print(f"Invalid data: {e}")
        return False
    
    return True





def is_new_ticket():
    """
    Ask if user wants to start the process
    of entering new ticket.
    Returns True or False depending on user choice.
    """
    while True:
        is_new_ticket = input(
            f"Do you wish to register new issue?\nAnswer Y for yes, or N for no: \n")
        
        if validate_yes_no_question(is_new_ticket):

            if is_new_ticket.lower() == "y":
                result = True
            elif is_new_ticket.lower() == "n":
                result = False

            break
    
    return result








def get_urgency():
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
        print("\nPlease enter brief description of issue.")
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


def validate_issue_type(value):
    """
    Checks validity of issue type entered by user.
    Returns ValueError if entered value 
    is not in correct format.
    """
    try:
        # issue_type = value.lower()
        if str(value) != "m" and str(value) != "e" and str(value) != "h":
            raise ValueError(f"Issue type must be: \nm - for mechanical, e - for electrical, h - for hydraulic.\nTry again!")

    except ValueError as e:
        print(f"Invalid data: {e}")
        return False
    
    return True


def should_send_ticket():
    """
    Ask if user wants to send new ticket.
    Returns True or False depending on 
    whether user confirms sending ticket to the system.
    """
    while True:
        should_send_ticket = input(f"\nDo you wish to send the ticket?\nAnswer Y for yes, or N for no: \n")
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


def create_ticket(room, urgency, issue_type, description, status):
    """
    Put together data for new maintenance ticket.
    Returns full maintenence ticket.
    """
    # make timestamp as unique ticket number
    now = datetime.datetime.now()
    ticket_id = now.strftime("%y%m%d-%H%M")
    status = "open"
    ticket = [room, urgency, issue_type, description, status, ticket_id]

    return ticket



def to_main_menu():
    """
    Ask if user wants to go to main menu.
    Returns True or False.
    """
    while True:
        is_new_ticket = input(
            f"Do you wish to return to the Main Menu?\nAnswer Y for yes, or N for no: \n")
        
        if validate_yes_no_question(is_new_ticket):

            if is_new_ticket.lower() == "y":
                result = True
            elif is_new_ticket.lower() == "n":
                result = False

            break
    
    return result