#!/usr/bin/env python3

from gemc_api_utils import GConfiguration
from geometry import build_geometry

# Define GConfiguration: use TEXT factory.
# Initialize geometry file. No materials are built here.
txt_config = GConfiguration("flux_detector", "TEXT", "a simple geometry with a target and a flux detector")
txt_config.init_geom_file()

# build materials and print out the GConfiguration
build_geometry(txt_config)
txt_config.printC()
