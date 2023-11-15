![](https://github.com/mateuszmatu/LCS/blob/master/gifs/DG_animation.gif)

# Important: This is still work in progress

This is a repository containing more general scripts for computing hyperbolic LCSs, utilizing the FTLE approach.
The goal of the files in this folder is to make the scripts as robust as possible, so that they can be used with any model in any region. 
These scripts compute LCSs in the ocean, but should work for 2D atmosphere as well (not tested).

# Dependencies

Particles are advected using MET Norways OpenDrift python module. This module and an installation guide can be found on https://opendrift.github.io/.
Other packages needed can all be installed normally through 
```
pip install [package name]
```

# Using the software

The goal of this software is for it to be simple to use, and yet general. Particles are first advected using the ```Advection``` class.


# Using the software

To use the software, first run 
```
python getting_file_names.py
```
This generates a .txt file containing all links to the Barents-2.5 EPS files found in https://thredds.met.no/thredds/catalog/fou-hi/barents_eps_eps/catalog.html.


Particles can then be seeded in the Barents-2.5 EPS velocity field with ParticleAdvector.py.
The domain, gridsize, initial particle separation, ensemble member and date can be chosen here. 

A function for advecting particles in the double-gyre system is also contained in ParticleAdvector.py.

ParticleAdvector.py will save the initial and final positions of particles to a specified file. This file can then be used as input for the LCS.py script, which computes attracting hyperbolic LCSs. The FTLE values approximating LCSs are saved to an xarray dataset, with dimensions
```
[lon, lat, ALCS]
```
where lon and lat are the gridpoints and ALCS is an array containing FTLE values. Note that the method is specifically tailored for attracting hyperbolic LCSs, but can still be used for repelling LCSs. However, the dimension name will still be ALCS, and not RLCS, and the array has to be reversed, so that arr[ALCS][::-1,::-1] yields repelling LCSs (given that particles have been integrated forwards in time).
This xarray is saved to file, and can be plotted with for example

plt.pcolormesh(arr.lon, arr.lat, arr.ALCS)

# main.py

main.py is a script which runs both the ParticleAdvector.py and LCS.py scripts at the same time. 

Note that the .txt file from getting_file_names.py must exist in the working directory. 

Both the output files from ParticleAdvector.py and LCS.py will be saved to a directory specified in main.py. 
These will be named [filename].nc and [filename_LCS].nc. 
The script can be used to for example generate a large amount of LCSs with one run, by looping over the "run" function found in the script. 
