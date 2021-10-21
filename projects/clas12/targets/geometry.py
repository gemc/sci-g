from gemc_api_geometry import *

def build_geometry_lh2(configuration):
	def build_container():
		n_planes = 4
		phi_start = 0
		phi_total = 360 
		z_plane 	= [-140.0, 265.0, 280.0, 280.0]
		outer_radius = [50.3, 50.3, 21.1, 21.1]
		inner_radius = [0.0]*len(outer_radius)

		# Vacuum Target Container
		gvolume = GVolume('target')
		gvolume.description = 'Liquid Hydrogen Target Container'
		gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
		gvolume.material    = 'G4_Galactic'	# from GEANT4 materials database
		gvolume.color       = '22ff22'
		return gvolume
	
	def build_actual_target():
		n_planes = 5
		phi_start = 0
		phi_total = 360 
		z_plane 	= [-24.2, -21.2, 22.5, 23.5, 24.5]
		outer_radius = [2.5,  10.3,  7.3,  5.0,  2.5]
		inner_radius = [0.0]*len(outer_radius)

		gvolume = GVolume('lh2')
		gvolume.mother = "target"
		gvolume.description = 'Liquid Hydrogen Target Cell'
		gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
		gvolume.material    = 'G4_lH2'
		gvolume.color       = 'aa0000'
		return gvolume

	for builder in [
		build_container,
		build_actual_target
	]: 
		volume = builder()
		volume.publish(configuration)

def build_geometry_c12(configuration):
	def build_vacuum_container():
		n_planes = 4
		phi_start = 0
		phi_total = 360 
		z_plane 	= [-145.0,  235.0, 260.0, 370.0]
		outer_radius = [50.2,   50.2,  21.0,  21.0]
		inner_radius = [0.0]*len(outer_radius)

		gvolume = GVolume('target')
		gvolume.description = 'C12 Target Vacuum Container'
		gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
		gvolume.material    = 'G4_Galactic'	
		gvolume.color       = '22ff22'
		return gvolume

	def build_foil(
			name_prefix,
			descr_prefix,
			z_center,
			r_out=5,
			length=0.86,
			r_in=0.,
			phi_start=0.,
			phi_total=360,
			color="aa0000",
		):
			gvolume = GVolume(f"{name_prefix}NuclearTargFoil")
			gvolume.mother = "target"
			gvolume.description = f"{descr_prefix} 12C foil for EG2p Nuclear Targets Assembly"
			gvolume.material = "G4_C"
			gvolume.color = color
			gvolume.makeG4Tubs(r_in, r_out, length, phi_start, phi_total)
			gvolume.setPosition(0., 0., z_center)
			return gvolume


	def build_upstream_foil():
		return build_foil(
			name_prefix="1st",
			descr_prefix="First",
			z_center=-25.86,
			color="aa0011",
		)
	
	def build_second_foil():
		return build_foil(
			name_prefix="2nd",
			descr_prefix="Second",
			z_center=24.14,
		)

	def build_third_foil():
		return build_foil(
			name_prefix="3rd",
			descr_prefix="Third",
			z_center=74.14,
		)

	for builder in [
		build_vacuum_container,
		build_upstream_foil,
		build_second_foil,
		build_third_foil
	]:
		volume = builder()
		volume.publish(configuration)


MAP_TARGET_TO_BUILDER = {
	"lh2": build_geometry_lh2,
	"c12": build_geometry_c12,
}
