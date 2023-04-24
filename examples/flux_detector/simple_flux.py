#!/usr/bin/env python3

# imports: do not edit these lines
import sys, os, argparse
from gemc_api_utils import *
from gemc_api_geometry import *

# Provides the -h, --help message
desc_str = "   Will create the simple_flux geometry\n"
parser = argparse.ArgumentParser(description=desc_str)
args = parser.parse_args()

# Define GConfiguration name, factory and description. Initialize it.
configuration = GConfiguration("simple_flux", "TEXT", "a target and a flux plastic scintillator")
configuration.init_geom_file()

# build the geometry using the local geometry file
from geometry import *
buildGeometry(configuration)

# print out the GConfiguration
configuration.printC()
