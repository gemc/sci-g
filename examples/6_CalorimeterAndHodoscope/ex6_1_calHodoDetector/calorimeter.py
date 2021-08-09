from gemc_api_geometry import *
import math

# global vars

###########################################################################################
###########################################################################################
# Define the relevant parameters of FT Geometry
#
# the FT geometry will be defined starting from these parameters
# and the position on the torus inner ring
#
# all dimensions are in mm
#

degrad    = 57.27;
torus_z   = 2663.# position of the front face of the Torus ring (set the limit in z)



###########################################################################################
# CALORIMETER
#
# Define the number, dimensions and position of the crystals
Nx = 22                         # Number of crystals in horizontal directions
Ny = 22                         # Number of crystals in horizontal directions
Cfront  =  1897.8               # Position of the front face of the crystals
Cwidth  =    15.0               # Crystal width in mm (side of the squared front face)
Clength =   200.0               # Crystal length in mm
VM2000  =   0.130               # Thickness of the VM2000 wrapping
AGap    =   0.170               # Air Gap between Crystals, total wodth of crystal including wrapping and air gap is 15.3 mm
Flength =     8.0               # Length of the crystal front support
Fwidth  = Cwidth                # Width of the crystal front support
Wwidth  = Cwidth+VM2000         # Width of the wrapping volume
Vwidth  = Cwidth+VM2000+AGap    # Width of the crystal mother volume, total width of crystal including wrapping and air gap is 15.3 mm
Vlength = Clength+Flength       # Length of the crystal mother volume
Vfront  = Cfront-Flength        # z position of the volume front face
Slength =     7.0               # Length of the sensor "box"
Swidth  = Cwidth                # Width of the sensor "box"
Sgap    =     1.0               # Gap for flux detector
Sfront  = Vfront+Vlength+Sgap   # z position of the sensor front face

# Define the copper thermal shield parameters
# back disk
Bdisk_TN = 4.                                          # half thickness of the copper back disk
Bdisk_IR = 55.                                         # inner radius of the copper back disk
Bdisk_OR = 178.5                                       # outer radius of the copper back disk
Bdisk_Z  = Sfront+Slength+Bdisk_TN+0.1                 # z position of the copper back disk
# front disk
Fdisk_TN = 1.                                          # half thickness of the copper front disk supporting the crystal assemblies
Fdisk_IR = Bdisk_IR                                    # inner radius of the copper front disk
Fdisk_OR = Bdisk_OR                                    # outer radius of the copper front disk
Fdisk_Z  = Vfront-Fdisk_TN-0.1                         # z position of the copper front disk
# space for preamps
BPlate_TN = 25.                                        # half thickness of the preamps volume
BPlate_IR = Bdisk_IR                                   # inner radius of the preamps volume
BPlate_OR = Bdisk_OR                                   # outer radius of the preamps volume
BPlate_Z  = Bdisk_Z+Bdisk_TN+BPlate_TN+0.1             # z position of the preamps volume
# inner copper tube
Idisk_LT = (BPlate_Z+BPlate_TN-Fdisk_Z+Fdisk_TN)/2.    # length of the inner copper tube
Idisk_TN = 4                                           # thickness of the inner copper tube
Idisk_OR = Fdisk_IR                                    # outer radius of the inner copper tube matches inner radius of front and back disks
Idisk_IR = Fdisk_IR-Idisk_TN                           # inner radius of the inner copper tube
Idisk_Z  = (BPlate_Z+BPlate_TN+Fdisk_Z-Fdisk_TN)/2.    # z position of inner copper tube
# outer copper tube
Odisk_LT = (BPlate_Z+BPlate_TN-Fdisk_Z+Fdisk_TN)/2.    # length of the outer copper tube
Odisk_TN = 2                                           # thickness of the outer copper tube
Odisk_IR = Fdisk_OR                                    # inner radius of the outer copper tube matches outer radius of front and back disks
Odisk_OR = Fdisk_OR+Odisk_TN                           # outer radius of the outer copper tube
Odisk_Z  = Idisk_Z                                     # z position of the outer copper tube

# Define the motherboard parameters
Bmtb_TN = 1.                                           # half thickness of the motherboard
Bmtb_IR = Idisk_IR                                     # inner radius of the motherboard
Bmtb_OR = Odisk_OR                                     # outer radius of the motherboard
Bmtb_Z  = BPlate_Z + BPlate_TN + Bmtb_TN + 0.1         # z position of the motherboard
Bmtb_hear_WD = 80./2.                                  # half width of the motherboard extensions
Bmtb_hear_LN = 225./2                                  # half length of the motherboard extensions
Bmtb_hear_D0 = 0.                                      # displacement of the motherboard extensions
Bmtb_angle = [ 30., 150., 210., 330.]                  # angles of the motherboard extensions

# Define LED plate geometry parameters
LED_TN =   6.1                                        # half thickness of the pcb and pastic plate hosting the LEDs
LED_IR = Fdisk_IR                                     # inner radius of the pcb and pastic plate hosting the LEDs
LED_OR = Fdisk_OR                                     # outer radius of the pcb and pastic plate hosting the LEDs
LED_Z  = Fdisk_Z - Fdisk_TN - LED_TN - 0.1            # z position of the pcb and pastic plate hosting the LEDs

# bline: tungsten pipe inside the ft_cal
BLine_IR = 30.                                         # pipe inner radius;
BLine_SR = 33.5                                        # pipe inner radius in steel case;
BLine_DR = 25.1                                        # shield inner radius in steel case;
BLine_TN = 10.                                         # pipe thickness
BLine_FR = BLine_IR + BLine_TN                         # radius in the front part, connecting to moller shield
BLine_OR = 100.                                        # radius of the back flange
BLine_BG = 1644.7                                      # z location of the beginning of the beamline (to be matched to moller shield)
BLine_ML = 1760.0                                      # z location of the end of the Moller shield


# back tungsten cup
BCup_tang = 0.0962                                     # tangent of 5.5 degrees
BCup_TN = 5.                                           # thickness of the flat part of the cup
BCup_ZM = Bmtb_Z+Bmtb_TN+0.1+43.4                      # z of the downstream face of the cup
BCup_Z1 = Bmtb_Z+Bmtb_TN+0.1+1                         # z of the side close to the motherboard (downstream)
BCup_Z2 = Bmtb_Z-Bmtb_TN-0.1-1                         # z of the side close to the motherboard (upstream)
BCup_ZE = BCup_ZM+BCup_TN                              # z of the downstream face of the cup
BCup_ZB = BCup_ZM-120.                                 # z beginning of the conical part
BCup_IRM = 190.                                        # inner radius at the beginning of the cone
BCup_ORB = BCup_ZB*BCup_tang                           # outer radius at the beginning of the cone
BCup_OR1 = BCup_Z1*BCup_tang                           # outer radius close to the MTB
BCup_OR2 = BCup_Z2*BCup_tang                           # outer radius close to the MTB
BCup_ORM = BCup_ZM*BCup_tang                           # outer radius at the front face of the plate
BCup_ORE = BCup_ZE*BCup_tang                           # outer radius at the back face of the plate
BCup_angle = int(math.atan(Bmtb_hear_WD/Bmtb_OR)*degrad*10)/10+0.5;
BCup_iangle = [30.+BCup_angle, 150.+BCup_angle, 210.+BCup_angle, 330.+BCup_angle];
BCup_dangle = [(90.-BCup_iangle[0])*2., (180.-BCup_iangle[1])*2., (90.-BCup_iangle[0])*2.,(180.-BCup_iangle[1])*2.];

TPlate_TN= 20. # thickness of the tungsten plate on the back of the FT-Cal



###########################################################################################
# OUTER INSULATION
O_Ins_TN  = 15.-0.01;
O_Ins_Z1  = Fdisk_Z - Fdisk_TN - LED_TN*2 - 10.8 - O_Ins_TN #1849.6
O_Ins_Z2  = O_Ins_Z1 + O_Ins_TN;
O_Ins_Z3  = BCup_ZB;
O_Ins_Z4  = BCup_Z2;
O_Ins_Z5  = BCup_Z1;
O_Ins_Z6  = BCup_ZM;
O_Ins_Z7  = BCup_ZE;
O_Ins_Z8  = BCup_ZE + 0.01;
O_Ins_Z9  = O_Ins_Z8 + O_Ins_TN;
O_Ins_Z10 = O_Ins_Z9;
O_Ins_Z11 = O_Ins_Z10 + TPlate_TN;

O_Ins_I1  = BLine_IR + BLine_TN + 0.01;
O_Ins_I2  = O_Ins_Z2*BCup_tang +0.01;
O_Ins_I3  = O_Ins_Z3*BCup_tang +0.01;
O_Ins_I4  = O_Ins_Z4*BCup_tang +0.01;
O_Ins_I5  = O_Ins_Z5*BCup_tang +0.01;
O_Ins_I6  = O_Ins_Z6*BCup_tang +0.01;
O_Ins_I7  = O_Ins_Z7*BCup_tang +0.01;
O_Ins_I8  = O_Ins_Z8*BCup_tang +0.01;
O_Ins_I9  = O_Ins_I1;
O_Ins_I10 = O_Ins_Z10*BCup_tang +0.01;
O_Ins_I11 = O_Ins_I10;

O_Ins_O1  = O_Ins_Z1*BCup_tang +0.01 + O_Ins_TN;
O_Ins_O2  = O_Ins_I2 + O_Ins_TN;
O_Ins_O3  = O_Ins_I3 + O_Ins_TN;
O_Ins_O4  = O_Ins_I4 + O_Ins_TN;
O_Ins_O5  = O_Ins_I5 + O_Ins_TN;
O_Ins_O6  = O_Ins_I6 + O_Ins_TN;
O_Ins_O7  = O_Ins_I7 + O_Ins_TN;
O_Ins_O8  = O_Ins_I8 + O_Ins_TN;
O_Ins_O9  = O_Ins_Z9*BCup_tang +0.01 + O_Ins_TN;
O_Ins_O10 = O_Ins_I10 + O_Ins_TN;
O_Ins_O11 = O_Ins_I11 + O_Ins_TN;

O_Ins_I4 = O_Ins_Z4*BCup_tang +0.5;
O_Ins_I5 = O_Ins_Z5*BCup_tang +0.5;

###########################################################################################
# INNER INSULATION
I_Ins_LT = (BCup_ZE - O_Ins_Z2 -0.1)/2.;
I_Ins_OR =  Idisk_IR - 0.1;
I_Ins_IR =  O_Ins_I1;
I_Ins_Z  = (BCup_ZE + O_Ins_Z2)/2.;

###########################################################################################
# OUTER SHELL
O_Shell_TN = 2.-0.01;
O_Shell_Z1 = O_Ins_Z1-O_Shell_TN-0.01;
O_Shell_Z2 = O_Shell_Z1+O_Shell_TN;
O_Shell_Z3 = O_Ins_Z3;
O_Shell_Z4 = BCup_Z2;
O_Shell_Z5 = BCup_Z1;
O_Shell_Z6 = O_Ins_Z6 ;
O_Shell_Z7 = O_Ins_Z7 ;
O_Shell_Z8 = O_Ins_Z8 ;
O_Shell_Z9 = O_Ins_Z9 ;
O_Shell_Z10 = O_Ins_Z10;
O_Shell_Z11 = O_Ins_Z11 + 0.01;
O_Shell_Z12 = O_Shell_Z11;
O_Shell_Z13 = O_Shell_Z12 + O_Shell_TN;

O_Shell_I1 = O_Ins_I1;
O_Shell_I2 = O_Shell_Z2*BCup_tang + O_Ins_TN + 0.01;
O_Shell_I3 = O_Shell_Z3*BCup_tang + O_Ins_TN + 0.01;
O_Shell_I4 = O_Shell_Z4*BCup_tang + O_Ins_TN + 0.01;
O_Shell_I5 = O_Shell_Z5*BCup_tang + O_Ins_TN + 0.01;
O_Shell_I6 = O_Shell_Z6*BCup_tang + O_Ins_TN + 0.01;
O_Shell_I7 = O_Shell_Z7*BCup_tang + O_Ins_TN + 0.01;
O_Shell_I8 = O_Shell_Z8*BCup_tang + O_Ins_TN + 0.01;
O_Shell_I9 = O_Shell_Z9*BCup_tang + O_Ins_TN + 0.01;
O_Shell_I10 = O_Shell_Z10*BCup_tang + O_Ins_TN + 0.01;
O_Shell_I11 = O_Shell_Z11*BCup_tang + O_Ins_TN + 0.01;
O_Shell_I12 = O_Shell_I11 - O_Ins_TN -5.;
O_Shell_I13 = O_Shell_I12;

O_Shell_O1 = O_Shell_Z1*BCup_tang + O_Ins_TN + 0.01 + O_Shell_TN;
O_Shell_O2 = O_Shell_I2 + O_Shell_TN;
O_Shell_O3 = O_Shell_I3 + O_Shell_TN;
O_Shell_O4 = O_Shell_I4 + O_Shell_TN;
O_Shell_O5 = O_Shell_I5 + O_Shell_TN;
O_Shell_O6 = O_Shell_I6 + O_Shell_TN;
O_Shell_O7 = O_Shell_I7 + O_Shell_TN;
O_Shell_O8 = O_Shell_I8 + O_Shell_TN;
O_Shell_O9 = O_Shell_I9 + O_Shell_TN;
O_Shell_O10 = O_Shell_I10 + O_Shell_TN;
O_Shell_O11 = O_Shell_I11 + O_Shell_TN;
O_Shell_O12 = O_Shell_O11;
O_Shell_O13 = O_Shell_O12;

O_Shell_I4 = O_Shell_Z4*BCup_tang + O_Ins_TN + 0.7;
O_Shell_I5 = O_Shell_Z5*BCup_tang + O_Ins_TN + 0.7;

###########################################################################################
# FT BEAMLINE COMPONENTS

# ft to torus pipe
Tube_OR         =  75.0;
back_flange_OR  = 126.0;
front_flange_OR = 148.0;
flange_TN       =  15.0;


TPlate_RR  = TPlate_TN * 0.6;
TPlate_Z1  = O_Ins_Z9 + 0.01;
TPlate_Z2  = TPlate_Z1 + TPlate_TN-0.01;
TPlate_ZM  = TPlate_Z2 - TPlate_RR;
TPlate_MR  = BLine_IR  + BLine_TN + TPlate_RR;

BLine_MR  = BLine_IR + BLine_TN   # outer radius in the calorimeter section
BLine_Z1  = BLine_BG;
BLine_Z2  = BLine_ML   + 0.2;
BLine_Z3  = O_Shell_Z1 - 0.01;
BLine_Z4  = TPlate_Z2  + 0.01;
BLine_Z5  = BLine_Z4   - 0.01 + 20;




def buildCalorimeter(configuration):

	buildCalMotherVolume(configuration)

def buildCalMotherVolume(configuration):

	nplanes_FT = 6;
	z_plane_FT = [O_Shell_Z1,     2098.,  TPlate_ZM,   BLine_Z4,  BLine_Z4, BLine_Z5]
	iradius_FT = [  BLine_MR,  BLine_MR,   BLine_MR,  TPlate_MR,  BLine_OR, BLine_OR]
	oradius_FT = [     700.0,     700.0,      238.0,      238.0,     238.0,    238.0]


	# volume fields can be given either as named arguments in the MyDetector()
	# call or  assigned later to the GVolume instance variable
	gvolume = GVolume("chMother")

	# mandatory fields: solid, parameters, material
	# a G4Polycone is built with the same geant4 constructor parameters, in the same order.
	# an additional argument at the end can be given to specify the length units (default is mm)
	gvolume.makeG4Polycone('0*deg', '360*deg', nplanes_FT, z_plane_FT, iradius_FT, oradius_FT)
	gvolume.material     = "G4_AIR"	# G4_Si is a GEANT4 defined element name

	gvolume.description = "Calorimeter Mother Volume"
	gvolume.color       = "1437f4"

	gvolume.publish(configuration)
