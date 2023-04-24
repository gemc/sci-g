from gemc_api_geometry import *

def buildGeometry(configuration):


	gvolume = GVolume('target1')
	gvolume.description = 'Liquid Hydrogen Target - from G4 materials database'
	gvolume.make_tube(0, 20, 5, 0, 360)
	gvolume.set_position(0, 0, 0)
	gvolume.material    = 'G4_lH2'	# from GEANT4 materials database
	gvolume.color       = 'ff0000'
	gvolume.publish(configuration)

	gvolume = GVolume('target2')
	gvolume.description = 'My Peek - defined using Geant4 Materials'
	gvolume.make_tube(0, 20, 5, 0, 360)
	gvolume.set_position(0, 0, 20)
	gvolume.material    = 'my_peek'	# defined using Geant4 Materials
	gvolume.color       = '00ff00'
	gvolume.publish(configuration)

	gvolume = GVolume('target3')
	gvolume.description = 'my Epoxy - defined using Geant4 Materials'
	gvolume.make_tube(0, 20, 5, 0, 360)
	gvolume.set_position(0, 0, 40)
	gvolume.material    = 'my_epoxy'  # defined using Geant4 Elements
	gvolume.color       = '0000ff'
	gvolume.publish(configuration)

	gvolume = GVolume('my_carbonFiber')
	gvolume.description = 'my Carbon Fiber - defined using Geant4 and my aterials '
	gvolume.make_tube(0, 20, 5, 0, 360)
	gvolume.set_position(0, 0, 60)
	gvolume.material    = 'G4_lH2'	# from GEANT4 materials database
	gvolume.color       = '8888ff'
	gvolume.publish(configuration)

	gvolume = GVolume('target5')
	gvolume.description = 'My Resistive Paste - defined a Geant4 Material with different density'
	gvolume.make_tube(0, 20, 5, 0, 360)
	gvolume.set_position(0, 0, 80)
	gvolume.material = 'my_resistPaste'  # from GEANT4 materials database
	gvolume.color = 'ff8888'
	gvolume.publish(configuration)


