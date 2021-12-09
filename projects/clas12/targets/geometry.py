from gemc_api_geometry import *


def build_geometry_lhydrogen(configuration):

	variation = configuration.variation
	material_varmap = {
		"lh2": "G4_lH2",
		"ld2": "LD2",
		"lh2e": "G4_lH2"
		}

	z_plane_varmap = {
		"lh2": [-140.0, 265.0, 280.0, 280.0],
		"ld2": [-140.0, 265.0, 280.0, 280.0],
		"lh2e": [-145.0,  235.0, 260.0, 370.0]
	}

	def build_vacuum_container():
		n_planes = 4
		phi_start = 0
		phi_total = 360 
		z_plane 	= z_plane_varmap[variation]
		outer_radius = [50.3, 50.3, 21.1, 21.1]
		inner_radius = [0.0]*len(outer_radius)

		# Vacuum Target Container
		gvolume = GVolume('target')
		gvolume.description = f'Liquid Hydrogen Target Container for variation {variation}'
		gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
		gvolume.material = 'G4_Galactic'	# from GEANT4 materials database
		gvolume.color = '22ff22'
		return gvolume
	
	def build_target_cell():
		n_planes = 5
		phi_start = 0
		phi_total = 360 
		z_plane 	= [-24.2, -21.2, 22.5, 23.5, 24.5]
		outer_radius = [2.5,  10.3,  7.3,  5.0,  2.5]
		inner_radius = [0.0]*len(outer_radius)

		gvolume = GVolume(variation)
		gvolume.mother = "target"
		gvolume.description = f'Liquid Hydrogen Target Cell for vaiation {variation}'
		gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
		gvolume.material = material_varmap[variation]
		gvolume.color = 'aa0000'
		return gvolume

	for builder in [
		build_vacuum_container,
		build_target_cell
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
		gvolume.material = 'G4_Galactic'	
		gvolume.color = '22ff22'
		return gvolume

	def build_foil(
			name_prefix,
			descr_prefix,
			z_center,
			color="aa0000",
		):
			r_out = 5
			half_length = 0.86
			r_in = 0.
			phi_start = 0.
			phi_total = 360

			gvolume = GVolume(f"{name_prefix}NuclearTargFoil")
			gvolume.mother = "target"
			gvolume.description = f"{descr_prefix} 12C foil for EG2p Nuclear Targets Assembly"
			gvolume.material = "G4_C"
			gvolume.color = color
			gvolume.makeG4Tubs(r_in, r_out, half_length, phi_start, phi_total)
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


def _make_full_tubs(gvolume, r_in, r_out, half_length):
	gvolume.makeG4Tubs(r_in, r_out, half_length, 0, 360)


def build_geometry_pol_targ(configuration):
		# vacuum container
		r_in = 0
		r_out = 44
		half_length = 130

		gvolume = GVolume("PolTarg")
		gvolume.mother = "root"
		gvolume.description = "PolTarg Region"
		gvolume.color = "aaaaaa9"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Galactic"
		gvolume.publish(configuration)
		
		# LHe fill between targets
		z_center = 0  # center location of target along beam axis
		r_in = 0
		r_out = 10  # radius in mm
		half_length = 14.97  # half length along beam axis
		gvolume = GVolume("LHeVoidFill")
		gvolume.mother = "PolTarg"
		gvolume.description = "LHe between target cells"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "0000ff"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "lHeCoolant"
		gvolume.publish(configuration)
		
		# NH3Targ
		z_center = -25  # center location of target along beam axis
		r_in = 0
		r_out = 10  # radius in mm
		half_length = 9.96  # half length along beam axis
		gvolume = GVolume("NH3Targ")
		gvolume.mother = "PolTarg"
		gvolume.description = "Upstream NH3 target cell"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "f000f0"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "NH3target"
		gvolume.publish(configuration)

		# NH3Targ Cup
		z_center = -25
		r_in = 10.0001  # radius in mm
		r_out = 10.03  # radius in mm
		half_length = 9.75  # half length along beam axis
		gvolume = GVolume("NH3Cup")
		gvolume.mother = "PolTarg"
		gvolume.description = "Upstream NH3 Target cup"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		gvolume.publish(configuration)

		# NH3Targ Cup Down Stream Ring
		z_center = -35
		r_in = 10.0001  # radius in mm
		r_out = 11.43  # radius in mm
		half_length = 0.25  # half length along beam axis
		gvolume = GVolume("NH3CupDSRing")
		gvolume.mother = "PolTarg"
		gvolume.description = "Upstream NH3 Target cup downstream Ring"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		gvolume.publish(configuration)

		# NH3Targ Cup UP Stream Ring
		z_center = -15
		r_in = 10.0001  # radius in mm
		r_out = 12.7  # radius in mm
		half_length = 0.25  # half length along beam axis
		gvolume = GVolume("NH3CupUSRing")
		gvolume.mother = "PolTarg"
		gvolume.description = "Upstream NH3 Target cup Upstream Ring"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		gvolume.publish(configuration)

		# NH3Targ Cup Window Frame
		z_center = -35
		r_in = 11.44  # radius in mm
		r_out = 12.7  # radius in mm
		half_length = 1.5875  # half length along beam axis
		gvolume = GVolume("NH3CupWindowFrame_20")
		gvolume.mother = "PolTarg"
		gvolume.description = "Upstream NH3 Target cup Window frame"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		gvolume.publish(configuration)

		# NH3Targ Cup Up Stream Window
		z_center = -35
		r_in = 0  # radius in mm
		r_out = 10  # radius in mm
		half_length = 0.025  # half length along beam axis		
		gvolume = GVolume("NH3CupUSWindow_20")
		gvolume.mother = "PolTarg"
		gvolume.description = "Upstream NH3 Target cup Upstream Window"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		gvolume.publish(configuration)

		# NH3Targ Cup Downstream Stream Window
		z_center = -15
		r_in = 0  # radius in mm
		r_out = 10  # radius in mm
		half_length = 0.025  # half length along beam axis
		gvolume = GVolume("NH3CupDSWindow")
		gvolume.mother = "PolTarg"
		gvolume.description = "Upstream NH3 Target cup Downstream Window"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		gvolume.publish(configuration)

		# NH3Targ
		z_center = 25  # center location of target along beam axis
		r_in = 0
		r_out = 10  # radius in mm
		half_length = 9.96  # half length along beam axis	
		gvolume = GVolume("ND3Targ")
		gvolume.mother = "PolTarg"
		gvolume.description = "Downstream ND3 target cell"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "f000f0"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "ND3target"
		gvolume.publish(configuration)

		# NH3Targ Cup
		z_center = 25
		r_in = 10.0001  # radius in mm
		r_out = 10.03  # radius in mm
		half_length = 9.75  # half length along beam axis
		gvolume = GVolume("ND3Cup")
		gvolume.mother = "PolTarg"
		gvolume.description = "Downstream ND3 Target cup"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		gvolume.publish(configuration)

		# ND3Targ Cup Down Stream Ring
		z_center = 35
		r_in = 10.0001  # radius in mm
		r_out = 11.43  # radius in mm
		half_length = 0.25  # half length along beam axis
		gvolume = GVolume("ND3CupDSRing")
		gvolume.mother = "PolTarg"
		gvolume.description = "Downstream ND3 Target cup downstream Ring"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		gvolume.publish(configuration)

		# ND3Targ Cup UP Stream Ring
		z_center = 15
		r_in = 10.0001  # radius in mm
		r_out = 11.43  # radius in mm
		half_length = 0.25  # half length along beam axis
		gvolume = GVolume("ND3CupUSRing")
		gvolume.mother = "PolTarg"
		gvolume.description = "Downstrem ND3 Target cup Upstream Ring"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		gvolume.publish(configuration)

		# ND3Targ Cup Window Frame
		z_center = 15
		r_in = 11.44  # radius in mm
		r_out = 12.7  # radius in mm
		half_length = 1.5875  # half length along beam axis
		gvolume = GVolume("ND3CupWindowFrame_20")
		gvolume.mother = "PolTarg"
		gvolume.description = "Upstream NH3 Target cup Window frame"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		gvolume.publish(configuration)

		# ND3Targ Cup Up Stream Window
		z_center = 35
		r_in = 0.0  # radius in mm
		r_out = 10.0  # radius in mm
		half_length = 0.025  # half length along beam axis	
		gvolume = GVolume("ND3CupUSWindow_20")
		gvolume.mother = "PolTarg"
		gvolume.description = "Downstream ND3 Target cup Upstream Window"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		gvolume.publish(configuration)

		# ND3Targ Cup Downstream Stream Window
		z_center = 15
		r_in = 0.0  # radius in mm
		r_out = 10.0  # radius in mm
		half_length = 0.025  # half length along beam axis	
		gvolume = GVolume("ND3CupDSWindow")
		gvolume.mother = "PolTarg"
		gvolume.description = "Downstream ND3 Target cup Downstream Window"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		gvolume.publish(configuration)

		# Insert Bath Entrance window part 7 a
		z_center = -37.395
		r_in = 0.0  # radius in mm
		r_out = 11.5  # radius in mm
		half_length = 0.605  # half length along beam axis
		gvolume = GVolume("InsertBathEntranceWindow_7a")
		gvolume.mother = "PolTarg"
		gvolume.description = "Insert Bath Entrence window part 7 a"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		gvolume.publish(configuration)

		# Insert Bath Entrance window part 7 b
		z_center = -68.2
		r_in = 11.0  # radius in mm
		r_out = 11.5  # radius in mm
		half_length = 30.1  # half length along beam axis
		gvolume = GVolume("InsertBathEntranceWindow_7b")
		gvolume.mother = "PolTarg"
		gvolume.description = "Insert Bath Entrence window part 7 b"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		gvolume.publish(configuration)

		# Insert Bath Entrance window part 7 c
		z_center = -98.4
		r_in = 11.5001  # radius in mm
		r_out = 14.4  # radius in mm
		half_length = 3.17  # half length along beam axis
		gvolume = GVolume("InsertBathEntranceWindow_7c")
		gvolume.mother = "PolTarg"
		gvolume.description = "Insert Bath Entrence window part 7 c"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		gvolume.publish(configuration)

		# Insert Bath Entrance window part 7 d
		z_center = -102.23
		r_in = 11.0  # radius in mm
		r_out = 14.96  # radius in mm
		half_length = 0.66  # half length along beam axis
		gvolume = GVolume("InsertBathEntranceWindow_7d")
		gvolume.mother = "PolTarg"
		gvolume.description = "Insert Bath Entrence window part 7 d"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		gvolume.publish(configuration)
		
		# Shim Coil Carrier
		z_center = -19.3
		r_in = 28.8  # radius in mm
		r_out = 29.3  # radius in mm
		half_length = 80.95  # half length along beam axis	
		gvolume = GVolume("ShimCoilCarrier")
		gvolume.mother = "PolTarg"
		gvolume.description = "Shim Coil Carrier"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		gvolume.publish(configuration)

		# Shim Up Up stream Coil
		z_center = 43.5
		r_in = 29.3  # radius in mm
		r_out = 30.0  # radius in mm
		half_length = 6.0  # half length along beam axis
		gvolume = GVolume("ShimUpUpS")
		gvolume.mother = "PolTarg"
		gvolume.description = "Shim Coil Up Up stream Coil"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "a00000"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "ShimCoil"
		gvolume.publish(configuration)

		# Shim Up stream Coil
		z_center = 8.5
		r_in = 29.3  # radius in mm
		r_out = 30.0  # radius in mm
		half_length = 6.0  # half length along beam axis
		gvolume = GVolume("ShimUpS")
		gvolume.mother = "PolTarg"
		gvolume.description = "Shim Coil Up stream"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "a00000"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "ShimCoil"
		gvolume.publish(configuration)

		# Shim Down stream Coil
		z_center = -8.5
		r_in = 29.3  # radius in mm
		r_out = 30.0  # radius in mm
		half_length = 6.0  # half length along beam axis
		gvolume = GVolume("ShimDownS")
		gvolume.mother = "PolTarg"
		gvolume.description = "Shim Coil Down stream"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "a00000"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "ShimCoil"
		gvolume.publish(configuration)

		# Shim Down Down stream Coil
		z_center = -43.5
		r_in = 29.3  # radius in mm
		r_out = 30.0  # radius in mm
		half_length = 6.0  # half length along beam axis
		gvolume = GVolume("ShimDownDownS")
		gvolume.mother = "PolTarg"
		gvolume.description = "Shim Coil Down Down stream"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "a00000"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "ShimCoil"
		gvolume.publish(configuration)
		
		# Heat Shield tube
		z_center = -34.3
		r_in = 40.3  # radius in mm
		r_out = 41.3  # radius in mm
		half_length = 83.85  # half length along beam axis
		gvolume = GVolume("HeatShieldTube")
		gvolume.mother = "PolTarg"
		gvolume.description = "PolTarg Heat Shield Tube"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tubs(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		gvolume.publish(configuration)

		# Heat Shield Half Sphere
		z_center = 49.55
		r_in = 40.3  # radius in mm
		r_out = 41.3  # radius in mm
		gvolume = GVolume("HeatShieldSphere")
		gvolume.mother = "PolTarg"
		gvolume.description = "PolTarg Heat Shield Exit window Shere"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		gvolume.makeG4Sphere(r_in, r_out, 0, 360, 0, 90)
		gvolume.material = "G4_Al"
		gvolume.publish(configuration)


VARIATIONBUILDER_MAP = {
	"lh2": build_geometry_lhydrogen,
	"lh2e": build_geometry_lhydrogen,
	"ld2": build_geometry_lhydrogen,
	"c12": build_geometry_c12,
	"pol_targ": build_geometry_pol_targ
}
