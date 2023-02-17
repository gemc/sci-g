-------------------------------------------------------------------

     =========================================================
        GEMC: Monte Carlo Particles and Hardware Simulator
     =========================================================

									simple_flux
                         ----------------

A- GEOMETRY

 The setup consists of a target and a scintillator paddle.

 The 'flux' sensitive type assigned to the paddle volume is a pre-loaded digitization plugin that will record
 tracks parameters as they pass through. These are integrated through all geant4 steps in the
 volume and presented as one variable per track.

B- HOW TO BUILD THE GEOMETRY

  The geometry is constructed using the python script:

  ./simple_flux.py

  Take a look:
  - the geometry is created using a dedicated 'geometry.py' script.

C- OUTPUT

	The output is defined by the entry '+goutput' in the jcard 'example.jcard'.
	By default the output goes simultaneously to two files: 'text' and 'root' format.
	Modify filenames as needed. Comment out not needed entries.


D- HOW TO RUN GEMC

  Sets the desired number of cores, number of events, and verbosity in the jcard 'example.jcard'

  Run gemc:

  gemc simple_flux.jcard

  Use the '-gui' option to run interactively:

  gemc simple_flux.jcard -gui


