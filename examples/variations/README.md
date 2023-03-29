

| [GEMC: Monte Carlo Particles and Hardware Simulator](https://gemc.github.io/home/) |
|:----------------------------------------------------------------------------------:|
|                 Variations Example: Two version of the same system                 |


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

- #### Running gemc

  Select the desired variation in the steering card then run gemc:

  ```
  gemc variations.jcard
  ```

### Notes

  The variable `configuration.variation` is used in geometry.py to change the color
  and material of the target and to add a lead shield for the `lead_target` variation.

  The relevant lines in geometry.py are:

<script src="https://gist.github.com/maureeungaro/3fbb95835881f6a72f2f16116d16efb2.js"></script>

### Author(s)
M. Ungaro


