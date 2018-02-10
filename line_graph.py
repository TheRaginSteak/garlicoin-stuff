import matplotlib.pyplot as plt, matplotlib, calendar, time, datetime

def main():
    file = open("garlic_amounts.txt","r")
    data = file.read().split("\n\n")
    big_list = []
    for i in data:
        big_list.append(i.split("\n"))
    big_list[-1].remove("")
    datetimes= [datetime.datetime.fromtimestamp(float(i[0])) for i in big_list]
    num = 1
    for i in big_list:
        values = [float(i[num].split()[1]) for i in big_list]
        plt.plot(datetimes, values,linewidth=2.0, label=i[num].split()[0])
        num += 1
    plt.ylabel("garlicoin")
    plt.xlabel("time")
    plt.legend()
    plt.show()
    file.close()
main()

