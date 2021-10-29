-------------------------------------------------------------------

     =========================================================
        GEMC: Monte Carlo Particles and Hardware Simulator
     =========================================================

									simple_materials
                         -------------------

A- GEOMETRY

 The setup consists of four G4Boxes, with different materials

 The 'flux' sensitive type is assigned to each box, with its own identifier.

B- HOW TO BUILD THE GEOMETRY

  The geometry is constructed using the python script:

  ./example.py

  Take a look:
   - the geometry is created using a dedicated 'geometry.py' script.
   - the materials are created using a dedicated 'materials.py' script.


C- OUTPUT

	The output is defined by the entry '+goutput' in the jcard 'example.jcard'.
	By default the output is the 'root' format. Modify as needed.


D- HOW TO RUN GEMC

  Sets the desired number of cores, number of events, and verbosity in the jcard 'example.jcard'

  Run gemc:

  gemc example.jcard

  Use the '-gui' option to run interactively:

  gemc example.jcard -gui


