from gemc_api_geometry import GVolume

# === Fiber grid construction scheme (nrows=9, ncols=12) ===
#   A A A A A A A A A A A A
#    B B B B B B B B B B B
#   A A A A A A A A A A A A
#    B B B B B B B B B B B
#   A A A A A A A A A A A A
#    B B B B B B B B B B B
#   A A A A A A A A A A A A
#    B B B B B B B B B B B
#   A A A A A A A A A A A A
# A-volumes are built first and from the inside out,
# that is, the cores from the A-fibers are built first,
# then the first coating of the A-fibers and then the second one.
# Then it's the turn of the B-volumes.

# === Identification order ===
# volumen  | id
# lead_box | 0
# fiber    | %1d (a=0, b=1) 1 %4d (nx) %4d (ny)
# inclad   | %1d (a=0, b=1) 2 %4d (nx) %4d (ny)
# outclad  | %1d (a=0, b=1) 3 %4d (nx) %4d (ny)
# sensor1  | %1d (a=0, b=1) 4 %4d (nx) %4d (ny)
# sensor2  | %1d (a=0, b=1) 5 %4d (nx) %4d (ny)
# Id´s are generated like:
# 10**9 * (a or b) + 10**8 * vol_id + 10**4 * nx + 10**0 * ny.

# Global variables
nrows = 7  # Always odd for convinience. Number of rows.
ncols = 7  # Always odd for convinience. Number of columns.
nrowsa = (nrows - 1) / 2  # Number of A-rows
nrowsb = (nrows - 1) / 2  # Number of B-rows
flength = 1.99  # Fiber length
dx = (0.1 * ncols) / 2
dy = (0.1 + (nrows - 1) * (0.05 * 1.732050808 + 0.05)) / 2.


def build_bcal(configuration):
        build_lead(configuration)
        build_fiber_a(configuration)
        build_inclad_a(configuration)
        build_outclad_a(configuration)
        build_sensor_1a(configuration)
        build_sensor_2a(configuration)
        build_fiber_b(configuration)
        build_inclad_b(configuration)
        build_outclad_b(configuration)
        build_sensor_1b(configuration)
        build_sensor_2b(configuration)


def generate_id(id1, id0, id2, id3):
	'''
 	if ($_[1] >= 10) {die "row_id should be between 0 (a) and 1 (b)!";}
	if ($_[0] >= 10) {die "vol_id should be between 1 and 5!";}
	if ($_[2] >= 10**4) {die "nx should be between 0 and 10**4!";}
	if ($_[3] >= 10**4) {die "ny should be between 0 and 10**4!";}
	my $vol_id = 10**9 * $_[1];
	my $row_id = 10**8 * $_[0];
	my $nx     = 10**4 * $_[2];
	my $ny     = 10**0 * $_[3];
	return $vol_id + $row_id + $nx + $ny;
  	'''
	if id1 >= 10: raise Exception("row_id should be between 0 (a) and 1 (b)!")
	if id0 >= 10: raise Exception("vol_id should be between 1 and 5!")
	if id1 >= 10**4: raise Exception("nx should be between 0 and 10**4!")
	if id2 >= 10**4: raise Exception("ny should be between 0 and 10**4!")
	if id3 >= 10**4: raise Exception("ny should be between 0 and 10**4!")
	vol_id = 10**9 * id1
	row_id = 10**8 * id0
	nx     = 10**4 * id2
	ny     = 10**0 * id3
	return vol_id + row_id + nx + ny		

# THE INIT_DET() FUNCTION IS REPLACED BY THE GVOLUME CLASS IN ALL FUNCTIONS

def build_lead(configuration):
	# The lead box is a simple box (complete description)
	'''
	my $xposlead = $Dx;
	my $yposlead = $Dy;
	my $id = 0;
	my %detector = init_det();

	$detector{"name"}        = "lead_box";
	$detector{"mother"}      = "root";
	$detector{"description"} = "lead box container";
	$detector{"pos"}         = "0*cm 0*cm 0*cm";
	$detector{"rotation"}    = "0*deg 0*deg 0*deg";
	$detector{"color"}       = "7070702";
	$detector{"type"}        = "Box";
	$detector{"dimensions"}  = "$Dx*cm $Dy*cm 2*cm";
	$detector{"material"}    = "G4_Pb";
	$detector{"mfield"}      = "no";
	$detector{"style"}       = 1;
	$detector{"visible"}     = 0;
	$detector{"sensitivity"} = "flux";
	$detector{"hit_type"}    = "flux";
	$detector{"identifiers"} = "lead manual $id";

	print_det(\%configuration, \%detector);
 	'''
  	#xposlead = dx
	#yposlead = dy
	#id = 0	
	gvolume = GVolume('lead_box')
	gvolume.mother = 'root'
	gvolume.description = 'lead box container'
	#gvolume.pos = "0*cm 0*cm 0*cm"
	#gvolume.rotation = "0*deg 0*deg 0*deg" 
	gvolume.color = '7070702'
	#gvolume.type = 'Box'
	gvolume.make_box(dx, dy, 2, 'cm')
	gvolume.material = 'G4_Pb'
	gvolume.mfield = 'no'
	gvolume.style = 1
	gvolume.visible = 0
	#gvolume.sensitivity = 'flux'
	#gvolume.hit_type = 'flux'
	#gvolume.identifiers = 'id manual ' + str(id)
	gvolume.publish(configuration)


# === A-fibers ===
def build_fiber_a(configuration):
	# The A-fibers are a simple tube (complete description)
	# The A-fibers are built from the inside out, that is,
	# the cores are built first, then the first coating and then the second one
	'''
 	for (my $nx=0; $nx<$ncols; $nx++) {
		for (my $ny=0; $ny<$nrowsa; $ny++) {
			my $id   = generate_id(1, 0, $nx, $ny);
			my $posx = -$Dx + 0.05 + 2 * 0.05 * $nx;
			my $posy = -$Dy + 0.05 + (0.05 * 1.732050808 + 0.05)* $ny * 2;
			my %detector = init_det();

			$detector{"name"}        = "core_$id";
			$detector{"mother"}      = "lead_box";
			$detector{"description"} = "$nx $ny fiber a";
			$detector{"pos"}         = "$posx*cm $posy*cm 0*cm";
			$detector{"rotation"}    = "0*deg 0*deg 0*deg";
			$detector{"color"}       = "FFFFFF";
			$detector{"type"}        = "Tube";
			$detector{"dimensions"}  = "0*cm 0.046*cm $flength*cm 0*deg 360*deg";
			$detector{"material"}    = "core";
			$detector{"mfield"}      = "no";
			$detector{"style"}       = 1;
			$detector{"visible"}     = 1;
			$detector{"sensitivity"} = "flux";
			$detector{"hit_type"}    = "flux";
			$detector{"identifiers"} = "fiber_a manual $id";
			print_det(\%configuration, \%detector);
  	'''
	for nx in range(0, ncols):
		for ny in range(0, nrowsa):
			id   = generate_id(1, 0, nx, ny)
			#posx = -dx + 0.05 + 2 * 0.05 * nx
			#posy = -dy + 0.05 + (0.05 * 1.732050808 + 0.05) * ny * 2;
			gvolume = GVolume('core_' + str(id))
			gvolume.name = "core_" + str(id)
			gvolume.mother = "lead_box"
			gvolume.description = str(nx) + ' ' + str(ny) + ' fiber a'
			#gvolume.pos = str(posx) + '*cm ' + str(posy) + '*cm 0*cm'
			#gvolume.rotation = "0*deg 0*deg 0*deg"
			gvolume.color = 'FFFFFF'
			#gvolume.type = 'Tube'
			gvolume.make_tube(0, 0.046, flength, 0, 360, 'cm')
			gvolume.material = 'core'
			gvolume.mfield = 'no'
			gvolume.style = 1
			gvolume.visible = 1
			#gvolume.sensitivity = 'flux'
			#gvolume.hit_type = 'flux'
			#gvolume.identifiers = 'fiber_a manual ' + str(id)
			gvolume.publish(configuration)

# === A-inclad ===
def build_inclad_a(configuration):
	'''
	for (my $nx=0; $nx<$ncols; $nx++) {
		for (my $ny=0; $ny<$nrowsa; $ny++) {
			my $id   = generate_id(2, 0, $nx, $ny);
			my $posx = -$Dx + 0.05 + 2 * 0.05 * $nx;
			my $posy = -$Dy + 0.05 + (0.05 * 1.732050808 + 0.05) * $ny * 2;
			my %detector = init_det();

			$detector{"name"}        = "inclad_$id";
			$detector{"mother"}      = "lead_box";
			$detector{"description"} = "$nx $ny inclad a";
			$detector{"pos"}         = "$posx*cm $posy*cm 0*cm";
			$detector{"rotation"}    = "0*deg 0*deg 0*deg";
			$detector{"color"}       = "7CCBFF";
			$detector{"type"}        = "Tube";
			$detector{"dimensions"}  = "0.046*cm 0.048*cm $flength*cm 0*deg 360*deg";
			$detector{"material"}    = "inclad";
			$detector{"mfield"}      = "no";
			$detector{"style"}       = 1;
			$detector{"visible"}     = 1;
			$detector{"sensitivity"} = "flux";
			$detector{"hit_type"}    = "flux";
			$detector{"identifiers"} = "inclad_a manual $id";
			print_det(\%configuration, \%detector);
        '''
	for nx in range(0, ncols):
		for ny in range(0, nrowsa):
			id   = generate_id(2, 0, nx, ny)
			posx = -dx + 0.05 + 2 * 0.05 * nx
			posy = -dy + 0.05 + (0.05 * 1.732050808 + 0.05) * ny * 2;
			gvolume = GVolume('inclad_' + str(id))
			gvolume.name = "inclad_" + str(id)
			gvolume.mother = "lead_box"
			gvolume.description = str(nx) + ' ' + str(ny) + ' inclad a'
			#gvolume.pos = str(posx) + '*cm ' + str(posy) + '*cm 0*cm'
			#gvolume.rotation = '0*deg 0*deg 0*deg'
			gvolume.color = '7CCBFF'
			#gvolume.type = 'Tube'
			gvolume.make_tube(0.046, 0.048, flength, 0, 360, 'cm')
			gvolume.material = 'inclad'
			gvolume.mfield = 'no'
			gvolume.style = 1
			gvolume.visible = 1
			#gvolume.sensitivity = 'flux'
			#gvolume.hit_type = 'flux'
			#gvolume.identifiers = 'inclad_a manual ' + str(id)
			gvolume.publish(configuration)


# === A-outclad ===
def build_outclad_a(configuration):
	'''
	for (my $nx=0; $nx<$ncols; $nx++) {
		for (my $ny=0; $ny<$nrowsa; $ny++) {
			my $id   = generate_id(3, 0, $nx, $ny);
			my $posx = -$Dx + 0.05 + 2 * 0.05 * $nx;
			my $posy = -$Dy + 0.05 + (0.05 * 1.732050808 + 0.05)* $ny * 2;
			my %detector = init_det();

			$detector{"name"}        = "outclad_$id";
			$detector{"mother"}      = "lead_box";
			$detector{"description"} = "$nx $ny outclad a";
			$detector{"pos"}         = "$posx*cm $posy*cm 0*cm";
			$detector{"rotation"}    = "0*deg 0*deg 0*deg";
			$detector{"color"}       = "0089E4";
			$detector{"type"}        = "Tube";
			$detector{"dimensions"}  = "0.048*cm 0.05*cm $flength*cm 0*deg 360*deg";
			$detector{"material"}    = "outclad";
			$detector{"mfield"}      = "no";
			$detector{"style"}       = 1;
			$detector{"visible"}     = 1;
			$detector{"sensitivity"} = "flux";
			$detector{"hit_type"}    = "flux";
			$detector{"identifiers"} = "outclad_a manual $id";
			print_det(\%configuration, \%detector);
	'''
	for nx in range(0, ncols):
		for ny in range(0, nrowsa):
			id   = generate_id(3, 0, nx, ny)
			#posx = -dx + 0.05 + 2 * 0.05 * nx
			#posy = -dy + 0.05 + (0.05 * 1.732050808 + 0.05) * ny * 2;
			gvolume = GVolume('outclad_' + str(id))
			gvolume.name = "outclad_" + str(id)
			gvolume.mother = "lead_box"
			gvolume.description = str(nx) + ' ' + str(ny) + ' outclad a'
			#gvolume.pos = str(posx) + '*cm ' + str(posy) + '*cm 0*cm'
			#gvolume.rotation = '0*deg 0*deg 0*deg'
			gvolume.color = '0089E4'
			#gvolume.type = 'Tube'
			gvolume.make_tube(0.048, 0.05, flength, 0, 360, 'cm')
			gvolume.material = 'outclad'
			gvolume.mfield = 'no'
			gvolume.style = 1
			gvolume.visible = 1
			#gvolume.sensitivity = 'flux'
			#gvolume.hit_type = 'flux'
			#gvolume.identifiers = 'outclad_a manual ' + str(id)
			gvolume.publish(configuration)
        
        
def build_sensor_1a(configuration):
	'''
	for (my $nx=0; $nx<$ncols; $nx++) {
		for (my $ny=0; $ny<$nrowsa; $ny++) {
			my $id   = generate_id(4, 0, $nx, $ny);
			my %detector = init_det();
			$detector{"name"}        = "sensor_$id";
			$detector{"description"} = "$nx $ny sensor1 a";
            		$detector{"mother"}      = "lead_box";
            		my $posx = -$Dx + 0.05 + 2 * 0.05 * $nx;
			my $posy = -$Dy + 0.05 + (0.05 * 1.732050808 + 0.05)* $ny * 2;
            		
              		$detector{"pos"}         = "$posx*cm $posy*cm -1.99*cm";
			$detector{"rotation"}    = "0*deg 0*deg 0*deg";
			$detector{"color"}       = "339999";
			$detector{"type"}        = "Tube";
			$detector{"dimensions"}  = "0*cm 0.046*cm 0.01*cm 0*deg 360*deg";
			$detector{"material"}    = "core";
			$detector{"mfield"}      = "no";
			$detector{"style"}       = 1;
			$detector{"visible"}     = 1;
			$detector{"sensitivity"} = "flux";
			$detector{"hit_type"}    = "flux";
			$detector{"identifiers"} = "sensor1_a manual $id";
			print_det(\%configuration, \%detector);
	'''
	for nx in range(0, ncols):
		for ny in range(0, nrowsa):
			id   = generate_id(4, 0, nx, ny)
			#posx = -dx + 0.05 + 2 * 0.05 * nx
			#posy = -dy + 0.05 + (0.05 * 1.732050808 + 0.05) * ny * 2;
			gvolume = GVolume('sensor_' + str(id))
			gvolume.name = "sensor_" + str(id)
			gvolume.mother = "lead_box"
			gvolume.description = str(nx) + ' ' + str(ny) + ' sensor1 a'
			#gvolume.pos = str(posx) + '*cm ' + str(posy) + '*cm -1.99*cm'
			#gvolume.rotation = '0*deg 0*deg 0*deg'
			gvolume.color = '339999'
			#gvolume.type = 'Tube'
			gvolume.make_tube(0, 0.046, 0.01, 0, 360, 'cm')
			gvolume.material = 'core'
			gvolume.mfield = 'no'
			gvolume.style = 1
			gvolume.visible = 1
			#gvolume.sensitivity = 'flux'
			#gvolume.hit_type = 'flux'
			#gvolume.identifiers = 'sensor1_a manual ' + str(id)
			gvolume.publish(configuration)
 
def build_sensor_2a(configuration):
	'''
	for (my $nx=0; $nx<$ncols; $nx++) {
		for (my $ny=0; $ny<$nrowsa; $ny++) {
			my $id   = generate_id(5, 0, $nx, $ny);
			my %detector = init_det();

			$detector{"name"}        = "sensor_$id";
			$detector{"description"} = "$nx $ny sensor2 a";
			$detector{"mother"}      = "lead_box";
			my $posx = -$Dx + 0.05 + 2 * 0.05 * $nx;
			my $posy = -$Dy + 0.05 + (0.05 * 1.732050808 + 0.05)* $ny * 2;

			$detector{"pos"}         = "$posx*cm $posy*cm 1.99*cm";
			$detector{"rotation"}    = "0*deg 0*deg 0*deg";
			$detector{"color"}       = "339999";
			$detector{"type"}        = "Tube";
			$detector{"dimensions"}  = "0*cm 0.046*cm 0.01*cm 0*deg 360*deg";
			$detector{"material"}    = "core";
			$detector{"mfield"}      = "no";
			$detector{"style"}       = 1;
			$detector{"visible"}     = 1;
			$detector{"sensitivity"} = "flux";
			$detector{"hit_type"}    = "flux";
			$detector{"identifiers"} = "sensor2_a manual $id";
			print_det(\%configuration, \%detector);
	'''
	for nx in range(0, ncols):
		for ny in range(0, nrowsa):
			id   = generate_id(5, 0, nx, ny)
			#posx = -dx + 0.05 + 2 * 0.05 * nx
			#posy = -dy + 0.05 + (0.05 * 1.732050808 + 0.05) * ny * 2;
			gvolume = GVolume('sensor_' + str(id))
			gvolume.name = "sensor_" + str(id)
			gvolume.mother = "lead_box"
			gvolume.description = str(nx) + ' ' + str(ny) + ' sensor2 a'
			#gvolume.pos = str(posx) + '*cm ' + str(posy) + '*cm 1.99*cm'
			#gvolume.rotation = '0*deg 0*deg 0*deg'
			gvolume.color = '339999'
			#gvolume.type = 'Tube'
			gvolume.make_tube(0, 0.046, 0.01, 0, 360, 'cm')
			gvolume.material = 'core'
			gvolume.mfield = 'no'
			gvolume.style = 1
			gvolume.visible = 1
			#gvolume.sensitivity = 'flux'
			#gvolume.hit_type = 'flux'
			#gvolume.identifiers = 'sensor2_a manual ' + str(id)
			gvolume.publish(configuration)
	
    
def build_fiber_b(configuration):
	'''
        for (my $nx=0; $nx<($ncols-1); $nx++) {
		for (my $ny=0; $ny<$nrowsb; $ny++) {
			my $id   = generate_id(1, 1, $nx, $ny);
			my $posx = 2 * 0.05 * $nx + 0.1 - $Dx;
			my $posy = -$Dy + 0.05 + (0.05 * 1.732050808 + 0.05) * $ny * 2  + 0.05 * 1.732050808 + 0.05;
			my %detector = init_det();

			$detector{"name"}        = "core_$id";
			$detector{"mother"}      = "lead_box" ;
			$detector{"description"} = "$nx $ny fiber b";
			$detector{"pos"}         = "$posx*cm $posy*cm 0*cm";
			$detector{"rotation"}    = "0*deg 0*deg 0*deg";
			$detector{"color"}       = "FFFFFF";
			$detector{"type"}        = "Tube";
			$detector{"dimensions"}  = "0*cm 0.046*cm $flength*cm 0*deg 360*deg";
			$detector{"material"}    = "core";
			$detector{"mfield"}      = "no";
			$detector{"style"}       = 1;
			$detector{"visible"}     = 1;
			$detector{"sensitivity"} = "flux";
			$detector{"hit_type"}    = "flux";
			$detector{"identifiers"} = "fiber_b manual $id";
			print_det(\%configuration, \%detector);
        '''
	for nx in range(0, ncols-1):
		for ny in range(0, nrowsb):
			id   = generate_id(1, 1, nx, ny)
			#posx = 2 * 0.05 * nx + 0.1 - dx
			#posy = -dy + 0.05 + (0.05 * 1.732050808 + 0.05) * ny * 2  + 0.05 * 1.732050808 + 0.05
			gvolume = GVolume('core_' + str(id))
			gvolume.name = "core_" + str(id)
			gvolume.mother = "lead_box"
			gvolume.description = str(nx) + ' ' + str(ny) + ' fiber b'
			#gvolume.pos = str(posx) + '*cm ' + str(posy) + '*cm 0*cm'
			#gvolume.rotation = '0*deg 0*deg 0*deg'
			gvolume.color = 'FFFFFF'
			#gvolume.type = 'Tube'
			gvolume.make_tube(0, 0.046, flength, 0, 360, 'cm')
			gvolume.material = 'core'
			gvolume.mfield = 'no'
			gvolume.style = 1
			gvolume.visible = 1
			#gvolume.sensitivity = 'flux'
			#gvolume.hit_type = 'flux'
			#gvolume.identifiers = 'fiber_b manual ' + str(id)
			gvolume.publish(configuration)
        
def build_inclad_b(configuration):
	'''
 	    for(my $nx=0; $nx<($ncols-1); $nx++) {
		for(my $ny=0; $ny<$nrowsb; $ny++) {
			my $id   = generate_id(2, 1, $nx, $ny);
			my $posx = 2 * 0.05 * $nx + 0.1 - $Dx;
			my $posy = -$Dy + 0.05 + (0.05 * 1.732050808 + 0.05) * $ny * 2  + 0.05 * 1.732050808 + 0.05;
			my %detector = init_det();

			$detector{"name"}        = "inclad_$id";
			$detector{"mother"}      = "lead_box" ;
			$detector{"description"} = "$nx $ny inclad b";
			$detector{"pos"}         = "$posx*cm $posy*cm 0*cm";
			$detector{"rotation"}    = "0*deg 0*deg 0*deg";
			$detector{"color"}       = "7CCBFF";
			$detector{"type"}        = "Tube";
			$detector{"dimensions"}  = "0.046*cm 0.048*cm $flength*cm 0*deg 360*deg";
			$detector{"material"}    = "inclad";
			$detector{"mfield"}      = "no";
			$detector{"style"}       = 1;
			$detector{"visible"}     = 1;
			$detector{"sensitivity"} = "flux";
			$detector{"hit_type"}    = "flux";
			$detector{"identifiers"} = "inclad_b manual $id";
			print_det(\%configuration, \%detector);
		}
	'''
	for nx in range(0, ncols-1):
		for ny in range(0, nrowsb):
			id   = generate_id(2, 1, nx, ny)
			#posx = 2 * 0.05 * nx + 0.1 - dx
			#posy = -dy + 0.05 + (0.05 * 1.732050808 + 0.05) * ny * 2  + 0.05 * 1.732050808 + 0.05
			gvolume = GVolume('inclad_' + str(id))
			gvolume.name = "inclad_" + str(id)
			gvolume.mother = "lead_box"
			gvolume.description = str(nx) + ' ' + str(ny) + ' inclad b'
			#gvolume.pos = str(posx) + '*cm ' + str(posy) + '*cm 0*cm'
			#gvolume.rotation = '0*deg 0*deg 0*deg'
			gvolume.color = '7CCBFF'
			#gvolume.type = 'Tube'
			gvolume.make_tube(0.046, 0.048, flength, 0, 360, 'cm')
			gvolume.material = 'inclad'
			gvolume.mfield = 'no'
			gvolume.style = 1
			gvolume.visible = 1
			#gvolume.sensitivity = 'flux'
			#gvolume.hit_type = 'flux'
			#gvolume.identifiers = 'inclad_b manual ' + str(id)
			gvolume.publish(configuration)

def build_outclad_b(configuration):
	'''
        for (my $nx=0; $nx<($ncols-1); $nx++) {
		for (my $ny=0; $ny<$nrowsb; $ny++) {
			my $id   = generate_id(3, 1, $nx, $ny);
			my $posx = 2 * 0.05 * $nx + 0.1 - $Dx;
			my $posy = -$Dy + 0.05 + (0.05 * 1.732050808 + 0.05) * $ny * 2  + 0.05 * 1.732050808 + 0.05;
			my %detector = init_det();

			$detector{"name"}        = "outclad_$id";
			$detector{"mother"}      = "lead_box";
			$detector{"description"} = "$nx $ny outclad b";
			$detector{"pos"}         = "$posx*cm $posy*cm 0*cm";
			$detector{"rotation"}    = "0*deg 0*deg 0*deg";
			$detector{"color"}       = "0089E4";
			$detector{"type"}        = "Tube";
			$detector{"dimensions"}  = "0.048*cm 0.05*cm $flength*cm 0*deg 360*deg";
			$detector{"material"}    = "outclad";
			$detector{"mfield"}      = "no";
			$detector{"style"}       = 1;
			$detector{"visible"}     = 1;
			$detector{"sensitivity"} = "flux";
			$detector{"hit_type"}    = "flux";
			$detector{"identifiers"} = "outclad_b manual $id";
			print_det(\%configuration, \%detector);
        '''
	for nx in range(0, ncols-1):
		for ny in range(0, nrowsb):
			id   = generate_id(3, 1, nx, ny)
			#posx = 2 * 0.05 * nx + 0.1 - dx
			#posy = -dy + 0.05 + (0.05 * 1.732050808 + 0.05) * ny * 2  + 0.05 * 1.732050808 + 0.05
			gvolume = GVolume('outclad_' + str(id))
			gvolume.name = "outclad_" + str(id)
			gvolume.mother = "lead_box"
			gvolume.description = str(nx) + ' ' + str(ny) + ' outclad b'
			#gvolume.pos = str(posx) + '*cm ' + str(posy) + '*cm 0*cm'
			#gvolume.rotation = '0*deg 0*deg 0*deg'
			gvolume.color = '0089E4'
			#gvolume.type = 'Tube'
			gvolume.make_tube(0.048, 0.05, flength, 0, 360, 'cm')
			gvolume.material = 'outclad'
			gvolume.mfield = 'no'
			gvolume.style = 1
			gvolume.visible = 1
			#gvolume.sensitivity = 'flux'
			#gvolume.hit_type = 'flux'
			#gvolume.identifiers = 'outclad_b manual ' + str(id)
			gvolume.publish(configuration)


def build_sensor_1b(configuration):
	'''
	for (my $nx=0; $nx<($ncols-1); $nx++) {
		for (my $ny=0; $ny<$nrowsb; $ny++) {
			my $id   = generate_id(4, 1, $nx, $ny);
			my %detector = init_det();

			$detector{"name"}        = "sensor_$id";
            		$detector{"description"} = "$nx $ny sensor1 b";
            		$detector{"mother"}      = "lead_box";
            		my $posx = 2 * 0.05 * $nx + 0.1 - $Dx;
			my $posy = -$Dy + 0.05 + (0.05 * 1.732050808 + 0.05) * $ny * 2  + 0.05 * 1.732050808 + 0.05;
            		$detector{"pos"}         = "$posx*cm $posy*cm -1.99*cm";
			$detector{"rotation"}    = "0*deg 0*deg 0*deg";
			$detector{"color"}       = "339999";
			$detector{"type"}        = "Tube";
			$detector{"dimensions"}  = "0*cm 0.046*cm 0.01*cm 0*deg 360*deg";
			$detector{"material"}    = "core";
			$detector{"mfield"}      = "no";
			$detector{"style"}       = 1;
			$detector{"visible"}     = 1;
			$detector{"sensitivity"} = "flux";
			$detector{"hit_type"}    = "flux";
			$detector{"identifiers"} = "sensor1_b manual $id";
			print_det(\%configuration, \%detector);
 	'''
	for nx in range(0, ncols-1):
		for ny in range(0, nrowsb):
			id   = generate_id(4, 1, nx, ny)
			#posx = 2 * 0.05 * nx + 0.1 - dx
			#posy = -dy + 0.05 + (0.05 * 1.732050808 + 0.05) * ny * 2  + 0.05 * 1.732050808 + 0.05
			gvolume = GVolume('sensor_' + str(id))
			gvolume.name = "sensor_" + str(id)
			gvolume.mother = "lead_box"
			gvolume.description = str(nx) + ' ' + str(ny) + ' sensor1 b'
			#gvolume.pos = str(posx) + '*cm ' + str(posy) + '*cm -1.99*cm'
			#gvolume.rotation = '0*deg 0*deg 0*deg'
			gvolume.color = '339999'
			#gvolume.type = 'Tube'
			gvolume.make_tube(0, 0.046, 0.01, 0, 360, 'cm')
			gvolume.material = 'core'
			gvolume.mfield = 'no'
			gvolume.style = 1
			gvolume.visible = 1
			#gvolume.sensitivity = 'flux'
			#gvolume.hit_type = 'flux'
			#gvolume.identifiers = 'sensor1_b manual ' + str(id)
			gvolume.publish(configuration)

def build_sensor_2b(configuration):
	'''
        for (my $nx=0; $nx<($ncols-1); $nx++) {
		for (my $ny=0; $ny<$nrowsb; $ny++) {
            		my $id   = generate_id(5, 1, $nx, $ny);
			my %detector = init_det();

			$detector{"name"}        = "sensor_$id";
            		$detector{"description"} = "$nx $ny sensor2 b";
            		$detector{"mother"}      = "lead_box";
            		my $posx = 2 * 0.05 * $nx + 0.1 - $Dx;
			my $posy = -$Dy + 0.05 + (0.05 * 1.732050808 + 0.05) * $ny * 2  + 0.05 * 1.732050808 + 0.05;
            		$detector{"pos"}         = "$posx*cm $posy*cm 1.99*cm";
			$detector{"rotation"}    = "0*deg 0*deg 0*deg";
			$detector{"color"}       = "339999";
			$detector{"type"}        = "Tube";
			$detector{"dimensions"}  = "0*cm 0.046*cm 0.01*cm 0*deg 360*deg";
			$detector{"material"}    = "core";
			$detector{"mfield"}      = "no";
			$detector{"style"}       = 1;
			$detector{"visible"}     = 1;
			$detector{"sensitivity"} = "flux";
			$detector{"hit_type"}    = "flux";
			$detector{"identifiers"} = "sensor2_b manual $id";
			print_det(\%configuration, \%detector);
        '''
	for nx in range(0, ncols-1):
		for ny in range(0, nrowsb):
			id   = generate_id(5, 1, nx, ny)
			#posx = 2 * 0.05 * nx + 0.1 - dx
			#posy = -dy + 0.05 + (0.05 * 1.732050808 + 0.05) * ny * 2  + 0.05 * 1.732050808 + 0.05
			gvolume = GVolume('sensor_' + str(id))
			gvolume.name = "sensor_" + str(id)
			gvolume.mother = "lead_box"
			gvolume.description = str(nx) + ' ' + str(ny) + ' sensor2 b'
			#gvolume.pos = str(posx) + '*cm ' + str(posy) + '*cm 1.99*cm'
			#gvolume.rotation = '0*deg 0*deg 0*deg'
			gvolume.color = '339999'
			#gvolume.type = 'Tube'
			gvolume.make_tube(0, 0.046, 0.01, 0, 360, 'cm')
			gvolume.material = 'core'
			gvolume.mfield = 'no'
			gvolume.style = 1
			gvolume.visible = 1
			#gvolume.sensitivity = 'flux'
			#gvolume.hit_type = 'flux'
			#gvolume.identifiers = 'sensor2_b manual ' + str(id)
			gvolume.publish(configuration)
