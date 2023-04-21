#!/usr/bin/env python3

from gemc_api_utils import *
from materials import define_materials

# Define GConfiguration name, factory and description. Initialize it.
configuration = GConfiguration("cad_imports", "TEXT", "cad imports")
configuration.init_mats_file()

define_materials(configuration)
configuration.printC()
