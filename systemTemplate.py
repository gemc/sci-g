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
	
	path=system + '.py'

	if os.path.exists(path):
		checkWithUser = input('File already exist. Ok to overwrite? y/n ')
		if checkWithUser == "y":
			print(f'Overwriting files {path}, geometry.py and materials.py')
		else:
			print('Stopping execution')
			exit()
	
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
		ps.write('from materials import define_materials\n')
		ps.write(f'from geometry import build_{system}\n\n')

		ps.write(f'_logger = logging.getLogger("{system}")\n\n')
		ps.write('VARIATIONS = {\n')
		for v in variations:
			ps.write(f'    \"{v}",\n')
		ps.write('}\n\n')

		ps.write('def main():\n')
		ps.write('	logging.basicConfig(level=logging.DEBUG)\n\n')
		ps.write('	# Provides the -h, --help message\n')
		ps.write(f'	desc_str = "   Will create the {system}')
		ps.write(' system\\n"\n')
		ps.write('	parser = argparse.ArgumentParser(description=desc_str)\n')
		ps.write('	args = parser.parse_args()\n\n')
		ps.write('	for variation in VARIATIONS:\n\n')
		ps.write(f'		_logger.info(f"Building {system} volumes for variation')
		ps.write(' {variation}")\n')
		ps.write('		# Define GConfiguration name, factory and description.\n')
		ps.write(f'		configuration = GConfiguration(\'{system}\', \'TEXT\', \'The {system} system\')\n')
		ps.write('		configuration.setVariation(variation)\n\n')
		ps.write('		# define materials\n')
		ps.write('		configuration.init_mats_file()\n')
		ps.write('		define_materials(configuration)\n\n')
		ps.write('		# build geometry\n')
		ps.write('		configuration.init_geom_file()\n')
		ps.write(f'		build_{system}(configuration)\n\n')
		ps.write('		# print out the GConfiguration\n')
		ps.write('		configuration.printC()\n\n\n')
		ps.write('if __name__ == "__main__":\n')
		ps.write('	main()\n\n\n')
	# change permission
	os.chmod(path, 0o755)

	### materials.py
	with open('materials.py', 'w') as pm:
		pm.write('from gemc_api_materials import GMaterial\n\n')
		pm.write('def define_materials(configuration):\n\n')
		pm.write('# example of material: epoxy glue, defined with number of atoms\n')
		pm.write('	gmaterial = GMaterial("epoxy")\n')
		pm.write('	gmaterial.description = "epoxy glue 1.16 g/cm3"\n')
		pm.write('	gmaterial.density = 1.16\n')
		pm.write('	gmaterial.addNAtoms("H",  32)\n')
		pm.write('	gmaterial.addNAtoms("N",   2)\n')
		pm.write('	gmaterial.addNAtoms("O",   4)\n')
		pm.write('	gmaterial.addNAtoms("C",  15)\n')
		pm.write('	gmaterial.publish(configuration)\n\n')
		pm.write('# example of material: carbon fiber, defined using the fractional mass\n')
		pm.write('	gmaterial = GMaterial("carbonFiber")\n')
		pm.write('	gmaterial.description = "carbon fiber - 1.75g/cm3"\n')
		pm.write('	gmaterial.density = 1.75\n')
		pm.write('	gmaterial.addMaterialWithFractionalMass("G4_C",  0.745)\n')
		pm.write('	gmaterial.addMaterialWithFractionalMass("epoxy", 0.255)\n')
		pm.write('	gmaterial.publish(configuration)\n\n\n\n')


	### geometry.py
	with open('geometry.py', 'w') as pg:
		pg.write('from gemc_api_geometry import GVolume\n')
		pg.write('import math\n\n')
		pg.write(f'def build_{system}(configuration):\n')
		pg.write('	buildMotherVolume(configuration)\n')
		pg.write('	buildTarget(configuration)\n\n')
		pg.write('def buildMotherVolume(configuration):\n')
		pg.write('	gvolume = GVolume(\'absorber\')\n')
		pg.write('	gvolume.description = \'ft scintillation hodoscope inner volume\'\n')
		pg.write('	gvolume.makeG4Box(160.0, 160.0, 800.0)\n')
		pg.write('	gvolume.material    = \'carbonFiber\'\n')
		pg.write('	gvolume.color       = \'3399FF\'\n')
		pg.write('	gvolume.style       = 0\n')
		pg.write('	gvolume.publish(configuration)\n\n')
		pg.write('def buildTarget(configuration):\n')
		pg.write('	gvolume = GVolume(\'target\')\n')
		pg.write('	gvolume.description = \'epoxy target\'\n')
		pg.write('	gvolume.mother    = \'absorber\'\n')
		pg.write('	gvolume.makeG4Tubs(0, 20, 40, 0, 360)\n')
		pg.write('	gvolume.material    = \'epoxy\'\n')
		pg.write('	gvolume.color       = \'ff0000\'\n')
		pg.write('	gvolume.publish(configuration)\n\n\n\n')

	### jcard
	with open(f'{system}.jcard', 'w') as pj:
		pj.write('{\n')
		pj.write('	# no nthreads specified: runs on all available threads\n')
		pj.write('	# uncomment this line to specify number of threads\n')
		pj.write('	# "nthreads": 4,\n\n')
		pj.write('	# verbosities\n')
		pj.write('	"verbosity": 1,\n')
		pj.write('	"g4displayv": 2,\n')
		pj.write('	"gsystemv": 1,\n')
		pj.write('	"g4systemv": 2,\n\n')
		pj.write(f'	# the {system} system\n')
		pj.write('	"+gsystem": [\n')
		pj.write('		{\n')
		pj.write(f'			"system":   "./{system}",\n')
		pj.write('			"factory": "text",\n')
		pj.write('			"variation": "default"\n')
		pj.write('		}\n')
		pj.write('	],\n\n')
		pj.write('	"+goutput": [\n')
		pj.write('		{\n')
		pj.write('			"format": "ROOT",\n')
		pj.write('			"name": "events.root",\n')
		pj.write('			"type": "event"\n')
		pj.write('		},\n')
		pj.write('		{\n')
		pj.write('			"format": "TEXT",\n')
		pj.write('			"name": "events.txt",\n')
		pj.write('			"type": "event"\n')
		pj.write('		}\n')
		pj.write('	],\n\n')
		pj.write('	"n": 1,\n')
		pj.write('	"+gparticle": [\n')
		pj.write('		{ "pname": "pi0", "multiplicity": 1,  "p": 300,  "theta": 20.0, "delta_phi": 180.0, "vz": -20.0}\n')
		pj.write('	]\n')

		pj.write('}\n\n')

if __name__ == "__main__":
	main()




