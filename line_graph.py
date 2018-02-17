import matplotlib.pyplot as plt, matplotlib, calendar, time, datetime

def main():
    file = open("garlic_amounts.txt","r")
    data = file.read().split("\n\n")
    big_list = []
    for i in data:
        big_list.append(i.split("\n"))
    big_list[-1].remove("")
    names = [str(i.split()[0]) for i in big_list[0] if i.split()[0].isalpha()]
    datetimes = [datetime.datetime.fromtimestamp(float(i[0])) for i in big_list]
    raw_values = [[float(item[num].split()[1]) for num in range(1,len(big_list[0]))] for item in big_list]
    values = list(zip(*raw_values))
    for i in range(len(values)):
        plt.plot(datetimes,values[i],label=names[i])
    plt.ylabel("garlicoin")
    plt.xlabel("time")
    plt.legend()
    plt.show()
    file.close()

