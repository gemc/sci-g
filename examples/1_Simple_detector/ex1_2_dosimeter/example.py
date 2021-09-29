#!/usr/bin/env python

import sys, os, argparse

# define system configurations and various utilities
from gemc_api_utils import *
from gemc_api_geometry import *


# This section handles checking for the required configuration filename argument and also provides help and usage messages
desc_str = "   Will create the dsphere example geometry\n"
parser = argparse.ArgumentParser(description=desc_str)
args = parser.parse_args()

# Define configuration
# The first
configuration = GConfiguration("dsphere", "TEXT", "Example 1-3: a sphere dosimeter detector")

# initialize geometry file
# this is only necessary for TEXT or JSON confgurations
configuration.init_geom_file()


# build the geometry using the local geometry file
from geometry import *

buildGeometry(configuration)




