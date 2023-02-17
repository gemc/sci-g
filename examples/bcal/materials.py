from gemc_api_materials import GMaterial

def define_materials(configuration):

# example of material: epoxy glue, defined with number of atoms
	gmaterial = GMaterial("epoxy")
	gmaterial.description = "epoxy glue 1.16 g/cm3"
	gmaterial.density = 1.16
	gmaterial.addNAtoms("H",  32)
	gmaterial.addNAtoms("N",   2)
	gmaterial.addNAtoms("O",   4)
	gmaterial.addNAtoms("C",  15)
	gmaterial.publish(configuration)

# example of material: carbon fiber, defined using the fractional mass
	gmaterial = GMaterial("carbonFiber")
	gmaterial.description = "carbon fiber - 1.75g/cm3"
	gmaterial.density = 1.75
	gmaterial.addMaterialWithFractionalMass("G4_C",  0.745)
	gmaterial.addMaterialWithFractionalMass("epoxy", 0.255)
	gmaterial.publish(configuration)

# 'Core': Core of the double cladded scintillating fiber
	'''
  	$mat{"name"}          		= "core";
	$mat{"description"}   		= "core of the double cladded scintillating fiber";
	$mat{"density"}       		= "1.05";
	$mat{"ncomponents"}   		= "2";
	$mat{"components"}    		= "C 9 H 9";
	$mat{"photonEnergy"}            = "0.187*eV 0.224*eV 0.236*eV 0.28*eV 0.311*eV 0.33*eV 0.4*eV 10.45*eV";
	$mat{"indexOfRefraction"} 	= "1.572 1.576 1.577 1.582 1.587 1.592 1.606 1.617";
	$mat{"reflectivity"} 		= "0.001 0.001 0.001 0.001 0.001 0.001 0.001";
	$mat{"efficiency"}		= "0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3";#TEST VALUE
	$mat{"absorptionLenght"}	= "0.394*m 0.394*m 0.394*m 0.394*m 0.394*m 0.394*m 0.394*m 0.394*m";
	$mat{"slowtimeconstant"}	= "2.8*ns";
	$mat{"fasttimeconstant"}        = "0.9*ns";
	$mat{"rayleigh"}                = "0.394*m";
	$mat{"yieldratio"}		= "0.9";	#TEST VALUE
	$mat{"scintillationyield"}	= "8000";   #TEST VALUE
	print_mat(\%configuration, \%mat);
	'''
	gmaterial = GMaterial("core")
	gmaterial.description = "core of the double cladded scintillating fiber"
	gmaterial.density = 1.05
	gmaterial.addMaterialWithFractionalMass("C",  0.9)
	gmaterial.addMaterialWithFractionalMass("H",  0.1)
	gmaterial.addPhotonEnergy("0.187*eV")
	gmaterial.addPhotonEnergy("0.224*eV")
	gmaterial.addPhotonEnergy("0.236*eV")
	gmaterial.addPhotonEnergy("0.28*eV")
	gmaterial.addPhotonEnergy("0.311*eV")
	gmaterial.addPhotonEnergy("0.33*eV")
	gmaterial.addPhotonEnergy("0.4*eV")
	gmaterial.addPhotonEnergy("10.45*eV")
	gmaterial.addIndexOfRefraction("1.572")
	gmaterial.addIndexOfRefraction("1.576")
	gmaterial.addIndexOfRefraction("1.577")
	gmaterial.addIndexOfRefraction("1.582")
	gmaterial.addIndexOfRefraction("1.587")
	gmaterial.addIndexOfRefraction("1.592")
	gmaterial.addIndexOfRefraction("1.606")
	gmaterial.addIndexOfRefraction("1.617")
	gmaterial.addReflectivity("0.001")
	gmaterial.addReflectivity("0.001")
	gmaterial.addReflectivity("0.001")
	gmaterial.addReflectivity("0.001")
	gmaterial.addReflectivity("0.001")
	gmaterial.addReflectivity("0.001")
	gmaterial.addReflectivity("0.001")
	gmaterial.addEfficiency("0.3")
	gmaterial.addEfficiency("0.3")
	gmaterial.addEfficiency("0.3")
	gmaterial.addEfficiency("0.3")
	gmaterial.addEfficiency("0.3")
	gmaterial.addEfficiency("0.3")
	gmaterial.addEfficiency("0.3")
	gmaterial.addEfficiency("0.3")
	gmaterial.addAbsorptionLength("0.394*m")
	gmaterial.addAbsorptionLength("0.394*m")
	gmaterial.addAbsorptionLength("0.394*m")
	gmaterial.addAbsorptionLength("0.394*m")
	gmaterial.addAbsorptionLength("0.394*m")
	gmaterial.addAbsorptionLength("0.394*m")
	gmaterial.addAbsorptionLength("0.394*m")
	gmaterial.addAbsorptionLength("0.394*m")
	gmaterial.addSlowTimeConstant("2.8*ns")
	gmaterial.addFastTimeConstant("0.9*ns")
	gmaterial.addRayleigh("0.394*m")
	gmaterial.addYieldRatio("0.9")
	gmaterial.addScintillationYield("8000")
	gmaterial.publish(configuration)
	
 # Inclad: Inner cladding of the Scintillator
	'''
	my %mat2 = init_mat();
	$mat2{"name"} 			= "inclad";
	$mat2{"description"} 		= "Inner cladding of the Scintillator";
	$mat2{"density"} 		= "1.19";
	$mat2{"ncomponents"} 		= "3";
	$mat2{"components"} 		= "O 2 C 5 H 8";
	$mat2{"photonEnergy"}  		= "0.447*eV";
	$mat2{"indexOfRefraction"} 	= "1.49";
	$mat2{"reflectivity"} 		= "0.00057";
	$mat2{"absorptionLenght"}	= "0.394*m";
	$mat2{"slowtimeconstant"}	= "2.8*ns";
	$mat2{"rayleigh"}               = "0.394*m";
	print_mat(\%configuration, \%mat2);
	'''
	gmaterial = GMaterial("inclad")
	gmaterial.description = "Inner cladding of the Scintillator"
	gmaterial.density = 1.19
	gmaterial.addMaterialWithFractionalMass("C",  0.9)
	gmaterial.addMaterialWithFractionalMass("H",  0.1)
	gmaterial.addPhotonEnergy("0.447*eV")
	gmaterial.addIndexOfRefraction("1.49")
	gmaterial.addReflectivity("0.00057")
	gmaterial.addAbsorptionLength("0.394*m")
	gmaterial.addSlowTimeConstant("2.8*ns")
	gmaterial.addRayleigh("0.394*m")
	gmaterial.publish(configuration)
	
 # Outclad: Outter cladding of the Scintillator
	'''
	my %mat3 = init_mat();
	$mat3{"name"} 			= "outclad";
	$mat3{"description"} 		= "Outter cladding of the Scintillator";
	$mat3{"density"} 		= "1.42";
	$mat3{"ncomponents"} 		= "3";
	$mat3{"components"} 		= "O 2 C 5 H 8";
	$mat3{"photonEnergy"}  		= "0.447*eV";
	$mat3{"indexOfRefraction"} 	= "1.42";
	$mat3{"reflectivity"}		= "0.03";
	$mat3{"absorptionLenght"}	= "0.0002*cm";
	$mat3{"slowtimeconstant"}	= "2.8*ns";
	$mat3{"rayleigh"}               = "0.0002*cm";
	print_mat(\%configuration, \%mat3);
	'''
	gmaterial = GMaterial("outclad")
	gmaterial.description = "Outter cladding of the Scintillator"
	gmaterial.density = 1.42
	gmaterial.addMaterialWithFractionalMass("C",  0.9)
	gmaterial.addMaterialWithFractionalMass("H",  0.1)
	gmaterial.addPhotonEnergy("0.447*eV")
	gmaterial.addIndexOfRefraction("1.42")
	gmaterial.addReflectivity("0.03")
	gmaterial.addAbsorptionLength("0.0002*cm")
	gmaterial.addSlowTimeConstant("2.8*ns")
	gmaterial.addRayleigh("0.0002*cm")
	gmaterial.publish(configuration)
	