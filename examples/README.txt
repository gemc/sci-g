-------------------------------------------------------------------

     =========================================================
        GEMC: Monte Carlo Particles and Hardware Simulator
     =========================================================

                             Examples
                         ----------------

 This folder contains a series of examples for using various features of gemc.
 It is hoped that the user can take these basic ideas and expand them in their
 own projects.

 The instructions to run and build each example are given in README.txt files in each folder.

 The examples are divided into several general categories.

 ## 1_Simple_detector:

  - ex1_1_simple_det......a target and a sensitive (flux) detector
  - ex1_2_dosimeter.......importing cad volumes and the dosimeter digitization





** Working on porting to gemc3
2_Working_with_materials:
ex2_1_det_materials		Shows different ways to define a material in gemc

3_Working_with_geometry:
ex3_1_building_shapesù	Examples of using the Geant4 solids, including boolean operations
ex3_2_parameters_and_variations	Shows how to use a parameter file to import geometry values

4_Optical_properties:
ex4_1_scintillation			Shows how to define optical properties for scintillation
ex4_2_cerenkov_radiation  	Shows how to define materials to generate Cerenkov photons
ex4_3a_optical_fresnel_refraction	Shows reflection and refraction at the boundary of two optical materials
ex4_3b_optical_skin_surface	Shows a parabolic mirror by adding a reflective coating to a shaped glass block
ex4_3c_optical_border_surface	Shows an optical boundary at the border between two volumes with touching surfaces

5_Working_with_fields:
ex5_1_uniform_field		Simple dipole magnet with a uniform magnetic field


6_CalorimeterAndHodoscope:
ex6_1_calHodoDetector: A real CLAS12 detector: Calorimeter + Hodoscope setup
