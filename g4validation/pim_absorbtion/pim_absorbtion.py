#!/usr/bin/env python3

# python:
import sys, os, argparse
import logging
import subprocess

# sci-g:
from gemc_api_utils import GConfiguration

# pim_absorbtion:
from geometry import build_pim_absorbtion

_logger = logging.getLogger("pim_absorbtion")

VARIATIONS = {
    "default",
}

def main():
	logging.basicConfig(level=logging.DEBUG)

	# Provides the -h, --help message
	desc_str = "   Will create the pim_absorbtion system\n"
	parser = argparse.ArgumentParser(description=desc_str)
	args = parser.parse_args()

	for variation in VARIATIONS:

		_logger.info(f"Building pim_absorbtion volumes for variation {variation}")
		# Define GConfiguration name, factory and description.
		configuration = GConfiguration('pim_absorbtion', 'TEXT', 'The pim_absorbtion system')
		configuration.setVariation(variation)

		# build geometry
		configuration.init_geom_file()
		build_pim_absorbtion(configuration)

		# print out the GConfiguration
		configuration.printC()


if __name__ == "__main__":
	main()


