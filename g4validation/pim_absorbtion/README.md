## pi- absorption test

This is a test of pi- absorption in aluminum:

An electron is impinging in a beam dump, producing pi+ and pi- which decays:

### - weak force (bf =  0.999877)

- π+ → μ+ + νμ
- π− → μ− + νμ*

### - em force (bf = 0.000123)

- π+ → e+ + νe
- π− → e− + νe*


If pi- is absorbed in Al, as we expect, the electrons anti-neutrino νe* are suppressed.

The test counts the various neutrinos.


## Geometry

A G4_Galactic tube encompass a beam dump made of aluminum.
In the stepping action, calls to the event action fill the ntuple when the step is in the scoring tube.

To create the geometry run the python script:

pim_absorption.py

** Run GEMC

gemc needs to be run with the switch -recordZeroEdep to allow recording of neutrinos.
Use the provided jcard:

gemc -recordZeroEdep pim_absorbtion.jcard


** Changing physics list



** ROOT Analysis:

The following macro counts the number of neutrinos:

root test.C


TODO:

- run this example with several physics lists

