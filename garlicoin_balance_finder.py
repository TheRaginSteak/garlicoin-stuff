"""
Script to find balances of garlicoin wallets and manipulate them
globals created: VALUE_DICTIONARY, OUR_TOTAL, PERCENT_DICTIONARY_US
"""
import urllib.request
import time
import calendar
from ast import literal_eval

def get_bool(prompt):
    """A simple function to get boolean options"""
    while True:
        try:
            return {"true":True, "false":False, "y":True, "n":False}[input(prompt).lower()]
        except KeyError:
            print("Invalid input")

USER_AGENT = \
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
HEADERS = {"User-Agent":USER_AGENT,}

def address_dict():
    """Function to get all the addresses into a dictionary"""
    address_dictionary = {}
    with open("addresses.txt", "r") as address_file:
        for line in address_file:
            if line[:1] == "#":
                continue
            (key, value) = line.split()
            address_dictionary.setdefault(key, [])
            address_dictionary[key] = value
    return address_dictionary


def url_dict():
    """Converts a file with addresses in into a dictionary"""
    url_dictionary = {}
    for key, value in address_dict().items():
        url_dictionary.setdefault(key, [])
        url_dictionary[key].append("https://explorer.grlc-bakery.fun/ext/getbalance/" + value)
    return url_dictionary


def url_value_finder(url):
    """Finds and returns the value of an address"""
    request = urllib.request.Request(url, None, HEADERS)
    response = urllib.request.urlopen(request)
    return response.read()


def money_value_dict():
    """Creates a dictionary with everyone's dollar grlc values"""
    money_value_dictionary = {}
    for key, value in VALUE_DICTIONARY.items():
        money_value_dictionary[key] = float(value) * GRLC_VALUE
    return money_value_dictionary

def value_dict():
    """Creates and prints a dictionary with all the wallet balances"""
    value_dictionary = {}
    url_dictionary = url_dict()
    for key in url_dictionary:
        value_dictionary[key] = 0.0
    for key, value in url_dictionary.items():
        for i in enumerate(value):
            i = i[0]
            try:
                value_dictionary[key] += float(url_value_finder(value[i]))
            except ValueError:
                value_dictionary[key] = 0.0

    value_dictionary_sorted = {}
    for i in sorted(value_dictionary, key=value_dictionary.get, reverse=True):
        """ this statement gets the sorted keys, then gets the index of the key and gets
        the sorted value with the same index"""
        value_dictionary_sorted[i] = sorted(value_dictionary.values(), reverse=True)\
            [sorted(value_dictionary, key=value_dictionary.get, reverse=True).index(i)]
    return value_dictionary_sorted


def record_balance():
    """Records the balance into a .txt file for grlc/hr functionality"""
    with open("garlic_amounts.txt", "a") as grlc_file:
        grlc_file.write("\n" + str(calendar.timegm(time.gmtime())) + "\n")
        for key, value in VALUE_DICTIONARY.items():
            grlc_file.write(key + " " + str(value)+"\n")


def print_values():
    """Prints all the values for balances and Percentages"""
    percent = get_bool("Do you want to view your wallet's percentage of the network? (Y/N) ")
    names = [key for key in VALUE_DICTIONARY]
    balances = [value for key, value in VALUE_DICTIONARY.items()]
    percentages = [value for key, value in PERCENT_DICTIONARY_US.items()]
    money_balances = [value for key, value in MONEY_VALUE_DICTIONARY.items()]
    if percent is True:
        percentages_network = [value for key, value in percent_dict_network().items()]

    print("\n")
    for i in enumerate(names):
        i = i[0]
        print(names[i].capitalize() + " " + str(round(balances[i], 3)) +
              "GRLC Monetary Value: $" + str(round(money_balances[i], 2)) +
              " Percentage of our supply: " + str(round(percentages[i], 3)) + "%")
        if percent is True:
            print("Percentage of total supply: " + str(round(percentages_network[i], 5)) + "%\n")
        else:
            print()
    print("Current GRLC value (Coin Market Cap) is: $" + str(round(GRLC_VALUE, 2)))
    print("Our garlic supply is: " + str(round(OUR_TOTAL, 3)))
    print("Total garlic supply is: " + str(round(float(
        url_value_finder("https://explorer.grlc-bakery.fun/ext/getmoneysupply")), 3)))


def percent_dict_us():
    """Creates a dictionary with the percentages of our supply"""
    percent_dictionary = {}
    for key, value in VALUE_DICTIONARY.items():
        percent_dictionary[key] = value / OUR_TOTAL * 100
    return percent_dictionary


def percent_dict_network():
    """Creates a dictionary with the percentages of the network"""
    percent_dictionary = {}
    total_value_network = url_value_finder("https://explorer.grlc-bakery.fun/ext/getmoneysupply")
    for key, value in VALUE_DICTIONARY.items():
        percent_dictionary[key] = value / float(total_value_network) * 100
    return percent_dictionary

VALUE_DICTIONARY = value_dict()

OUR_TOTAL = sum(value for key, value in VALUE_DICTIONARY.items())

PERCENT_DICTIONARY_US = percent_dict_us()

GRLC_STATS = literal_eval(url_value_finder("https://api.coinmarketcap.com/v1/ticker/garlicoin/").decode("utf-8"))[0]
GRLC_VALUE = float(GRLC_STATS["price_usd"])

MONEY_VALUE_DICTIONARY = money_value_dict()

def main():
    """Runs the functions"""
    print_values()
    record_balance()
