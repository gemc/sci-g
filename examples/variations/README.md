

| GEMC: Monte Carlo Particles and Hardware Simulator |
|:--------------------------------------------------:|
|                 Variations Example                 |
|           Two version of the same system           |


### Description

Two version of the same systems are created using `variations`: 
`default` and `lead_target`. 
The `lead_target` variation is identical to the `default` except for the target material and the presence of
a lead shield.

The discrimination is done in geometry.py, using the variable `configuration.variation`.


### Usage

- #### Building the detector
  
  Execute variations.py:

  ```
  ./variations.py
  ```

- ### Running gemc

  Select the desired variation in the steering card then run gemc:

  ```
  gemc variations.jcard
  ```
  

### Notes

### Author(s)
M. Ungaro


