"""Module to create graphs from garlicoin balances"""
import matplotlib.pyplot as plt
from garlicoin_balance_finder import value_dict

def plot_bar_graph():
    plt.ylabel('GRLC')
    names = []
    values = []
    for key, value in value_dict():
        names.append[key.capitalize()]
        values.append(value)
