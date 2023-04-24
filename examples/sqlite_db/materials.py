from gemc_api_materials import GMaterial

def build_materials(configuration):

	# epoxy glue, defined with number of atoms
	gmaterial = GMaterial("epoxy")
	gmaterial.description = "epoxy glue 1.16 g/cm3"
	gmaterial.density = 1.16
	gmaterial.addNAtoms("H",  32)
	gmaterial.addNAtoms("N",   2)
	gmaterial.addNAtoms("O",   4)
	gmaterial.addNAtoms("C",  15)
	gmaterial.publish(configuration)


