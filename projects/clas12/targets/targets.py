#!/usr/bin/env python

# imports: do not edit these lines
import sys, os, argparse
from gemc_api_utils import *
from gemc_api_geometry import *

from geometry import MAP_TARGET_TO_BUILDER


def main():
    # Provides the -h, --help message
    desc_str = '   Will create the clas12 targets geometry\n'
    parser = argparse.ArgumentParser(description=desc_str)
    parser.add_argument('target',
        choices=list(MAP_TARGET_TO_BUILDER.keys())
    )
    args = parser.parse_args()
    target = args.target

    # Define GConfiguration name, factory and description. Initialize it.
    configuration = GConfiguration('clas12Target', 'TEXT', 'CLAS12 Targets')
    configuration.setVariation(target)
    configuration.init_geom_file()

    # select the builder function based on the target passed as a command-line argument
    build_geometry = MAP_TARGET_TO_BUILDER[target]
    # run the selected builder function
    build_geometry(configuration)
    # print out the GConfiguration
    configuration.printC()


if __name__ == '__main__':
    main()
