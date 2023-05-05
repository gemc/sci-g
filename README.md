
	
|  SCI-G:  System Construction Interface for GEMC  |
| :----------------------------------------------: |
|        A Python API to build detectors           |


SCI-G is part of the [GEMC](https://gemc.github.io/home/) project. 
It provides a python API to build detectors, create materials, assign sensitivity, etc.


# Quickstart

The ptyhon script `scigTemplate.py` can be used to create 
a new system or template code to build a new volume, 
material, etc.


### Create a system 

To create a 'my_project' system:

``` 
scigTemplate.py -s my_project
```

See [gemc systems](https://gemc.github.io/home/documentation/system) for more details.



## Validation

[![Build Examples](https://github.com/gemc/sci-g/actions/workflows/build.yml/badge.svg)](https://github.com/gemc/sci-g/actions/workflows/build.yml)
[![Examples Overlap](https://github.com/gemc/sci-g/actions/workflows/overlaps.yml/badge.svg)](https://github.com/gemc/sci-g/actions/workflows/overlaps.yml)
[![Examples Test](https://github.com/gemc/sci-g/actions/workflows/tests.yml/badge.svg)](https://github.com/gemc/sci-g/actions/workflows/tests.yml)
