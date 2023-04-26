

| [GEMC: Monte Carlo Particles and Hardware Simulator](https://gemc.github.io/home/) |
|:----------------------------------------------------------------------------------:|
|                             Dosimeter Digitization                                 |



### Description

 The setup consists of a target cell, two CAD imported volumes, and a silicon G4Sphere as the sensitive detector.

 The `dosimeter` sensitive type assigned to the sphere is a pre-loaded digitization plugin that will record
 radiation dose as particles pass through.

### Assigning cad volumes properties

The json file `target_cad/cad__default.json` contains the list of volumes to be assigned properties and sensitivity. 
The filename points to the 'default' variation, which is the default variation for the example.

The properties assigned in the json file are:

- color
- shift
- tilt
- material


### Building the custom scintillator material
  
Execute dosimeter.py:

```
./dosimeter.py
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

The root file contains ntuples with true information and digitized output.

The dosimeter digitization includes a `nielWeight` variable that is the radiation 
dose in units of NIEL (Non-Ionizing Energy Loss). 



### Notes

- the cell and dosimeter geometry is created using the dedicated `geometry.py` script.



### Author(s)
[M. Ungaro](https://maureeungaro.github.io/home/) [:email:](mailto:ungaro@jlab.org) [:octocat:](https://github.com/maureeungaro)



