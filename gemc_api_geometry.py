# -*- coding: utf-8 -*-
#=======================================
#	gemc geometry definition
#
#	This file defines a GVolume class that holds the parameters needed to define a geant4 physical volume in gemc.
#	Any volume in the project is an instance of this class.
#  The "publish" function writes out the volume parameters according to the factory.
#
#  A GVolume is be instantiated with these mandatory arguments:
#
#	name			- The name of the volume
#
#	solid			- The GEANT4 solid name, as defined in the documentation:
#                https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/Detector/Geometry/geomSolids.html
#
#	parameters	- A string giving the parameters (with units) required to define the solid
#                The order of the parameters matches the GEANT4 solid constructors.
#					  For example a "G4Box" type needs 3 dimensions:  pX, pY, pZ "2*cm 5*m 24*cm"
#
#	material		- A string defining the volume's material.  This can be a sci-g GMaterial name, or one from the GEANT4 material database:
#                https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/Appendix/materialNames.html#g4matrdb
#					  for example, "G4_MYLAR" or "G4_PLEXIGLASS".
#
#	The following GVolume parameters are optional:
#
#	mother			- The name of the parent volume. Defaults to the world volume "root"
#	position			- A string giving the location of this volume relative to the GEANT4 parent solid definition.
#                   Default is "0*mm, 0*mm, 0*mm"
#	rotations		- The rotation matrix of this volume relative to the GEANT4 parent solid definition.
#                   Default is "0*deg, 0*deg, 0*deg"
#                   The matrix can be defined by using either of two GVolume functions:
#                   1. setRotation(string):
#                      Define a single, ordered rotation.
#						     a. If the rotation string has 3 values, the rotation refers the x-, y-, and z- axes in order.
#                         For example "10*deg, 45*deg, 30*deg":
#                         rotation of 10° around x first, then 45° around y, then 30° around z.
#						     b. An additional string can be given at the end of the string to define the rotation's order.
#                         For example "10*deg, 45*deg, 30*deg, zyx":
#                         rotation of 30° around z first, then 45° around y, then 10° around x.
#                   2. addRotation(string):
#                      Adds a single rotation that refers the x-, y-, and z- axes in order. Note: addRotation is cumulative.
#                      For example addRotation("0*deg, 0*deg, 40*deg") follow by addRotation("10*deg, 0*deg, 0*deg"):
#                      defines a rotation of 40° around z first then apply a rotation of 10° around x.
#
#	mfild				- The name of a magnetic field file attached to the gvolume. Default is "no".
#                   The field is defined in the file header. In case of a field map, the data is contained in the file itself.
#
#
#	visible			- This is an integer field: 1 if the volume should be visible when the geometry is displayed, 0 if not. Default is "1".
#
#	style				- This is an integer field: 1 means display the volume as a solid, 0 means display as wireframe. Default is "1".
#
#	color			 	- A hexidecimal color value string, two chars for each f Red, Green, Blue (RGB) colors.  Default is "778899".
#                   For example, "0000ff" is blue.
#                   An optional 7th digit from 0-5 sets the transparency value where 0 is fully opaque and 5 is fully transparent
#					     Example:  "0000ff4" gives the volume a mostly transparent blue color
#
#	digitization	- A string defining the name of the plugin used to digitized the hit. Default is "none".
#                   Here pre-defined plugin can be selected:
#                   - flux: each tracks leaves a hit in the volume
#                   - particleCounter: used to count particles types passing through a volume
#
#                   In addition users can define their own plugin using c++, starting from predefined templates.
#                   The plugin filename is <name>.gplugin
#
#	copyOf	      - Not supported yet. Meant to make a copy of a volume
#	replicaOf	   - Not supported yet. Meant to make a g4replica
#	solidsOpr	   - Not supported yet. Meant to make a boolean operation between solids
#	mirror	      - Not supported yet. Meant to make a g4surface
#
#	exist				- This is an integer field:  1 if the volume exists, 0 if not.  It is a way to turn off volumes.
#						  This value can also be accessed in the jcard modifiers. Default is "1".
#
#	description		- A description of the volume. Default is "no description"

import sys, os, argparse

WILLBESET     = 'notSetYet' # for mandatory fields. Used in function checkValidity
NOTAPPLICABLE = 'na'        # for optionals fields
DEFAULTMOTHER = 'root'
DEFAULTCOLOR  = '778899'

# GVolume class definition
class GVolume():
	def __init__(self, name):

		# mandatory fields. Checked at publish time
		self.name        = name
		self.solid       = WILLBESET
		self.parameters  = WILLBESET
		self.material    = WILLBESET

		# optional fields
		self.mother       = DEFAULTMOTHER
		self.position     = '0*mm, 0*mm, 0*mm'
		self.rotations    = ['0*deg, 0*deg, 0*deg']
		self.mfield       = NOTAPPLICABLE

		self.visible      = 1		# 0 is invisible, 1 is visible
		self.style        = 1		# 0 is wireframe, 1 is solid
		self.color        = DEFAULTCOLOR

		self.digitization = NOTAPPLICABLE
		self.identifier   = NOTAPPLICABLE

		self.copyOf       = NOTAPPLICABLE
		self.replicaOf    = NOTAPPLICABLE
		self.solidsOpr    = NOTAPPLICABLE

		self.mirror       = NOTAPPLICABLE

		self.exist        = 1      # 0 does not exist, 1 exists
		self.description  = NOTAPPLICABLE

	def setRotation(self, x, y, z, lunit = 'deg', order = ''):
		with_units = [
			f"{val}*{lunit}"
			for val in [x,y,z]
		]
		string_with_units = ", ".join(with_units)
		if order: 
			self.rotations = f"ordered: {order}, {string_with_units}"
		else:
			self.rotations = string_with_units

	def setPosition(self, x, y, z, lunit = 'mm'):
		myposition  = str(x) + '*' + lunit + ', '
		myposition += str(y) + '*' + lunit + ', '
		myposition += str(z) + '*' + lunit
		self.position = myposition

	def addRotation(self, x, y, z, lunit = 'deg'):
		myrotation  = str(x) + '*' + lunit + ', '
		myrotation += str(y) + '*' + lunit + ', '
		myrotation += str(z) + '*' + lunit
		self.rotations.append(' + ' + myrotation)

	def getRotationString(self):
		rotationString = ''
		for r in self.rotations:
			rotationString = rotationString + r
		return rotationString

	def checkValidity(self):
		# need to add checking if it's operation instead
		if self.solid == WILLBESET:
			sys.exit(' Error: solid not defined for GVolume '      + str(self.name) )
		if self.parameters == WILLBESET:
			sys.exit(' Error: parameters not defined for GVolume ' + str(self.name) )
		if self.material == WILLBESET:
			sys.exit(' Error: material not defined for GVolume '   + str(self.name) )

	def publish(self, configuration):
		self.checkValidity()
		# TEXT factory
		if configuration.factory == 'TEXT':
			fileName = configuration.geoFileName
			configuration.nvolumes += 1
			with open(fileName, 'a+') as dn:
				lstr = ''
				lstr += '%s | ' % self.name
				lstr += '%s | ' % self.mother
				lstr += '%s | ' % self.solid
				lstr += '%s | ' % self.parameters
				lstr += '%s | ' % self.material
				lstr += '%s | ' % self.position
				lstr += '%s | ' % self.getRotationString()
				lstr += '%s | ' % self.mfield
				lstr += '%s | ' % self.visible
				lstr += '%s | ' % self.style
				lstr += '%s | ' % self.color
				lstr += '%s | ' % self.digitization
				lstr += '%s | ' % self.identifier
				lstr += '%s | ' % self.copyOf
				lstr += '%s | ' % self.replicaOf
				lstr += '%s | ' % self.solidsOpr
				lstr += '%s | ' % self.mirror
				lstr += '%s | ' % self.exist
				lstr += '%s |\n' % self.description

				dn.write(lstr)

	# in polycone the zplane and radious order are swapped w.r.t. gemc2 implementation
	# in order to match the geant4 constructor
	def makeG4Polycone(self, phiStart, phiTotal, zplane, iradius, oradius, lunit1 = 'mm', lunit2 = 'deg'):
		nplanes = len(zplane)
		if not len(iradius) == nplanes and not len(oradius) == nplanes:
			sys.exit(' Error: the G4Polycone array lengths do not match: zplane=' + str(len(zplane)) + ', iradius=' + str(len(iradius)) + ', oradius=' + str(len(oradius)) )

		self.solid = 'G4Polycone'
		mylengths  = ' '
		for ele in zplane:
			mylengths += str(ele) + '*' + lunit1 + ', '
		for ele in iradius:
			mylengths += str(ele) + '*' + lunit1 + ', '
		for ele in oradius[:-1]:
			mylengths += str(ele) + '*' + lunit1 + ', '

		# last element w/o the extra comment
		mylengths += str(oradius[-1]) + '*' + lunit1
		self.parameters = f'{phiStart}*{lunit2}, {phiTotal}*{lunit2}, {nplanes}, {mylengths}'

	def makeG4Box(self, dx, dy, dz, lunit = 'mm'):
		self.solid       = WILLBESET
		self.solid = 'G4Box'
		mylengths  = str(dx) + '*' + lunit + ', '
		mylengths += str(dy) + '*' + lunit + ', '
		mylengths += str(dz) + '*' + lunit 
		self.parameters = mylengths

	def makeG4Sphere(self, rmin, rmax, sphi, dphi, stheta, dtheta, lunit1 = 'mm', lunit2 = 'deg'):
		self.solid       = WILLBESET
		self.solid = 'G4Sphere'
		mydims  = str(rmin)   + '*' + lunit1 + ', '
		mydims += str(rmax)   + '*' + lunit1 + ', '
		mydims += str(sphi)   + '*' + lunit2 + ', '
		mydims += str(dphi)   + '*' + lunit2 + ', '
		mydims += str(stheta) + '*' + lunit2 + ', '
		mydims += str(dtheta) + '*' + lunit2
		self.parameters = mydims


	def makeG4Tubs(self, rin, rout, length, phiStart, totalPhi, lunit1 = 'mm', lunit2 = 'deg'):
		self.solid = 'G4Tubs'
		mydims  = str(rin)      + '*' + lunit1 + ', '
		mydims += str(rout)     + '*' + lunit1 + ', '
		mydims += str(length)   + '*' + lunit1 + ', '
		mydims += str(phiStart) + '*' + lunit2 + ', '
		mydims += str(totalPhi) + '*' + lunit2
		self.parameters = mydims


	def makeG4Cons(self, rin1, rout1, rin2, rout2, length, phiStart, totalPhi, lunit1 = 'mm', lunit2 = 'deg'):
		self.solid = 'G4Cons'
		mydims  = str(rin1)      + '*' + lunit1 + ', '
		mydims += str(rout1)     + '*' + lunit1 + ', '
		mydims += str(rin2)      + '*' + lunit1 + ', '
		mydims += str(rout2)     + '*' + lunit1 + ', '
		mydims += str(length)    + '*' + lunit1 + ', '
		mydims += str(phiStart)  + '*' + lunit2 + ', '
		mydims += str(totalPhi)  + '*' + lunit2
		self.parameters = mydims


	def makeG4Trd(self, dx1, dx2, dy1, dy2, z, lunit="mm"):
		self.solid = "G4Trd"
		with_units = [
			f"{val}*{lunit}"
			for val in [dx1, dx2, dy1, dy2, z]
		]
		self.parameters = ", ".join(with_units)

	# Right Angular Wedge (4 parameters)
	# pZ: Length along Z
	# pY: Length along Y
	# pX: Length along X at the wider side
	# pLTX: Length along X at the narrower side (plTX<=pX)
	def makeG4TrapRAW(self, pZ, pY, pX, pLTX, lunit1="mm"):
		self.solid = "G4Trap"
		with_units = [
			f"{pZ}*{lunit1}",
			f"{pY}*{lunit1}",
			f"{pX}*{lunit1}",
			f"{pLTX}*{lunit1}"
		]
		self.parameters = ", ".join(with_units)


	# general trapezoid (11 parameters)
	# pDz: Half Z length - distance from the origin to the bases
	# pTheta: Polar angle of the line joining the centres of the bases at -/+pDz
	# pPhi: Azimuthal angle of the line joining the centre of the base at -pDz to the centre of the base at +pDz
	# pDy1: Half Y length of the base at -pDz
	# pDy2: Half Y length of the base at +pDz
	# pDx1: Half X length at smaller Y of the base at -pDz
	# pDx2: Half X length at bigger Y of the base at -pDz
	# pDx3: Half X length at smaller Y of the base at +pDz
	# pDx4: Half X length at bigger y of the base at +pDz
	# pAlp1: Angle between the Y-axis and the centre line of the base at -pDz (lower endcap)
	# pAlp2: Angle between the Y-axis and the centre line of the base at +pDz (upper endcap)
	def makeG4TrapG(self, pDz, pTheta, pPhi, pDy1, pDx1, pDx2, pAlp1, pDy2, pDx3, pDx4, pAlp2, lunit1="mm", lunit2="deg"):
		self.solid = "G4Trap"
		with_units = [
			f"{pDz}*{lunit1}",
			f"{pTheta}*{lunit2}",
			f"{pPhi}*{lunit2}",
			f"{pDy1}*{lunit1}",
			f"{pDx1}*{lunit1}",
			f"{pDx2}*{lunit1}",
			f"{pAlp1}*{lunit2}",
			f"{pDy2}*{lunit1}",
			f"{pDx3}*{lunit1}",
			f"{pDx4}*{lunit1}",
			f"{pAlp2}*{lunit2}"
		]
		self.parameters = ", ".join(with_units)

	# from eight points (8 parameters)
	# pt | Coordinates of the vertices
	# pt[0], pt[1] | Edge with smaller Y of the base at -z
	# pt[2], pt[3] | Edge with bigger Y of the base at -z
	# pt[4], pt[5] | Edge with smaller Y of the base at +z
	# pt[6], pt[7] | Edge with bigger Y of the base at +z
	def makeG4Trap8(self, pt, lunit1="mm"):
		self.solid = "G4Trap"
		with_units = [
			f"{pt[0]}*{lunit1}",
			f"{pt[1]}*{lunit1}",
			f"{pt[2]}*{lunit1}",
			f"{pt[3]}*{lunit1}",
			f"{pt[4]}*{lunit1}",
			f"{pt[5]}*{lunit1}",
			f"{pt[6]}*{lunit1}",
			f"{pt[7]}*{lunit1}",
			f"{pt[8]}*{lunit1}",
			f"{pt[9]}*{lunit1}",
			f"{pt[10]}*{lunit1}",
			f"{pt[11]}*{lunit1}",
			f"{pt[12]}*{lunit1}",
			f"{pt[13]}*{lunit1}",
			f"{pt[14]}*{lunit1}",
			f"{pt[15]}*{lunit1}",
			f"{pt[16]}*{lunit1}",
			f"{pt[17]}*{lunit1}",
			f"{pt[18]}*{lunit1}",
			f"{pt[19]}*{lunit1}",
			f"{pt[20]}*{lunit1}",
			f"{pt[21]}*{lunit1}",
			f"{pt[22]}*{lunit1}",
			f"{pt[23]}*{lunit1}"
		]
		self.parameters = ", ".join(with_units)


	# G4Trap has three main constructors:
	# - for a Right Angular Wedge (4 parameters)
	# - for a general trapezoid (11 parameters)
	# - from eight points (8 parameters)
	def makeG4Trap(self, params, lunit1="mm", lunit2="deg"):
		if   len(params) == 4 :
			makeG4TrapRAW(self, *params, lunit1)
		elif len(params) == 11:
			self.makeG4TrapG(params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], params[9], params[10], lunit1, lunit2 )
		elif len(params) == 24:
			makeG4Trap8(self, *params, lunit1)
		else :
			sys.exit(' Error: the G4Trap eight points constructor parameter must be an array with 24 points' )

	# Pass a List to a Function as Multiple Arguments
	def setIdentifier(self, *identifiers):
		identitySize = int(len(identifiers) / 2)
		myidentifiers  = ''
		# looping over all pairs. Last one will not have the final comma
		for i in range(identitySize):
			idname = identifiers[2*i]
			idtag  = identifiers[2*i+1]
			myidentifiers += str(idname) + ': '
			if i == identitySize - 1 :
				myidentifiers += str(idtag)
			else :
				myidentifiers += str(idtag) + ', '

		self.identifier = myidentifiers
