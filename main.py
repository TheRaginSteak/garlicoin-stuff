"""
Runs all the modules
"""

import garlicoin_balance_finder as grlc_balance
import garlicoin_grapher as grlc_grapher

def main():
    """Runs the modules the user wants"""
    printing_values = grlc_balance.get_bool("Do you want to print garlicoin values? (Y/N) ")
    if printing_values is True:
        grlc_balance.main()

    chart = grlc_balance.get_bool("Do you want a chart? (Y/N) ")
    if chart is True:
        grlc_grapher.main()

if __name__ == '__main__':
    main()
