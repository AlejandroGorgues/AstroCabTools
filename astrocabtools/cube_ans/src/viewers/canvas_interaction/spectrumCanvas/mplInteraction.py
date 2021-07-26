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
import numpy as np
import weakref

from pubsub import pub

import matplotlib.pyplot as _plt
from matplotlib.patches import Rectangle

from ....models.rectangleSpectrum import rectangle_spectrum

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MplInteraction(object):

    def __init__(self, figure):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param Canvas FigureCanvas: The matplotlib PyQT canvas to allow focus after declaration
        """
        self._fig_ref = weakref.ref(figure)
        self.canvas = FigureCanvas(figure)

        self._rectangle_interactions = None
        self._line_position = None

        self._rectangle_yAxis_limits = [None, None]
        self._range_wavelength_limits = [0.0,0.0]

        self._cids_zoom = []
        self._cids_pan = []
        self._cids_rectangle_creation = []
        self._cids_rectangle_interaction = []

        self._cids_callback_zoom = {}
        self._cids_callback_pan = {}
        self._cids_callback_rectangle_creation = {}
        self._cids_callback_rectangle_interaction = {}

        self._cids = []

        self._rectangleStats = rectangle_spectrum(0)

    def __del__(self):
        self.disconnect()

    def _add_connection(self, event_name, callback):
        """Called to add a connection to an event of the figure
        :param str event_name: The matplotlib event name to connect to.
        :param callback: The callback to register to this event.
        """
        cid = self.canvas.mpl_connect(event_name, callback)
        self._cids.append(cid)


    def _add_connection_zoom(self, event_name, callback):
        """Called to add a connection of type zoom to an event of the figure
        :param str event_name: The matplotlib event name to connect to.
        :param callback: The callback to register to this event.
        """

        #cid = self.canvas.mpl_connect(event_name, callback)
        #self._cids_zoom.append(cid)
        self._cids_callback_zoom[event_name] = callback

    def _add_connection_pan(self, event_name, callback):
        """Called to add a connection of type pan to an event of the figure
        :param str event_name: The matplotlib event name to connect to.
        :param callback: The callback to register to this event.
        """
        #cid = self.canvas.mpl_connect(event_name, callback)
        #self._cids_pan.append(cid)
        self._cids_callback_pan[event_name] = callback

    def _add_connection_rectangle_creation(self, event_name, callback):
        """Called to add a connection of type rectangle to an event of the figure
        :param str event_name: The matplotlib event name to connect to.
        :param callback: The callback to register to this event.
        """
        self._cids_callback_rectangle_creation[event_name] = callback

    def _add_connection_rectangle_interaction(self, event_name, callback):
        """Called to add a connection of type rectangle to an event of the figure
        :param str event_name: The matplotlib event name to connect to.
        :param callback: The callback to register to this event.
        """
        self._cids_callback_rectangle_interaction[event_name] = callback

    def disconnect_zoom(self):
        """
        Disconnect all zoom events and disable the rectangle selector
        """
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids_zoom:
                    figure.canvas.mpl_disconnect(cid)
            self._cids_zoom.clear()

    def disconnect_pan(self):
        """
        Disconnect all pan events
        """
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids_pan:
                    figure.canvas.mpl_disconnect(cid)
            self._cids_pan.clear()

    def disconnect_rectangle_creation(self):
        """
        Disconnect all rectangle events
        """
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids_rectangle_creation:
                    figure.canvas.mpl_disconnect(cid)
            self._cids_rectangle_creation.clear()

    def disconnect_rectangle_interaction(self):
        """
        Disconnect all rectangle events
        """
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids_rectangle_interaction:
                    figure.canvas.mpl_disconnect(cid)
            self._cids_rectangle_interaction.clear()

    def disconnect(self):
        """Disconnect interaction from Figure."""
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids:
                    figure.canvas.mpl_disconnect(cid)
            self._fig_ref = None

    def connect_zoom(self):
        """
        Assign all callback zoom events to the mpl
        """
        for event_name, callback in self._cids_callback_zoom.items():
            cid = self.canvas.mpl_connect(event_name, callback)
            self._cids_zoom.append(cid)

    def connect_pan(self):
        """
        Assign all callback pan events to the mpl
        """
        for event_name, callback in self._cids_callback_pan.items():
            cid = self.canvas.mpl_connect(event_name, callback)
            self._cids_pan.append(cid)

    def connect_rectangle_creation(self):
        """
        Assign all callback rectangle events to the mpl
        """
        for event_name, callback in self._cids_callback_rectangle_creation.items():
            cid = self.canvas.mpl_connect(event_name, callback)
            self._cids_rectangle_creation.append(cid)

    def connect_rectangle_interaction(self):
        """
        Assign all callback rectangle events to the mpl
        """
        for event_name, callback in self._cids_callback_rectangle_interaction.items():
            cid = self.canvas.mpl_connect(event_name, callback)
            self._cids_rectangle_interaction.append(cid)

    def draw_line_position(self, x):
        """Set parametes (x positions and height) of the line that will
        move along x_axis according to the current wavelength and the wavelength yAxis limits
        :param float x: current wavelength selected
        """
        if self._line_position is not None:
            for ax in self.figure.axes:
                yAxis_limits = self._rectangle_yAxis_limits

                segments = []
                segments.append(tuple(zip((x,x), (yAxis_limits[0], yAxis_limits[1]))))
                self._line_position.set_segments(segments)
        else:
            for ax in self.figure.axes:
                yAxis_limits = self._rectangle_yAxis_limits
                self._line_position = ax.vlines(x=x, ymin = yAxis_limits[0], ymax= yAxis_limits[1])
        self._draw()

    def set_rectangle_yAxis_limits(self, ymin, ymax):
        """Pass the spectrum min and max values into an object to use it as the height
        of the range rectangle figure
        :param float ymin: minimum flux value of the spectrum
        :param float ymax: maximum flux value of the spectrum
        """
        self._rectangle_yAxis_limits[0] = ymin
        self._rectangle_yAxis_limits[1] = ymax

    def update_rectangle_yAxis_limits_on_range_update(self, yAxis_range_limits):
        """Set the height of the rectangle every time a rectangle is created or is moved
        :param tuple yAxis_range_limits: tuple with the bottom and top "y" limits
        """
        if isinstance(self._rectangle_interactions, Rectangle):
            self._rectangle_interactions.set_height(abs(yAxis_range_limits[0]*0.9 - \
                                                        yAxis_range_limits[1]*1.1))
            self._rectangle_interactions.set_y(yAxis_range_limits[0]*0.9)

        self._draw()

    def update_rectangle_yAxis_limits_on_spectrum_update(self, yAxis_range_limits):
        """Set the height of the rectangle every time the spectrum data changes to
        adapt it based on the max and min values of the spectrum
        """
        if isinstance(self._rectangle_interactions, Rectangle):
            self._rectangle_interactions.set_height(abs(yAxis_range_limits[0]*0.9 - \
                                                        yAxis_range_limits[1]*1.1))
            self._rectangle_interactions.set_y(yAxis_range_limits[0]*0.9)
        self._draw()

    def set_initial_limits(self, xlim, ylim):
        """ Set initial limits of the representation to use it when the zoom reset
        button is pushed
        :param tuple xlim: limit values on x axis
        :param tuple ylim: limit values on y axis
        """

        self._spectrum_initial_xlim = xlim
        self._spectrum_initial_ylim = ylim

    def zoom_reset(self):

        for ax in self.figure.axes:
            ax.set_xlim((self._spectrum_initial_xlim[0],\
                         self._spectrum_initial_xlim[1]))

            ax.set_ylim((self._spectrum_initial_ylim[0],\
                         self._spectrum_initial_ylim[1]))
        self._draw()

    def clear_elements_axes(self):
        self._rectangle_interactions = None
        self._line_position = None

    @property
    def figure(self):
        """The Figure this interaction is connected to or
        None if not connected."""
        return self._fig_ref() if self._fig_ref is not None else None

    def _axes_to_update(self, event):
        """Returns two sets of Axes to update according to event.
        :param MouseEvent event: Matplotlib event to consider
        :return: Axes for which to update xlimits and ylimits
        :rtype: 2-tuple of set (xaxes, yaxes)
        """
        x_axes, y_axes = set(), set()

        for ax in self.figure.axes:
            if ax.contains(event)[0]:
                x_axes.add(ax)
                y_axes.add(ax)

        return x_axes, y_axes

    def _draw(self):
        """Conveninent method to redraw the figure"""
        self.canvas.draw()
