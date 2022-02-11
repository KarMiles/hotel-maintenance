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
    Ask if user wants to enter new ticket.
    Returns True or False depending on user choice.
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
    Returns True or False.
    """
    while True:
        is_new_ticket = input(f"Do you wish to return to the Main Menu?\nAnswer Y for yes, or N for no: \n")
        
        if validate_yes_no_question(is_new_ticket):

            if is_new_ticket.lower() == "y":
                result = True
            elif is_new_ticket.lower() == "n":
                result = False

            break
    
    return result