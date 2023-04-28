

| [GEMC: Monte Carlo Particles and Hardware Simulator](https://gemc.github.io/home/) |
|:----------------------------------------------------------------------------------:|
|              Cad Imports: importing volumes and modifying attributes               |


### Description

Two directories that contain STL files are imported:

- target_cad: a scattering chamber and a the target walls inside it
- tof_cad: 10 scintillator bars and a json file to assign properties such as sensitivity and material.

The custom material `my_scintillator` is created and assigned to the scintillator bars.

![cad_import_screenshot](./cad_imports.png)


### Assigning CAD volumes properties

The json file `tof_cad/cad__default.json` assigns properties to the scintillator bars. 
The filename points to the 'default' variation, which is the default variation for the example.

The properties assigned in the json file are:

- color
- shift
- tilt
- flux sensitivity
- paddle identifier
- material

Notice that for the `default` variation there are no properties assigned to the scattering 
chamber and target walls as no `cad__default.json` file is present in the target_cad directory.


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
`TEXT` and `ROOT` format. The files are identical in content and contain both true information 
and digitized output.

The root file contains ntuples with true information and digitized output.

### CAD Variation `tilted`

For demonstration purposes, a variation that adds a 5 degrees rotation around the x-axis to the scattering chamber 
and target wall is included.

The json file `target_cad/cad__tilted.json` assigns the properties to the volumes
for the `tilted` variation. To use this variation, it must be specified in the jcard:

``` 
{ "system":   "./target_cad",  "factory": "CAD",  "variation": "tilted" }
```



![cad_import_tilted_screenshot](./cad_imports_tilted.png)



### Notes
- the custom scintillator material is created using the dedicated `materials.py` script.


---

### Author(s)

| M. Ungaro |   [![Homepage](https://cdn3.iconfinder.com/data/icons/feather-5/24/home-64.png)](https://maureeungaro.github.io/home/)   |        [![email](https://cdn4.iconfinder.com/data/icons/aiga-symbol-signs/439/aiga_mail-64.png)](mailto:ungaro@jlab.org)         | [![github](https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-social-github-64.png)](https://github.com/maureeungaro)  | [![gemc](https://github.com/gemc/home/blob/main/assets/images/gemcLogo64.png?raw=true  )](https://gemc.github.io/home/) |
|:---------:|:------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------------:|

