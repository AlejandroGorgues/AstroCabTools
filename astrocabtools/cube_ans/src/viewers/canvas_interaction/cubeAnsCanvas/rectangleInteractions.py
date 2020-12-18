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

from .panOnClick import PanOnClick

class RectangleInteractions(PanOnClick):

    def __init__(self, figure=None, scale_factor=1.1):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param float scale_factor: The scale factor to apply on wheel event.
        """
        super(RectangleInteractions, self).__init__(figure, scale_factor=1.1)
        self._add_connection_rectangle('button_release_event', self._on_rectangle_release)

        self._add_rectangle_callback(self.rectangle_line_select_callback)

        self._pressed_button = None

        self._initialx = -1
        self._initialy = -1
        self._endx = -1
        self._endy = -1

    def _on_rectangle_release(self, event):
        """
        Apply the selection on initial and final values of the rectangle
        selector and send message to update the coordinates values on the coordinates window
        """
        if self._initialx == -1 and self._initialy == -1 and self._endx == -1 and self._endy == -1:
            pressed_button = None
            return

        self.rectangleStats.ix = self._initialx
        self.rectangleStats.iy = self._initialy
        self.rectangleStats.ex = self._endx
        self.rectangleStats.ey = self._endy

        pub.sendMessage('rectangleUpdateCoordinates', ix = self._initialx, iy =self._initialy
                            , ex = self._endx, ey= self._endy)
        pub.sendMessage('rectangleSelected')

    def rectangle_line_select_callback(self, eclick, erelease):
        """
        Obtain initial and final x and y values with the button pressed
        """
        self._initialx, self._initialy = eclick.xdata, eclick.ydata
        self._endx, self._endy = erelease.xdata, erelease.ydata
        self._pressed_button = eclick.button
