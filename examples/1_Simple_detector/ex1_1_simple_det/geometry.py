from gemc_api_geometry import *

def buildGeometry(configuration):

	# volume fields can be given either as named arguments in the MyDetector() call or  assigned later to the instance variable
	gvolume = GVolume('ctof')
	gvolume.description = 'Si detector'

	# mandatory fields: solid, parameters, material
	# G4Tubs shape parameters are:  inner_radius, outer_radius, half-length, starting_angle, total angle
	# A non-zero inner radius will produce a hollow tube.  The angles allow for an angular cut in the cross section
	gvolume.solid        = 'G4Tubs'
	gvolume.parameters   = '0.*cm, 200.*cm, 50.*cm, 0*deg, 360*deg'
	gvolume.material     = 'G4_Si'	# G4_Si is a GEANT4 defined element name

	# add 2 consecutive rotations
	# TODO: verify these
	gvolume.addRotation('0*deg, 0*deg, 40*deg')
	gvolume.addRotation('10*deg, 0*deg, 0*deg')
	gvolume.color       = 'f4a988'

	gvolume.publish(configuration)
