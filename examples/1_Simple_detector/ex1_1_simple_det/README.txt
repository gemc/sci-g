-------------------------------------------------------------------

     =========================================================
        GEMC: Monte Carlo Particles and Hardware Simulator
     =========================================================

									Example 1_1
                         ----------------

 This folder contains one of the simplest possible projects: a target at the coordinate center and
 a scintillator paddle named 'ctof'
 The detector has been tagged "flux", that is, it will record hits when a track passes through it.

 The target material are GEANT4 predefined:
  - target: “G4_lH2”
  - ctof: G4_PLASTIC_SC_VINYLTOLUENE

 The “flux” sensitive type assigned to 'ctof' is a pre-loaded digitization plugin that will record every
 track that passes through it. The track parameters (energy deposited, time, position, etc.) are integrated
 through all geant4 steps in the volume and presented as one hit per track.


 HOW TO BUILD THE GEOMETRY

 The geometry is built using the 

 HOW TO RUN
