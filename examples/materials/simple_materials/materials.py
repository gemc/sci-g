#=====================================
#
#	There are several ways to define a material in gemc.
#
#	1. Use a predefined material from the GEANT4 and NIST materials lists.
#		In this case gemc does not need an external definition from a materials input file, the detector may call directly
#		For example, use "G4_WATER" or "G4_Fe" in the detector material field. For box1, the material used is G4_Si
#
#	2. Define a material using the chemical formula, # of atoms per element. A dedicated function should be used:
#		addNAtoms( # of atoms, element Name ).
#
#	3. Define a material using the fractional mass. A dedicated function should be used:
#		addMaterialWithFractionalMass( material Name, fractional mass )
#
#=====================================

from gemc_api_materials import *

def defineMaterials(configuration):

	# scintillator for box 2
	# defined using the chemical formula
	gmaterial = GMaterial('scintillator')
	gmaterial.description = 'scintillator material'
	gmaterial.density     = 1.032
	gmaterial.addNAtoms('C', 9)
	gmaterial.addNAtoms('H', 10)
	gmaterial.publish(configuration)

	# water for box 3
	# defined using the chemical formula
	gmaterial = GMaterial('water')
	gmaterial.description = 'water material'
	gmaterial.density     = 1.0
	gmaterial.addNAtoms('H', 2)
	gmaterial.addNAtoms('O', 1)
	gmaterial.publish(configuration)

	# air for box 4
	# defined using fractional masses
	gmaterial = GMaterial('my_air')
	gmaterial.description = 'air material'
	gmaterial.density     = 0.001
	gmaterial.addMaterialWithFractionalMass('G4_N', 0.7)
	gmaterial.addMaterialWithFractionalMass('G4_O', 0.3)
	gmaterial.publish(configuration)
