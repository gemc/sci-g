from gemc_api_geometry import GVolume

def build_geometry(configuration):

	gvolume = GVolume('target')
	gvolume.description = 'Liquid Hydrogen Target - from G4 materials database'
	gvolume.make_tube(0, 20, 5, 0, 360)
	gvolume.set_position(0, 0, 0)
	gvolume.material    = 'G4_lH2'	# from GEANT4 materials database
	gvolume.color       = 'ff0000'
	gvolume.mfield      = 'simple_dipole' # must match jcard entry, or entry in DB
	gvolume.publish(configuration)



