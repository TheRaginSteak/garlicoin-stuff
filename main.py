"""
Runs all the modules
"""

import garlicoin_balance_finder as grlc_balance
import garlicoin_grapher as grlc_grapher

PRINTING_VALUES = grlc_balance.get_bool("Do you want to print garlicoin values? (Y/N) ")

def main():
    if PRINTING_VALUES is True:
        grlc_balance.main()

    CHART = grlc_balance.get_bool("Do you want a chart? (Y/N) ")
    if CHART is True:
        grlc_grapher.main()

if __name__ == '__main__':
    main()