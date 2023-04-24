#!/usr/bin/env python3

from gemc_api_utils import GConfiguration
from geometry import build_geometry


# Define GConfiguration name, factory and description. Initialize it.
configuration = GConfiguration("dosimeter", "TEXT", "target, cad import, and a dosimeter sphere made of plastic scintillator")
configuration.init_geom_file()

sql_config = GConfiguration("dosimeter", "SQLITE", "target, cad import, and a dosimeter sphere made of plastic scintillator")
sql_config.init_sqlite_file("dosimeter.sqlite")

# build the geometry using the local geometry file

build_geometry(configuration)
configuration.printC()



buildGeometry(sql_config)
sql_config.printC()
sql_config.close_sqlite_file()

