

| [GEMC: Monte Carlo Particles and Hardware Simulator](https://gemc.github.io/home/) |
|:----------------------------------------------------------------------------------:|
|          Cad Imports Example: importing volumes and modifying attributes           |


### Description

Two directories contain STL files:

- target_cad: a scattering chamber and a the target walls inside it
- tof_cad: 10 scintillator bars and a json file to assign them properties and sensitivity

The custom material `my_scintillator` is created and assigned to the scintillator bars.

### Assigning cad volumes properties

The json file `tof_cad/cad__default.json` contains the list of volumes to be assigned properties and sensitivity. 
The filename points to the 'default' variation, which is the default variation for the example.

Among the properties assigned in the json file:

- color
- shift
- tilt
- flux sensitivity
- paddle identifier
- material

### Usage

- #### Building the custom scintillator material
  
  Execute cad_imports.py:

  ```
  ./cad_imports.py
  ```

- #### Running gemc

  Select the desired number of events and run:

  ```
  gemc cad_imports.jcard
  ```

### Notes

- the target does not have custom assigned properties because a `cad` json file is not present in the target_cad directory. 


### Author(s)
M. Ungaro


