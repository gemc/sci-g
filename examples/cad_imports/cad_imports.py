#!/usr/bin/env python3

from gemc_api_utils import GConfiguration
from materials import build_materials

# Define GConfiguration: use TEXT factory.
# Initialize materials file. No geometry is built here.
configuration = GConfiguration("cad_imports", "TEXT", "cad imports")
configuration.init_mats_file()

# build materials and print out the GConfiguration
build_materials(configuration)
configuration.printC()
