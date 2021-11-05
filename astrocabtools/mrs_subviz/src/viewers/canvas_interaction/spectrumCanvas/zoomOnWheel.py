# This Copyright is paste from https://gist.github.com/t20100/e5a9ba1196101e618883
# /*##########################################################################
#
# Copyright (c) 2016 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/
import numpy
import weakref
import numpy as np

from pubsub import pub

import matplotlib.pyplot as _plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from .mplInteraction import MplInteraction

class ZoomOnWheel(MplInteraction):
    """Class providing zoom on wheel interaction to a matplotlib Figure.
    """

    def __init__(self, figure=None, scale_factor=1.1):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param float scale_factor: The scale factor to apply on wheel event.
        """
        super(ZoomOnWheel, self).__init__(figure)
        self._add_connection_zoom('button_release_event', self._rectangle_release)
        #Because the rectangle selector can only be created when an axe is created, it passes
        #the callback function that is gonna be added to the rectangle selector properties
        self._add_rectangle_callback(self._line_select_callback)
        #self._add_connection_zoom('scroll_event', self._on_mouse_wheel)

        #self.scale_factor = scale_factor
        self._pressed_button = None  # To store active button
        #Set initial values to the rectangle coordinates
        self._initial_x = -1
        self._initial_y = -1
        self._end_x = -1
        self._end_y = -1

    def _rectangle_release(self, event):
        """
        Apply the zoom base on initial and final values of the rectangle selector
        """
        #Because _line_select_callback is not called when user push and release on the same pixel,
        #the coordinates values change to -1 and this conditional checkif if that it's the value instead
        #of the ones from _line_select_callback
        if self._initial_x == -1 and self._initial_y == -1 and self._end_x == -1 and self._end_y == -1:
            pressed_button= None
            return

        #self._add_initial_zoom_reset()
        #Create the command, and execute it
        #zoomCommand = ZoomCommand(self._pressed_button, self._initial_x, self._initial_y, self._end_x, self._end_y, event, self.figure)
        #self._invokerZoom.command(zoomCommand)

        x_axes, y_axes = self._axes_to_update(event)
        if self._pressed_button == 1:  # Zoom in

            for ax in x_axes:
                xmin0, xmax0 = ax.get_xbound()
                xmin, xmax = np.clip(sorted([self._initial_x, self._end_x]), xmin0, xmax0)
                ax.set_xbound(xmin, xmax)

            for ax in y_axes:
                ymin0, ymax0 = ax.get_ybound()
                ymin, ymax = np.clip(sorted([self._initial_y, self._end_y]), ymin0, ymax0)

                ax.set_ybound(ymin, ymax)

        elif self._pressed_button == 3: #Zoom out

            #For each axes, get the bounds, create an np array between selected values
            #and the bound values. Get the transformation function and apply it to
            #each of the values between the limits and the selected one. Get the
            #factor that need to be applied to the values and apply it
            for ax in x_axes:
                xmin0, xmax0 = ax.get_xbound()
                xmin, xmax = np.clip(sorted([self._initial_x, self._end_x]), xmin0, xmax0)
                x_trf = ax.get_xaxis().get_transform()
                sxmin0, sxmax0, sxmin, sxmax = x_trf.transform(
                    [xmin0, xmax0, xmin, xmax])  # To screen space.
                factor = (sxmax0 - sxmin0) / (sxmax - sxmin)  # Unzoom factor.
                # Move original bounds away by
                # (factor) x (distance between unzoom box and axes bbox).
                sxmin1 = sxmin0 - factor * (sxmin - sxmin0)
                sxmax1 = sxmax0 + factor * (sxmax0 - sxmax)
                # And back to data space.
                new_xbound = x_trf.inverted().transform([sxmin1, sxmax1])
                ax.set_xbound(new_xbound)

                #repeat for y axes
            for ax in y_axes:
                ymin0, ymax0 = ax.get_ybound()
                ymin, ymax = np.clip(sorted([self._initial_y, self._end_y]), ymin0, ymax0)

                y_trf = ax.get_yaxis().get_transform()
                symin0, symax0, symin, symax = y_trf.transform(
                    [ymin0, ymax0, ymin, ymax])
                factor = (symax0 - symin0) / (symax - symin)
                symin1 = symin0 - factor * (symin - symin0)
                symax1 = symax0 + factor * (symax0 - symax)
                new_ybound = y_trf.inverted().transform([symin1, symax1])
                ax.set_ybound(new_ybound)

        if x_axes or y_axes:
            self._draw()

        self._pressed_button = None

        self._initial_x = -1
        self._initial_y = -1
        self._end_x = -1
        self._end_y = -1

    def _line_select_callback(self, eclick, erelease):
        """
        Obtain initial x and y values, end x and y values and button pressed
        """
        self._initial_x, self._initial_y = eclick.xdata, eclick.ydata
        self._end_x, self._end_y  = erelease.xdata, erelease.ydata
        self._pressed_button = eclick.button
