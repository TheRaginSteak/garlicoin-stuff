"""
Script to find balances of garlicoin wallets and manipulate them
Need to create an external file to store addresses rather than store them as a constant
"""
import urllib.request
import time

USER_AGENT = \
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
HEADERS = {"User-Agent":USER_AGENT,}

def get_bool(prompt):
    """A simple function to get boolean options"""
    while True:
        try:
            return {"true":True, "false":False, "y":True, "n":False}[input(prompt).lower()]
        except KeyError:
            print("Invalid input")

def url_dict():
    """Converts a file with addresses in into a dictionary"""
    address_dict = {}
    with open("addresses.txt", "r") as address_file:
        for line in address_file:
            if line[:1] == "#":
                continue
            (key, value) = line.split()
            address_dict[key] = "https://explorer.grlc-bakery.fun/ext/getbalance/" + value
    return address_dict

def url_value_finder(url):
    """Finds and returns the value of an address"""
    request = urllib.request.Request(url, None, HEADERS)
    response = urllib.request.urlopen(request)
    return response.read()

def value_dict():
    """Creates and prints a dictionary with all the wallet balances"""
    value_dictionary = {}
    for key, value in url_dict().items():
        try:
            if key in value_dictionary:
                value_dictionary[key] += float(url_value_finder(value))
            else:
                value_dictionary[key] = float(url_value_finder(value))
        except ValueError:
            value_dictionary[key] = 0.0
    return value_dictionary

def record_balance(name, balance):
    """Records the balance into a .txt file for grlc/hr functionality"""
    person_value = name + " " + str(balance)
    with open(time.time() +" GRLC balances.txt", 'a') as time_file:
        time_file.write(person_value)
    return 1

def print_values():
    """Prints all the values for balances and Percentages"""
    names = []
    balances = []
    percentages = []
    for key, value in VALUE_DICTIONARY.items():
        names.append(key)
        balances.append(value)
    for key, value in PERCENT_DICTIONARY_US.items():
        percentages.append(value)
    if PERCENT is True:
        percentages_network = []
        for key, value in percent_dict_network().items():
            percentages_network.append(value)

    for i in enumerate(names):
        i = i[0]
        print(names[i].capitalize() + " " + str(round(balances[i], 3)) +
              " Percentage of our supply: " + str(round(percentages[i], 3)) + "%")

        if PERCENT is True:
            print("Percentage of total supply: " + str(round(percentages_network[i], 5)) + "%\n")
        else:
            print()
    print("Total garlic supply is: " + str(round(float(
        url_value_finder("https://explorer.grlc-bakery.fun/ext/getmoneysupply")), 3)))

def percent_dict_us():
    """Creates a dictionary with the percentages of our supply"""
    percent_dictionary = {}
    total_value = 0
    for key, value in VALUE_DICTIONARY.items():
        total_value += value
    for key, value in VALUE_DICTIONARY.items():
        percent_dictionary[key] = value / total_value * 100
    return percent_dictionary

def percent_dict_network():
    """Creates a dictionary with the percentages of the network"""
    percent_dictionary = {}
    total_value = url_value_finder("https://explorer.grlc-bakery.fun/ext/getmoneysupply")
    for key, value in VALUE_DICTIONARY.items():
        percent_dictionary[key] = value / float(total_value) * 100
    return percent_dictionary

VALUE_DICTIONARY = value_dict()

PERCENT_DICTIONARY_US = percent_dict_us()

PERCENT = get_bool("Do you want to view your wallet's percentage of the network? (Y/N) ")

RECORD_TIME_FILE = get_bool("Do you want to write to a file for calculating GRLC/hr later? ")

def main():
    """Running the functions"""
    print_values()

if __name__ == "__main__":
    main()
