"""
Module to create graphs from garlicoin balances
globals used: VALUE_DICTIONARY OUR_TOTAL
"""
import matplotlib.pyplot as plt
from time import strftime
from garlicoin_balance_finder import VALUE_DICTIONARY, OUR_TOTAL, get_bool

NAMES = []
BALANCES = []
EXPLODE = []
COLORS = []
USABLE_COLOURS = ["red", "orange", "yellow", "green", "blue", "indigo", "lightgreen", "lightblue", "gold"]
SAVE_AS_FILE = None

def general_values():
    SAVE_AS_FILE = get_bool("Do you want to save as a file? (Y/N) ")

    for key, value in VALUE_DICTIONARY.items():
        NAMES.append(key.capitalize())
        BALANCES.append(value)

    for size in BALANCES:
        if size < 10:
            EXPLODE.append(0.4)
        else:
            EXPLODE.append(0)

    for i in range(len(BALANCES)):
        COLORS.append(USABLE_COLOURS[i])


def pie_chart():
    """Creates a pie chart and saves it to a file"""



    plt.title("Our total supply is: " + str(round(OUR_TOTAL, 3)))
    plt.pie(BALANCES, explode = EXPLODE, labels = NAMES, colors = COLORS, autopct = make_autopct(BALANCES))
    plt.axis("equal")
    if SAVE_AS_FILE is True:
        plt.savefig("charts/" + input("What file do you want to save to? ") + strftime(" %d.%m.%Y %H%M") +".png")
    plt.show()


def bar_chart():
    return

def make_autopct(sizes):
    def my_autopct(pct):
        total = sum(sizes)
        val = int(round(pct * total / 100))
        return("{p:.2f}% ({v:d})".format(p = pct, v = val))
    return my_autopct

def main():
    general_values()
    while True:
        chart_type = input("Do you want a bar chart or a pie chart?")
        if chart_type == "pie":
            pie_chart()
            return
        elif chart_type == 'bar':
            bar_chart()
            return
        else:
            print("Please enter a valid value")

