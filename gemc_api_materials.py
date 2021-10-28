# -*- coding: utf-8 -*-
#=======================================
#	gemc materials definition
#
#	This file defines a GMaterial class that holds the parameters needed to define a Geant4 material in gemc.
#	Any material in the project is an instance of this class.
#  The "publish" function writes out the volume parameters according to the factory.
#
#  A GMaterial is be instantiated with these mandatory arguments:
#
#	Class members (all members are text strings):
#	name			  - The name of the material
#	description	  - A description of the material, for documentation purposes only
#	density		  - The material density, in g/cm3
#	ncomponents	  - The number of of components of the material, e.g., water (H2O) has 2 components: H and O
#	components	  - A string that lists the components and their relative amounts in the material, e.g. "H 2 O 1"
#
#	The following GMaterial parameters are optional: FIX ME: NOT SUPPORTED YET
#
#	*****  The next values set optical properties for materials.
#
#	photonEnergy		- A list of photon energies at which any other optical parameters will be provided
#					- Not required (leave as default "none" if not using optical physics)
#					- if any optical parameter (indexOfRefraction, reflectivity, etc.) is defined, photonEnergy MUST also be defined
#					- provide as a list of energies with units, for example:  "1.0*eV 2.0*eV 3.0*eV 4.0*eV 5.0*eV 6.0*eV"
#	indexOfRefraction	- A list of the refractive index evaluated at the energies named in photonEnergy "1.40 1.39 1.38 1.37 1.36"
#					- must have same number of elements in list as in photonEnergy - same for all optical parameters
#	absorptionLength	- A list of the material absorption length evaluated at the energies in photonEnergy
#					- includes units, for example:  "72.8*m 53.2*cm 39.1*cm"
#	reflectivity			- A list of reflectivity values evaluated at the energies in photonEnergy
#	efficiency			- A list of absorption efficiency evaluated at the energies in photonEnergy
#					- efficiency is only used for a dielectric-metal optical boundary where there is no refraction
#					- At this boundary the photon is either reflected or absorbed by the metal with this efficiency
#					- This parameter can be used to define a quantum efficiency for a PMT, for example
#
#	*****  The next values are about defining scintillators.  They can be ignored (left to default values) if not using a scintillator
#	***** Scintillators are assumed to have a fast and slow response component, defined by relative spectra
#
#	fastcomponent		- A list of the fast component relative spectra values evaluated at the energies in photonEnergy
#	slowcomponent		- A list of the fast component relative spectra values evaluated at the energies in photonEnergy
#	scintillationyield		- Characteristic light yield in photons/MeV e-, given as a single number not a list:  "8400."
#	resolutionscale		- Resolution scale broadens the statistical distribution of generated photons
#					- due to impurities typical of doped crystals like NaI(Tl) and CsI(Tl).  Can be narrower
#					- when the Fano factor plays a role.  Actual number of emitted photons in a step fluctuates
#					- around the mean number with width (ResolutionScale*sqrt(MeanNumberOfPhotons)
#					- Resolution scale is given as a single number, not a list:  "2.0"
#	fasttimeconstant		- (??) believe this is related to the scintillator pulse rise time.  Given as number with units: "1.6*ns"
#	slowtimeconstant	- (??) believe this is related to scintillator slow decay time. Given as number with units: "3.2*ns"
#	yieldratio			- relative strength of the fast component as a fraction of total scintillation yield:  "0.8"
#	rayleigh			- A list of the Rayleigh scattering attenuation coefficient evaluated at the energies in photonEnergy
#
#
#	******	Note that photon energies can be obtained from the wavelength:
#			lambda * nu = c	where lambda is wavelength, c is the speed of light, and nu is frequency
#			E = h * nu		where h is Plank's constant
#			A handy relation for estimating is that h*c ~ 197 eV*nm


# for mandatory fields. Used in function checkValidity
WILLBESETSTRING     = 'notSetYet'
WILLBESETNUMBER     = -987654

# for optionals fields
NOTAPPLICABLESTRING = 'na'
NOTAPPLICABLENUMBER = -123456

# Material class definition
class GMaterial():
	def __init__(self, name):

		# mandatory fields. Checked at publish time
		self.name        = name
		self.density     = WILLBESETNUMBER
		self.ncomponents = WILLBESETNUMBER
		self.components  = WILLBESETSTRING

		# optional fields
		self.description        = NOTAPPLICABLESTRING
		self.photonEnergy       = NOTAPPLICABLESTRING
		self.indexOfRefraction  = NOTAPPLICABLESTRING
		self.absorptionLength   = NOTAPPLICABLESTRING
		self.reflectivity       = NOTAPPLICABLESTRING
		self.efficiency         = NOTAPPLICABLESTRING
		self.fastcomponent      = NOTAPPLICABLENUMBER
		self.slowcomponent      = NOTAPPLICABLENUMBER
		self.scintillationyield = NOTAPPLICABLENUMBER
		self.resolutionscale    = NOTAPPLICABLENUMBER
		self.fasttimeconstant   = NOTAPPLICABLENUMBER
		self.slowtimeconstant   = NOTAPPLICABLENUMBER
		self.yieldratio         = NOTAPPLICABLENUMBER
		self.rayleigh = NOTAPPLICABLENUMBER

	def checkValidity(self):
		# need to add checking if it's operation instead
		if self.density == WILLBESETNUMBER:
			sys.exit(' Error: density not defined for GMaterial '     + str(self.name) )
		if self.ncomponents == WILLBESETNUMBER:
			sys.exit(' Error: ncomponents not defined for GMaterial ' + str(self.name) )
		if self.components == WILLBESETSTRING:
			sys.exit(' Error: components not defined for GMaterial ' + str(self.name) )

	def publish(self, configuration):
		self.checkValidity()
		# TEXT factory
		if configuration.factory == 'TEXT':
			fileName = configuration.matFileName
			configuration.nvolumes += 1
			with open(fileName, 'a+') as dn:
				lstr = ''
				lstr += '%s | ' % self.name
				lstr += '%s | ' % self.description
				lstr += '%s | ' % self.density
				lstr += '%s | ' % self.ncomponents
				lstr += '%s | ' % self.components
				# optical parameters
				lstr += '%s | ' % self.photonEnergy
				lstr += '%s | ' % self.indexOfRefraction
				lstr += '%s | ' % self.absorptionLengt
				lstr += '%s | ' % self.reflectivity
				lstr += '%s | ' % self.efficiency
				# scintillation parameters
				lstr += '%s | ' % self.fastcomponent
				lstr += '%s | ' % self.slowcomponent
				lstr += '%s | ' % self.scintillationyield
				lstr += '%s | ' % self.resolutionscale
				lstr += '%s | ' % self.fasttimeconstant
				lstr += '%s | ' % self.slowtimeconstant
				lstr += '%s | ' % self.yieldratio
				# other optical processes
				lstr += '%s | ' % self.rayleigh

				dn.write(lstr)


