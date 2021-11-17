#!/usr/bin/env python3

# imports: do not edit these lines
import sys, os, argparse
from gemc_api_utils import *
from gemc_api_geometry import *

from geometry import MAP_TARGET_TO_BUILDER

def main():
    # Provides the -h, --help message
    desc_str = '   Will create the clas12 targets geometry\n'

    # loop over all the defined builder finctions
    for target_key, builder in MAP_TARGET_TO_BUILDER.items():
        print(f"Building {target_key} target geometry")
        # Define GConfiguration name, factory and description. Initialize it.
        configuration = GConfiguration('clas12Target', 'TEXT', 'CLAS12 Targets')
        configuration.setVariation(target_key)
        configuration.init_geom_file()
        # run the selected builder function
        builder(configuration)
        # print out the GConfiguration
        configuration.printC()


if __name__ == '__main__':
    main()
