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
from pubsub import pub

import matplotlib.pyplot as _plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from .rectangleCreationOnClick import RectangleCreationOnClick


class RectangleInteractionsOnClick(RectangleCreationOnClick):
    """Class providing rectangle interaction to a matplotlib Figure.
    Left button to move the position of current rectangle.
    """

    def __init__(self, figure=None, scale_factor=1.1):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param float scale_factor: The scale factor to apply on wheel event.
        """
        super(RectangleInteractionsOnClick, self).__init__(figure, scale_factor=1.1)
        self._add_connection_rectangle_interaction('button_press_event', self._on_mouse_press_interaction)
        self._add_connection_rectangle_interaction('button_release_event', self._on_mouse_release_interaction)
        self._add_connection_rectangle_interaction('motion_notify_event', self._on_mouse_motion_interaction)

        self._pressed_button = None  # To store active button
        self._axes = None  # To store x and y axes concerned by interaction
        self._event = None  # To store reference event during interaction
        self._press = None


    def _rectangle_actions(self, event):
        """Execute function based on the name of it"""
        if event.name == 'button_press_event':  # begin action
            contains, attrd = self._rectangle_interactions.contains(event)
            if not contains:return
            x0, y0 = self._rectangle_interactions.xy
            self._press = x0,y0, event.xdata, event.ydata

        elif event.name == 'button_release_event':  # end action
            self._press = None

            pub.sendMessage('rangeData', iw = self._rectangle_interactions.get_x(),
                            ew = self._rectangle_interactions.get_bbox().x1)

        elif event.name == 'motion_notify_event':  # move
            if self._press is None:
                return

            if self._rectangle_interactions is None:
                return

            if event.inaxes == self._rectangle_interactions.axes:
                x0,y0, xpress, ypress = self._press
                dx = event.xdata - xpress
                #Because I want to block the possibility to move
                #around the y-axis, the value for it will always be y0
                self._rectangle_interactions.set_xy((x0 + dx, y0))
            else:
                return

    def _on_mouse_press_interaction(self, event):
        """Set axes values based on point selected"""
        x_axes = set()
        y_axes = set()
        for ax in self.figure.axes:
            #Simmilar to event.inaxis = axis
            if ax.contains(event)[0]:
                x_axes.add(ax)
                y_axes.add(ax)
                self._axes = x_axes, y_axes
                self._pressed_button = event.button
                if self._pressed_button == 1 and self._rectangle_interactions is not None:
                    self._rectangle_actions(event)

    def _on_mouse_release_interaction(self, event):
        if self._pressed_button == 1:
            self._rectangle_actions(event)

        self._pressed_button = None
        self._draw()

    def _on_mouse_motion_interaction(self, event):
        if self._pressed_button == 1:
            self._rectangle_actions(event)

        self._draw()
