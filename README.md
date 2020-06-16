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
+ fit_line.py - Representation of multiple gauss fitted models based on an spectrum.

### Tools used

For each tool, this repo uses a number of libraries and packages on python:

+ [PyQt](https://wiki.python.org/moin/PyQt) - Binding of C++ GUI library
+ [Numpy](https://numpy.org/) - Library that allow large data manipulation
+ [Matplotlib](https://matplotlib.org/) - Graph visualization library.
+ [Astropy](https://www.astropy.org/) - Collection of software packages used for astronomy
+ [Seaborn](https://seaborn.pydata.org/) - Statistical data visualization
+ [Lmfit](https://lmfit.github.io//lmfit-py/) - Non-Linear Least-Squares Minimization and Curve-Fitting for Python
+ [PyPubSub](https://github.com/schollii/pypubsub/) - Package that provides a publish-subscribe API

### Requirements
+ Python 3.8.0 or newer
+ Matplotlib 3.1.2 or newer
+ Numpy 1.81.1 or newer
+ PyQt5 5.14.0 or newer
+ Seaborn 0.9.0 or newer
+ lmfit 1.0.0 or newer
+ PyPubSub 4.0.3 or newer

## How to install and execute
1. Download the project as a zip and unzip it or clone it.
2. Open the terminal and move to the project directory.
3. Write `python setup.py install` on the terminal.
4. Once all the libraries had been updated and the package installed, to execute each program, the next commands need to be written on the terminal:
  1. `bandChan` to execute mrs_chan.
  2. `specChan` to execute mrs_spec_chan.
  3. `detPlot` to execute mrs_det_plot.
  4. `fitLine` to execute fit_line.

### Development

### To dos

Old:

+ [ ] Optimize code of all tools
+ [ ] Write proper documentation

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
+ fit_line features:
 + [x] Make several fitted gauss models
 + [x] Show residuals
 + [x] Make units conversion to the normalized units
 + [x] Select columns and units where the wavelength and flux values are
 + [x] Modified Zoom to do a zoom on rectangle selected area
 + [x] Add zoom undo feature
 + [x] Calculate flux density
