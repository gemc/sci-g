#!/usr/bin/env python3

import argparse
from gemc_api_utils import *
from geometry import *

# Provides the -h, --help message
desc_str = "   Will create the dosimeter geometry\n"
parser = argparse.ArgumentParser(description=desc_str)
args = parser.parse_args()

# Define GConfiguration name, factory and description. Initialize it.
configuration = GConfiguration("dosimeter", "TEXT", "target, cad import, and a dosimeter sphere made of plastic scintillator")
configuration.init_geom_file()

sql_config = GConfiguration("dosimeter", "SQLITE", "target, cad import, and a dosimeter sphere made of plastic scintillator")
sql_config.init_sqlite_file("dosimeter.sqlite")

# build the geometry using the local geometry file

buildGeometry(configuration)
configuration.printC()



buildGeometry(sql_config)
sql_config.printC()
sql_config.close_sqlite_file()

