from math import cos, sin

from gemc_api_geometry import *

def buildGeometry(configuration):

	# all dimensions are in cm
	NBARS = 36             # number of bars in the array
	dx1 = 3.0              # width of the paddle at the bottom
	dx2 = 2.15              # width of the paddle at the top
	dy  = 50               # length of the paddle
	dz  = 5                # heigth of the paddle
	theta0 = 360. / NBARS  # double the angle of one of the trapezoid sides
	RMIN = 25              # inner radius of the array
	gap  = 1.8             # gap to avoid overlaps


	# first buld the other volume, it'a G4Tubs
	gvolume = GVolume('tof')
	gvolume.description = 'Time of flight'
	gvolume.make_tube(RMIN - gap, RMIN + 2*dz + gap, dy+gap, 0, 360, 'cm')
	gvolume.material = 'G4_AIR'
	gvolume.color = 'f4f4ff5'
	gvolume.style = 1
	gvolume.publish(configuration)


	# now build the bars
	for i in range(NBARS):

		theta_pl  = (i * theta0) * 3.1415926 / 180.
		theta_rot = (i * theta0 + 90)

		R = RMIN + dz

		x = R * cos(theta_pl)
		y = R * sin(theta_pl)
		z = 0

		gvolume = GVolume(f'bar_{i}')
		gvolume.description = f'Scintillator bar_{i}'
		gvolume.mother = 'tof'
		gvolume.make_trapezoid(dx1, dx2, dy, dy, dz, 'cm')
		gvolume.set_position(x, y, z, 'cm')
		gvolume.set_rotation(90, theta_rot, 0, 'deg')
		gvolume.material = 'G4_POLYSTYRENE'
		gvolume.color = '66aaaa0'
		gvolume.digitization = 'flux'
		gvolume.set_identifier('bar_id', i+1)
		gvolume.publish(configuration)

