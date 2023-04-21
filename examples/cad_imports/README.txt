-------------------------------------------------------------------

     =========================================================
        GEMC: Monte Carlo Particles and Hardware Simulator
     =========================================================

						    dosimeter
                         ----------------

A- GEOMETRY

 The setup consists of a target, two CAD imported volumes, and a silicon sphere.

 The 'dosimeter' sensitive type assigned to the sphere is a pre-loaded digitization plugin that will record
 radiation dose as particles pass through.


B- HOW TO BUILD THE GEOMETRY

  The geometry is constructed using the python script:

  ./dosimeter.py

  Take a look:
   - the geometry is created using a dedicated 'geometry.py' script.
   - In the jcard the 'cad' factory imports the two CAD files from the targetCad directory
   - Notice how the scatteringChamber volume is rotated and shifted in the jcard using the 'gmodifier' option

C- OUTPUT

	The output is defined by the entry '+goutput' in the jcard 'example.jcard'.
	By default the output goes simultaneously to two files: 'text' and 'root' format.
	Modify filenames as needed. Comment out not needed entries.


D- HOW TO RUN GEMC

  Sets the desired number of cores, number of events, and verbosity in the jcard 'example.jcard'

  Run gemc:

  gemc dosimeter.jcard

  Use the '-gui' option to run interactively:

  gemc dosimeter.jcard -gui


