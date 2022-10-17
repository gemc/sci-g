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


	# dosimeter volume: a G4Sphere
	# G4Sphere shape parameters are:  inner_radius, outer_radius, starting phi, delta phi, starting theta, delta theta
	# A non-zero inner radius will produce a hollow sphere.  The angles allow for an angular cut in the cross section
	# make_sphere default units are 'mm' and 'deg'
	gvolume = GVolume('dosimeter')
	gvolume.description  = 'Silicon dosimeter detector'
	gvolume.make_sphere(148, 150, 0, 180, 0, 180)
	gvolume.material     = 'G4_Si'	# from GEANT4 materials database
	gvolume.setRotation(-90, 0, 0)
	gvolume.setPosition(0, 0, 150)
	gvolume.color        = 'f4a988'
	gvolume.digitization = 'dosimeter'
	gvolume.setIdentifier('doseID', 14)  # identifier for this dosimeter
	gvolume.publish(configuration)
