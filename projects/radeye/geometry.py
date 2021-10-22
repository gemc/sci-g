from gemc_api_geometry import *
import random
import json
import cls_jcard_generator as card


def buildGeometry(configuration):

	# radeye exterior paramaters
	src_x = 5
	src_y = 50
	src_z = 50


	#build a simple plastic box to house the scintillator
	gvolume = GVolume("Radeye_Exterior")
	gvolume.mother = 'root'
	gvolume.style = 0 # set to wireframe for easier viewing
	gvolume.description = "RadEye Exterior - Plastic"
	# box: x, y, z - half-lengths
	gvolume.makeG4Box(31/2, 61/2, 101/2)
	gvolume.material = "G4_POLYVINYL_CHLORIDE"
	gvolume.setPosition(0,0,0)
	gvolume.setIdentifier("exterior", 6)
	gvolume.publish(configuration)

	# # target volume: a G4Tubs
	# # G4Tubs shape parameters are: inner_radius, outer_radius, half-length, starting_angle, total angle
	# # A non-zero inner radius will produce a hollow tube.  The angles allow for an angular cut in the cross section
	# makeG4Tube default units are 'mm' and 'deg'
	gvolume = GVolume('Radeye_Scintillator')
	gvolume.mother = 'Radeye_Exterior'
	gvolume.description = 'RadEye Scintillator Crystal'
	# tubs: rin, rout, length, phiStart, totalPhi, dtheta, lunit='mm'
	gvolume.makeG4Tubs(0, 20/2, 43.5/2, 0, 360)
	gvolume.setPosition(0, 0, 20.5)
	gvolume.material    = 'G4_SODIUM_IODIDE'	# from GEANT4 materials database
	gvolume.color       = 'ff0000'
	gvolume.digitization = 'flux'
	gvolume.setIdentifier('targetid', 7)
	gvolume.publish(configuration)
	


	# Scintillator paddle volume, with a rotation and a shift
	# makeG4Box shape parameters are x, y, z half-lengths
	# makeG4Box default units are 'mm', but here they are overwritten to 'cm'
	gvolume = GVolume('release_material')
	gvolume.description = 'Scintillator paddle'
	gvolume.style = 0 # set to wireframe for easier viewing
	gvolume.makeG4Box(src_x, src_y, src_z, 'mm')
	gvolume.material = 'G4_SODIUM_IODIDE'	# from GEANT4 materials database
	gvolume.setRotation(0, 0, 0)         # default unit is 'deg'
	gvolume.setPosition(10, 0, 2.5, 'cm')   # overwriting default unit of 'mm'
	gvolume.color        = '00ff00'
	
	gvolume.setIdentifier('paddleid', 5)  # identifier for this paddle
	gvolume.publish(configuration)


	jcard  = card.jcard_ops()
	jdict = jcard.generateBase()
	jdict = jcard.generateOutput(jdict)
	jdict = jcard.generateVolumePoints(jdict, 
										pname="e-", 
										vol_x=(-src_x+100,src_x+100), 
										vol_y=(-src_y,src_y), 
										vol_z=(-src_z+25, 
										src_z+25),
										points=1000 )
	jcard.save(jdict)
	