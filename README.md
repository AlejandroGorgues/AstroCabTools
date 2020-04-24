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

### Tools used

For each tool, this repo uses a number of libraries and packages on python:

+ [PyQt](https://wiki.python.org/moin/PyQt) - Binding of C++ GUI library
+ [Numpy](https://numpy.org/) - Library that allow large data manipulation
+ [Matplotlib](https://matplotlib.org/) - Graph visualization library.
+ [Astropy](https://www.astropy.org/) - Collection of software packages used for astronomy
+ [Seaborn](https://seaborn.pydata.org/) - Statistical data visualization

### Development

This repository will continue to grow with new tools based on the future needs.

### Todos

Old:

+ [ ] Optimize code of all tools
+ [ ] Add seaborn as graph visualization
+ [ ] Proper documentaton on the code

New:

+ mrs_spec_chan features:
 + [ ] Enlarge wavelenth values to all JWST values
 + [ ] Save spectrum as ".jpg"
 + [ ] Add zoom event to specturm
 + [ ] Allow to add multiple spectrums
 + [ ] Add gap as color
 + [ ] Draw rgb channels with 50% alpha
 + [ ] Allow to draw new optionall wavelengths without reloading the app

+ mrs_det_plot features:
 + [ ] Mark the pixel selected with a color
 + [ ] Allow to open 4 at the same time to compare dithers
 + [ ] Show flux vs frame (and time) for a pixel selected
 
Done:

+ [x] Finish first version mrs_chan.py
+ [x] Finish first version mrs_spec_chan.py
+ [x] Finish first version mrs_det_plot.py
