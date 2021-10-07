from gemc_api_geometry import *

def buildGeometry(configuration):

	# target volume: a G4Tubs
	# G4Tubs shape parameters are: inner_radius, outer_radius, half-length, starting_angle, total angle
	# A non-zero inner radius will produce a hollow tube.  The angles allow for an angular cut in the cross section
	# makeG4Tube default units are 'mm' and 'deg'
	gvolume = GVolume('target')
	gvolume.description = 'Liquid Hydrogen Target'
	gvolume.makeG4Tubs(0, 20, 40, 0, 360)
	gvolume.material    = 'G4_lH2'	# from GEANT4 materials database
	gvolume.color       = 'ff0000'
	gvolume.publish(configuration)


