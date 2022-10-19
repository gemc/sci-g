from gemc_api_geometry import GVolume

# could you convert to english if possible?
#
# === Esquema de construcción de grilla de fibras ($nrows=9 $ncols=12) =============================
#   A A A A A A A A A A A A
#    B B B B B B B B B B B
#   A A A A A A A A A A A A
#    B B B B B B B B B B B
#   A A A A A A A A A A A A
#    B B B B B B B B B B B
#   A A A A A A A A A A A A
#    B B B B B B B B B B B
#   A A A A A A A A A A A A
# Se construyen primero los volúmenes a desde adentro hacia afuera, es decir, primero se construyen
# los núcleos de las fibras a, luego el primer revestimiento de las fibras a y para finalizar el
# segundo revestimiento. Después toca el turno de los volúmenes b.

# === Orden de Identificación ======================================================================
# volumen  | id
# lead_box | 0
# fiber    | %1d (a=0, b=1) 1 %4d (nx) %4d (ny)
# inclad   | %1d (a=0, b=1) 2 %4d (nx) %4d (ny)
# outclad  | %1d (a=0, b=1) 3 %4d (nx) %4d (ny)
# sensor1  | %1d (a=0, b=1) 4 %4d (nx) %4d (ny)
# sensor2  | %1d (a=0, b=1) 5 %4d (nx) %4d (ny)
# Los ids son generados como 10**9 * (a or b) + 10**8 * vol_id + 10**4 * nx + 10**0 * ny.

# global variables
nrows=7
ncols=7
nrowsa=(nrows-1)/2
nrowsb=(nrows-1)/2
dx=(0.1+ncols)/2
dy=(0.1 + (nrows - 1) * (0.05 * 1.732050808 + 0.05))/2.

def build_bcal(configuration):
	build_lead(configuration)
	# build_fiber_a(configuration)
	# build_inclad_a(configuration)
	# build_outclad_a(configuration)
	# build_sensor_1a(configuration)
	# build_sensor_2a(configuration)
	# build_fiber_b(configuration)
	# build_inclad_b(configuration)
	# build_outclad_b(configuration)
	# build_sensor_1b(configuration)
	# build_sensor_2b(configuration)

def generate_id(id1, id2, id3, id4):
	# modify to match the perl code
	return id1*100000000 + id2*1000000 + id3*10000 + id4

def build_lead(configuration):

	# The lead box is a simple box (complete description)

	gvolume = GVolume('lead_box')
	gvolume.description = 'ead box container'
	gvolume.make_box(dx, dy, 2, 'cm')
	gvolume.material    = 'G4_Pb'
	gvolume.color       = '7070702'
	gvolume.style       = 1
	gvolume.publish(configuration)




