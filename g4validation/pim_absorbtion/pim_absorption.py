#!/usr/bin/env python3

import logging

# sci-g:
from gemc_api_utils import GConfiguration

# pim_absorption:
from geometry import build_pim_absorption

_logger = logging.getLogger("pim_absorption")

VARIATIONS = {
    "default",
}


def main():
    logging.basicConfig(level=logging.DEBUG)

    for variation in VARIATIONS:
        _logger.info(f"Building pim_absorption volumes for variation {variation}")

        # Define GConfiguration name, factory and description.
        configuration = GConfiguration('pim_absorption', 'TEXT', 'The pim absorption system')
        configuration.setVariation(variation)

        # build geometry
        configuration.init_geom_file()
        build_pim_absorption(configuration)

        # print out the GConfiguration
        configuration.printC()


if __name__ == "__main__":
    main()
