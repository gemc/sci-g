#!/usr/bin/env python3

from gemc_api_utils import GConfiguration
from geometry import build_geometry

sql_config = GConfiguration("fields", "SQLITE", "A small target with a magnetic field.")
sql_config.init_sqlite_file("sqlite_db.sqlite")

# build geometry, materials and print out the GConfiguration
# notice: for SQLITE factory, we also need to close the sqlite file connection.
build_geometry(sql_config)
sql_config.printC()

sql_config.close_sqlite_file()

