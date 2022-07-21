#!/usr/bin/env python3

# imports: do not edit these lines
import sys, os, argparse
import logging

_logger = logging.getLogger("sci-g")


# Purposes:
# 1. write a geometry/material/mirror template file, using the system name and optional variation
# 2. print on screen geometry/material python snippets

def main():
	logging.basicConfig(level=logging.DEBUG)
	
	# Provides the -h, --help message
	desc_str = "   SCI-G template creator\n"
	parser = argparse.ArgumentParser(description=desc_str)
	
	# file writers
	parser.add_argument('-g', action='store_true', help='write a geometry template file (system name required) ')
	parser.add_argument('-m', action='store_true', help='write a materials template file (system name required) ')
	parser.add_argument('-s', metavar='system',    action='store', type=str, help='sets system name')
	parser.add_argument('-v', metavar='variation', action='store', type=str, help='sets system variation(s)', nargs='*', default='default')

	# code snippets loggers: volume
	parser.add_argument('-sl',    action='store_true', help='show available solids and geant4 documentation link')
	parser.add_argument('-gvolume', metavar='volume',      action='store',  type=str, help='log on screen sci-g code for selected geant4 volumes definitions', default='G4Box')
	parser.add_argument('-gname',   metavar='volume name', action='store',  type=str, help='log on screen sci-g code for selected geant4 solid', default='myname')

	# code snippets loggers: materialz

	args = parser.parse_args()



	_logger.info(f" Building PCAL configuration for variation ")
	
	print(vars(args))
	
	# print(args.g)


if __name__ == "__main__":
	main()




