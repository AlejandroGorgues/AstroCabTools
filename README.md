# Astro tools

Set of tools made in order to:

+ Integrate processing tools, algorithms, visualization and data analysis of images and 3D infrarred spectroscopy for the James Webb Espacial Telescope (JWST).
+ Integration of JWST calibrated data  and advance products into astronomics data bases and astrophisics specialized packages.
+ Develop procedures to the JWST data combination and the joint analysis of large volumnes of data.
+ Simulation and study of observationes made from the MIRI tool of the JWST with the MIRISim simulator.

## Tools

+ mrs_chan.py - To identify wich channels from the MRS range, an emitted wavelenth is.
+ mrs_spec_chan.py - Visualization of relationship emitted wavelength and density flux associate.
+ mrs_det_plot.py - Manipulation of astronomic images based of frame and integration values.
+ fit_line.py - Representation of multiple gauss fitting models based on an spectrum.

### Tools used

For each tool, this repo uses a number of libraries and packages on python:

+ [PyQt](https://wiki.python.org/moin/PyQt) - Binding of C++ GUI library
+ [Numpy](https://numpy.org/) - Library that allow large data manipulation
+ [Matplotlib](https://matplotlib.org/) - Graph visualization library.
+ [Astropy](https://www.astropy.org/) - Collection of software packages used for astronomy
+ [Seaborn](https://seaborn.pydata.org/) - Statistical data visualization
+ [Lmfit](https://lmfit.github.io//lmfit-py/) - Non-Linear Least-Squares Minimization and Curve-Fitting for Python

### Development

This repository will continue to grow with new tools based on the future needs.

### Todos

Old:

+ [ ] Optimize code of all tools
+ [ ] Write proper documentation

New:

+ fit_line features:
 + [ ] Make gauss fitting model based on five points from an spectrum
 + [ ] Allow to make more than one gauss fitting model
 + [ ] Represent all gauss models



Done:

+ [x] Finish developing basic functionalities of mrs_chan.py
 + [x] Specific wavelength location inside mrsSpec channels
+ [x] Finish developing basic functionalities mrs_spec_chan.py
 + [x] Representation and management of spectra on a range of wavelength values
 + [x] Representation of specific observed wavelengths selected on the plot
 + [x] Representation of specific lines of interest from a list on the plot
 + [x] Management of different specification ranges where each plot is going to appear
+ [x] Finish developing basic functionalities mrs_det_plot.py
 + [x] Visualization of multiple .fits images
 + [x] Management of the scale, stretch and colour of all the images
 + [x] Visualization of values selected on an specified image along each axis
