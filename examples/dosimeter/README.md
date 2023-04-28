

| [GEMC: Monte Carlo Particles and Hardware Simulator](https://gemc.github.io/home/) |
|:----------------------------------------------------------------------------------:|
|                             Dosimeter Digitization                                 |



### Description

 The setup consists of a target cell, two CAD imported volumes, and a silicon spherical wedge as the sensitive detector.

 The `dosimeter` sensitive type assigned to the wedge is a preloaded digitization plugin that will record
 radiation dose as particles pass through.

![dosimeter_screenshot](./dosimeter.png)


### Assigning cad volumes properties to the STL files

The scattering chamber and the target wall STL files in the `target_cad` directory.
The json file `target_cad/cad__default.json` assigns them properties.
The filename points to the `default` variation, which is the default variation for the example.

The properties assigned in the json file are:

- color
- shift
- tilt
- material


### Building target cell and dosimeter spherical wedge
  
Execute dosimeter.py:

```
./dosimeter.py
 ```


### Running gemc

Modify the jcard as needed (for example, set the desired number of events) and run:

```
gemc dosimeter.jcard -gui
```

Omit the '-gui' option to run in batch mode.


### Output

The output is defined by the entry `+goutput` in the jcard: two files are created simultaneously: 
`TEXT` and `ROOT` format. The files are identical in content and contain both true information 
and digitized output.

The root file contains ntuples with true information and digitized output.

The dosimeter digitization includes a `nielWeight` variable that is the radiation 
dose in units of NIEL (Non-Ionizing Energy Loss). 



### Notes

- the cell and dosimeter geometry is created using the dedicated `geometry.py` script.


---

### Author(s)

| M. Ungaro |   [![Homepage](https://cdn3.iconfinder.com/data/icons/feather-5/24/home-64.png)](https://maureeungaro.github.io/home/)   |        [![email](https://cdn4.iconfinder.com/data/icons/aiga-symbol-signs/439/aiga_mail-64.png)](mailto:ungaro@jlab.org)         | [![github](https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-social-github-64.png)](https://github.com/maureeungaro)  | [![gemc](https://github.com/gemc/home/blob/main/assets/images/gemcLogo64.png?raw=true  )](https://gemc.github.io/home/) |
|:---------:|:------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------------:|

