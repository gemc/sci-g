from gemc_api_geometry import *

def buildGeometry(configuration):

	# volume fields can be given either as named arguments in the MyDetector() call or  assigned later to the instance variable
	gvolume = GVolume('target')
	gvolume.description = 'Liquid Hydrogen Target'

	# mandatory fields: solid, parameters, material
	# G4Tubs shape parameters are:  inner_radius, outer_radius, half-length, starting_angle, total angle
	# A non-zero inner radius will produce a hollow tube.  The angles allow for an angular cut in the cross section
	# makeG4Tube default units are 'mm' and 'deg'
	gvolume.makeG4Tubs(0, 2, 4, 0, 360)
	gvolume.material     = 'G4_lH2'	# G4_Si is a GEANT4 defined element name
	gvolume.color       = 'ff0000'
	gvolume.publish(configuration)

	# volume fields can be given either as named arguments in the MyDetector() call or  assigned later to the instance variable
	gvolume = GVolume('ctof')
	gvolume.description = 'Scintillator paddle'

	# mandatory fields: solid, parameters, material
	# G4Tubs shape parameters are:  inner_radius, outer_radius, half-length, starting_angle, total angle
	# A non-zero inner radius will produce a hollow tube.  The angles allow for an angular cut in the cross section
	# makeG4Tube default units are 'mm' and 'deg'
	gvolume.makeG4Box(10, 10, 40)
	gvolume.material     = 'G4_PLASTIC_SC_VINYLTOLUENE'	# G4_Si is a GEANT4 defined element name

	# add 2 rotations
	gvolume.setRotation(90, 0, 0)
	gvolume.setPosition(0, 50, 100)
	gvolume.color       = 'f44455'
	gvolume.digitization = 'flux'
	gvolume.setIdentifier('ctofid', 22)
	gvolume.publish(configuration)

	# volume fields can be given either as named arguments in the MyDetector() call or  assigned later to the instance variable
	gvolume = GVolume('dosimeter')
	gvolume.description = 'Si detector'

	# mandatory fields: solid, parameters, material
	# G4Sphere shape parameters are:  inner_radius, outer_radius, starting phi, delta phi, starting theta, delta theta
	# A non-zero inner radius will produce a hollow sphere.  The angles allow for an angular cut in the cross section
	# makeG4Sphere default units are 'mm' and 'deg'
	gvolume.makeG4Sphere(148, 150, 0, 180, 0, 180)
	gvolume.material     = 'G4_Si'	# G4_Si is a GEANT4 defined element name
	gvolume.setRotation(-90, 0, 0)
	gvolume.setPosition(0, 0, 100)
	gvolume.color       = 'f4a988'
	gvolume.digitization = 'dosimeter'
	gvolume.setIdentifier('id', 1)
	#gvolume.publish(configuration)
