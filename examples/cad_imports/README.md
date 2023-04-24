

| [GEMC: Monte Carlo Particles and Hardware Simulator](https://gemc.github.io/home/) |
|:----------------------------------------------------------------------------------:|
|              Cad Imports: importing volumes and modifying attributes               |


### Description

Two directories that contain STL files are imported:

- target_cad: a scattering chamber and a the target walls inside it
- tof_cad: 10 scintillator bars and a json file to assign them properties and sensitivity

The custom material `my_scintillator` is created and assigned to the scintillator bars.

### Assigning cad volumes properties

The json file `tof_cad/cad__default.json` contains the list of volumes to be assigned properties and sensitivity. 
The filename points to the 'default' variation, which is the default variation for the example.

The properties assigned in the json file are:

- color
- shift
- tilt
- flux sensitivity
- paddle identifier
- material

### Building the custom scintillator material
  
Execute cad_imports.py:

  ```
  ./cad_imports.py
  ```

### Running gemc

Modify the jcard as needed (for example, set the desired number of events) and run:

```
gemc cad_imports.jcard -gui
```

Omit the '-gui' option to run in batch mode.


### Output

The output is defined by the entry `+goutput` in the jcard: two files are created simultaneously: 
`TEXT` and `ROOT` format.
Modify filenames as needed. Comment out not needed entries.

The root file contains the true information and digitized output.

### Notes

- the target does not have custom assigned properties: a `cad` json file 
  is not present in the target_cad directory.
- the custom scintillator material is created using the dedicated `materials.py` script.


### Author(s)
M. Ungaro


