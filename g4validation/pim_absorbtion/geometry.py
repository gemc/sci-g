from gemc_api_geometry import GVolume
import math

def build_pim_absorbtion(configuration):
	buildMotherVolume(configuration)
	buildTarget(configuration)

def buildMotherVolume(configuration):
	gvolume = GVolume("vacuumDetector")
	gvolume.makeG4Tubs(0, 60, 210, 0, 360, 'cm')
	gvolume.material = 'G4_Galactic'
	gvolume.color = 'FFAAAA4'
	gvolume.digitization = 'flux'
	gvolume.setIdentifier('det', 1)
	gvolume.publish(configuration)

def buildTarget(configuration):
	gvolume = GVolume("beamDump")
	gvolume.mother = 'vacuumDetector'
	gvolume.makeG4Tubs(0, 50, 200, 0, 360, 'cm')
	gvolume.color = 'AAAAFF'
	gvolume.material = 'G4_Al'
	gvolume.publish(configuration)



