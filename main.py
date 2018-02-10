"""
Runs all the modules
"""

import checker as grlc_balance
import chart as grlc_grapher
import line_graph as grlc_line

def main():
    PRINTING_VALUES = grlc_balance.get_bool("Do you want to print garlicoin values? (Y/N) ")
    if PRINTING_VALUES is True:
        grlc_balance.main()

    CHART = grlc_balance.get_bool("Do you want a chart? (Y/N) ")
    if CHART:
        grlc_grapher.main()
    
    LINE = grlc_balance.get_bool("Do you want a line graph? (Y/N) ")
    if LINE:
        grlc_line.main()

if __name__ == '__main__':
    main()
