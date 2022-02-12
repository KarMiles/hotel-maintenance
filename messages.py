# external libraries imports
from tabulate import tabulate


class Encapsulate:
    """
    Creates encapsulation of a message for visual effect.
    Formats allowed for tabulate are:
    "plain", "simple", "github", "grid", "fancy_grid",
    "pipe", "orgtbl", "jira", "presto", "pretty", "psql"
    "rst", "mediawiki", "moinmoin", "youtrack", "html",
    "unsafehtml", "latex", "latex_raw", "latex_booktabs",
    "latex_longtable", "textile", "tsv".
    Both message and format should be in "".
    """
    def __init__(self, message: str, format: str):
        """
        Format message in a frame of chosen kind.
        """
        self.message = message
        self.format = format

        table = [[message]]
        msg = tabulate(table, tablefmt=format)
        print(f"\n{msg}\n")


def welcome_message():
    """
    Message to be shown at the start of the system.
    """
    Encapsulate(" Welcome to Hotel Maintenance System! ", "fancy_grid")


def end_message():
    """
    Message shown at the end of interaction
    between user and system.
    """
    print("\nThank you for using *** Hotel Maintenance System! ***\n")
