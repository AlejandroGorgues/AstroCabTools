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
from matplotlib.widgets import RectangleSelector

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MplInteraction(object):

    def __init__(self, figure):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param Canvas FigureCanvas: The matplotlib PyQT canvas to allow focus after declaration
        """
        self._fig_ref = weakref.ref(figure)
        self.canvas = FigureCanvas(figure)
        self._cids_zoom = []
        self._cids_pan = []
        self._cids_rectangle_selection = []
        self._cids_callback_zoom = {}
        self._cids_callback_pan = {}
        self._cids_callback_rectangle_selection = {}

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

    def _add_rectangle_callback(self, callback):
        """
        Because the callback method can only be created when the Zoom event is
        created and the axis can only be known after the creation if it, this
        method allow to assign the callback before the creation fo the
        rectangle selector object
        """
        self._callback_rectangle = callback

    def _add_connection_rectangle_selection(self, event_name, callback):
        """Called to add a connection of type rectangle release to an event of the figure
        :param str event_name: The matplotlib event name to connect to.
        :param callback: The callback to register to this event.
        """
        self._cids_callback_rectangle_selection[event_name] = callback

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

    def disconnect_rectangle_selection(self, changeFigure=False):
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids_rectangle_selection:
                    figure.canvas.mpl_disconnect(cid)
            self._cids_rectangle_selection.clear()

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

    def _disable_rectangle(self):
        self._rectangle_selector.set_visible(False)
        self._rectangle_selector.set_active(False)

    def _enable_rectangle(self):
        self._rectangle_selector.set_active(True)

        self._rectangle_selector.set_visible(True)

    def connect_rectangle_selection(self):
        for event_name, callback in self._cids_callback_rectangle_selection.items():
            cid = self.figure.canvas.mpl_connect(event_name, callback)
            self._cids_rectangle_selection.append(cid)
        self._enable_rectangle()

    def connect_zoom(self):
        """
        Assign all callback zoom events to the mpl
        """
        for event_name, callback in self._cids_callback_zoom.items():
            cid = self.figure.canvas.mpl_connect(event_name, callback)
            self._cids_zoom.append(cid)

    def connect_pan(self):
        """
        Assign all callback pan events to the mpl
        """
        for event_name, callback in self._cids_callback_pan.items():
            cid = self.figure.canvas.mpl_connect(event_name, callback)
            self._cids_pan.append(cid)

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
                shared_x_axes = set(ax.get_shared_x_axes().get_siblings(ax))
                if x_axes.isdisjoint(shared_x_axes):
                    x_axes.add(ax)

                shared_y_axes = set(ax.get_shared_y_axes().get_siblings(ax))
                if y_axes.isdisjoint(shared_y_axes):
                    y_axes.add(ax)

        return x_axes, y_axes


    def create_rectangle_ax(self, ax):
        rectprops = dict(edgecolor = 'red',fill = False,
                         linewidth = 2.5, linestyle= '-')

        self._rectangle_selector = RectangleSelector(ax, self._callback_rectangle,
                                    drawtype= 'box', useblit= True, rectprops= rectprops,
                                    button= [1,3], minspanx = 5, minspany=5,
                                    spancoords='pixels')

        self._disable_rectangle()

    def set_initial_limits(self, xlim, ylim, cubeXCPix, cubeYCPix, cubeRAValue, cubeDValue, cubeXCRVal, cubeYCRVal):

        self.initial_xlim = xlim
        self.initial_ylim = ylim
        self.twin_initial_xlim = ((self.initial_xlim[0]- cubeXCPix)*cubeRAValue*3600 + cubeXCRVal*3600, (self.initial_xlim[1]- cubeXCPix)*cubeRAValue*3600 + cubeXCRVal*3600)
        self.twin_initial_ylim = ((self.initial_ylim[0]- cubeYCPix)*cubeDValue*3600 + cubeYCRVal*3600, (self.initial_ylim[1]- cubeYCPix)*cubeDValue*3600 + cubeYCRVal*3600)

    def zoom_reset(self):
        for ax in self.figure.axes:
            if ax.get_gid() == 'main_axis':
                ax.set_xlim(self.initial_xlim)
                ax.set_ylim(self.initial_ylim)
            elif ax.get_gid() == 'twinx_axis':
                ax.set_ylim(self.twin_initial_xlim)
            elif ax.get_gid() == 'twiny_axis':
                ax.set_xlim(self.twin_initial_ylim)

        self._draw()

    def clear_elements_axes(self, ax):

        ax.patches.clear()

    def _draw(self):
        """Conveninent method to redraw the figure"""
        self.figure.canvas.draw()
