"""
Script to find balances of garlicoin wallets and manipulate them
Need to create an external file to store addresses rather than store them as a constant
"""
import urllib.request
import time
import os

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

def address_to_dict():
    """Converts a file with addresses in into a dictionary"""
    address_dict = {}
    with open("addresses.txt", "r") as address_file:
        for line in address_file:
            if line[:1] == "#":
                continue
            (key, value) = line.split()
            address_dict[key] = value
    return address_dict

def address_to_url(address):
    """Turns the address into a usable URL"""
    return "https://explorer.grlc-bakery.fun/ext/getbalance/" + address

def url_dict():
    """Creates a dictionary with all the URLs for the wallet balances"""
    url_dictionary = {}
    for key, value in address_to_dict().items():
        url_dictionary.update({key : address_to_url(value)})
    return url_dictionary

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
            test = value_dictionary[key]
        except KeyError:
            try:
                value_dictionary[key] = float(url_value_finder(value))
            except ValueError:
                value_dictionary[key] = 0.0
        else:
            value_dictionary[key] += float(url_value_finder(value))

    return value_dictionary

def return_total():
    """Prints the total of all the wallet balances"""
    total = 0
    for i in url_dict():
        try:
            total += float(url_value_finder(url_dict()[i]))
        except ValueError:
            continue
    return total

def percentage_finder_network(balance):
    """Returns the percentage of the total supply of a wallet"""
    total_supply = float(url_value_finder("https://explorer.grlc-bakery.fun/ext/getmoneysupply"))
    return (balance / total_supply) * 100

def percentage_of_us(balance):
    """returns the percentage of the total out of our wallets"""
    try:
        return float(balance / return_total()) * 100
    except ZeroDivisionError:
        return 0

PERCENT = get_bool("Do you want to view your wallet's percentage of the network? (Y/N) ")

#def last_balance():



def main():
    """Running the functions"""
    print("Individual Balances:\n")
    total = 0
    value_dictionary = value_dict()
    with open(time.strftime("%d.%m.%Y %H%M GRLC balances.txt"), 'a') as time_file:
        if PERCENT is True:
            for key, value in value_dictionary.items():
                person_value = key.capitalize() + " " + str(round(value, 3))
                time_file.write(person_value)
                print(person_value +
                      " Percentage of our supply: " + str(round(percentage_of_us(value))) +
                      "% Percentage of total supply: " +
                      str(round(percentage_finder_network(value), 3)) + "%\n")
                total += value

        else:
            for key, value in value_dictionary.items():
                person_value = key.capitalize() + " " + str(round(value, 3)) + "\n"
                print(person_value)
                time_file.write(person_value)
                total += value

    print("Total balance is: " + str(round(total, 4)) + " GRLC")
    print("Total garlic supply is: " + str(round(float(url_value_finder("https://explorer.grlc-bakery.fun/ext/getmoneysupply")), 4)) + " GRLC")

if __name__ == "__main__":
    main()
