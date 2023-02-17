#!/usr/bin/env python3

# python:
import sys, os, argparse
import logging
import subprocess

# sci-g:
from gemc_api_utils import GConfiguration

# bcal:
from materials import define_materials
from geometry import build_bcal

_logger = logging.getLogger("bcal")

VARIATIONS = {
    "default",
}

def main():
	logging.basicConfig(level=logging.DEBUG)

	# Provides the -h, --help message
	desc_str = "   Will create the bcal system\n"
	parser = argparse.ArgumentParser(description=desc_str)
	args = parser.parse_args()

	for variation in VARIATIONS:

		_logger.info(f"Building bcal volumes for variation {variation}")
		# Define GConfiguration name, factory and description.
		configuration = GConfiguration('bcal', 'TEXT', 'The bcal system')
		configuration.setVariation(variation)

		# define materials
		configuration.init_mats_file()
		define_materials(configuration)

		# build geometry
		configuration.init_geom_file()
		build_bcal(configuration)

		# print out the GConfiguration
		configuration.printC()


if __name__ == "__main__":
	main()


