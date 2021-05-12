from gemc_api_geometry import *

def buildGeometry(configuration):

	# volume fields can be given either as named arguments in the MyDetector() call or  assigned later to the instance variable
	detector = GVolume(name="my_det")

	# mandatory fields: solid, parameters, material
	# G4Tubs shape parameters are:  inner_radius, outer_radius, half-length, starting_angle, total angle
	# A non-zero inner radius will produce a hollow tube.  The angles allow for an angular cut in the cross section
	detector.solid        = "G4Tubs"
	detector.parameters   = "0.*cm 1.*cm 5.*mm 0*deg 360*deg"
	detector.material     = "G4_Si"	# G4_Si is a GEANT4 defined element name

	detector.description = "Si detector"
	detector.color       = "f4a988"

	detector.publish(configuration)
