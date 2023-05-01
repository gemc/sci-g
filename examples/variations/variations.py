#!/usr/bin/env python3

from gemc_api_utils import GConfiguration
from geometry import build_geometry
from materials import build_materials

VARIATIONS = {
    "default",
    "lead_target",
}

for variation in VARIATIONS:
    # Define GConfiguration: use TEXT factory.
    # Initialize geometry and materials files.
    txt_config = GConfiguration("variations", "TEXT", "The variations system")
    txt_config.setVariation(variation)
    txt_config.init_geom_file()
    txt_config.init_mats_file()

    # build geometry, materials and print out the GConfiguration
    build_geometry(txt_config)
    build_materials(txt_config)
    txt_config.printC()

