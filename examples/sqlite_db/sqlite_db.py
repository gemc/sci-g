#!/usr/bin/env python3

from gemc_api_utils import GConfiguration
from geometry import build_geometry
from materials import build_materials

# Define GConfiguration: use TEXT factory.
# Initialize geometry and materials files.
txt_config = GConfiguration("cloudc", "TEXT", "water vapor cloud chamber with a target and a lead shield")
txt_config.init_geom_file()
txt_config.init_mats_file()

# build geometry, materials and print out the GConfiguration
build_geometry(txt_config)
build_materials(txt_config)
txt_config.printC()

# Define GConfiguration: use SQLITE factory.
# Set the sqlite file name and open the connection to it.
sql_config = GConfiguration("cloudc", "SQLITE", "water vapor cloud chamber with a target and a lead shield")
sql_config.init_sqlite_file("sqlite_db.sqlite")

# build geometry, materials and print out the GConfiguration
# notice: for SQLITE factory, we also need to close the sqlite file connection.
build_geometry(sql_config)
build_materials(sql_config)

sql_config.printC()

sql_config.close_sqlite_file()

