from gemc_api_geometry import GVolume
import math

# These are example of methods to build a mother and daughter volume.

def build_variations(configuration):
	build_mother_volume(configuration)
	build_target(configuration)
	if configuration.variation == 'lead_target':
		build_lead_shield(configuration)

def build_mother_volume(configuration):
	gvolume = GVolume('absorber')
	gvolume.description = 'carbon fiber absorber'
	gvolume.make_box(100.0, 100.0, 100.0)
	gvolume.material    = 'carbonFiber'
	gvolume.color       = '3399FF'
	gvolume.style       = 0
	gvolume.publish(configuration)

def build_target(configuration):
	gvolume = GVolume('target')
	gvolume.description = 'epoxy target'
	gvolume.mother    = 'absorber'
	gvolume.make_tube(0, 20, 40, 0, 360)
	gvolume.material    = 'epoxy'
	gvolume.color       = 'ff0000'
	if configuration.variation == 'lead_target':
		gvolume.color       = '0000ff'
		gvolume.material    = 'G4_Pb'
	gvolume.publish(configuration)

def build_lead_shield(configuration):
	gvolume = GVolume('shield')
	gvolume.description = 'target shield'
	gvolume.make_tube(50, 50.1, 50, 0, 360)
	gvolume.material    = 'G4_Pb'
	gvolume.color       = '00ff00'
	gvolume.publish(configuration)



