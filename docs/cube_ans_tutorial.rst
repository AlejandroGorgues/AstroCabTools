.. _cube_ans_tutorial:

Cube Ans Tutorial
=================

Overview
--------

Cube_Ans allows to represent a space cube that comes from a MIRI cube in form of an image for each slice with the options to move along each one.
Based on the image represented, a rectangle or ellipse selection can be made on it, showing an spectrum along all the slices, with the posibility to represent it in the fit_line tool.

.. note::
        Only works with the MIRI Cube format

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
* Photutils (tested for 1.0.1)

Initial display
---------------

After the tool is loaded, a window with a menu bar and several buttons in it at the top of it will appear. Those buttons and menu will interact with the images that will appear on the canvas.

Data insertion
---------------

To be able to interact with the images the "Open" button in the "File" menu option on the top left of the window need to be pressed, showing a new window which will allow to select the type of cube that is going be loaded. The selection of the cube is necessary because of the different headers that heahc cube has (see :numref:`figure1_cube_ans`).

.. _figure1_cube_ans:
.. figure:: _static/proj4-in1.png

Data interaction
----------------

Once the cube has been selected, the first slice, which corresponds to the first wavelenght, will appear on the canvas (see :numref:`figure2_cube_ans`). Using the top componentes, the slice can be changed with:

* An slider that has a range determinated from the minimum and máximum range of all the wavelengths avaliable. This slider can be used to move along all the slices. Once it has been moved, the "Slice Value" spin and the "Wavelength Value" text edit field will update with it's associated values based on the current wavelength and slice values.
* An spin that can be used to changed to the slice that want to be shown. As told before. Once this field change, the other components related, will change too.
* A text field that can be used to change to the slice that want to be shown based on the approximated wavelength value. After this filed change, the other componentes will change too.

.. _figure2_cube_ans:
.. figure:: _static/proj4-in1.png

Image manipulation
^^^^^^^^^^^^^^^^^^

The "Tools" option in the menu bar contains multiple sections related to different actions (see :numref:`figure3_cube_ans`). In this section, the first part contains different choices to manipulate the images:

* The Zoom option allow to make zoom to the current image with the mouse wheel and maintain that zoom along all the slices
* The Pan option allow to move the current image with the left mouse button and maintaint that shift alonw all the slices
* The Rectangle and Ellipse option allow to select an area based on the type of figure and obtain the associated spectrum. After the figure has been drawn, it's properties can be modified left clicking inside the figure to move it, or in the borders to extend or reduce the size of it. Once the area has been selected, a new window will appear, showing the spectrum associated to the area along with different buttons, whose functionalities will be explained in the SECTION X.
* The Unselect option which disallow all the previous ones.

.. _figure3_cube_ans:
.. figure:: _static/proj4-in1.png

Rectangle manipulation
^^^^^^^^^^^^^^^^^^^^^^

Following the next section of the "Tools" option, two actions can be taken (see :numref:`figure4_cube_ans`):

1. The "Rectangle Coordinates" option show a new window that contains the X and Y coordinates of the left and right side of the rectangle, which will update when the figure moved.
2. The "Creation of Rectangle parameterized" option show a new window that allow to select the coordinates of the rectangle that shares the same figure as the one created in the section before. In this case, the figure can be created using the bottom left or the center coordinates along with the height and the width, which can be written in it's associated text fields. Once the parameters had been written, the button located at the bottom of the window will update the coordinates of it.

.. _figure4_cube_ans:
.. figure:: _static/proj4-in1.png

Style manipulation
^^^^^^^^^^^^^^^^^^
The third option listed on the top bar corresponds to the style which allows to change the scale, stretch and color of the current image displayed (see :numref:`figure5_cube_ans`):

* The Color of the image can be change with a palette of them like Accent or CoolWarm
* The Scale of the image can be set to show it with a Min-Max interval or a ZScale
* The Stretch of the image can be set to use a sqrt, log or linear stretch.

.. _figure5_cube_ans:
.. figure:: _static/proj4-in1.png

Spectrum visualization
^^^^^^^^^^^^^^^^^^^^^^

As told in the section X, an spectrum will appear. This spectrum corresponds to the representation of each aperture for each wavelength (see :numref:`figure6_cube_ans`). By default the zoom and pan are active in order to use them with the mouse wheel and the left click mouse correspondingly.

Along with the spectrum, two buttoms are located at the bottom of it. This buttons are related to export it:

1. As a text file pressing the "Save" button. This text file will contain two columns associated with the wavelength and flux value, which allows to use it on the fit_line tool or into another one.
2. As arguments to load into the fit_line tool. To make it possible, a new window will appear which require to select the redshift that will be applied to both wavelength and flux values and the units that are originally because a conversion to X and Y are gonna be applied. This process follows the same structure as if an spectrum would be loaded using the fit_line tool with the exception of the colums where both values are, that in this case are not needed. Once all had been selected, pressing the "Accept" button will apply the changes and the result will be shown in the main window of fit_line.

.. _figure6_cube_ans:
.. figure:: _static/proj4-in1.png

.. note::
        This window can be closed, in order to load it again, a button located in the tool section called "Spectrum Visualization" can be clicked (see :numref:`figure7_cube_ans`).

        .. _figure7_cube_ans:
        .. figure:: _static/proj4-in1.png

Background subtraction
^^^^^^^^^^^^^^^^^^^^^^

One of the biggest features of this tool is the possibility to obtain the spectrum resulting from the subtraction of a background delimited manually from the spectrum of the aperture. In order to delimite the area of the background, one of the two figures need to be drawed, this is because the center where the delimited background area in form of two rings (one for the inner and another for the outer, on which the circular annulus will be applied) is needed in order to do all the operations.

.. _figure8_cube_ans:
.. figure:: _static/proj4-in1.png

Once the figure has been drawed, the button located in the tool section will be avaliable (see :numref:`figure8_cube_ans`). Clicking on it will make a new window to appear, which shows the center coordinates of the figure, two forms, associated to the radius of each ring (the inner and outer) which contains each one a text field to write the radius, a button to set it and draw it in the image, and a button at the bottom that will apply the subtraction of the area from the spectrum of the aperture (see :numref:`figure9_cube_ans`). The result will be shown in the window where the initial spectrum is represented with a total of three spectrums (see :numref:`figure10_cube_ans`):

* The blue spectrum shows the one obtained from the initial aperture
* The red spectrum shows the mean values of the background for each wavelength
* The green spectrum shows the subtraction of the area of the mean background from the inital aperture

.. _figure9_cube_ans:
.. figure:: _static/proj4-in1.png

|

.. _figure10_cube_ans:
.. figure:: _static/proj4-in1.png

Everytime the figure is moved or resized or changed (from rectangle to ellipse or vice versa), the previous spectrums will change in order to adjust to the new values.


.. note::
        Because a background subtraction has been applied to the initial spectrum, the spectrum that is the result of it will be loaded into the fit_line tool instead of the first one.

Example
-------

.. note::
        The file called "FILE" located in the templates section had been used.

This example shows the process of representing the spectrum that is the result of subtract the aperture from the background aperture in the fit_line tool.

After the cube have been loaded, the wavelength X have been selected, which corresponds to the slice X (see :numref:`figure11_cube_ans`).

.. _figure11_cube_ans:
.. figure:: _static/proj4-in1.png

As described before, there are two figures from which the aperture can be obtained, in this case, the ellipse have been selected to be drawn starting from the center of the image to be the center of it. Once it had been drawned, the window that represent the spectrum should have been appeared as show in the figure :numref:`figure12_cube_ans`).

.. _figure12_cube_ans:
.. figure:: _static/proj4-in1.png

The next part of this example corresponds to the subtraction operation, this is done by selecting previously the background aperture with two rings that will determine it. Both rings will have the center located in the same coordinates as the figure (if the figure is gonna be moved, the rings will not move along with it), but the radius of the inner and outer are different, 5 and 10 respectively (see :numref:`figure13_cube_ans`).

.. note::
        To be able to create both rings and to make the background subtraction, the "Background subtraction" button from the "Tools" option located in the menu bar was selected.

.. _figure13_cube_ans:
.. figure:: _static/proj4-in1.png

Once both rings have been drawned, the "Apply background subtraction" button need to be pressed. This action will update the window that shows the initial spectrum with two more, the red and green one, that corresponds to the mean flux value of the background for each wavelength and the subtraction of the background aperture area from the initial spectrum (see :numref:`figure14_cube_ans`).

.. _figure14_cube_ans:
.. figure:: _static/proj4-in1.png

In order to load the fit_line tool, the "Load spectrum on fitLine" button from the previous window need to be pressed, which will show the last window associated to set the desired paramaters that are gonna be represented in the fit_line too. In this example, the redshift value has been set to 0.0 and the units of the wavelength and flux parameters to X and Y respectively. After all actions have been made, the "Accept" button is pressed, and the fit_line tool appear, showing the spectrum (see :numref:`figure15_cube_ans`).

.. _figure15_cube_ans:
.. figure:: _static/proj4-in1.png
