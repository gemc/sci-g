from gemc_api_geometry import *

def buildGeometry(configuration):

	# box1
	# made by G4_Si, from GEANT4 materials database
	# it's assigned flux digitization with id 1
	gvolume = GVolume('box1')
	gvolume.description = 'Si detector'
	gvolume.make_box(5, 5, 0.4, 'cm')
	gvolume.material    = 'G4_Si'
	gvolume.color       = 'aa9999'
	gvolume.digitization = 'flux'
	gvolume.set_identifier('boxNumber', 1)
	gvolume.publish(configuration)

	# box2
	# made by 'scintillator', created in materials.py
	# it's assigned flux digitization with id 2
	gvolume = GVolume('box2')
	gvolume.description = 'Si detector'
	gvolume.make_box(5, 5, 0.4, 'cm')
	gvolume.set_position(0, 0, 10)
	gvolume.material    = 'scintillator'
	gvolume.color       = '99aa99'
	gvolume.digitization = 'flux'
	gvolume.set_identifier('boxNumber', 2)
	gvolume.publish(configuration)

	# box3
	# made by 'water', created in materials.py
	# it's assigned flux digitization with id 3
	gvolume = GVolume('box3')
	gvolume.description = 'S detector'
	gvolume.make_box(5, 5, 0.4, 'cm')
	gvolume.set_position(0, 0, 20)
	gvolume.material    = 'water'
	gvolume.color       = '9999aa'
	gvolume.digitization = 'flux'
	gvolume.set_identifier('boxNumber', 3)
	gvolume.publish(configuration)

	# box4
	# made by 'my_air', created in materials.py
	# it's assigned flux digitization with id 4
	gvolume = GVolume('box4')
	gvolume.description = 'Si detector'
	gvolume.make_box(5, 5, 0.4, 'cm')
	gvolume.set_position(0, 0, 30)
	gvolume.material    = 'my_air'
	gvolume.color       = 'ffbb00'
	gvolume.digitization = 'flux'
	gvolume.set_identifier('boxNumber', 4)
	gvolume.publish(configuration)

