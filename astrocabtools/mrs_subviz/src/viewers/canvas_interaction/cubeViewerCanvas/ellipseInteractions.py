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

from matplotlib.widgets import EllipseSelector
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from .rectangleInteractions import RectangleInteractions

class EllipseInteractions(RectangleInteractions):

    def __init__(self, figure=None, scale_factor=1.1):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param float scale_factor: The scale factor to apply on wheel event.
        """
        super(EllipseInteractions, self).__init__(figure, scale_factor=1.1)
        self._add_connection_ellipse('button_release_event', self._on_ellipse_release)

        self._add_ellipse_callback(self.ellipse_line_select_callback)

        self._pressed_button = None

    def _on_ellipse_release(self, event):
        """
        Apply the selection on initial and final values of the rectangle
        selector and send """
        ellipse_data = self.get_ellipse_data()

        self.ellipseStats.centerX = ellipse_data[1][0]
        self.ellipseStats.centerY = ellipse_data[1][1]
        self.ellipseStats.aAxis = ellipse_data[0][2]
        self.ellipseStats.bAxis = ellipse_data[0][3]

        patchesData = {}
        patchesData['centerX'] = ellipse_data[1][0]
        patchesData['centerY'] = ellipse_data[1][1]
        patchesData['aAxis'] = ellipse_data[0][2]
        patchesData['bAxis'] = ellipse_data[0][3]
        pub.sendMessage('emit_data', order = "ellipseAp", patchesData = patchesData)

    def ellipse_line_select_callback(self, eclick, erelease):
        """
        Obtain initial and final x and y values with the button pressed
        """
        self._pressed_button = eclick.button
