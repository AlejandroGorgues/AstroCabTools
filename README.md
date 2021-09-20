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
+ cube_ans.py - Representation and analyisis of miri cubes
+ mrs_subviz.py - Representation and analyisis of all MRS subbands
+ quick_spec.py - Easy representation of spectra with specific format and from fit__line, cube_ans and mrs_subviz
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
+ [Photutils](https://photutils.readthedocs.io/en/stable/#) - Package that provides tools for detecting and performing photometry of astronomical sources.
+ [jwst](https://jwst-pipeline.readthedocs.io/en/latest/index.html#) - Package to structurize cube models and transform data from pixel to coordinates and vice versa

### Tested with
+ Python (tested for 3.7.0)
+ Matplotlib (tested for 3.1.2)
+ Numpy (tested for 1.81.1)
+ PyQt5 (tested for 5.14.0)
+ Seaborn (tested for 0.9.0)
+ lmfit (tested for 1.0.0)
+ PyPubSub (tested for 4.0.3)
+ Photutils (tested for 1.0.1)
+ jwst (tested for 1.1.0)

> We have detected a problem with older versions of Mac not working with newer versons of pip because it can not found any version of matplotlib avaliable, for this case it is recommended to create an enviroment with a **pip version** no more than **20.2.2**.

## How to install and execute
1. Open the terminal and write `pip install AstroCabTools`
2. Once all the libraries had been updated and the package installed, to execute each program, the next commands need to be written on the terminal:
 - `bandChan` to execute mrs_chan.
 - `specChan` to execute mrs_spec_chan.
 - `detPlot` to execute mrs_det_plot.
 - `fitLine` to execute fit_line.
 - `cubeAns` to execute cube_ans.
 - `subViz` to execute mrs_subviz.
 - `quick_spec` to execute quick_spec.
 - `allTools` to execute all_tools.

### Manually installation
If your plan is to download from this repository and install it manually, execute `pip install .` inside the folder.
Rather than using the python install, this makes all the packages to be installed in the same folder where the libraries can not find any problem of not finding libraries where they should be.

## Templates
Templates for different tools can be downloaded in the next links and in the documentation.

### Mrs_spec_chan templates

The templates for this tool can be downloaded from this [link](https://cab.inta-csic.es/users/alabiano/templates_mrs_spec_chan.zip).

### Mrs_det_plot templates

The templates for this tool can be downloaded from this [link](https://cab.inta-csic.es/users/alabiano/templates_mrs_det_plot.zip).

### Fit_line templates

The templates for this tool can be downloaded from this [link](https://cab.inta-csic.es/users/alabiano/templates_fit_line.zip).

### Cube_ans and mrs_subviz templates

The templates for this tools can be downloaded from this [link](https://cab.inta-csic.es/users/alabiano/templates_cubes.zip).

## Development

### To dos

New:

+ [ ] Online documentation
+ [ ] Update templates zip file of cube_ans and mrs_subviz to new fits file standards

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
  + [x] Make gauss, double gauss, lorentz, lorentz + gauss, line and quadratic fitting model based on five points from an spectrum
  + [x] Represent all models

+ cube_ans features:
  + [x] MIRI, MEGARA and MUSE cube representation
  + [x] Possibility to make aperture from an area selected
  + [x] Creation of annulus background for subtraction from the initial area selected
  + [x] Representation of the initial spectrum or the resultant from the subtraction in the fit_line tool
  + [x] Obtain image based on the sum of flux for each pixel along a range of wavelength values

+ mrs_subviz features:
  + [x] Representation of all 12 subbands of the MRS channels in same interface
  + [x] Possibility to make aperture operation on all subbands at the same time
  + [x] Creation of annulus background for subtraction from the initial area selected from each cube
  + [x] Representation of the initial spectrum or the resultant from the subtraction for each cube

+ quick_spec features:
  + [x] Representation of spectra that follows the same pattern as the ones that fit_line, cube_ans and mrs_subViz generates in order to interact with it(zoom and pan)

+ all_tools features:
  + [x] Execute each one of the four programs independently
