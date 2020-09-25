.. _cube_ans_tutorial:

Cube Ans Tutorial
=================

Overview
--------

Cube_Ans allows to represent a space cube that comes from the Miri (CHANGE) in form of an image for each slice with the options to move along each slice.
Based on the image represented, a rectangle selection can be made on it, showing an spectrum along all the slices, with the posibility to represent it in the fit_line tool.

.. note::
        #. Only works with the Miri Cube format

Requirements
-------------

To execute and use the too, the next libraries need to be installed:

* Python (tested for 3.8.0)
* Matplotlib (tested for 3.1.2)
* Numpy (tested for 1.81.1)
* PyQt5 (tested for 5.14.0)
* Seaborn (tested for 0.9.0)
* Lmfit (tested for 1.0.0)
* PyPubSub (tested for 4.0.3)

Initial display
---------------

After the tool is loaded, a window with multiple buttons on the top and on the bottom of it, that will be explained later, will appear. Those buttons interact with the spectrum that will appear on the canvas.

Data insertion
---------------

To be able to interact with the spectrum and to create gaussian fitted models, the button on the top left of the window need to be pressed, showing a new window which will allow to select the spectrum to be loaded and it's associated parameters that can be modified (see :numref:`figure1`).

.. _figure1:
.. figure:: _static/proj4-in1.png

Once a file has been selected, several parameters can be modified (see :numref:`figure2`):

* The redshift that is going to be applied to both values after they have been transformed, if necessary
* The columns where the values are. By default, the wavelength and flux column are located in column 0 and column 1 respectively.
* The units both columns are in order to transform into 'erg/cm2/s/um' and 'uj'.

.. _figure2:
.. figure:: _static/proj4-in2.png

Example2
^^^^^^^^^
