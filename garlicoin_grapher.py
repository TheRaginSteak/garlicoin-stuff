"""
Module to create graphs from garlicoin balances
globals used: VALUE_DICTIONARY OUR_TOTAL
"""
from time import strftime
import matplotlib.pyplot as plt
import numpy as np
from garlicoin_balance_finder import VALUE_DICTIONARY, OUR_TOTAL, get_bool

NAMES = []
BALANCES = []
EXPLODE = []
COLORS = []
USABLE_COLOURS = ["red", "orange", "yellow", "green",
                  "blue", "indigo", "lightgreen", "lightblue", "gold"] * 2

def general_values():
    """Creates all the values that the charts need"""
    for key, value in VALUE_DICTIONARY.items():
        NAMES.append(key.capitalize())
        BALANCES.append(value)

    for i in range(len(BALANCES)):
        COLORS.append(USABLE_COLOURS[i])


def pie_chart():
    """Creates a pie chart and saves it to a file"""
    save_as_file = get_bool("Do you want to save as a file? (Y/N) ")

    for i in BALANCES:
        if i == 0:
            NAMES.pop(BALANCES.index(i))
            BALANCES.remove(i)

    for size in BALANCES:
        if size < 10:
            EXPLODE.append(0.4)
        else:
            EXPLODE.append(0)

    plt.title("Our total supply is: " + str(round(OUR_TOTAL, 3)))
    plt.pie(BALANCES, explode=EXPLODE, labels=NAMES, colors=COLORS, autopct=make_autopct(BALANCES))
    plt.axis("equal")
    if save_as_file is True:
        plt.savefig("charts/" + input("What file do you want to save to? ")
                    + strftime(" %d.%m.%Y %H%M") +" Pie Chart.png")
    plt.show()


def bar_chart():
    """Creates a bar chart
    WIP"""
    save_as_file = get_bool("Do you want to save as a file? (Y/N) ")
    range_of_values = np.arange(len(BALANCES))

    plt.title("Our total supply is: " + str(round(OUR_TOTAL, 3)))
    plt.bar(range_of_values, BALANCES, color=COLORS)
    plt.xticks(range_of_values, NAMES)
    if save_as_file is True:
        plt.savefig("charts/" + input("What file do you want to save to? ")
                    + strftime(" %d.%m.%Y %H%M") +"Bar Chart.png")
    plt.show()


def make_autopct(sizes):
    """Automatic percentages"""
    def my_autopct(pct):
        """I'm not sure, stackoverflow said to do this"""
        total = sum(sizes)
        val = int(round(pct * total / 100))
        return "{p:.2f}% ({v:d})".format(p=pct, v=val)
    return my_autopct


def main():
    """Runs all the functions"""
    general_values()
    while True:
        chart_type = input("Do you want a bar chart or a pie chart? ").lower()
        if chart_type == "pie":
            pie_chart()
            return
        elif chart_type == 'bar':
            bar_chart()
            return
        else:
            print("Please enter a valid value")
