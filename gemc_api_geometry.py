# -*- coding: utf-8 -*-
#=======================================
#	gemc geometry definition
#
#	This file defines a GVolume class that holds the parameters needed to define a geant4 physical volume in gemc
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
#
#	The following GVolume parameters are optional and have default values
#
#	mother			- The name of the parent volume. Defaults to the world volume "root"
#	description		- A description of the volume. Default is "no description"
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
#	field				- The name of a magnetic field file attached to the gvolume. Default is "no".
#                   The field is defined in the file header. In case of a field map, the data is contained in the file itself.
#
#	exist				- This is an integer field:  1 if the volume exists, 0 if not.  It is a way to turn off volumes.
#						  This value can also be accessed in the jcard modifiers. Default is "1".
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
#	identifier	   - A string defining the name of the plugin used to digitized the hit. Default is "none".

# GVolume class definition
class GVolume():
	def __init__(self, name, solid, parameters, material):

		# mandatory fields. Checked at publish time
		self.name        = name
		self.solid       = "notSetYet"
		self.parameters  = "notSetYet"
		self.material    = "notSetYet"

		# optional fields
		self.mother       = "root"
		self.description  = "no description"
		self.pos          = "0*mm, 0*mm, 0*mm"
		self.rotation     = ["0*deg, 0*deg, 0*deg"]
		self.mfield       = "no"

		self.exist        = 1      # 0 does not exist, 1 exists

		self.visible      = 1		# 0 is invisible, 1 is visible
		self.style        = 1		# 0 is wireframe, 1 is solid
		self.color        = "778899"

		self.digitization = "none"
		self.identifier   = "none"

		self.copyOf      = "none"
		self.replicaOf   = "none"
		self.solidsOpr   = "none"

		self.mirror      = "none"

	def setRotation(self, newRotation):
		self.rotations = [newRotation]

	def addRotation(self, singleRotation):
		self.rotations.append(singleRotation)

	def publish(self, configuration):
		if configuration.factory == "TEXT":
			fileName = configuration.geoFileName
			with open(fileName, "a+") as dn:
				lstr = ""
				lstr += "%20s  |" % detector.name
				lstr += "%20s  |" % detector.mother
				lstr += "%30s  |" % detector.description
				lstr += "%50s  |" % detector.pos
				lstr += "%40s  |" % detector.rotation
				lstr += "%7s   |" % detector.color
				lstr += "%20s  |" % detector.type
				lstr += "%60s  |" % detector.dimensions
				lstr += "%20s  |" % detector.material
				lstr += "%20s  |" % detector.mfield
				lstr += "%6s   |" % detector.ncopy
				lstr += "%6s   |" % detector.pMany
				lstr += "%6s   |" % detector.exist
				lstr += "%4s   |" % detector.visible
				lstr += "%4s   |" % detector.style
				lstr += "%20s  |" % detector.sensitivity
				lstr += "%20s  |" % detector.hit_type
				lstr += "%40s \n" % detector.identifiers

				dn.write(lstr)


		


