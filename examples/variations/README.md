

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

This will create the `TEXT` database for the system. To use `SQLITE` instead, check the 
[sqlite database](../sqlite_db) example.

- #### Running gemc

  Select the desired variation in the steering card then run gemc:

  ```
  gemc variations.jcard
  ```

### Notes

  The variable `configuration.variation` is used in geometry.py to change the color
  and material of the target and to add a lead shield for the `lead_target` variation.

  The relevant lines in geometry.py are shown below:

<script src="https://gist.github.com/maureeungaro/3fbb95835881f6a72f2f16116d16efb2.js"></script>



<br/><br/><br/>

---

### Author(s)

| M. Ungaro |   [![Homepage](https://cdn3.iconfinder.com/data/icons/feather-5/24/home-64.png)](https://maureeungaro.github.io/home/)   |        [![email](https://cdn4.iconfinder.com/data/icons/aiga-symbol-signs/439/aiga_mail-64.png)](mailto:ungaro@jlab.org)         | [![github](https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-social-github-64.png)](https://github.com/maureeungaro)  |
|:---------:|:------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------:|

