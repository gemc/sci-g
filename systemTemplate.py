#!/usr/bin/env python3

# imports: do not edit these lines
import sys, os, argparse
import logging

_logger = logging.getLogger("sci-g")

NGIVEN='NOTGIVEN'

# Purposes:
# 1. write a geometry/material/mirror template file, using the system name and optional variation
# 2. print on screen geometry/material python snippets

def main():
	logging.basicConfig(level=logging.DEBUG)
	
	# Provides the -h, --help message
	desc_str = "   SCI-G template creator\n"
	parser = argparse.ArgumentParser(description=desc_str)
	
	# file writers
	parser.add_argument('-s', metavar='system',    action='store', type=str, help='write geometry / materials templates for system name', default=NGIVEN)
	parser.add_argument('-v', metavar='variation', action='store', type=str, help='sets system variation(s)', nargs='*', default=['default'])

	# code snippets loggers: volume
	parser.add_argument('-sl',      action='store_true',   help='show available solids list') # and geant4 documentation link
	parser.add_argument('-gvolume', metavar='volume',      action='store',  type=str, help='show on screen sci-g code for selected geant4 volume definitions', default='G4Box')

	args = parser.parse_args()
	
	# print(vars(args))
		
	if args.s != NGIVEN:
		writeTemplates(args.s, args.v)




def writeTemplates(system, variations):
	print()
	print(f' Writing files system template >{system}< using variations >{variations}<:')
	print()
	print(f'  - {system}.py')
	print(f'  - geometry.py')
	print(f'  - materials.py')
	print()
	print(f'  - Variations defined in {system}.py:')
	for v in variations:
		print(f'    * {v}')
	print()
	
	### {system}.py
	with open(f'{system}.py', 'w') as ps:
		ps.write('#!/usr/bin/env python3\n\n')
		ps.write('# python:\n')
		ps.write('import sys, os, argparse\n')
		ps.write('import logging\n')
		ps.write('import subprocess\n\n')
		ps.write('# sci-g:\n')
		ps.write('from gemc_api_utils import GConfiguration\n')
		ps.write('from gemc_api_geometry import *\n\n')
		ps.write(f'# {system}:\n')
		ps.write('from materials import define_materials\n\n')


	path=system + '.py'
	#os.chmod(path, 0o444)




if __name__ == "__main__":
	main()




