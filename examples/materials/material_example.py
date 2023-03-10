#!/usr/bin/env python3

# imports: do not edit these lines
import sys, os, argparse
from gemc_api_utils import *
from gemc_api_geometry import *
from geometry import buildGeometry
from materials import define_materials


# Provides the -h, --help message
desc_str = "   Will create the dosimeter geometry\n"
parser = argparse.ArgumentParser(description=desc_str)
args = parser.parse_args()

# Define GConfiguration name, factory and description. Initialize it.
configuration = GConfiguration("material_example", "TEXT", "5 targets of different materials")

configuration.init_mats_file()
define_materials(configuration)

configuration.init_geom_file()
buildGeometry(configuration)

# print out the GConfiguration
configuration.printC()
