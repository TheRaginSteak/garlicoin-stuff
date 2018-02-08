"""
Module to create graphs from garlicoin balances
"""
import matplotlib.pyplot as plt
from time import strftime
from garlicoin_balance_finder import value_dict, get_bool, OUR_TOTAL

def pie_chart():
    """Creates a pie chart and saves it to a file"""
    SAVE_AS_FILE = get_bool("Do you want to save as a file? (Y/N) ")

    labels = []
    sizes = []
    explode = []
    colors = []
    USABLE_COLOURS = ["red", "orange", "yellow", "green", "blue", "indigo", "lightgreen", "lightblue", "gold"]
    for key,value in value_dict().items():
        if value > 0:
          labels.append(key.capitalize())
          sizes.append(value)
    for size in sizes:
        if size < 10:
            explode.append(0.4)
        else:
            explode.append(0)
    for i in range(len(sizes)):
        colors.append(USABLE_COLOURS[i])

    plt.title("Our total supply is: " + str(round(OUR_TOTAL, 3)))
    plt.pie(sizes, explode = explode, labels = labels, colors = colors, autopct = make_autopct(sizes))
    plt.axis("equal")
    if SAVE_AS_FILE is True:
        plt.savefig("charts/" + input("What file do you want to save to? ") + strftime(" %d.%m.%Y %H%M") +".png")
    plt.show()

def make_autopct(sizes):
    def my_autopct(pct):
        total = sum(sizes)
        val = int(round(pct * total / 100))
        return("{p:.2f}% ({v:d})".format(p = pct, v = val))
    return my_autopct

def main():
    pie_chart()
