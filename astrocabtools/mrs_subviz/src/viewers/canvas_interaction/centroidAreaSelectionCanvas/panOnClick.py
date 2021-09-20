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

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from .zoomOnWheel import ZoomOnWheel


class PanOnClick(ZoomOnWheel):
    """Class providing pan & zoom interaction to a matplotlib Figure.
    Left button for pan and zoom on wheel.
    """

    def __init__(self, figure=None, scale_factor=1.1):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param float scale_factor: The scale factor to apply on wheel event.
        """
        super(PanOnClick, self).__init__(figure, scale_factor=1.1)
        self._add_connection_pan('button_press_event', self._on_mouse_press)
        self._add_connection_pan('button_release_event', self._on_mouse_release)
        self._add_connection_pan('motion_notify_event', self._on_mouse_motion)

        self._pressed_button = None  # To store active button
        self._axes = None  # To store x and y axes concerned by interaction
        self._event = None  # To store reference event during interaction

    def _pan_update_limits(self, ax, axis_id, event, last_event):
        """Compute limits with applied pan."""
        if axis_id == 0:
            lim = ax.get_xlim()
        else:
            lim = ax.get_ylim()

        #TransData make it possible to transform data values to display values (display of the screen)
        #Inverted allows to transform from a data point to the data point based on the display inverted

        #Because this is possible, we can make for every pad made, transform every value of the image to
        #the ones that will fit on the screen based on the initial (x,y) and the final(x,y)
        #the initial x,y correspond to the button_press_event values, and the final correspond to the button_release_event
        #For each time the motion_notify_event ocurrs, the previous values will be saved and update the image
        pixel_to_data = ax.transData.inverted()
        data = pixel_to_data.transform_point((event.x, event.y))
        last_data = pixel_to_data.transform_point((last_event.x, last_event.y))

        #Otbtain the delta and apply it to update the limits of the figure into the plot
        delta = data[axis_id] - last_data[axis_id]
        new_lim = lim[0] - delta, lim[1] - delta
        return new_lim

    def _pan(self, event):
        """Execute function based on the name of it"""
        if event.name == 'button_press_event':  # begin pan

            self._event = event

        elif event.name == 'button_release_event':  # end pan
            self._event = None

        elif event.name == 'motion_notify_event':  # pan
            if self._event is None:
                return

            if event.x != self._event.x:
                for ax in self._axes[0]:
                    xlim = self._pan_update_limits(ax, 0, event, self._event)
                    ax.set_xlim(xlim)

            if event.y != self._event.y:
                for ax in self._axes[1]:
                    ylim = self._pan_update_limits(ax, 1, event, self._event)
                    ax.set_ylim(ylim)

            if event.x != self._event.x or event.y != self._event.y:
                self._draw()

            self._event = event

    def _on_mouse_press(self, event):
        """Set axes values based on point selected"""
        if self._pressed_button is not None:
            return  # Discard event if a button is already pressed

        x_axes = set()
        y_axes = set()
        for ax in self.figure.axes:
            #Simmilar to event.inaxis = axis
            x_axes, y_axes = self._axes_to_update(event)
            if ax.contains(event)[0]:
                x_axes.add(ax)
                y_axes.add(ax)
                self._axes = x_axes, y_axes
                self._pressed_button = event.button
                if self._pressed_button == 1:  # pan
                    self._pan(event)

    def _on_mouse_release(self, event):
        if self._pressed_button == 1:  # pan
            self.redraw_rectangle_without_interaction()
            self.redraw_ellipse_without_interaction()
            self._pan(event)
            pub.sendMessage('emit_data')

        self._pressed_button = None

    def _on_mouse_motion(self, event):
        if self._pressed_button == 1:  # pan
            self._pan(event)
