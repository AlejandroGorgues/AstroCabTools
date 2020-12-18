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

from pubsub import pub

import matplotlib.pyplot as _plt
from matplotlib.patches import Ellipse, Rectangle

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MplInteraction(object):

    def __init__(self, figure):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param Canvas FigureCanvas: The matplotlib PyQT canvas to allow focus after declaration
        """
        self._fig_ref = weakref.ref(figure)
        self.canvas = FigureCanvas(figure)

        self._rectangle = None
        self._ellipse = None

        self._cids_zoom = []
        self._cids_pan = []

        self._cids_callback_zoom = {}
        self._cids_callback_pan = {}

        self._cids = []

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

    def show_rectangle(self):
        if self._rectangle is not None:
            self._rectangle.set_visible(True)

    def show_ellipse(self):
        if self._ellipse is not None:
            self._ellipse.set_visible(True)


    def draw_rectangle(self, centerX, centerY, width, height):
        for ax in self.figure.axes:
            patch = next((patch for patch in ax.patches if patch == self._rectangle), None)

            #If patch exist in the ax, just edit the parameters
            if patch is not None:
                self._rectangle.set_xy([abs(width/2 - centerX), abs(height/2 - centerY)])
                self._rectangle.set_width(width)
                self._rectangle.set_height(height)

            #If patch does not exist in ax but self._rectangle is not None, edit and add the patch
            elif patch is None and self._rectangle is not None:
                self._rectangle.set_xy([abs(width/2 - centerX), abs(height/2 - centerY)])
                self._rectangle.set_width(width)
                self._rectangle.set_height(height)
                ax.add_patch(self._rectangle)

            #If patch does not exist in ax and self._rectangle is None, create it and add it
            else:
                self._rectangle = Rectangle([abs(width/2 - centerX), abs(height/2 - centerY)],
                                            width=width, height=height, edgecolor = "red",
                                            linewidth= 3, fill = False, alpha = 0.3)
                ax.add_patch(self._rectangle)
        self._draw()

    def draw_ellipse(self, centerX, centerY, aAxis, bAxis):
        for ax in self.figure.axes:
            patch = next((patch for patch in ax.patches if patch == self._ellipse), None)

            #If patch exist in the ax, just edit the parameters
            if patch is not None:
                self._ellipse.set_center([centerX, centerY])
                self._ellipse.width = aAxis
                self._ellipse.height = bAxis

            #If patch does not exist in ax but self._ellipse is not None, edit and add the patch
            elif patch is None and self._ellipse is not None:
                self._ellipse.set_center([centerX, centerY])
                self._ellipse.width = aAxis
                self._ellipse.height = bAxis
                ax.add_patch(self._ellipse)

            #If patch does not exist in ax and self._ellipse is None, create it and add it
            else:
                self._ellipse = Ellipse([centerX, centerY], width=aAxis, height=bAxis,
                                        edgecolor = "red", fill = False,
                                        linewidth = 3, alpha = 0.3)
                ax.add_patch(self._ellipse)
        self._draw()

    def hide_rectangle(self):
        if self._rectangle is not None:
            self._rectangle.set_visible(False)

    def hide_ellipse(self):
        if self._ellipse is not None:
            self._ellipse.set_visible(False)

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
