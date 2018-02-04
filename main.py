import garlicoin_balance_finder
import garlicoin_grapher

def get_bool(prompt):
    """A simple function to get boolean options"""
    while True:
        try:
            return {"true":True, "false":False, "y":True, "n":False}[input(prompt).lower()]
        except KeyError:
            print("Invalid input")


PRINTING_VALUES = get_bool("Do you want to print garlicoin values? (Y/N) ")

RECORD_TIME_FILE = get_bool("Do you want to write to a file for calculating GRLC/hr later? (Y/N) ")

def main():
    if PRINTING_VALUES is True:
        garlicoin_balance_finder.main()

    CHART = get_bool("Do you want a pie chart? (Y/N) ")
    if CHART is True:
        garlicoin_grapher.main()

if __name__ == '__main__':
    main()