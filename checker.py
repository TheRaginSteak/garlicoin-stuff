import urllib.request, calendar, time, datetime

USER_AGENT = \
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
HEADERS = {"User-Agent":USER_AGENT,}

def get_bool(prompt):
    while True:
        try:
            return {"true":True, "false":False, "y":True, "n":False, "yes":True, "no":False}[input(prompt).lower()]
        except KeyError:
            print("Invalid input")

def url_dict():
    address_dict = {}
    with open("addresses.txt", "r") as address_file:
        for line in address_file:
            if line[:1] == "#":
                continue
            (key, value) = line.split()
            address_dict.setdefault(key, [])
            address_dict[key].append("https://explorer.grlc-bakery.fun/ext/getbalance/" + value)
    return address_dict

def url_value_finder(url):
    request = urllib.request.Request(url, None, HEADERS)
    response = urllib.request.urlopen(request)
    return response.read()

def value_dict():
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
    return value_dictionary

VALUE_DICTIONARY = value_dict()
total_value = sum(value for key,value in VALUE_DICTIONARY.items())
percent_list = [((value/total_value)*100) for key,value in VALUE_DICTIONARY.items()]
network_value = url_value_finder("https://explorer.grlc-bakery.fun/ext/getmoneysupply")
network_percentages = [value / float(network_value) * 100 for key,value in VALUE_DICTIONARY.items()]

def record_balance():
    file = open("garlic_amounts.txt","a")
    file.write("\n")
    file.write(str(calendar.timegm(time.gmtime())))
    file.write("\n")
    for key,value in VALUE_DICTIONARY.items():
        file.write(key+" "+str(value)+"\n")
    file.close()

def print_values(boolean):
    names = [key.capitalize() for key,value in VALUE_DICTIONARY.items()]
    balances = [value for key,value in VALUE_DICTIONARY.items()]
    things=[str(names[position])+": "+str(round(balances[position],3))+"\nPercentage of our supply: "+str(round(percent_list[position],3))+
           "%\n" + "Percentage of total supply: " + str(round(network_percentages[position],3)) + "%\n" if boolean else str(names[position])+": "+str(round(balances[position],3))+
           "\nPercentage of our supply: "+str(round(percent_list[position],3)) + "%\n" for position,value in enumerate(names)]
    for i in things:
        print(i)
    print("Our garlic supply is: " + str(round(total_value, 3)))
    print("Total garlic supply is:",float(network_value))

def main():
    PERCENT = get_bool("Do you want to view your wallet's percentage of the network? (Y/N) ")
    RECORD_TIME_FILE = get_bool("Do you want to write to a file for calculating GRLC/hr later? (Y/N) ")
    print_values(PERCENT)
    if RECORD_TIME_FILE:
        record_balance()
