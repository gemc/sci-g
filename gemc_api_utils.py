# -*- coding: utf-8 -*-
#=======================================
#	gemc utils definition
#
#	This file defines a GConfiguration class that holds a GEMC system configuration.
#
#
#	Class members (all members are text strings):
#	system   	- The name of the system. Think project name here.
#	variation 	- The name of the project variation.  For example, one could have variations of the project where
#					- a volume has a different size or material.  The variation defaults to 'default'
#	factory		- The configuration factory defines how the generated files that gemc uses are stored.
#					- Possible choices: TEXT, MYSQL, JSON
#	dbhost		- The hostname of the mysql database server where gemc detectors, materials, etc. may be stored
#					- for the MYSQL factory. Default to "na".
#	description	- A one liner describing the project
#	verbosity	- The log verbosity level for the sci-g API. The default is 0 (print only summary information)
#	

class gcolors:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# Configuration class definition
class GConfiguration():
	def __init__(self, system, factory="TEXT", description="none"):
		self.system      = system
		self.factory     = factory
		self.variation   = "default"
		self.dbhost      = "na"
		self.description = description
		self.verbosity   = 0
		self.nvolumes    = 0
		self.geoFileName = "na"
		self.matFileName = "na"
		self.mirFileName = "na"
		# filenames
		if self.factory == "TEXT":
			self.geoFileName    = self.system + "__geometry_"  + str(self.variation) + ".txt"
			self.matFileName    = self.system + "__materials_" + str(self.variation) + ".txt"
			self.mirFileName    = self.system + "__mirrors_"   + str(self.variation) + ".txt"
		elif self.factory == "JSON":
			self.geoFileName    = self.system + "__geometry_"  + str(self.variation) + ".json"
			self.matFileName    = self.system + "__materials_" + str(self.variation) + ".json"
			self.mirFileName    = self.system + "__mirrors_"   + str(self.variation) + ".json"


	def setVariation(self, newVariation):
		self.variation = newVariation

	def setVerbosity(self, verbosity):
		self.verbosity = verbosity

	def setMYSQLHost(self, dbhost):
		self.dbhost = dbhost

	def printC(self):
		print("\n  ❖ Sci-g configuration for system " + gcolors.BOLD + str(self.system) + gcolors.END + " : " + str(self.description))
		print("   ▪︎ Factory: " + str(self.factory))
		if self.factory == "MYSQL":
			if self.dbhost == "na":
				sys.exit(' Error: MYSQL dbhost is not defined. Exiting.')
			else:
				print("   ▪︎ Host: " + str(self.dbhost) )
		print("   ▪︎ Variation: " + str(self.variation) )
		print("   ▪︎ Number of volumes: " + str(self.nvolumes) )
		print("\n")

	# Function to initialize the factory
	# For TEXT and JSON: it overwrites any existing geometry file.
	def init_geom_file(self):
		if self.factory == "TEXT" or self.factory == "JSON":
			open(self.geoFileName, "w+")



# The following code allows this module to be executed as a main python script for the purpose of testing the functions
# To test, type:  'python gemc_api_utils.py' on the command line
if __name__ == "__main__":	
	import argparse, sys

	desc_str = ' Will create and print three sci-g systems configurations, two with TEXT and one with MYSQL factory.\n'
	parser = argparse.ArgumentParser(description=desc_str)


	system1 = GConfiguration("ctof", "TEXT", "The CLAS12 Central Time-Of-Flight")
	system1.setVariation("rga")

	system2 = GConfiguration("dc", "TEXT", "The CLAS12 Drift Chambers")
	system2.setVariation("rga_fall2019")

	system3 = GConfiguration("ec", "MYSQL", "The CLAS12 Calorimeters")
	system3.setMYSQLHost('gemc.jlab.org')

	system1.printC()
	system2.printC()
	system3.printC()




# Function to load the configuration data from the configuration file.
# This is deprecated, keeping it here in case we need it later on, and for documentation
#def load_configuration(cFile):
#	configuration = MyConfiguration()
#	with open(cFile,"r") as cn:
#		for line in cn:
#			if line.startswith("#") or line.isspace():
#				continue
#			key, value = line.split(":")
#			setattr(configuration, key.strip(), value.strip() )
#
#	print_configuration()
#
#	return configuration

