[![Documentation Status](https://readthedocs.org/projects/astrotools/badge/?version=latest)](https://astrotools.readthedocs.io/en/latest/?badge=latest)

# AstroCabTools

Set of tools made in order to:

+ Integrate processing tools, algorithms, visualization and data analysis of images and 3D infrarred spectroscopy for the James Webb Espacial Telescope (JWST).
+ Integration of JWST calibrated data  and advance products into astronomics data bases and astrophisics specialized packages.
+ Develop procedures to the JWST data combination and the joint analysis of large volumnes of data.
+ Simulation and study of observationes made from the MIRI tool of the JWST with the MIRISim simulator.

## Tools

+ mrs_chan.py - To identify wich channels from the MRS range, an emitted wavelenth is (BETA version).
+ mrs_spec_chan.py - Visualization of relationship emitted wavelength and density flux associate (BETA version).
+ mrs_det_plot.py - Manipulation of astronomic images based of frame and integration values (BETA version).
+ fit_line.py - Representation of multiple gauss fitted models based on an spectrum.
+ all_tools - Interface that allows to load each tool without using command line.

### Packages used

For each tool, this repo uses a number of libraries and packages on python:

+ [PyQt](https://wiki.python.org/moin/PyQt) - Binding of C++ GUI library
+ [Numpy](https://numpy.org/) - Library that allow large data manipulation
+ [Matplotlib](https://matplotlib.org/) - Graph visualization library.
+ [Astropy](https://www.astropy.org/) - Collection of software packages used for astronomy
+ [Seaborn](https://seaborn.pydata.org/) - Statistical data visualization
+ [Lmfit](https://lmfit.github.io//lmfit-py/) - Non-Linear Least-Squares Minimization and Curve-Fitting for Python
+ [PyPuSub](https://github.com/schollii/pypubsub) - A Python publish-subcribe library

### Requirements
+ Python (tested for 3.7.0)
+ Matplotlib (tested for 3.1.2)
+ Numpy (tested for 1.81.1)
+ PyQt5 (tested for 5.14.0)
+ Seaborn (tested for 0.9.0)
+ lmfit (tested for 1.0.0)
+ PyPubSub (tested for 4.0.3)

## How to install and execute
1. Open the terminal and write `pip install AstroCabTools`
2. Once all the libraries had been updated and the package installed, to execute each program, the next commands need to be written on the terminal:
  	- `bandChan` to execute mrs_chan.
  	- `specChan` to execute mrs_spec_chan.
  	- `detPlot` to execute mrs_det_plot.
  	- `fitLine` to execute fit_line.
	- `allTools` to execute all_tools.

### Development

### To dos

New:
+ [ ] Online documentation

Done:

+ mrs_chan features:
 + [x] Specific wavelength location inside mrsSpec channels
+ mrs_spec_chan features:
 + [x] Representation and management of spectra on a range of wavelength values
 + [x] Representation of specific observed wavelengths selected on the plot
 + [x] Representation of specific lines of interest from a list on the plot
 + [x] Management of different specification ranges where each plot is going to appear
+ mrs_det_plot features:
 + [x] Visualization of multiple .fits images
 + [x] Management of the scale, stretch and colour of all the images
 + [x] Visualization of values selected on an specified image along each axis
+ fit_line features:
 + [x] Make gauss fitting model based on five points from an spectrum
 + [x] Allow to make more than one gauss fitting model
 + [x] Represent all gauss models
+ all_tools features:
 + [x] Execute each one of the four programs independently
