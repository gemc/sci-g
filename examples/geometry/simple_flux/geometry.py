from gemc_api_geometry import *

def buildGeometry(configuration):

	# target volume: a G4Tubs
	# G4Tubs shape parameters are: inner_radius, outer_radius, half-length, starting_angle, total angle
	# A non-zero inner radius will produce a hollow tube.  The angles allow for an angular cut in the cross section
	# makeG4Tube default units are 'mm' and 'deg'
	gvolume = GVolume('target')
	gvolume.description = 'Liquid Hydrogen Target'
	gvolume.make_tube(0, 20, 40, 0, 360)
	gvolume.material    = 'G4_lH2'	# from GEANT4 materials database
	gvolume.color       = 'ff0000'
	gvolume.publish(configuration)


	# Scintillator paddle volume, with a rotation and a shift
	# make_box shape parameters are x, y, z half-lengths
	# make_box default units are 'mm', but here they are overwritten to 'cm'
	gvolume = GVolume('paddle')
	gvolume.description = 'Scintillator paddle'
	gvolume.make_box(5, 0.5, 5, 'cm')
	gvolume.material = 'G4_PLASTIC_SC_VINYLTOLUENE'	# from GEANT4 materials database
	gvolume.set_rotation(90, 0, 0)         # default unit is 'deg'
	gvolume.set_position(0, 2, 10, 'cm')   # overwriting default unit of 'mm'
	gvolume.color        = 'f4f4ff'
	gvolume.digitization = 'flux'
	gvolume.set_identifier('paddleid', 5)  # identifier for this paddle
	gvolume.publish(configuration)

