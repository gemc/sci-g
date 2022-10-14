#!/usr/bin/env python3

# imports: do not edit these lines
import argparse
import logging
import os

_logger = logging.getLogger("sci-g")

NGIVEN = 'NOTGIVEN'

# Purposes:
# 1. write a geometry/material/mirror template file, using the system name and optional variation
# 2. print on screen geometry/material python snippets

# the first string in the array is the name of the solid
# the second string is the name of the api function to use
AVAILABLE_SOLIDS_MAP = {
    "G4Box": ["Simple Box",
              "make_box(dx, dy, dz, lunit='mm')"],
    "G4Tubs": ["Cylindrical Section or Tube",
               "make_tube(rin, rout, length, phistart, phitotal, lunit1='mm', lunit2='deg')"],
    # "G4CutTubs": "Cylindrical Cut Section or Cut Tube",
    # "G4Cons": "Cone or Conical section",
    # "G4Para": "Parallelepiped",
    # "G4Trd": "Trapezoid",
    # "G4TrapRAW": "Generic Trapezoid: right Angular Wedge",
    # "G4TrapG": "Generic Trapezoid: general trapezoid",
    # "G4Trap8": "Generic Trapezoid: from eight points",
    # "G4Sphere": "Sphere or Spherical Shell Section",
    # "G4Orb": "Full Solid Sphere",
    # "G4Torus": "Torus",
    # "G4Polycone": "Polycons",
    # "G4GenericPolycone": "Generic Polycone",
    # "G4Polyhedra": "Polyhedra",
    # "G4EllipticalTube": "Tube with an elliptical cross section",
    # "G4Ellipsoid": "General Ellipsoid",
    # "G4EllipticalCone": "Cone with Elliptical Cross Section",
    # "G4Paraboloid": "Paraboloid, a solid with parabolic profile",
    # "G4Hype": "Tube with Hyperbolic Profile",
    # "G4Tet": "Tetrahedra",
    # "G4ExtrudedSolid": "Extruded Polygon",
    # "G4TwistedBox": "Box Twisted",
    # "G4TwistedTrap": "Trapezoid Twisted along One Axis",
    # "G4TwistedTrd": "Twisted Trapezoid with X and Y dimensions varying along Z",
    # "G4GenericTrap": "Generic trapezoid with optionally collapsing vertices",
    # "G4TwistedTubs": "Tube Section Twisted along Its Axis"
}



def main():
    logging.basicConfig(level=logging.DEBUG)

    # Provides the -h, --help message
    desc_str = "   SCI-G template creator\n"
    parser = argparse.ArgumentParser(description=desc_str)

    # file writers
    parser.add_argument('-s', metavar='system', action='store', type=str,
                        help='write geometry / materials templates for system name', default=NGIVEN)
    parser.add_argument('-v', metavar='variation', action='store', type=str,
                        help='sets system variation(s)', nargs='*', default=['default'])

    # code snippets loggers: volume
    parser.add_argument('-sl', action='store_true', help='show available solids list')  # and geant4 documentation link
    parser.add_argument('-gvolume', metavar='volume', action='store', type=str,
                        help="show on screen sci-g code for selected geant4 volume type. "
                             "Use ' -sl ' to list the available types.",
                        default='NOTGIVEN')
    parser.add_argument('-gmatFM', metavar='material', action='store', type=str,
                        help='show on screen sci-g code for a material defined using fractional masses',
                        default='NOTGIVEN')
    parser.add_argument('-gmatNA', metavar='material', action='store', type=str,
                        help='show on screen sci-g code for a material defined using number of atoms',
                        default='NOTGIVEN')

    args = parser.parse_args()

    # print(vars(args))

    if args.s != NGIVEN:
        write_templates(args.s, args.v)

    if args.gvolume != NGIVEN:
        logGVolume(args.gvolume)

    if args.sl:
        printAllG4Solids()


def write_templates(system, variations):
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

    path = system + '.py'

    if os.path.exists(path):
        checkWithUser = input('File already exist. Ok to overwrite? y/n ')
        if checkWithUser == "y":
            print(f'Overwriting files {path}, geometry.py and materials.py')
        else:
            print('Stopping execution')
            exit()

    with open(f'{system}.py', 'w') as ps:
        ps.write('#!/usr/bin/env python3\n\n')
        ps.write('# python:\n')
        ps.write('import sys, os, argparse\n')
        ps.write('import logging\n')
        ps.write('import subprocess\n\n')
        ps.write('# sci-g:\n')
        ps.write('from gemc_api_utils import GConfiguration\n\n')
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

    # write materials file
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

    # write geometry file
    with open('geometry.py', 'w') as pg:
        pg.write('from gemc_api_geometry import GVolume\n')
        pg.write('import math\n\n')
        pg.write(f'def build_{system}(configuration):\n')
        pg.write('	buildMotherVolume(configuration)\n')
        pg.write('	buildTarget(configuration)\n\n')
        pg.write('def buildMotherVolume(configuration):\n')
        pg.write('	gvolume = GVolume(\'absorber\')\n')
        pg.write('	gvolume.description = \'ft scintillation hodoscope inner volume\'\n')
        pg.write('	gvolume.make_box(160.0, 160.0, 800.0)\n')
        pg.write('	gvolume.material    = \'carbonFiber\'\n')
        pg.write('	gvolume.color       = \'3399FF\'\n')
        pg.write('	gvolume.style       = 0\n')
        pg.write('	gvolume.publish(configuration)\n\n')
        pg.write('def buildTarget(configuration):\n')
        pg.write('	gvolume = GVolume(\'target\')\n')
        pg.write('	gvolume.description = \'epoxy target\'\n')
        pg.write('	gvolume.mother    = \'absorber\'\n')
        pg.write('	gvolume.make_tube(0, 20, 40, 0, 360)\n')
        pg.write('	gvolume.material    = \'epoxy\'\n')
        pg.write('	gvolume.color       = \'ff0000\'\n')
        pg.write('	gvolume.publish(configuration)\n\n\n\n')

    # write jcard file
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
        pj.write(
            '		{ "pname": "pi0", "multiplicity": 1,  "p": 300,  "theta": 20.0, "delta_phi": 180.0, "vz": -20.0}\n')
        pj.write('	]\n')

        pj.write('}\n\n')


def logGVolume(volumeType):
    volumeDefinitions = ['# Assign volume name, solid parameters and material below:']
    volumeDefinitions.append('gvolume = GVolume(\"myvolumeName\")')
    if volumeType == 'G4Box':
        volumeDefinitions.append('gvolume.make_box(myX, myY, myZ) # default units: mm.')
    elif volumeType == 'G4Tubs':
        volumeDefinitions.append(
            'gvolume.make_tube(rin, rout, length, phiStart, totalPhi) # default units: mm and degrees')
    else:
        print(f'\n Fatal error: {volumeType} not supported yet')
        exit(1)

    volumeDefinitions.append('gvolume.material = \'G4_AIR\'')
    volumeDefinitions.append('# Uncomment any of the lines below to set parameters different than these defaults:')
    volumeDefinitions.append('#  - mother volume: \'root\'')
    volumeDefinitions.append('#  - description: \'na\'')
    volumeDefinitions.append('#  - position: (0, 0, 0)')
    volumeDefinitions.append('#  - rotation: (0, 0, 0)')
    volumeDefinitions.append('#  - mfield: \'na\'')
    volumeDefinitions.append('#  - color: \'778899\' (2 digits for each of red,green,blue colors)')
    volumeDefinitions.append('#  - style: \'1\' (1 = surface, 0 = wireframe)')
    volumeDefinitions.append('#  - visible: \'1\' (1 = visible, 0 = invisible)')
    volumeDefinitions.append('#  - digitization: \'na\'')
    volumeDefinitions.append('#  - identifier: \'na\'')

    volumeDefinitions.append('#gvolume.mother = \'motherVolumeName\'')
    volumeDefinitions.append('#gvolume.description = \'describe your volume here\'')
    volumeDefinitions.append('#gvolume.setPosition(myX, myY, myZ)')
    volumeDefinitions.append('#gvolume.setRotation(myX, myY, myZ)')
    volumeDefinitions.append('#gvolume.color = \'838EDE\'')
    volumeDefinitions.append('#gvolume.style = \'0\'')
    volumeDefinitions.append('#gvolume.visible = \'0\'')
    volumeDefinitions.append('#gvolume.digitization = \'flux\'')
    volumeDefinitions.append('#gvolume.setIdentifier(\'paddleid\', 1)')

    volumeDefinitions.append('gvolume.publish(configuration)')

    logGVolumeFromDefs(volumeDefinitions)


def logGVolumeFromDefs(volumeDefinitions):
    print()
    for vd in volumeDefinitions:
        print(f'	{vd}')
    print()


def printAllG4Solids():
    print(
        '\n The Geant4\033[91m solid constructors\033[0m are described at:\n\n '
        'https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/Detector/Geometry/geomSolids'
        '.html\n')
    print(' The corresponding solids and their \033[92mconstructors\033[0m in gemc are:\n')
    for g4solid, description in AVAILABLE_SOLIDS_MAP.items():

        print(f'  - \033[91m{g4solid:20}\033[0m {description[0]:30}')
        print(f'  - \033[92m{description[1]} \033[0m\n')
    print('\n\n')


if __name__ == "__main__":
    main()
