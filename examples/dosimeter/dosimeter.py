#!/usr/bin/env python3

from gemc_api_utils import GConfiguration
from geometry import build_geometry

# Define GConfiguration: use TEXT factory.
# Initialize geometry file. No materials are built here.
configuration = GConfiguration("dosimeter", "TEXT", "target, cad import, and a dosimeter sphere made of plastic scintillator")
configuration.init_geom_file()

# build materials and print out the GConfiguration
build_geometry(configuration)
configuration.printC()

